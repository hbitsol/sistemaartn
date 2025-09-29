# Requisitos Detalhados para o Mecanismo de Precificação

Para o MVP do sistema de precificação, os franqueados precisarão informar os seguintes dados para cada item ou componente de um projeto de decoração:

## 1. Quantidade de Material:

*   **Tipo de Entrada:** Numérica.
*   **Unidades:** O sistema deve permitir a especificação de diferentes unidades de medida, como:
    *   Metros lineares (m)
    *   Metros quadrados (m²)
    *   Unidades (un)
    *   Litros (L)
    *   Quilogramas (kg)
*   **Validação:** A quantidade deve ser um número positivo.
*   **Impacto na Precificação:** Multiplicará o custo unitário do material.

## 2. Tipo de Material:

*   **Tipo de Entrada:** Seleção a partir de uma lista pré-definida (dropdown ou catálogo).
*   **Exemplos de Categorias/Tipos:**
    *   **Madeiras:** MDF, Compensado, Madeira Maciça (Pinus, Carvalho, Mogno, etc.)
    *   **Tecidos:** Algodão, Linho, Veludo, Seda, Sintéticos (Poliéster, Microfibra)
    *   **Metais:** Ferro, Alumínio, Aço Inox, Latão
    *   **Vidros:** Comum, Temperado, Laminado, Espelho
    *   **Pedras:** Mármore, Granito, Quartzo, Silestone
    *   **Revestimentos:** Papel de Parede, Cerâmica, Porcelanato, Cimento Queimado
    *   **Tintas:** Acrílica, Látex, Esmalte, Epóxi
    *   **Acessórios:** Puxadores, Dobradiças, Corrediças, Iluminação (spots, fitas LED)
*   **Atributos Associados:** Cada tipo de material terá um custo unitário base, que pode variar por fornecedor ou qualidade. Este custo será armazenado no backend e associado ao tipo de material selecionado.
*   **Impacto na Precificação:** Determinará o custo base do material antes da aplicação da quantidade.

## 3. Grau de Dificuldade:

*   **Tipo de Entrada:** Seleção a partir de uma escala ou categorias pré-definidas.
*   **Escala Sugerida:**
    *   **Baixo:** Projetos simples, montagem fácil, pouca personalização (ex: instalação de prateleiras simples).
    *   **Médio:** Projetos com alguma complexidade, personalização moderada, necessidade de ajustes (ex: montagem de móveis planejados padrão).
    *   **Alto:** Projetos complexos, alta personalização, detalhes intrincados, instalações desafiadoras, necessidade de múltiplos profissionais (ex: design de interiores completo com marcenaria sob medida e soluções integradas).
*   **Valores Associados:** Cada grau de dificuldade pode ter um fator multiplicador (ex: Baixo = 1.0x, Médio = 1.2x, Alto = 1.5x) que será aplicado sobre o custo da mão de obra ou sobre o custo total do projeto, ou uma taxa fixa adicional.
*   **Impacto na Precificação:** Influenciará diretamente o custo da mão de obra e/ou o custo total do projeto, refletindo a complexidade e o tempo necessário para a execução.

## Lógica de Cálculo (Exemplo Simplificado):

`Custo_Total_Item = (Quantidade * Custo_Unitário_Material) + (Horas_Mão_de_Obra * Custo_Hora_Mão_de_Obra * Fator_Dificuldade)`

`Preço_Venda_Item = Custo_Total_Item * (1 + Margem_Lucro)`

O sistema precisará permitir que o franqueador configure os custos unitários dos materiais, o custo da hora de mão de obra e os fatores de dificuldade, bem como a margem de lucro desejada. O franqueado apenas inserirá os dados específicos do projeto.

