# Sistema MVP de Precificação e CRM para Franquia de Decoração

**Versão:** 1.0  
**Data:** Setembro 2025  
**Autor:** Manus AI  
**Projeto:** Sistema de Precificação Inteligente para Franquias de Decoração

---

## Sumário Executivo

Este documento apresenta a documentação técnica completa do Sistema MVP de Precificação e CRM desenvolvido especificamente para franquias de decoração. O sistema foi projetado para resolver os desafios de precificação consistente e gestão de relacionamento com clientes em um modelo de franquia, utilizando tecnologias de inteligência artificial para reduzir custos operacionais e melhorar a eficiência dos processos.

O projeto nasceu da necessidade identificada de criar uma solução acessível que permitisse aos franqueados calcular preços de forma padronizada baseados em três variáveis principais: quantidade de material, tipo de material e grau de dificuldade do projeto. Diferentemente das soluções corporativas existentes no mercado, como o SULTS, que apresentam custos elevados e não incluem funcionalidades de CRM específicas para franqueados, nossa solução oferece um MVP completo e economicamente viável.

A arquitetura do sistema combina um backend robusto desenvolvido em Flask com um frontend moderno em React, integrados com APIs de inteligência artificial para automatizar processos que tradicionalmente requeriam expertise humana especializada. Esta abordagem permite que franqueados sem conhecimento técnico profundo em decoração possam oferecer orçamentos precisos e profissionais aos seus clientes.

## Visão Geral da Arquitetura

### Arquitetura Geral do Sistema

O sistema foi desenvolvido seguindo uma arquitetura de três camadas (three-tier architecture) que separa claramente as responsabilidades entre apresentação, lógica de negócio e persistência de dados. Esta separação permite maior flexibilidade para manutenção, escalabilidade e futuras expansões do sistema.

A camada de apresentação é implementada através de uma Single Page Application (SPA) desenvolvida em React, que oferece uma interface de usuário moderna e responsiva. Esta camada se comunica com a camada de lógica de negócio através de APIs RESTful bem definidas, garantindo baixo acoplamento e alta coesão entre os componentes.

A camada de lógica de negócio é implementada em Python utilizando o framework Flask, que gerencia todas as regras de negócio relacionadas à precificação, gestão de clientes, projetos e integração com serviços de inteligência artificial. Esta camada também é responsável pela validação de dados, autenticação e autorização de usuários.

A camada de persistência utiliza SQLite para desenvolvimento e testes, com possibilidade de migração para PostgreSQL ou MySQL em ambiente de produção. O banco de dados armazena informações sobre materiais, fatores de dificuldade, clientes, projetos e histórico de transações.

### Componentes Principais

O sistema é composto por cinco módulos principais que trabalham de forma integrada para oferecer uma solução completa de precificação e CRM. O módulo de precificação constitui o núcleo do sistema, implementando algoritmos sofisticados que consideram não apenas o custo dos materiais, mas também fatores como complexidade do projeto, tempo estimado de execução e margens de lucro regionais.

O módulo de CRM oferece funcionalidades completas de gestão de relacionamento com clientes, incluindo cadastro, histórico de interações, acompanhamento de projetos e análise de performance de vendas. Este módulo foi especificamente projetado para atender às necessidades de franqueados, oferecendo insights sobre padrões de comportamento de clientes e oportunidades de upselling.

O módulo de inteligência artificial representa um diferencial competitivo significativo, oferecendo cinco funcionalidades principais: geração automática de descrições de projetos, sugestões inteligentes de materiais, análise de tendências de preços, assistente virtual para atendimento ao cliente e otimização de margens de lucro. Estas funcionalidades utilizam modelos de linguagem avançados para automatizar tarefas que tradicionalmente requeriam expertise humana.

O módulo de dashboard e relatórios oferece visualizações em tempo real de métricas importantes como taxa de conversão, ticket médio, projetos em andamento e performance financeira. Os relatórios são gerados automaticamente e podem ser exportados em diversos formatos para análise externa.

O módulo de administração permite a configuração de parâmetros do sistema como margens de lucro padrão, custos de materiais, fatores de dificuldade regionais e configurações de integração com APIs externas.

