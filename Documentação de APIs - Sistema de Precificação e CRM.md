# Documentação de APIs - Sistema de Precificação e CRM

**Versão:** 1.0  
**Base URL:** `http://localhost:5000/api`  
**Formato:** JSON  
**Autenticação:** JWT Bearer Token  
**Autor:** Manus AI

---

## Visão Geral

Esta documentação descreve todas as APIs disponíveis no Sistema de Precificação e CRM para Franquias de Decoração. Todas as APIs seguem padrões RESTful e retornam dados em formato JSON.

### Autenticação

A maioria dos endpoints requer autenticação via JWT (JSON Web Token). Inclua o token no header Authorization:

```
Authorization: Bearer <seu_jwt_token>
```

### Códigos de Status HTTP

- `200 OK` - Requisição bem-sucedida
- `201 Created` - Recurso criado com sucesso
- `400 Bad Request` - Dados inválidos na requisição
- `401 Unauthorized` - Token inválido ou ausente
- `403 Forbidden` - Acesso negado
- `404 Not Found` - Recurso não encontrado
- `500 Internal Server Error` - Erro interno do servidor

---

## Endpoints de Materiais

### GET /materials

Retorna lista de todos os materiais disponíveis para precificação.

**Parâmetros de Query:**
- `category` (opcional) - Filtrar por categoria
- `min_price` (opcional) - Preço mínimo
- `max_price` (opcional) - Preço máximo

**Resposta de Sucesso (200):**
```json
[
  {
    "id": "0566bbcf-97ef-4cf3-9176-9a60686d4960",
    "nome": "MDF 15mm",
    "descricao": "Chapa de MDF de 15mm de espessura",
    "unidade_medida": "m²",
    "custo_unitario_base": 45.00,
    "categoria": "Madeira",
    "fornecedor": "Fornecedor A",
    "tempo_entrega": 3,
    "especificacoes": "Densidade média, acabamento liso"
  }
]
```

### GET /materials/{id}

Retorna detalhes de um material específico.

**Parâmetros de Path:**
- `id` (obrigatório) - UUID do material

**Resposta de Sucesso (200):**
```json
{
  "id": "0566bbcf-97ef-4cf3-9176-9a60686d4960",
  "nome": "MDF 15mm",
  "descricao": "Chapa de MDF de 15mm de espessura",
  "unidade_medida": "m²",
  "custo_unitario_base": 45.00,
  "categoria": "Madeira",
  "fornecedor": "Fornecedor A",
  "tempo_entrega": 3,
  "especificacoes": "Densidade média, acabamento liso",
  "data_criacao": "2025-09-28T10:00:00Z",
  "data_atualizacao": "2025-09-28T10:00:00Z"
}
```

---

## Endpoints de Fatores de Dificuldade

### GET /difficulty-factors

Retorna lista de todos os fatores de dificuldade disponíveis.

**Resposta de Sucesso (200):**
```json
[
  {
    "id": "31960d1f-a6ae-4f5c-9e1d-c606eb8d7276",
    "nome": "Baixo",
    "multiplicador": 1.0,
    "descricao": "Projetos simples com técnicas básicas"
  },
  {
    "id": "7f8e9d2c-1a3b-4c5d-6e7f-8g9h0i1j2k3l",
    "nome": "Médio",
    "multiplicador": 1.2,
    "descricao": "Projetos com complexidade intermediária"
  },
  {
    "id": "4m5n6o7p-8q9r-0s1t-2u3v-4w5x6y7z8a9b",
    "nome": "Alto",
    "multiplicador": 1.5,
    "descricao": "Projetos complexos que requerem expertise especializada"
  }
]
```

---

## Endpoints de Precificação

### POST /calculate-price

Calcula o preço de um item baseado no material, quantidade e dificuldade.

**Corpo da Requisição:**
```json
{
  "material_id": "0566bbcf-97ef-4cf3-9176-9a60686d4960",
  "quantity": 10,
  "difficulty_id": "31960d1f-a6ae-4f5c-9e1d-c606eb8d7276"
}
```

**Resposta de Sucesso (200):**
```json
{
  "material": {
    "id": "0566bbcf-97ef-4cf3-9176-9a60686d4960",
    "nome": "MDF 15mm",
    "unidade_medida": "m²"
  },
  "quantity": 10,
  "difficulty_factor": {
    "id": "31960d1f-a6ae-4f5c-9e1d-c606eb8d7276",
    "nome": "Baixo",
    "multiplicador": 1.0
  },
  "custo_unitario_material": 45.00,
  "custo_total_material": 450.00,
  "custo_mao_obra_unitario": 25.00,
  "custo_total_mao_obra": 250.00,
  "custo_total": 700.00,
  "margem_lucro_aplicada": 0.30,
  "preco_venda_sugerido": 910.00
}
```

