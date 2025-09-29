#!/bin/bash

# Oracle Cloud Deployment Script for Pricing and CRM System
# This script automates the deployment process on Oracle Cloud Free Tier

set -e

echo "🚀 Starting Oracle Cloud deployment for Pricing and CRM System..."

# Configuration variables
PROJECT_NAME="pricing-crm"
BACKEND_DIR="franchise_pricing_crm"
FRONTEND_DIR="pricing-frontend"
DOCKER_NETWORK="pricing_crm_network"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if user is in docker group
if ! groups $USER | grep &>/dev/null '\bdocker\b'; then
    print_error "User $USER is not in the docker group. Please add user to docker group and re-login."
    exit 1
fi

# Function to check if environment file exists
check_env_file() {
    if [ ! -f "$BACKEND_DIR/.env" ]; then
        print_warning "Environment file not found. Creating template..."
        cat > "$BACKEND_DIR/.env" << EOF
# Flask Configuration
FLASK_APP=src/main.py
FLASK_ENV=production
FLASK_RUN_HOST=0.0.0.0

# Database Configuration
DATABASE_URL=postgresql://username:password@hostname:port/database

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Security
SECRET_KEY=your_secret_key_here
EOF
        print_error "Please edit $BACKEND_DIR/.env with your actual configuration values"
        exit 1
    fi
}

# Function to update system packages
update_system() {
    print_status "Updating system packages..."
    sudo apt-get update -y
    sudo apt-get upgrade -y
}

# Function to install required packages
install_dependencies() {
    print_status "Installing required dependencies..."
    sudo apt-get install -y curl wget git nginx certbot python3-certbot-nginx
}

# Function to configure firewall
configure_firewall() {
    print_status "Configuring firewall rules..."
    
    # Check if ufw is installed
    if command -v ufw &> /dev/null; then
        sudo ufw --force enable
        sudo ufw allow ssh
        sudo ufw allow 80/tcp
        sudo ufw allow 443/tcp
        sudo ufw allow 5000/tcp
        print_status "Firewall configured successfully"
    else
        print_warning "UFW not installed. Please configure firewall manually."
    fi
}

# Function to create Docker network
create_docker_network() {
    print_status "Creating Docker network..."
    docker network create $DOCKER_NETWORK 2>/dev/null || print_warning "Network $DOCKER_NETWORK already exists"
}

# Function to build and start services
deploy_services() {
    print_status "Building and starting services..."
    
    # Navigate to backend directory
    cd $BACKEND_DIR
    
    # Build and start services using Docker Compose
    docker-compose -f docker-compose.oracle.yml down --remove-orphans
    docker-compose -f docker-compose.oracle.yml build --no-cache
    docker-compose -f docker-compose.oracle.yml up -d
    
    # Return to original directory
    cd ..
}

# Function to check service health
check_services() {
    print_status "Checking service health..."
    
    # Wait for services to start
    sleep 30
    
    # Check backend health
    if curl -f http://localhost:5000/api/health &>/dev/null; then
        print_status "Backend service is healthy"
    else
        print_error "Backend service is not responding"
        return 1
    fi
    
    # Check frontend health
    if curl -f http://localhost/health &>/dev/null; then
        print_status "Frontend service is healthy"
    else
        print_error "Frontend service is not responding"
        return 1
    fi
    
    print_status "All services are running successfully!"
}

# Function to display deployment information
show_deployment_info() {
    print_status "Deployment completed successfully!"
    echo ""
    echo "📋 Deployment Information:"
    echo "=========================="
    echo "🌐 Frontend URL: http://$(curl -s ifconfig.me)"
    echo "🔧 Backend API: http://$(curl -s ifconfig.me):5000"
    echo "📊 Health Check: http://$(curl -s ifconfig.me)/health"
    echo ""
    echo "🐳 Docker Services:"
    docker-compose -f $BACKEND_DIR/docker-compose.oracle.yml ps
    echo ""
    echo "📝 Logs:"
    echo "  Backend: docker-compose -f $BACKEND_DIR/docker-compose.oracle.yml logs backend"
    echo "  Frontend: docker-compose -f $BACKEND_DIR/docker-compose.oracle.yml logs frontend"
    echo ""
    echo "🔄 Management Commands:"
    echo "  Stop: docker-compose -f $BACKEND_DIR/docker-compose.oracle.yml down"
    echo "  Restart: docker-compose -f $BACKEND_DIR/docker-compose.oracle.yml restart"
    echo "  Update: ./deploy_oracle_cloud.sh"
}

# Function to setup SSL certificate (optional)
setup_ssl() {
    read -p "Do you want to setup SSL certificate with Let's Encrypt? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your domain name: " domain_name
        if [ ! -z "$domain_name" ]; then
            print_status "Setting up SSL certificate for $domain_name..."
            sudo certbot --nginx -d $domain_name --non-interactive --agree-tos --email admin@$domain_name
        fi
    fi
}

# Main deployment process
main() {
    print_status "Starting deployment process..."
    
    # Check prerequisites
    check_env_file
    
    # System setup
    update_system
    install_dependencies
    configure_firewall
    
    # Docker setup
    create_docker_network
    
    # Deploy services
    deploy_services
    
    # Health checks
    if check_services; then
        show_deployment_info
        setup_ssl
    else
        print_error "Deployment failed. Please check the logs."
        exit 1
    fi
    
    print_status "Deployment completed successfully! 🎉"
}

# Run main function
main "$@"