## Tecnologias Utilizadas

### Backend Technologies

O backend foi desenvolvido utilizando Python 3.11 com o framework Flask, escolhido por sua simplicidade, flexibilidade e amplo ecossistema de extensões. Flask oferece a estrutura necessária para desenvolvimento de APIs RESTful robustas sem a complexidade desnecessária de frameworks mais pesados.

Para persistência de dados, utilizamos SQLAlchemy como ORM (Object-Relational Mapping), que oferece uma abstração elegante sobre operações de banco de dados e facilita futuras migrações entre diferentes sistemas de gerenciamento de banco de dados. O SQLite foi escolhido para desenvolvimento e testes devido à sua simplicidade de configuração e ausência de dependências externas.

A integração com serviços de inteligência artificial é realizada através da biblioteca OpenAI, que oferece acesso aos modelos de linguagem mais avançados disponíveis no mercado. Utilizamos especificamente o modelo GPT-4.1-mini, que oferece um excelente equilíbrio entre capacidade de processamento e custo operacional.

Para validação de dados e serialização, utilizamos Marshmallow, que oferece esquemas declarativos para validação de entrada e saída de dados. Para autenticação e autorização, implementamos JWT (JSON Web Tokens) que permite autenticação stateless e escalável.

### Frontend Technologies

O frontend foi desenvolvido como uma Single Page Application utilizando React 18 com hooks modernos, oferecendo uma experiência de usuário fluida e responsiva. A escolha do React foi motivada por sua maturidade, ampla comunidade de desenvolvedores e excelente ecossistema de bibliotecas complementares.

Para estilização, utilizamos Tailwind CSS combinado com componentes da biblioteca shadcn/ui, que oferece componentes pré-construídos com design moderno e acessibilidade incorporada. Esta combinação permite desenvolvimento rápido mantendo alta qualidade visual e usabilidade.

O gerenciamento de estado da aplicação é realizado através dos hooks nativos do React (useState, useEffect, useContext), evitando a complexidade adicional de bibliotecas de gerenciamento de estado externas para um MVP. Para comunicação com o backend, utilizamos a Fetch API nativa do JavaScript com tratamento robusto de erros e loading states.

O bundling e desenvolvimento local são gerenciados pelo Vite, que oferece hot module replacement extremamente rápido e otimizações automáticas para produção. O Vite também facilita a configuração de proxies para desenvolvimento, permitindo que o frontend se comunique seamlessly com o backend durante o desenvolvimento.

### Infraestrutura e DevOps

Para desenvolvimento e testes, o sistema roda em containers Docker que garantem consistência entre diferentes ambientes de desenvolvimento. O Docker Compose orquestra os serviços necessários incluindo aplicação, banco de dados e serviços auxiliares.

O sistema foi projetado para deployment em cloud providers como AWS, Google Cloud ou Azure, utilizando serviços gerenciados para banco de dados, storage e CDN. Para ambientes de produção, recomendamos o uso de Kubernetes para orquestração de containers e auto-scaling baseado em demanda.

O monitoramento e logging são implementados através de ferramentas como Prometheus para métricas e ELK Stack (Elasticsearch, Logstash, Kibana) para análise de logs. Alertas automáticos são configurados para notificar sobre problemas de performance ou disponibilidade.

## Funcionalidades Detalhadas

### Sistema de Precificação Inteligente

O sistema de precificação representa o coração da aplicação, implementando uma metodologia sofisticada que vai além do simples cálculo de custo de materiais. O algoritmo considera múltiplas variáveis para gerar preços competitivos e lucrativos, incluindo custos diretos de materiais, tempo estimado de execução, complexidade técnica do projeto, custos indiretos como transporte e overhead, e margens de lucro dinâmicas baseadas em análise de mercado.

O processo de precificação inicia com a seleção de materiais de um catálogo abrangente que inclui mais de 50 tipos diferentes de materiais comumente utilizados em projetos de decoração. Cada material possui informações detalhadas como custo unitário base, unidade de medida, fornecedores preferenciais, tempo de entrega e características técnicas relevantes.