---

## Endpoints de Clientes

### GET /clients

Retorna lista de clientes do franqueado autenticado.

**Parâmetros de Query:**
- `franchisee_id` (obrigatório) - UUID do franqueado
- `search` (opcional) - Buscar por nome ou email
- `page` (opcional) - Número da página (padrão: 1)
- `limit` (opcional) - Itens por página (padrão: 20)

**Resposta de Sucesso (200):**
```json
[
  {
    "id": "b7bd7514-c72a-4fd3-b146-3e004ba87ad5",
    "nome": "Maria Santos",
    "email": "maria@email.com",
    "telefone": "(11) 88888-8888",
    "endereco": "Av. Paulista, 1000, São Paulo, SP",
    "id_franqueado": "2dc82321-5f18-46f6-af0f-2b9a0f84e136",
    "data_cadastro": "2025-09-28T13:37:33.025684"
  }
]
```

### POST /clients

Cria um novo cliente.

**Corpo da Requisição:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "telefone": "(11) 99999-9999",
  "endereco": "Rua das Flores, 123",
  "id_franqueado": "2dc82321-5f18-46f6-af0f-2b9a0f84e136"
}
```

**Resposta de Sucesso (201):**
```json
{
  "message": "Client created successfully",
  "client": {
    "id": "2f5433f1-e97f-4c86-95de-9dabea582eb9",
    "nome": "João Silva",
    "email": "joao@email.com",
    "telefone": "(11) 99999-9999",
    "endereco": "Rua das Flores, 123",
    "id_franqueado": "2dc82321-5f18-46f6-af0f-2b9a0f84e136",
    "data_cadastro": "2025-09-28T13:57:00.332466"
  }
}
```

### PUT /clients/{id}

Atualiza informações de um cliente existente.

**Parâmetros de Path:**
- `id` (obrigatório) - UUID do cliente

**Corpo da Requisição:**
```json
{
  "nome": "João Silva Santos",
  "telefone": "(11) 98888-8888",
  "endereco": "Rua das Flores, 123, Apto 45"
}
```

**Resposta de Sucesso (200):**
```json
{
  "message": "Client updated successfully",
  "client": {
    "id": "2f5433f1-e97f-4c86-95de-9dabea582eb9",
    "nome": "João Silva Santos",
    "email": "joao@email.com",
    "telefone": "(11) 98888-8888",
    "endereco": "Rua das Flores, 123, Apto 45",
    "id_franqueado": "2dc82321-5f18-46f6-af0f-2b9a0f84e136",
    "data_cadastro": "2025-09-28T13:57:00.332466",
    "data_atualizacao": "2025-09-28T14:15:30.123456"
  }
}
```

### DELETE /clients/{id}

Remove um cliente (apenas se não tiver projetos associados).

**Parâmetros de Path:**
- `id` (obrigatório) - UUID do cliente

**Resposta de Sucesso (200):**
```json
{
  "message": "Client deleted successfully"
}
```

---

## Endpoints de Projetos

### GET /projects

Retorna lista de projetos do franqueado autenticado.

**Parâmetros de Query:**
- `franchisee_id` (obrigatório) - UUID do franqueado
- `status` (opcional) - Filtrar por status
- `client_id` (opcional) - Filtrar por cliente
- `page` (opcional) - Número da página
- `limit` (opcional) - Itens por página

**Resposta de Sucesso (200):**
```json
[
  {
    "id": "a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6",
    "descricao": "Reforma completa da sala de estar",
    "status": "Enviado",
    "cliente": {
      "id": "b7bd7514-c72a-4fd3-b146-3e004ba87ad5",
      "nome": "Maria Santos",
      "email": "maria@email.com"
    },
    "custo_total_estimado": 2500.00,
    "preco_venda_sugerido": 3250.00,
    "margem_lucro_aplicada": 0.30,
    "data_criacao": "2025-09-28T10:00:00Z",
    "data_envio": "2025-09-28T14:30:00Z",
    "itens": [
      {
        "material": "MDF 15mm",
        "quantidade": 15,
        "custo_total": 675.00
      }
    ]
  }
]
```

### POST /projects

Cria um novo projeto.

**Corpo da Requisição:**
```json
{
  "descricao": "Reforma da cozinha",
  "id_cliente": "b7bd7514-c72a-4fd3-b146-3e004ba87ad5",
  "id_franqueado": "2dc82321-5f18-46f6-af0f-2b9a0f84e136",
  "itens": [
    {
      "material_id": "0566bbcf-97ef-4cf3-9176-9a60686d4960",
      "quantidade": 10,
      "difficulty_id": "31960d1f-a6ae-4f5c-9e1d-c606eb8d7276"
    }
  ]
}
```

**Resposta de Sucesso (201):**
```json
{
  "message": "Project created successfully",
  "project": {
    "id": "q6r7s8t9-u0v1-w2x3-y4z5-a6b7c8d9e0f1",
    "descricao": "Reforma da cozinha",
    "status": "Rascunho",
    "custo_total_estimado": 700.00,
    "preco_venda_sugerido": 910.00,
    "margem_lucro_aplicada": 0.30,
    "data_criacao": "2025-09-28T15:00:00Z"
  }
}
```

### PUT /projects/{id}

Atualiza um projeto existente.

**Parâmetros de Path:**
- `id` (obrigatório) - UUID do projeto

**Corpo da Requisição:**
```json
{
  "status": "Aprovado",
  "observacoes": "Cliente aprovou o orçamento via telefone"
}
```

**Resposta de Sucesso (200):**
```json
{
  "message": "Project updated successfully",
  "project": {
    "id": "q6r7s8t9-u0v1-w2x3-y4z5-a6b7c8d9e0f1",
    "status": "Aprovado",
    "data_aprovacao": "2025-09-28T16:30:00Z",
    "observacoes": "Cliente aprovou o orçamento via telefone"
  }
}
```

---

## Endpoints de Dashboard

### GET /dashboard/stats

Retorna estatísticas consolidadas do franqueado.

**Parâmetros de Query:**
- `franchisee_id` (obrigatório) - UUID do franqueado
- `period` (opcional) - Período para análise (month, quarter, year)

**Resposta de Sucesso (200):**
```json
{
  "total_clients": 25,
  "total_projects": 48,
  "approved_projects_count": 32,
  "total_revenue": 85000.00,
  "projects_by_status": {
    "Rascunho": 3,
    "Enviado": 8,
    "Aprovado": 32,
    "Rejeitado": 5
  },
  "conversion_rate": 0.67,
  "average_ticket": 2656.25,
  "monthly_revenue": [
    {"month": "2025-07", "revenue": 25000.00},
    {"month": "2025-08", "revenue": 30000.00},
    {"month": "2025-09", "revenue": 30000.00}
  ]
}
```

---

## Endpoints de Inteligência Artificial

### POST /ai/generate-project-description

Gera descrição profissional para um projeto baseado nos materiais.

**Corpo da Requisição:**
```json
{
  "materials": [
    {
      "name": "MDF 15mm",
      "quantity": "10",
      "unit": "m²"
    },
    {
      "name": "Tinta Acrílica",
      "quantity": "2",
      "unit": "L"
    }
  ],
  "client_info": {
    "name": "Maria Santos"
  },
  "project_type": "Reforma de sala"
}
```

**Resposta de Sucesso (200):**
```json
{
  "description": "Este projeto de reforma da sala de estar para Maria Santos utiliza materiais de alta qualidade para criar um ambiente moderno e acolhedor. O MDF 15mm proporcionará acabamento uniforme e durável para móveis planejados e revestimentos, enquanto a tinta acrílica garantirá proteção e beleza duradoura às paredes. O resultado será um espaço renovado que combina funcionalidade e estética, valorizando o imóvel e proporcionando maior conforto para toda a família.",
  "success": true
}
```

### POST /ai/suggest-materials

Sugere materiais adequados baseado nas características do projeto.

**Corpo da Requisição:**
```json
{
  "project_type": "Reforma de cozinha",
  "room_type": "cozinha",
  "budget_range": "medio",
  "style": "moderno"
}
```

**Resposta de Sucesso (200):**
```json
{
  "suggestions": [
    {
      "material_id": "0566bbcf-97ef-4cf3-9176-9a60686d4960",
      "material_name": "MDF 15mm",
      "suggested_quantity": 12,
      "unit": "m²",
      "justification": "MDF é versátil e econômico para armários e revestimentos modernos na cozinha."
    },
    {
      "material_id": "9c61ba37-5828-4399-b5ae-02d54f087cc0",
      "material_name": "Porcelanato 60x60",
      "suggested_quantity": 10,
      "unit": "m²",
      "justification": "Porcelanato oferece acabamento moderno, durabilidade e fácil limpeza para o piso da cozinha."
    }
  ]
}
```

### POST /ai/virtual-assistant

Assistente virtual para responder dúvidas sobre decoração.

**Corpo da Requisição:**
```json
{
  "question": "Qual a melhor tinta para cozinha?",
  "context": {}
}
```

**Resposta de Sucesso (200):**
```json
{
  "response": "Para cozinhas, o ideal é escolher uma tinta que seja resistente à umidade, fácil de limpar e que suporte bem a gordura e o vapor comuns nesse ambiente. A melhor opção costuma ser a tinta acrílica esmalte ou a tinta acrílica lavável com acabamento acetinado ou semi-brilho. Essas tintas oferecem boa resistência à limpeza frequente e ajudam a manter a parede com aspecto bonito por mais tempo.",
  "success": true
}
```

### POST /ai/analyze-pricing-trends

Analisa tendências de preços e fornece insights de otimização.

**Corpo da Requisição:**
```json
{
  "franchisee_id": "2dc82321-5f18-46f6-af0f-2b9a0f84e136"
}
```

**Resposta de Sucesso (200):**
```json
{
  "analysis": "Baseado no histórico de 48 projetos, sua taxa de conversão de 67% está acima da média do mercado. Projetos na faixa de R$ 2.000-3.000 têm maior taxa de aprovação (78%), enquanto projetos acima de R$ 5.000 têm conversão menor (45%). Recomenda-se focar em projetos de médio porte e considerar estratégias de parcelamento para projetos maiores.",
  "recommendations": [
    "Focar em projetos na faixa de R$ 2.000-3.000 para maximizar conversão",
    "Oferecer opções de parcelamento para projetos acima de R$ 4.000",
    "Desenvolver pacotes promocionais para aumentar ticket médio"
  ],
  "key_metrics": {
    "average_margin": "28.5%",
    "approval_rate": "67%",
    "average_ticket": "R$ 2.656"
  }
}
```

---

## Códigos de Erro Comuns

### 400 Bad Request
```json
{
  "error": "Validation failed",
  "details": {
    "material_id": ["Este campo é obrigatório"],
    "quantity": ["Deve ser um número positivo"]
  }
}
```

### 401 Unauthorized
```json
{
  "error": "Token inválido ou expirado",
  "code": "INVALID_TOKEN"
}
```

### 403 Forbidden
```json
{
  "error": "Acesso negado. Você não tem permissão para acessar este recurso",
  "code": "ACCESS_DENIED"
}
```

### 404 Not Found
```json
{
  "error": "Recurso não encontrado",
  "code": "RESOURCE_NOT_FOUND"
}
```

### 500 Internal Server Error
```json
{
  "error": "Erro interno do servidor. Tente novamente mais tarde",
  "code": "INTERNAL_ERROR"
}
```

---

## Exemplos de Uso

### Fluxo Completo de Criação de Orçamento

1. **Obter lista de materiais:**
```bash
curl -X GET "http://localhost:5000/api/materials" \
  -H "Authorization: Bearer <token>"
