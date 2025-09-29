## Guia de Instalação e Deployment do Sistema de Precificação e CRM

Este guia detalha as etapas para instalar e implantar o sistema de precificação e CRM, com foco na implantação em produção utilizando a DigitalOcean App Platform, mas também cobrindo opções de desenvolvimento local e Docker.

---

### 1. Visão Geral da Arquitetura

O sistema é composto por dois componentes principais:

*   **Backend (Flask):** Uma API RESTful que gerencia a lógica de precificação, dados de materiais, fatores de dificuldade, gestão de clientes, projetos e integrações com IA.
*   **Frontend (React):** Uma aplicação web que fornece a interface do usuário para franqueados, permitindo a interação com a calculadora de preços, CRM e funcionalidades de IA.

---

### 2. Deployment em Produção (DigitalOcean App Platform - Recomendado)

A DigitalOcean App Platform é uma excelente escolha para implantar este MVP, pois simplifica o deployment, gerenciamento e escalabilidade. Ela suporta a implantação de múltiplos componentes (backend e frontend) dentro do mesmo aplicativo.

#### Pré-requisitos:

*   Conta na DigitalOcean.
*   Código-fonte do **backend** (`franchise_pricing_crm`) e **frontend** (`pricing-frontend`) em repositórios Git (GitHub, GitLab, etc.).
*   `extracted_pricing_data.json` deve estar na raiz do diretório `franchise_pricing_crm`.

#### 2.1. Implantação do Backend (Flask com Docker)

Para o backend, utilizaremos um `Dockerfile` para garantir que todas as dependências sejam resolvidas corretamente no ambiente de contêiner.

1.  **Verifique o `Dockerfile`:** Certifique-se de que o `Dockerfile` está na raiz do diretório `franchise_pricing_crm` e tem o seguinte conteúdo:

    ```dockerfile
    FROM python:3.11-slim-buster

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    EXPOSE 5000

    ENV FLASK_APP=src/main.py
    ENV FLASK_RUN_HOST=0.0.0.0

    CMD ["flask", "run"]
    ```

2.  **Verifique `requirements.txt`:** Certifique-se de que o arquivo `requirements.txt` na raiz do diretório `franchise_pricing_crm` lista todas as dependências Python, incluindo `openai`, `pandas`, `openpyxl`, `Flask`, `Flask-CORS`, `Flask-SQLAlchemy`, etc. Exemplo:

    ```
    blinker==1.9.0
    click==8.2.1
    Flask==3.1.1
    flask-cors==6.0.0
    Flask-SQLAlchemy==3.1.1
    itsdangerous==2.2.0
    Jinja2==3.1.6
    MarkupSafe==3.0.2
    SQLAlchemy==2.0.41
    typing_extensions==4.14.0
    Werkzeug==3.1.3
    openai==1.109.1
    pandas==2.2.2
    openpyxl==3.1.2
    ```

3.  **Crie um Aplicativo na DigitalOcean App Platform:**
    *   No painel da DigitalOcean, navegue até **Apps** e clique em **Create App**.
    *   Conecte seu repositório Git onde o código do backend (`franchise_pricing_crm`) está hospedado.
    *   A DigitalOcean detectará automaticamente o `Dockerfile` e sugerirá um **Service** component.
    *   **Configurações do Componente (Service):**
        *   **Source:** Seu repositório Git.
        *   **Branch:** A branch que você deseja implantar (ex: `main` ou `master`).
        *   **Build Command:** Deixe em branco (o Dockerfile cuidará do build).
        *   **Run Command:** `flask run` (conforme definido no Dockerfile).
        *   **HTTP Port:** `5000` (conforme definido no Dockerfile).
        *   **Environment Variables:** Adicione as variáveis de ambiente necessárias:
            *   `DATABASE_URL`: URL de conexão com seu banco de dados (ex: `postgresql://user:password@host:port/database`).
            *   `OPENAI_API_KEY`: Sua chave de API da OpenAI (use como segredo).
            *   `FLASK_ENV`: `production`
            *   `FLASK_APP`: `src/main.py`
        *   **Health Check:** Configure um health check HTTP para `/` ou `/api/health` (se você criar um endpoint de saúde).

4.  **Crie um Banco de Dados Gerenciado (Opcional, mas Recomendado):**
    *   Na DigitalOcean, vá para **Databases** e crie um novo banco de dados (ex: PostgreSQL).
    *   Conecte este banco de dados ao seu aplicativo na App Platform. A DigitalOcean injetará automaticamente a `DATABASE_URL` como uma variável de ambiente no seu componente de serviço.

5.  **Deployment Inicial:** Após configurar o componente de serviço e o banco de dados, inicie o deployment. A App Platform construirá a imagem Docker e implantará o serviço.

#### 2.2. Implantação do Frontend (React)

1.  **Verifique o `package.json`:** Certifique-se de que o `package.json` na raiz do diretório `pricing-frontend` tem um script `build` que gera os arquivos estáticos para deployment (ex: `"build": "vite build"`).