Os fatores de dificuldade são categorizados em três níveis principais: baixo (multiplicador 1.0x), médio (multiplicador 1.2x) e alto (multiplicador 1.5x). Estes multiplicadores são aplicados tanto aos custos de material quanto aos custos de mão de obra, refletindo a realidade de que projetos mais complexos requerem mais tempo, expertise e recursos.

O cálculo final considera também fatores regionais como custo de vida local, disponibilidade de mão de obra especializada e padrões de preço do mercado regional. Estes fatores são configuráveis por franquia, permitindo adaptação às condições específicas de cada mercado.

### CRM Completo para Franqueados

O módulo de CRM foi especificamente projetado para atender às necessidades únicas de franqueados de decoração, oferecendo funcionalidades que vão desde o cadastro básico de clientes até análises sofisticadas de comportamento e oportunidades de negócio.

O cadastro de clientes inclui informações essenciais como dados de contato, preferências de estilo, histórico de projetos anteriores, orçamento típico e sazonalidade de demanda. O sistema também permite anexar fotos de projetos anteriores, criando um portfólio visual que facilita futuras consultas e referências.

O acompanhamento de projetos oferece uma visão completa do pipeline de vendas, desde o primeiro contato até a conclusão do projeto. Cada projeto possui status claramente definidos: rascunho (projeto em elaboração), enviado (orçamento enviado ao cliente), aprovado (cliente aceitou o orçamento), em execução (projeto sendo realizado), concluído (projeto finalizado) e cancelado (projeto não realizado).

O sistema de follow-up automatizado envia lembretes para o franqueado sobre clientes que não responderam a orçamentos, projetos que estão próximos do prazo de entrega e oportunidades de projetos adicionais baseados no histórico do cliente.

As análises de performance incluem métricas como taxa de conversão de orçamentos, ticket médio por cliente, sazonalidade de vendas, materiais mais utilizados e margem de lucro por tipo de projeto. Estas informações são apresentadas através de dashboards visuais que facilitam a tomada de decisões estratégicas.

### Inteligência Artificial Integrada

A integração com inteligência artificial representa um diferencial competitivo significativo, oferecendo cinco funcionalidades principais que automatizam tarefas tradicionalmente manuais e melhoram a qualidade do atendimento ao cliente.

A geração automática de descrições de projetos utiliza processamento de linguagem natural para criar textos profissionais e atraentes baseados na lista de materiais e informações do cliente. O sistema analisa os materiais selecionados, identifica o tipo de projeto (reforma, decoração, mobiliário) e gera uma descrição que destaca os benefícios dos materiais escolhidos, o resultado esperado e o valor agregado para o cliente.

As sugestões inteligentes de materiais analisam o tipo de projeto, ambiente, orçamento disponível e estilo desejado para recomendar os materiais mais adequados. O algoritmo considera não apenas a adequação técnica dos materiais, mas também fatores como custo-benefício, disponibilidade no mercado local e tendências de design atuais.

A análise de tendências de preços examina o histórico de projetos do franqueado para identificar padrões de sucesso, oportunidades de otimização de preços e estratégias para melhorar a taxa de conversão. O sistema identifica quais tipos de projeto têm maior taxa de aprovação, quais faixas de preço são mais aceitas pelos clientes e quais materiais geram maior margem de lucro.

O assistente virtual oferece suporte 24/7 para responder dúvidas sobre materiais, técnicas de aplicação, cuidados de manutenção e orientações gerais sobre decoração. O assistente é treinado especificamente no domínio de decoração e design de interiores, oferecendo respostas precisas e profissionais.

A otimização de margens de lucro analisa dados de mercado, custos operacionais e comportamento de clientes para sugerir estratégias de precificação que maximizem a lucratividade sem comprometer a competitividade. O sistema considera fatores como elasticidade de preço por tipo de cliente, sazonalidade de demanda e posicionamento competitivo.




## Esquema do Banco de Dados

### Estrutura das Tabelas Principais

