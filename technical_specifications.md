# Especificações Técnicas do MVP de Precificação e CRM para Franquias de Decoração

## 1. Arquitetura Geral do Sistema

O MVP será construído com uma arquitetura de três camadas, visando modularidade, escalabilidade e facilidade de manutenção. Esta abordagem permitirá a separação clara das responsabilidades entre a interface do usuário, a lógica de negócios e o armazenamento de dados.

### 1.1. Camada de Apresentação (Frontend)

Esta camada será responsável pela interface do usuário, permitindo que os franqueados interajam com o sistema de forma intuitiva. Será uma aplicação web acessível via navegador.

### 1.2. Camada de Lógica de Negócios (Backend)

O backend abrigará toda a lógica de negócios, incluindo o motor de precificação, a gestão de dados do CRM, a autenticação de usuários e a integração com serviços de IA. Ele atuará como uma API que o frontend consumirá.

### 1.3. Camada de Dados (Database)

Esta camada será responsável pelo armazenamento persistente de todos os dados do sistema, incluindo informações de materiais, custos, franqueados, clientes e projetos.

## 2. Escolha de Tecnologias

Para garantir um desenvolvimento ágil e um MVP robusto, as seguintes tecnologias serão utilizadas:

### 2.1. Frontend

*   **Framework:** React.js (com Create React App ou Vite para agilidade na configuração).
*   **Linguagem:** JavaScript/TypeScript.
*   **Estilização:** CSS Modules ou Styled Components para modularidade e escopo de estilos.
*   **Motivação:** React.js é uma biblioteca popular para construção de interfaces de usuário interativas e reativas, com uma vasta comunidade e ecossistema, o que facilita o desenvolvimento e a busca por soluções.

### 2.2. Backend

*   **Framework:** Flask (Python).
*   **Linguagem:** Python.
*   **Motivação:** Flask é um microframework web leve e flexível para Python, ideal para construir APIs RESTful de forma rápida. Python é uma linguagem versátil, com forte suporte para IA e manipulação de dados, o que será benéfico para o motor de precificação e futuras integrações de IA.

### 2.3. Banco de Dados

*   **Tipo:** PostgreSQL (Relacional).
*   **Motivação:** PostgreSQL é um sistema de gerenciamento de banco de dados relacional robusto, de código aberto, conhecido por sua confiabilidade, integridade de dados e capacidade de lidar com dados complexos. É uma excelente escolha para armazenar informações estruturadas como materiais, custos, franqueados e clientes.

## 3. Especificações das APIs de IA

Para o MVP, a integração com IA será focada em otimizar a precificação e, futuramente, aprimorar o CRM. Inicialmente, a 


integração será mais conceitual, com a lógica de precificação incorporando fatores de dificuldade e tipo de material que podem ser ajustados com base em análises futuras de IA. No entanto, para futuras iterações, as seguintes APIs de IA podem ser consideradas:

### 3.1. Precificação Otimizada (Futuro)

*   **Serviço:** Poderíamos utilizar APIs de Machine Learning (ML) de plataformas como Google Cloud AI Platform, AWS SageMaker ou Azure Machine Learning para construir e treinar modelos de precificação. Estes modelos poderiam analisar dados históricos de vendas, custos, concorrência e sazonalidade para sugerir preços ideais e fatores de dificuldade.
*   **Funcionalidade no MVP:** No MVP, a "IA" na precificação será simulada por regras de negócio configuráveis (fatores multiplicadores para dificuldade, custos base por material) que o franqueador poderá ajustar. A base para a IA será a coleta de dados de cada transação para futuro treinamento de modelos.

### 3.2. Automação e Análise de CRM (Futuro)

*   **Serviço:** APIs de Processamento de Linguagem Natural (NLP) como Google Cloud Natural Language API ou OpenAI GPT (para análise de sentimento, sumarização de interações com clientes) e APIs de Machine Learning para Lead Scoring.
*   **Funcionalidade no MVP:** O CRM no MVP terá funcionalidades básicas de gestão de contatos e pipeline de vendas. A coleta de dados de interação com o cliente será fundamental para futuras integrações de IA, como análise de sentimento em e-mails ou chamadas registradas.

## 4. Estrutura do Banco de Dados

O banco de dados PostgreSQL será estruturado para armazenar as seguintes entidades principais:

