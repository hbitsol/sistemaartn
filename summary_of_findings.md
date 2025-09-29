# Resumo das Descobertas da Fase 1: Análise de Requisitos e Pesquisa de Mercado

## 1. Modelos de Precificação para Serviços de Decoração:

A pesquisa revelou que a precificação em serviços de decoração geralmente combina abordagens baseadas em custos, valor e mercado. Para o nosso MVP, a **precificação baseada em custos** será a espinha dorsal, onde o preço final é a soma dos custos de materiais, mão de obra e uma margem de lucro. É crucial identificar e quantificar todos os custos fixos e variáveis, além de considerar o tempo e a expertise envolvidos. A flexibilidade para ajustar a margem de lucro e os fatores de custo será essencial para o franqueador.

## 2. CRM para Franquias e Integração de Precificação:

Um CRM é vital para gerenciar o relacionamento com os clientes, otimizar vendas e monitorar o desempenho da rede de franquias. Embora existam plataformas robustas como SULTS e Bitrix24, o custo é um fator limitante para o MVP. A solução ideal para nós é um **CRM simplificado com um módulo de precificação integrado (CPQ)**. Essa integração permitirá que os franqueados configurem projetos, calculem preços automaticamente e gerem orçamentos diretamente, agilizando o processo de vendas e garantindo a conformidade com as políticas de precificação da franqueadora.

## 3. Ferramentas de IA para Precificação e Funcionalidades de CRM:

A Inteligência Artificial oferece um grande potencial para otimizar tanto a precificação quanto as funcionalidades do CRM. Para a precificação, a IA pode ser usada para **análise de dados e otimização de margem de lucro**, permitindo ajustes de preços com base em custos, complexidade e até mesmo dados de mercado. Para o CRM, a IA pode **automatizar tarefas repetitivas**, como o envio de e-mails, e auxiliar na **análise de sentimento** ou **lead scoring**, melhorando a eficiência e a personalização do atendimento ao cliente. Para o MVP, a integração de APIs de IA será a abordagem mais viável para manter os custos baixos.

## 4. Requisitos Detalhados para o Mecanismo de Precificação:

O mecanismo de precificação do MVP exigirá que os franqueados informem:

*   **Quantidade de Material:** Com suporte a diversas unidades de medida (m, m², un, L, kg).
*   **Tipo de Material:** Selecionável de uma lista pré-definida, com custos unitários base associados.
*   **Grau de Dificuldade:** Uma escala (Baixo, Médio, Alto) que aplicará um fator multiplicador sobre o custo da mão de obra ou do projeto total.

A lógica de cálculo básica será: `Custo_Total_Item = (Quantidade * Custo_Unitário_Material) + (Horas_Mão_de_Obra * Custo_Hora_Mão_de_Obra * Fator_Dificuldade)` e `Preço_Venda_Item = Custo_Total_Item * (1 + Margem_Lucro)`. O franqueador terá controle sobre os custos unitários, custos de mão de obra, fatores de dificuldade e margens de lucro.

## Conclusão da Fase 1:

Com base nesta análise, temos uma compreensão clara dos requisitos e das tecnologias que podem ser empregadas para construir um MVP eficaz e de baixo custo. O próximo passo será definir a arquitetura técnica e as especificações detalhadas para o desenvolvimento do sistema.