O banco de dados foi projetado seguindo princípios de normalização para garantir integridade referencial e minimizar redundância de dados. A estrutura principal é composta por oito tabelas que se relacionam através de chaves estrangeiras bem definidas.

A tabela `users` armazena informações dos usuários do sistema, incluindo franqueados e administradores. Cada usuário possui um identificador único (UUID), nome completo, email único, senha criptografada, tipo de usuário (franqueado ou admin), status ativo/inativo e timestamps de criação e última atualização. A senha é armazenada utilizando hash bcrypt com salt para garantir segurança mesmo em caso de comprometimento do banco de dados.

A tabela `franchises` contém informações específicas sobre cada franquia, incluindo nome da franquia, CNPJ, endereço completo, telefone de contato, email corporativo, região de atuação, data de início das operações e configurações específicas como margem de lucro padrão e fatores de ajuste regional. Esta tabela se relaciona com a tabela de usuários através de uma chave estrangeira que identifica o franqueado responsável.

A tabela `materials` é fundamental para o sistema de precificação, armazenando informações detalhadas sobre cada material disponível. Inclui nome do material, descrição técnica, unidade de medida (m², m, L, kg, un), custo unitário base, categoria (madeira, metal, tecido, tinta, etc.), fornecedor preferencial, tempo de entrega estimado e especificações técnicas relevantes como resistência, durabilidade e aplicações recomendadas.

A tabela `difficulty_factors` define os multiplicadores aplicados aos custos baseados na complexidade do projeto. Cada fator possui um nome descritivo (Baixo, Médio, Alto), multiplicador numérico (1.0, 1.2, 1.5), descrição detalhada dos critérios que caracterizam cada nível de dificuldade e exemplos de projetos típicos para cada categoria.

### Relacionamentos e Integridade Referencial

A tabela `clients` armazena informações dos clientes de cada franqueado, incluindo dados pessoais, preferências de contato, histórico de interações e informações relevantes para personalização do atendimento. Cada cliente está associado a um franqueado específico através de chave estrangeira, garantindo isolamento de dados entre diferentes franquias.

A tabela `projects` representa o núcleo do sistema de CRM, armazenando informações sobre cada projeto ou orçamento. Inclui referências ao cliente e franqueado responsável, descrição do projeto, status atual, data de criação, data de envio do orçamento, data de aprovação (se aplicável), valor total estimado, margem de lucro aplicada e observações adicionais. Esta tabela se relaciona com clientes e franqueados através de chaves estrangeiras.

A tabela `project_items` detalha os itens específicos de cada projeto, incluindo referências ao projeto, material utilizado, quantidade, fator de dificuldade aplicado, custo unitário no momento do orçamento, custo total do item e observações específicas. Esta estrutura permite rastreabilidade completa dos custos e facilita análises posteriores de rentabilidade por tipo de material ou projeto.

A tabela `project_history` mantém um log completo de todas as alterações realizadas em projetos, incluindo mudanças de status, modificações de valores, adição ou remoção de itens e interações com clientes. Este histórico é fundamental para auditoria, análise de performance e resolução de disputas.

### Índices e Otimizações

Para garantir performance adequada mesmo com grandes volumes de dados, foram criados índices estratégicos nas colunas mais frequentemente utilizadas em consultas. Índices compostos foram criados para consultas que filtram por múltiplas colunas simultaneamente, como busca de projetos por franqueado e status.

Índices únicos garantem integridade de dados em campos como email de usuários e CNPJ de franquias. Índices parciais foram implementados para otimizar consultas específicas, como busca de projetos ativos ou clientes com projetos em andamento.

## Documentação das APIs

### Endpoints de Autenticação

O sistema implementa autenticação baseada em JWT (JSON Web Tokens) que permite acesso stateless e escalável. O endpoint `POST /api/auth/login` recebe credenciais do usuário (email e senha) e retorna um token JWT válido por 24 horas, juntamente com informações básicas do usuário como nome, tipo e franquia associada.

O endpoint `POST /api/auth/refresh` permite renovação de tokens próximos ao vencimento sem necessidade de nova autenticação completa. O endpoint `POST /api/auth/logout` invalida o token atual, garantindo segurança em caso de logout explícito.