2.  **Crie um Componente de Site Estático:**
    *   No mesmo aplicativo da App Platform, adicione um novo componente e selecione **Static Site**.
    *   **Source:** Seu repositório Git onde o código do frontend (`pricing-frontend`) está hospedado.
    *   **Branch:** A branch que você deseja implantar.
    *   **Build Command:** `npm install && npm run build` ou `pnpm install && pnpm run build`.
    *   **Output Directory:** `dist` (ou o diretório onde seu build gera os arquivos estáticos).
    *   **Environment Variables:** Se o frontend precisar se comunicar com o backend implantado, você precisará de uma variável de ambiente para a URL da API do backend. Por exemplo:
        *   `VITE_API_URL`: A URL do seu serviço de backend na App Platform (ex: `https://seu-backend.ondigitalocean.app`).

3.  **Deployment:** Inicie o deployment do componente de site estático. A App Platform construirá o frontend e o disponibilizará.

#### 2.3. Configuração de Domínio Personalizado (Opcional)

*   Após o deployment, você pode adicionar um domínio personalizado (ex: `app.suafranquia.com.br`) aos seus componentes de frontend e/ou backend na App Platform.

#### 2.4. Inicialização do Banco de Dados em Produção

Após o deployment do backend, você precisará inicializar o banco de dados e popular os dados iniciais (materiais, fatores de dificuldade, etc.).

*   **Opção 1 (Recomendado - Via Endpoint):** Se você tiver um endpoint de seed de dados (como `/api/seed-data` que criamos), você pode fazer uma requisição POST para ele após o deployment para popular o banco de dados.
*   **Opção 2 (Via Console da App Platform):** Você pode acessar o console do seu componente de serviço na App Platform e executar comandos Python para inicializar o banco de dados e rodar o script de seed:

    ```bash
    flask db upgrade # Se estiver usando Flask-Migrate
    python -c "from src.main import app; with app.app_context(): from src.routes.seed_data import seed_data; seed_data()"
    ```

---

### 3. Instalação e Execução Local (Ambiente de Desenvolvimento)

Para desenvolvimento local, você pode executar o backend e o frontend separadamente.

#### 3.1. Backend (Flask)

1.  **Navegue até o diretório do backend:**
    ```bash
    cd franchise_pricing_crm
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure as variáveis de ambiente:**
    ```bash
    export FLASK_APP=src/main.py
    export FLASK_ENV=development
    export DATABASE_URL="sqlite:///instance/app.db" # Ou sua URL de banco de dados local
    export OPENAI_API_KEY="sua_chave_openai"
    ```
5.  **Inicialize o banco de dados e popule os dados (se necessário):**
    ```bash
    flask db upgrade # Se estiver usando Flask-Migrate
    python -c "from src.main import app; with app.app_context(): from src.routes.seed_data import seed_data; seed_data()"
    ```
6.  **Execute o servidor Flask:**
    ```bash
    flask run
    ```
    O backend estará disponível em `http://127.0.0.1:5000`.

#### 3.2. Frontend (React)

1.  **Navegue até o diretório do frontend:**
    ```bash
    cd pricing-frontend
    ```
2.  **Instale as dependências:**
    ```bash
    pnpm install # ou npm install / yarn install
    ```
3.  **Configure a variável de ambiente para a API do backend:**
    *   Crie um arquivo `.env.local` na raiz do diretório `pricing-frontend` com o seguinte conteúdo:
        ```
        VITE_API_URL=http://localhost:5000
        ```
4.  **Execute o servidor de desenvolvimento React:**
    ```bash
    pnpm run dev # ou npm run dev / yarn dev
    ```
    O frontend estará disponível em `http://localhost:5173` (ou outra porta, dependendo da configuração do Vite).

---

### 4. Deployment com Docker (Manual)

Se você preferir um controle mais granular ou usar outro provedor de nuvem que suporte Docker, pode construir e executar a imagem Docker manualmente.

1.  **Navegue até o diretório do backend:**
    ```bash
    cd franchise_pricing_crm
    ```
2.  **Construa a imagem Docker:**
    ```bash
    docker build -t meu-backend-franquia .
    ```
3.  **Execute o contêiner Docker:**
    ```bash
    docker run -p 5000:5000 -e DATABASE_URL="sua_url_db" -e OPENAI_API_KEY="sua_chave_openai" meu-backend-franquia
    ```
    Substitua `sua_url_db` e `sua_chave_openai` pelos valores reais. O backend estará disponível em `http://localhost:5000`.

---

### 5. Considerações Finais

*   **Segurança:** Sempre use variáveis de ambiente para credenciais e chaves de API, e nunca as exponha diretamente no código-fonte.
*   **HTTPS:** Em produção, certifique-se de que seu aplicativo esteja servindo tráfego via HTTPS. A DigitalOcean App Platform geralmente configura isso automaticamente.
*   **Backup:** Implemente uma estratégia de backup regular para seu banco de dados.
*   **Monitoramento:** Monitore a performance e os logs da sua aplicação para identificar e resolver problemas rapidamente.

Este guia deve fornecer todas as informações necessárias para implantar e gerenciar seu sistema. Em caso de dúvidas, consulte a documentação oficial da DigitalOcean ou entre em contato com o suporte.