### 4.1. Usuários (Franqueados)

*   `id` (PK, UUID)
*   `nome` (VARCHAR)
*   `email` (VARCHAR, UNIQUE)
*   `senha_hash` (VARCHAR)
*   `id_franquia` (FK para Franquias)
*   `data_cadastro` (TIMESTAMP)

### 4.2. Franquias

*   `id` (PK, UUID)
*   `nome_franquia` (VARCHAR, UNIQUE)
*   `cnpj` (VARCHAR, UNIQUE)
*   `endereco` (VARCHAR)
*   `telefone` (VARCHAR)

### 4.3. Materiais

*   `id` (PK, UUID)
*   `nome` (VARCHAR, UNIQUE)
*   `unidade_medida` (VARCHAR - ex: 'm', 'm²', 'un', 'L', 'kg')
*   `custo_unitario_base` (DECIMAL)
*   `descricao` (TEXT)
*   `data_atualizacao` (TIMESTAMP)

### 4.4. Fatores de Dificuldade

*   `id` (PK, UUID)
*   `nivel` (VARCHAR - ex: 'Baixo', 'Médio', 'Alto', UNIQUE)
*   `fator_multiplicador_mao_obra` (DECIMAL)
*   `descricao` (TEXT)

### 4.5. Projetos (Orçamentos)

*   `id` (PK, UUID)
*   `id_franqueado` (FK para Usuários)
*   `id_cliente` (FK para Clientes)
*   `nome_projeto` (VARCHAR)
*   `data_criacao` (TIMESTAMP)
*   `status` (VARCHAR - ex: 'Rascunho', 'Enviado', 'Aprovado', 'Rejeitado')
*   `margem_lucro_aplicada` (DECIMAL)
*   `custo_total_estimado` (DECIMAL)
*   `preco_venda_sugerido` (DECIMAL)

### 4.6. Itens do Projeto

*   `id` (PK, UUID)
*   `id_projeto` (FK para Projetos)
*   `id_material` (FK para Materiais)
*   `quantidade` (DECIMAL)
*   `id_dificuldade` (FK para Fatores de Dificuldade)
*   `custo_item` (DECIMAL)
*   `preco_venda_item` (DECIMAL)
*   `observacoes` (TEXT)

### 4.7. Clientes

*   `id` (PK, UUID)
*   `id_franqueado` (FK para Usuários - indica qual franqueado gerencia este cliente)
*   `nome` (VARCHAR)
*   `email` (VARCHAR)
*   `telefone` (VARCHAR)
*   `endereco` (VARCHAR)
*   `data_cadastro` (TIMESTAMP)

## 5. Detalhamento das Funcionalidades do MVP

### 5.1. Módulo de Precificação

*   **Interface:** Formulário no frontend onde o franqueado seleciona o tipo de material, insere a quantidade e escolhe o grau de dificuldade para cada item do projeto.
*   **Cálculo:** O backend receberá esses dados, consultará os custos unitários dos materiais e os fatores de dificuldade no banco de dados, aplicará a lógica de cálculo definida e retornará o custo total e o preço de venda sugerido para o item e para o projeto completo.
*   **Configuração:** Interface administrativa (para o franqueador) para gerenciar materiais (adicionar, editar, remover), seus custos unitários, unidades de medida, e os fatores de dificuldade.

### 5.2. Módulo CRM Simplificado

*   **Gestão de Clientes:** Cadastro, edição e visualização de informações de clientes (nome, contato, endereço).
*   **Gestão de Projetos/Orçamentos:** Criação, edição, visualização e acompanhamento do status de projetos/orçamentos associados a clientes específicos.
*   **Histórico de Interações:** Registro manual de interações com clientes (ligações, e-mails, reuniões) dentro do contexto de um projeto.

## 6. Considerações de Segurança

*   **Autenticação:** Sistema de login para franqueados com senhas hashadas.
*   **Autorização:** Controle de acesso baseado em papéis para diferenciar franqueados e franqueador.
*   **Proteção de Dados:** Uso de HTTPS para todas as comunicações entre frontend e backend.

## 7. Próximos Passos

Com esta arquitetura e especificações em mente, o próximo passo será iniciar o desenvolvimento do backend, seguido pelo frontend e, por fim, a integração e testes.

