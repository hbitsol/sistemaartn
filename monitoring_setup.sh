#!/bin/bash

# Monitoring and Logging Setup Script for Oracle Cloud Deployment
# This script sets up basic monitoring and logging for the deployed application

set -e

echo "🔍 Setting up monitoring and logging..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Create log directories
create_log_directories() {
    print_status "Creating log directories..."
    sudo mkdir -p /var/log/pricing-crm
    sudo mkdir -p /var/log/nginx
    sudo chown -R $USER:$USER /var/log/pricing-crm
}

# Setup log rotation
setup_log_rotation() {
    print_status "Setting up log rotation..."
    
    sudo tee /etc/logrotate.d/pricing-crm > /dev/null << EOF
/var/log/pricing-crm/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
    postrotate
        docker-compose -f /home/$USER/franchise_pricing_crm/docker-compose.oracle.yml restart backend
    endscript
}
EOF
}

# Create monitoring script
create_monitoring_script() {
    print_status "Creating monitoring script..."
    
    cat > /home/$USER/monitor_services.sh << 'EOF'
#!/bin/bash

# Service monitoring script
LOG_FILE="/var/log/pricing-crm/monitor.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Function to log messages
log_message() {
    echo "[$DATE] $1" >> $LOG_FILE
}

# Check if services are running
check_backend() {
    if curl -f -s http://localhost:5000/api/health > /dev/null; then
        log_message "Backend service is healthy"
        return 0
    else
        log_message "ERROR: Backend service is not responding"
        return 1
    fi
}

check_frontend() {
    if curl -f -s http://localhost/health > /dev/null; then
        log_message "Frontend service is healthy"
        return 0
    else
        log_message "ERROR: Frontend service is not responding"
        return 1
    fi
}

# Check Docker containers
check_containers() {
    cd /home/$USER/franchise_pricing_crm
    
    backend_status=$(docker-compose -f docker-compose.oracle.yml ps -q backend | xargs docker inspect -f '{{.State.Status}}' 2>/dev/null || echo "not_found")
    frontend_status=$(docker-compose -f docker-compose.oracle.yml ps -q frontend | xargs docker inspect -f '{{.State.Status}}' 2>/dev/null || echo "not_found")
    
    if [ "$backend_status" != "running" ]; then
        log_message "ERROR: Backend container is not running (status: $backend_status)"
        # Attempt to restart
        log_message "Attempting to restart backend container..."
        docker-compose -f docker-compose.oracle.yml restart backend
    fi
    
    if [ "$frontend_status" != "running" ]; then
        log_message "ERROR: Frontend container is not running (status: $frontend_status)"
        # Attempt to restart
        log_message "Attempting to restart frontend container..."
        docker-compose -f docker-compose.oracle.yml restart frontend
    fi
}

# Check system resources
check_resources() {
    # Check disk space
    disk_usage=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ $disk_usage -gt 80 ]; then
        log_message "WARNING: Disk usage is at ${disk_usage}%"
    fi
    
    # Check memory usage
    memory_usage=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
    if [ $memory_usage -gt 90 ]; then
        log_message "WARNING: Memory usage is at ${memory_usage}%"
    fi
    
    # Check CPU load
    cpu_load=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    if (( $(echo "$cpu_load > 2.0" | bc -l) )); then
        log_message "WARNING: CPU load is high: $cpu_load"
    fi
}

# Main monitoring function
main() {
    log_message "Starting health check..."
    
    check_containers
    check_backend
    check_frontend
    check_resources
    
    log_message "Health check completed"
}

# Run main function
main
EOF

    chmod +x /home/$USER/monitor_services.sh
}

# Setup cron job for monitoring
setup_monitoring_cron() {
    print_status "Setting up monitoring cron job..."
    
    # Add cron job to run every 5 minutes
    (crontab -l 2>/dev/null; echo "*/5 * * * * /home/$USER/monitor_services.sh") | crontab -
}

# Create system stats script
create_stats_script() {
    print_status "Creating system stats script..."
    
    cat > /home/$USER/system_stats.sh << 'EOF'
#!/bin/bash

# System statistics script
echo "=== System Statistics ==="
echo "Date: $(date)"
echo ""

echo "=== System Resources ==="
echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')%"
echo "Memory Usage: $(free | awk 'NR==2{printf "%.1f%%", $3*100/$2}')"
echo "Disk Usage: $(df -h / | awk 'NR==2{print $5}')"
echo ""

echo "=== Docker Containers ==="
cd /home/$USER/franchise_pricing_crm
docker-compose -f docker-compose.oracle.yml ps
echo ""

echo "=== Service Health ==="
if curl -f -s http://localhost:5000/api/health > /dev/null; then
    echo "Backend: ✅ Healthy"
else
    echo "Backend: ❌ Unhealthy"
fi

if curl -f -s http://localhost/health > /dev/null; then
    echo "Frontend: ✅ Healthy"
else
    echo "Frontend: ❌ Unhealthy"
fi
echo ""

echo "=== Recent Logs ==="
echo "Backend logs (last 10 lines):"
docker-compose -f /home/$USER/franchise_pricing_crm/docker-compose.oracle.yml logs --tail=10 backend
echo ""
echo "Frontend logs (last 10 lines):"
docker-compose -f /home/$USER/franchise_pricing_crm/docker-compose.oracle.yml logs --tail=10 frontend
EOF

    chmod +x /home/$USER/system_stats.sh
}

# Create backup script
create_backup_script() {
    print_status "Creating backup script..."
    
    cat > /home/$USER/backup_system.sh << 'EOF'
#!/bin/bash

# Backup script for pricing CRM system
BACKUP_DIR="/home/$USER/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="pricing_crm_backup_$DATE.tar.gz"

# Create backup directory
mkdir -p $BACKUP_DIR

echo "Creating backup: $BACKUP_FILE"

# Create backup
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    --exclude='node_modules' \
    --exclude='venv' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    /home/$USER/franchise_pricing_crm \
    /home/$USER/pricing-frontend \
    /var/log/pricing-crm

echo "Backup created: $BACKUP_DIR/$BACKUP_FILE"

# Keep only last 7 backups
cd $BACKUP_DIR
ls -t pricing_crm_backup_*.tar.gz | tail -n +8 | xargs -r rm

echo "Backup completed successfully"
EOF

    chmod +x /home/$USER/backup_system.sh
}

# Main setup function
main() {
    create_log_directories
    setup_log_rotation
    create_monitoring_script
    setup_monitoring_cron
    create_stats_script
    create_backup_script
    
    print_status "Monitoring and logging setup completed!"
    echo ""
    echo "📊 Available commands:"
    echo "  Monitor services: ./monitor_services.sh"
    echo "  System stats: ./system_stats.sh"
    echo "  Create backup: ./backup_system.sh"
    echo ""
    echo "📝 Log files:"
    echo "  Monitor log: /var/log/pricing-crm/monitor.log"
    echo "  Application logs: docker-compose logs"
}

# Run main function
main "$@"
