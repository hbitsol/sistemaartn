#!/bin/bash

# Script para corrigir e executar o sistema localmente com Docker

set -e

echo "🔧 Corrigindo problemas do SQLite e configurando ambiente local..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    print_error "Docker não está rodando. Por favor, inicie o Docker Desktop."
    exit 1
fi

# Criar diretórios necessários
print_status "Criando diretórios necessários..."
mkdir -p franchise_pricing_crm/src/instance
mkdir -p franchise_pricing_crm/src/database
mkdir -p franchise_pricing_crm/logs

# Copiar arquivos corrigidos
print_status "Aplicando correções..."

# Copiar o main.py corrigido
if [ -f "main_fixed.py" ]; then
    cp main_fixed.py franchise_pricing_crm/src/main.py
    print_status "main.py corrigido aplicado"
fi

# Copiar Dockerfile para desenvolvimento local
if [ -f "Dockerfile.local" ]; then
    cp Dockerfile.local franchise_pricing_crm/
    print_status "Dockerfile local criado"
fi

# Criar arquivo .env local se não existir
if [ ! -f "franchise_pricing_crm/.env" ]; then
    print_status "Criando arquivo .env local..."
    cat > franchise_pricing_crm/.env << EOF
# Configuração local para desenvolvimento
FLASK_APP=src/main.py
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_RUN_HOST=0.0.0.0

# Database local (SQLite)
DATABASE_URL=sqlite:///instance/app.db

# OpenAI (opcional para testes)
OPENAI_API_KEY=your_openai_key_here

# Secret key para desenvolvimento
SECRET_KEY=dev-secret-key-change-in-production
EOF
fi

# Parar containers existentes
print_status "Parando containers existentes..."
docker-compose -f docker-compose.local.yml down --remove-orphans 2>/dev/null || true

# Remover imagens antigas
print_warning "Removendo imagens antigas..."
docker rmi pricing_crm_backend_local 2>/dev/null || true
docker rmi pricing_crm_frontend_local 2>/dev/null || true

# Construir e executar
print_status "Construindo e executando containers..."
docker-compose -f docker-compose.local.yml build --no-cache
docker-compose -f docker-compose.local.yml up -d

# Aguardar serviços iniciarem
print_status "Aguardando serviços iniciarem..."
sleep 10

# Verificar se os serviços estão rodando
print_status "Verificando status dos serviços..."

# Verificar backend
if curl -f -s http://localhost:5000/api/health > /dev/null; then
    print_status "✅ Backend está rodando em http://localhost:5000"
else
    print_error "❌ Backend não está respondendo"
    echo "Logs do backend:"
    docker-compose -f docker-compose.local.yml logs backend
fi

# Verificar frontend (se estiver configurado)
if curl -f -s http://localhost:3000 > /dev/null 2>&1; then
    print_status "✅ Frontend está rodando em http://localhost:3000"
else
    print_warning "⚠️ Frontend pode ainda estar iniciando ou não configurado"
fi

# Seed do banco de dados
print_status "Populando banco de dados com dados iniciais..."
sleep 5
if curl -f -s -X POST http://localhost:5000/api/seed-data > /dev/null; then
    print_status "✅ Dados iniciais carregados com sucesso"
else
    print_warning "⚠️ Falha ao carregar dados iniciais (pode ser normal se já existirem)"
fi

echo ""
print_status "🎉 Sistema configurado com sucesso!"
echo ""
echo "📋 URLs disponíveis:"
echo "   Backend API: http://localhost:5000"
echo "   Health Check: http://localhost:5000/api/health"
echo "   Materiais: http://localhost:5000/api/materials"
echo "   Frontend: http://localhost:3000 (se configurado)"
echo ""
echo "🐳 Comandos úteis:"
echo "   Ver logs: docker-compose -f docker-compose.local.yml logs"
echo "   Parar: docker-compose -f docker-compose.local.yml down"
echo "   Reiniciar: docker-compose -f docker-compose.local.yml restart"
echo ""
echo "🔧 Para testar a API:"
echo "   curl http://localhost:5000/api/health"
echo "   curl http://localhost:5000/api/materials"