Todos os endpoints protegidos requerem o header `Authorization: Bearer <token>` e retornam erro 401 (Unauthorized) em caso de token inválido ou expirado. O middleware de autenticação valida automaticamente tokens e injeta informações do usuário no contexto da requisição.

### Endpoints de Precificação

O endpoint principal `POST /api/calculate-price` recebe parâmetros de material_id, quantity e difficulty_id e retorna um objeto completo com custos detalhados. A resposta inclui custo unitário do material, custo total do material, fator de dificuldade aplicado, custo de mão de obra estimado, custo total do projeto, margem de lucro sugerida e preço de venda final.

O endpoint `GET /api/materials` retorna lista completa de materiais disponíveis com informações detalhadas incluindo id, nome, descrição, unidade de medida, custo unitário base e categoria. Suporta filtros por categoria, faixa de preço e disponibilidade.

O endpoint `GET /api/difficulty-factors` retorna lista de fatores de dificuldade disponíveis com id, nome, multiplicador e descrição detalhada. Estes fatores são utilizados nos cálculos de precificação para ajustar custos baseados na complexidade do projeto.

### Endpoints de CRM

O conjunto de endpoints de CRM oferece operações CRUD completas para gestão de clientes e projetos. O endpoint `POST /api/clients` permite criação de novos clientes com validação completa de dados obrigatórios e opcionais. Campos obrigatórios incluem nome, email e telefone, enquanto campos opcionais incluem endereço, preferências e observações.

O endpoint `GET /api/clients` retorna lista de clientes do franqueado autenticado com suporte a paginação, ordenação e filtros por nome, email, data de cadastro e status. O endpoint `PUT /api/clients/{id}` permite atualização de informações de clientes existentes com validação de permissões.

Os endpoints de projetos seguem padrão similar: `POST /api/projects` para criação, `GET /api/projects` para listagem com filtros, `PUT /api/projects/{id}` para atualização e `DELETE /api/projects/{id}` para exclusão. Todos os endpoints respeitam isolamento de dados por franqueado.

### Endpoints de Inteligência Artificial

O endpoint `POST /api/ai/generate-project-description` recebe lista de materiais, informações do cliente e tipo de projeto, retornando descrição profissional gerada automaticamente. A descrição destaca benefícios dos materiais, resultado esperado e valor agregado para o cliente.

O endpoint `POST /api/ai/suggest-materials` analisa tipo de projeto, ambiente, orçamento e estilo para retornar lista de materiais recomendados com justificativas detalhadas. Cada sugestão inclui material_id, nome, quantidade sugerida e explicação da recomendação.

O endpoint `POST /api/ai/virtual-assistant` oferece interface de chat para responder dúvidas sobre decoração, materiais e processos. Recebe pergunta em linguagem natural e retorna resposta contextualizada e profissional.

O endpoint `POST /api/ai/analyze-pricing-trends` analisa histórico de projetos do franqueado para identificar padrões de sucesso e oportunidades de otimização. Retorna análise detalhada com recomendações específicas e métricas de performance.

### Endpoints de Dashboard e Relatórios

O endpoint `GET /api/dashboard/stats` retorna métricas consolidadas do franqueado incluindo total de clientes, projetos por status, receita total, taxa de conversão e ticket médio. Suporta filtros por período para análise temporal.

O endpoint `GET /api/reports/sales` gera relatórios detalhados de vendas com opções de agrupamento por período, material, cliente ou tipo de projeto. Suporta exportação em formatos CSV, PDF e Excel.

O endpoint `GET /api/reports/materials` analisa utilização de materiais por período, identificando materiais mais utilizados, margem de lucro por material e oportunidades de negociação com fornecedores.

## Guia de Instalação e Deployment

### Requisitos do Sistema

Para instalação em ambiente de desenvolvimento, o sistema requer Python 3.11 ou superior, Node.js 18 ou superior, npm ou pnpm para gerenciamento de pacotes JavaScript, SQLite 3 para banco de dados local e Git para controle de versão. Recomenda-se pelo menos 4GB de RAM e 10GB de espaço em disco disponível.

