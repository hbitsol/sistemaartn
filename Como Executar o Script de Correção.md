# Como Executar o Script de Correção

## Problema: Permission Denied

O erro `zsh: permission denied: ./fix_and_run_local.sh` acontece porque o arquivo não tem permissão de execução.

## Solução Passo a Passo

### Opção 1: Dar Permissão de Execução (Recomendado)

```bash
# 1. Navegar para o diretório onde está o script
cd /caminho/para/seu/projeto

# 2. Dar permissão de execução ao script
chmod +x fix_and_run_local.sh

# 3. Executar o script
./fix_and_run_local.sh
```

### Opção 2: Executar com bash diretamente

```bash
# Executar sem dar permissão de execução
bash fix_and_run_local.sh
```

### Opção 3: Executar Comandos Manualmente

Se ainda tiver problemas, execute os comandos manualmente:

```bash
# 1. Verificar se Docker está rodando
docker info

# 2. Criar diretórios necessários
mkdir -p franchise_pricing_crm/src/instance
mkdir -p franchise_pricing_crm/src/database
mkdir -p franchise_pricing_crm/logs

# 3. Criar arquivo .env se não existir
cat > franchise_pricing_crm/.env << 'EOF'
FLASK_APP=src/main.py
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_RUN_HOST=0.0.0.0
DATABASE_URL=sqlite:///instance/app.db
OPENAI_API_KEY=your_openai_key_here
SECRET_KEY=dev-secret-key-change-in-production
EOF

# 4. Parar containers existentes
docker-compose -f docker-compose.local.yml down --remove-orphans

# 5. Construir e executar
docker-compose -f docker-compose.local.yml build --no-cache
docker-compose -f docker-compose.local.yml up -d

# 6. Aguardar e testar
sleep 10
curl http://localhost:5000/api/health
```

## Estrutura de Arquivos Necessária

Certifique-se de que você tem esta estrutura:

```
seu-projeto/
├── fix_and_run_local.sh
├── docker-compose.local.yml
├── Dockerfile.local
├── main_fixed.py
├── franchise_pricing_crm/
│   ├── src/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   └── instance/
│   └── requirements.txt
└── pricing-frontend/
    ├── package.json
    └── src/
```

## Comandos de Verificação

### Verificar se o Docker está funcionando:
```bash
docker --version
docker info
```

### Verificar se os serviços estão rodando:
```bash
# Ver containers ativos
docker ps

# Ver logs do backend
docker-compose -f docker-compose.local.yml logs backend

# Testar API
curl http://localhost:5000/api/health
curl http://localhost:5000/api/materials
```

### Parar os serviços:
```bash
docker-compose -f docker-compose.local.yml down
```

## Solução de Problemas Comuns

### 1. "Docker command not found"
- Instale o Docker Desktop
- Reinicie o terminal após a instalação

### 2. "Cannot connect to Docker daemon"
- Abra o Docker Desktop
- Aguarde a inicialização completa

### 3. "Port already in use"
```bash
# Verificar o que está usando a porta 5000
lsof -i :5000

# Ou matar processos na porta 5000
sudo kill -9 $(lsof -t -i:5000)
```

### 4. "No such file or directory"
- Verifique se você está no diretório correto
- Verifique se todos os arquivos foram copiados

## Exemplo Completo de Execução

```bash
# 1. Navegar para o diretório do projeto
cd ~/meu-projeto-pricing

# 2. Listar arquivos para verificar
ls -la

# 3. Dar permissão ao script
chmod +x fix_and_run_local.sh

# 4. Executar o script
./fix_and_run_local.sh

# 5. Aguardar a mensagem de sucesso
# 6. Testar a API
curl http://localhost:5000/api/health
```

## Se Nada Funcionar

Execute este comando simples para testar apenas o backend:

```bash
# Método mais simples - apenas o backend
docker run --rm -p 5000:5000 \
  -e DATABASE_URL="sqlite:///tmp/app.db" \
  -e FLASK_ENV=development \
  -v $(pwd)/franchise_pricing_crm:/app \
  python:3.11-slim bash -c "
    cd /app && 
    pip install -r requirements.txt && 
    mkdir -p /tmp && 
    python -m flask run --host=0.0.0.0 --port=5000
  "
```

Depois teste com:
```bash
curl http://localhost:5000/api/health
```