```

2. **Obter fatores de dificuldade:**
```bash
curl -X GET "http://localhost:5000/api/difficulty-factors" \
  -H "Authorization: Bearer <token>"
```

3. **Calcular preço:**
```bash
curl -X POST "http://localhost:5000/api/calculate-price" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "material_id": "0566bbcf-97ef-4cf3-9176-9a60686d4960",
    "quantity": 10,
    "difficulty_id": "31960d1f-a6ae-4f5c-9e1d-c606eb8d7276"
  }'
```

4. **Criar projeto:**
```bash
curl -X POST "http://localhost:5000/api/projects" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "descricao": "Reforma da sala",
    "id_cliente": "b7bd7514-c72a-4fd3-b146-3e004ba87ad5",
    "id_franqueado": "2dc82321-5f18-46f6-af0f-2b9a0f84e136",
    "itens": [...]
  }'
```

### Utilizando IA para Sugestões

```bash
curl -X POST "http://localhost:5000/api/ai/suggest-materials" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "project_type": "Reforma de cozinha",
    "room_type": "cozinha",
    "budget_range": "medio",
    "style": "moderno"
  }'
```

---

## Limitações e Considerações

### Rate Limiting

As APIs de IA têm limitação de 100 requisições por hora por usuário para evitar sobrecarga dos serviços externos. Outras APIs têm limite de 1000 requisições por hora.

### Tamanho de Requisições

O tamanho máximo de requisições é 10MB. Para uploads de arquivos maiores, utilize endpoints específicos de upload.

### Timeout

Todas as requisições têm timeout de 30 segundos. APIs de IA podem levar até 10 segundos para responder devido ao processamento de linguagem natural.

### Versionamento

Esta é a versão 1.0 da API. Futuras versões manterão compatibilidade com versões anteriores sempre que possível. Mudanças breaking serão comunicadas com antecedência mínima de 30 dias.