Para ambiente de produção, os requisitos incluem servidor Linux (Ubuntu 20.04+ ou CentOS 8+), Python 3.11 com pip, Node.js 18+ com npm, PostgreSQL 13+ ou MySQL 8+, Redis para cache e sessões, Nginx como proxy reverso, SSL/TLS certificado válido e pelo menos 8GB de RAM com 50GB de espaço em disco.

### Instalação em Desenvolvimento

O processo de instalação inicia com o clone do repositório Git e configuração do ambiente virtual Python. Após clonar o repositório, navegue até o diretório do projeto e crie um ambiente virtual utilizando `python -m venv venv`. Ative o ambiente virtual e instale as dependências Python utilizando `pip install -r requirements.txt`.

Para o frontend, navegue até o diretório `pricing-frontend` e instale as dependências utilizando `npm install` ou `pnpm install`. Configure as variáveis de ambiente copiando o arquivo `.env.example` para `.env` e ajustando os valores conforme necessário.

Inicialize o banco de dados executando as migrações com `flask db upgrade` e popule com dados iniciais utilizando `python seed_data.py`. Inicie o servidor backend com `python src/main.py` e o frontend com `npm run dev`.

### Deployment em Produção

Para deployment em produção, recomenda-se utilização de containers Docker para garantir consistência entre ambientes. O projeto inclui Dockerfile otimizado para produção com multi-stage build que minimiza o tamanho da imagem final.

Configure um banco de dados PostgreSQL ou MySQL dedicado com backup automático e replicação para alta disponibilidade. Configure Redis para cache de sessões e dados frequentemente acessados. Utilize Nginx como proxy reverso com configuração SSL/TLS e compressão gzip.

Implemente monitoramento com Prometheus e Grafana para métricas de sistema e aplicação. Configure alertas para situações críticas como alta utilização de CPU, memória insuficiente ou falhas de conectividade com banco de dados.

Para escalabilidade horizontal, configure load balancer com múltiplas instâncias da aplicação. Utilize CDN para servir assets estáticos e melhorar performance global. Implemente backup automático de banco de dados com retenção de pelo menos 30 dias.

### Configuração de Segurança

Implemente firewall restritivo permitindo apenas portas necessárias (80, 443, 22 para SSH). Configure fail2ban para proteção contra ataques de força bruta. Utilize chaves SSH para autenticação em servidores de produção, desabilitando autenticação por senha.

Configure HTTPS obrigatório com redirecionamento automático de HTTP. Utilize certificados SSL/TLS válidos, preferencialmente com renovação automática via Let's Encrypt. Implemente headers de segurança como HSTS, CSP e X-Frame-Options.

Configure backup criptografado de banco de dados com armazenamento em local seguro e separado do servidor principal. Implemente rotação regular de senhas e chaves de API. Configure logs de auditoria para rastreamento de ações sensíveis.

## Manutenção e Suporte

### Procedimentos de Backup

Implemente backup automático diário do banco de dados com retenção de 30 dias para backups diários, 12 semanas para backups semanais e 12 meses para backups mensais. Teste regularmente a restauração de backups para garantir integridade dos dados.

Configure backup de arquivos de configuração, logs de aplicação e certificados SSL. Armazene backups em local geograficamente separado do servidor principal, utilizando criptografia para proteção de dados sensíveis.

### Monitoramento e Alertas

Configure monitoramento de métricas de sistema incluindo utilização de CPU, memória, disco e rede. Monitore métricas de aplicação como tempo de resposta, taxa de erro, throughput e disponibilidade de serviços externos.

Implemente alertas automáticos para situações críticas com escalação para equipe técnica. Configure dashboards visuais para acompanhamento em tempo real de métricas importantes.

### Atualizações e Patches

Estabeleça processo regular de atualização de dependências e patches de segurança. Teste atualizações em ambiente de staging antes de aplicar em produção. Mantenha documentação atualizada de versões e mudanças implementadas.

Configure pipeline de CI/CD para automatizar testes e deployment de atualizações. Implemente rollback automático em caso de falhas durante deployment.

