# Resultados do Desafio

Este documento reúne os principais resultados obtidos durante o desenvolvimento das questões do desafio.

---

## Questão 1 — Análise Exploratória de Dados (EDA)

### Visão geral da tabela `orders`

A análise exploratória foi realizada exclusivamente sobre a tabela `orders`, sem aplicação de limpeza ou tratamento dos dados.

| Métrica | Resultado |
|---|---:|
| Quantidade de linhas | 48.998 |
| Quantidade de colunas | 13 |
| Data mínima (`created_at`) | 2020-01-01 01:19:28 |
| Data máxima (`created_at`) | 2026-12-31 23:43:09 |

### Análise da coluna `total`

| Métrica | Resultado |
|---|---:|
| Valor mínimo | R$ 32,62 |
| Valor máximo | R$ 127.262,02 |
| Valor médio | R$ 28.704,99 |

### Qualidade dos dados

Não foram identificados valores nulos nas colunas `total` e `created_at`. Também não foram encontrados valores iguais ou inferiores a zero em `total`, IDs duplicados ou números de pedido duplicados.

A consistência entre os valores monetários também foi verificada. Em todos os registros analisados, a relação abaixo foi satisfeita:

`subtotal - discount_amount = total`

A coluna `salesperson_id` apresentou 24.131 valores nulos. A análise por canal mostrou que essas ocorrências estão concentradas no canal `ecommerce`:

| Canal | Pedidos | `salesperson_id` nulos | Percentual |
|---|---:|---:|---:|
| ecommerce | 34.342 | 24.131 | 70,27% |
| pos | 14.656 | 0 | 0,00% |

A concentração dos valores ausentes em um canal específico indica um padrão nos dados, porém não é suficiente para determinar sua causa ou classificá-los como erro sem informações adicionais sobre as regras de negócio.

### Análise de possíveis outliers

Para avaliar valores extremos em `total`, foi utilizado o método do intervalo interquartil (IQR).

| Métrica | Resultado |
|---|---:|
| Q1 | R$ 13.171,24 |
| Q3 | R$ 40.941,88 |
| IQR | R$ 27.770,65 |
| Limite superior | R$ 82.597,85 |
| Possíveis outliers | 452 |
| Percentual | 0,92% |
| Maior valor observado | R$ 127.262,02 |

Os 452 registros identificados pelo critério IQR foram considerados potenciais outliers, e não necessariamente inconsistências. Valores elevados podem representar pedidos legítimos e, portanto, exigiriam análise adicional antes de qualquer decisão de tratamento ou exclusão.

### Diagnóstico

A tabela `orders` apresenta boa consistência para análises exploratórias iniciais. Não foram observadas duplicidades nas chaves verificadas, valores nulos nas principais variáveis utilizadas nesta análise ou inconsistências na relação entre subtotal, desconto e total.

Entretanto, foram identificados potenciais outliers na coluna `total` e uma quantidade relevante de valores ausentes em `salesperson_id`, concentrados no canal `ecommerce`. Esses pontos devem ser considerados em análises futuras e investigados de acordo com o contexto e as regras de negócio antes da aplicação de qualquer tratamento.

Dessa forma, os dados apresentam condições adequadas para análises exploratórias, mas determinadas análises de negócio podem exigir validações adicionais.

---

## Questão 2 — Geração do Schema PostgreSQL

### Objetivo

Desenvolver um script em Python capaz de identificar automaticamente os arquivos CSV disponíveis no diretório de dados e gerar um único arquivo `schema.sql` contendo as instruções de criação das respectivas tabelas em PostgreSQL.

### Implementação

O script `generate_schema.py` foi desenvolvido utilizando exclusivamente bibliotecas padrão do Python 3.

A solução percorre automaticamente os arquivos `.csv` presentes em `data/raw`, identifica os nomes e valores das colunas e realiza a inferência dos tipos de dados para PostgreSQL.

Foram considerados os seguintes tipos:

| Característica identificada | Tipo PostgreSQL |
|---|---|
| Valores inteiros | `BIGINT` |
| Valores decimais | `NUMERIC` |
| Valores booleanos | `BOOLEAN` |
| Datas | `DATE` |
| Data e horário | `TIMESTAMP` |
| Textos, códigos e identificadores | `TEXT` |

Colunas que representam códigos ou identificadores, como `ncm_code`, são preservadas como `TEXT`, evitando perda de significado ou de possíveis zeros à esquerda.

### Resultado

Foram identificados os 24 arquivos CSV fornecidos no desafio e geradas automaticamente 24 instruções `CREATE TABLE` no arquivo `schema.sql`.

A quantidade de tabelas geradas foi validada por meio da contagem das instruções `CREATE TABLE`:

`24`

Também foram verificadas tabelas relevantes, como `orders`, `customers`, `order_items`, `products` e `product_variants`, confirmando a coerência dos tipos inferidos.

Exemplos:

- valores monetários, como `total` e `sale_price`, foram classificados como `NUMERIC`;
- identificadores relacionais foram classificados como `BIGINT`;
- campos booleanos, como `is_active`, foram classificados como `BOOLEAN`;
- campos temporais, como `created_at`, foram classificados como `TIMESTAMP`;
- códigos e identificadores textuais foram preservados como `TEXT`.

### Conclusão

O processo gerou um schema reproduzível a partir dos arquivos de origem, sem necessidade de definição manual das 24 tabelas. A solução utiliza somente recursos da biblioteca padrão do Python 3 e produz um único arquivo SQL compatível com PostgreSQL.

---

## Questão 3 — Carregamento dos Dados

### Objetivo

Realizar o carregamento dos arquivos CSV no banco PostgreSQL utilizando o schema gerado na Questão 2, preservando os dados brutos sem remoção de valores nulos ou correção dos registros.

### Implementação

O carregamento foi realizado por meio de um script em Python utilizando a biblioteca `psycopg` para conexão com o PostgreSQL.

Os arquivos CSV armazenados em `data/raw` foram identificados automaticamente e carregados para as tabelas correspondentes por meio do comando `COPY FROM STDIN`.

Nenhum tratamento, remoção de valores nulos ou alteração dos arquivos de origem foi realizado durante o processo.

### Validação da carga

Para validar o carregamento, a quantidade de registros de cada arquivo CSV foi comparada com a quantidade de registros inseridos na respectiva tabela PostgreSQL.

Foram validadas todas as 24 tabelas:

`24/24 tabelas com quantidade de registros correspondente aos arquivos de origem.`

### Questão 3.2

A quantidade de registros nas tabelas solicitadas foi:

| Tabela | Registros |
|---|---:|
| `customers` | 2.000 |
| `orders` | 48.998 |
| `order_items` | 147.320 |
| `payments` | 53.546 |

A soma total corresponde a:

**251.864 registros**

### Conclusão

O carregamento dos 24 arquivos CSV foi concluído com sucesso no PostgreSQL. A comparação entre os arquivos de origem e as tabelas carregadas não apresentou divergências na quantidade de registros.

---

## Questão 4 — Análise de Clientes

### Objetivo

Identificar os clientes considerados fiéis de acordo com os critérios definidos no desafio: ticket médio elevado e diversidade de pelo menos 13 categorias distintas adquiridas.

### Metodologia

O cálculo foi dividido em etapas para evitar duplicações decorrentes das relações entre pedidos e itens.

Primeiramente, foram calculadas as métricas financeiras diretamente na tabela `orders`:

- **Faturamento Total:** soma de `total` por cliente;
- **Frequência:** quantidade de transações por cliente;
- **Ticket Médio:** faturamento total dividido pela frequência.

A diversidade foi calculada separadamente a partir das categorias distintas adquiridas por cada cliente.

O relacionamento utilizado para identificar as categorias foi:

`orders → order_items → product_variants → products → categories`

Foram considerados elegíveis somente clientes com diversidade igual ou superior a 13 categorias. Em seguida, os clientes foram ordenados pelo Ticket Médio em ordem decrescente, utilizando `customer_id` crescente como critério de desempate.

### Top 10 clientes

| customer_id | Faturamento Total | Frequência | Ticket Médio | Categorias |
|---:|---:|---:|---:|---:|
| 22 | 1.087.838,44 | 26 | 41.839,94 | 14 |
| 1477 | 916.262,58 | 22 | 41.648,30 | 14 |
| 929 | 1.082.775,89 | 26 | 41.645,23 | 14 |
| 1116 | 655.737,20 | 16 | 40.983,58 | 14 |
| 1691 | 815.471,30 | 20 | 40.773,57 | 14 |
| 774 | 726.127,99 | 18 | 40.340,44 | 14 |
| 1470 | 1.040.553,09 | 26 | 40.021,27 | 14 |
| 1599 | 997.616,46 | 25 | 39.904,66 | 14 |
| 965 | 677.297,78 | 17 | 39.841,05 | 14 |
| 1722 | 1.146.455,22 | 29 | 39.532,94 | 14 |

### Categoria com maior quantidade de itens

Após a seleção dos Top 10 clientes, seus pedidos foram novamente relacionados aos itens, variantes e produtos.

A quantidade adquirida foi agregada por categoria utilizando `SUM(order_items.quantity)`. Dessa forma, somente as compras realizadas pelos clientes previamente selecionados participaram do cálculo.

**Categoria com maior quantidade de itens: Hélices (`category_id = 8`)**

**Quantidade total: 492 itens**

### Conclusão

A análise identificou os dez clientes com maior Ticket Médio entre aqueles que adquiriram produtos de pelo menos 13 categorias distintas. Para esse grupo, a categoria **Hélices** apresentou a maior quantidade acumulada de itens comprados, com **492 unidades**.

### Respostas para a Questão 4.2

#### 1. Como você chegou nas categorias mais vendidas?

O mapeamento partiu da tabela `orders`, utilizando `customer_id` para identificar os pedidos de cada cliente. A partir de `orders.id`, os pedidos foram relacionados a `order_items` por meio de `order_id`. Em seguida, `product_variant_id` permitiu chegar à tabela `product_variants` e, por meio de `product_id`, à tabela `products`, onde foi obtido o `category_id` de cada produto.

Após a definição dos Top 10 clientes, foi realizada a soma de `order_items.quantity` agrupada por categoria. Dessa forma, foi possível identificar a categoria que concentrou a maior quantidade de itens adquiridos por esse grupo.

#### 2. Qual lógica foi utilizada para filtrar os clientes com diversidade mínima?

A diversidade de cada cliente foi calculada por meio da quantidade de `category_id` distintos presentes em suas compras, utilizando `COUNT(DISTINCT category_id)`. Foram considerados elegíveis apenas os clientes que apresentaram diversidade igual ou superior a 13 categorias.

Sobre esse conjunto foi aplicado o ranking pelo Ticket Médio em ordem decrescente. O `customer_id` em ordem crescente foi utilizado como critério de desempate, conforme definido no enunciado, e os dez primeiros clientes formaram o grupo final.

#### 3. Como foi garantido que a contagem de itens refletisse apenas os Top 10?

A seleção dos clientes foi realizada antes da análise das categorias, em uma CTE específica denominada `top_10_customers`. O cálculo da quantidade de itens foi realizado posteriormente, partindo exclusivamente dos clientes presentes nessa CTE e relacionando seus pedidos às tabelas `order_items`, `product_variants` e `products`.

Dessa forma, o `SUM(quantity)` utilizado no ranking das categorias considera somente os pedidos pertencentes aos dez clientes previamente selecionados, impedindo que compras de outros clientes influenciem o resultado.

---

## Questão 5 — Dimensão de Calendário

### Objetivo

Calcular a média diária de vendas das lojas físicas por dia da semana, considerando também os dias em que a loja esteve aberta, mas não apresentou registros de vendas.

### Metodologia

Foi construída uma dimensão de datas em PostgreSQL utilizando `generate_series`, abrangendo todas as datas entre o menor e o maior valor de `created_at` presentes na tabela `orders`.

Cada data foi associada ao respectivo dia da semana em português.

As vendas diárias foram calculadas considerando somente os pedidos do canal `pos`:

`SUM(total) por data`

A dimensão de datas foi então relacionada às vendas por meio de `LEFT JOIN`. Para os dias sem registros de vendas, o valor nulo resultante da junção foi substituído por zero utilizando `COALESCE`.

Somente após essa etapa foi calculada a média das vendas por dia da semana.

### Resultado

| Dia da semana | Média diária de vendas |
|---|---:|
| Quinta-feira | R$ 157.154,32 |
| Domingo | R$ 157.616,13 |
| Segunda-feira | R$ 158.241,15 |
| Sábado | R$ 164.858,27 |
| Terça-feira | R$ 166.118,83 |
| Sexta-feira | R$ 170.193,68 |
| Quarta-feira | R$ 173.605,44 |

A **Quinta-feira** apresentou a menor média diária de vendas no canal físico, com **R$ 157.154,32**.

### Validação dos dias sem venda

Como validação adicional, foi contabilizada a quantidade de dias sem registros de vendas POS em cada dia da semana.

| Dia da semana | Total de dias | Dias sem venda | Dias com venda |
|---|---:|---:|---:|
| Segunda-feira | 365 | 7 | 358 |
| Terça-feira | 365 | 8 | 357 |
| Quarta-feira | 366 | 10 | 356 |
| Quinta-feira | 366 | 20 | 346 |
| Sexta-feira | 365 | 10 | 355 |
| Sábado | 365 | 11 | 354 |
| Domingo | 365 | 12 | 353 |

A validação confirma que o uso direto da tabela `orders` excluiria da média os dias em que nenhuma venda foi registrada. Quinta-feira, por exemplo, apresentou 20 dias sem vendas durante o período analisado.

### Respostas para a Questão 5.2

#### 1. Por que é necessário utilizar uma tabela de datas em vez de agrupar diretamente a tabela de vendas?

A tabela `orders` possui registros apenas para as datas em que ocorreram pedidos. Dessa forma, um agrupamento realizado diretamente sobre essa tabela desconsideraria os dias em que a loja esteve aberta, mas não registrou vendas.

A dimensão de datas garante a existência de todas as datas do período analisado. Por meio de um `LEFT JOIN`, as vendas existentes são associadas ao calendário e, nos dias sem registros, o valor é substituído por zero. Assim, a média considera todos os dias em que a loja esteve aberta e não apenas aqueles em que houve vendas.

#### 2. O que aconteceria com a média se um dia da semana tivesse muitos dias sem nenhuma venda registrada?

Caso os dias sem vendas fossem ignorados, a média seria calculada somente com as datas em que ocorreram vendas e, consequentemente, ficaria artificialmente elevada.

Ao incluir os dias sem venda com valor igual a zero, esses dias passam a compor o denominador da média, produzindo um resultado mais representativo do desempenho real daquele dia da semana.

### Conclusão

Considerando todos os dias do calendário, inclusive aqueles sem registros de vendas, a Quinta-feira apresentou a menor média diária de vendas das lojas físicas, com R$ 157.154,32.

Esse resultado identifica o dia de menor desempenho médio sob as premissas estabelecidas no desafio, mas isoladamente não é suficiente para recomendar o fechamento das lojas, pois uma decisão desse tipo também dependeria de informações como custos operacionais, margem e comportamento individual de cada unidade.

---

## Questão 6 — Previsão de Demanda

### Objetivo

Construir um modelo baseline para prever a demanda mensal do produto `Bússola de Bordo 702` no primeiro trimestre de 2026, utilizando uma média móvel dos últimos três meses.

### Construção do dataset

Foram utilizados os datasets:

- `products.csv`
- `product_variants.csv`
- `order_items.csv`
- `orders.csv`

O relacionamento utilizado foi:

`products → product_variants → order_items → orders`

Foram identificados dois registros em `products` com o nome exato `Bússola de Bordo 702`, correspondentes aos IDs 74 e 240. Ambos foram considerados na construção da série histórica de demanda.

A demanda mensal foi calculada por meio da soma de `order_items.quantity` por mês.

### Baseline

O período de treino considerou os dados disponíveis até 31/12/2025.

O baseline foi construído utilizando a média móvel dos três meses imediatamente anteriores à data prevista.

Para evitar o uso de informações futuras, as previsões do primeiro trimestre de 2026 foram geradas de forma recursiva:

- Jan/2026 utiliza Out/2025, Nov/2025 e Dez/2025;
- Fev/2026 utiliza Nov/2025, Dez/2025 e a previsão de Jan/2026;
- Mar/2026 utiliza Dez/2025 e as previsões de Jan/2026 e Fev/2026.

Os valores reais do período de teste não foram utilizados para gerar previsões posteriores.

### Resultados

| Mês | Valor real | Previsão | Erro absoluto |
|---|---:|---:|---:|
| Jan/2026 | 79 | 38,67 | 40,33 |
| Fev/2026 | 68 | 40,22 | 27,78 |
| Mar/2026 | 60 | 33,63 | 26,37 |

**MAE: 31,49 unidades**

A soma das previsões para o primeiro trimestre de 2026 foi:

**112,52 unidades**

Arredondando para número inteiro:

**113 unidades**

### Avaliação do baseline

O baseline é útil como referência inicial por ser simples, interpretável e de baixo custo computacional. Entretanto, para esse produto, o desempenho observado indica que ele não é suficiente como modelo final de previsão.

As previsões ficaram abaixo dos valores reais nos três meses do período de teste, e o MAE foi de 31,49 unidades, indicando erro relevante para um problema de planejamento de estoque.

### Resposta para a Questão 6.2
### Validação

Utilizando seu modelo treinado, qual é a soma total da previsão de vendas (arredondada para número inteiro) para o 'Bússola de Bordo 702' durante o primeiro trimestre de 2026?
Resp.: 113

### Respostas para a Questão 6.3

#### 1. Como o baseline foi construído?

A demanda foi agregada mensalmente a partir da soma das quantidades vendidas do produto. Para cada mês previsto, foi calculada a média das três observações imediatamente anteriores disponíveis no histórico.

#### 2. Como foi evitado data leakage?

O conjunto de treino foi limitado aos dados até 31/12/2025. Nenhum valor real do primeiro trimestre de 2026 foi utilizado para construir as previsões.

Como a previsão foi realizada para três meses futuros, o processo foi recursivo. Após prever janeiro, esse valor previsto foi incorporado ao histórico utilizado para prever fevereiro. O mesmo procedimento foi aplicado para março. Dessa forma, apenas informações disponíveis até cada momento de previsão foram utilizadas.

#### 3. Uma limitação do modelo proposto

A média móvel considera apenas o comportamento recente da demanda e não incorpora fatores como tendência, sazonalidade, promoções, disponibilidade de estoque ou outras variáveis que possam influenciar as vendas. Mudanças rápidas no padrão de demanda podem, portanto, não ser capturadas pelo modelo.

### Conclusão

O baseline apresentou previsões inferiores aos valores reais durante todo o primeiro trimestre de 2026. Apesar de ser adequado como referência inicial de comparação, o erro observado indica a necessidade de avaliar modelos mais capazes de representar mudanças no comportamento da demanda.

---

## Questão 7 — Sistema de Recomendação

### Objetivo

Identificar os produtos com comportamento de compra mais semelhante ao produto `Motor de Popa 1949`, utilizando um sistema de recomendação baseado na similaridade entre os históricos de compra dos clientes.

### Construção da matriz usuário–produto

Para relacionar os clientes aos produtos adquiridos, foi utilizada a seguinte cadeia de relacionamentos:

`orders → order_items → product_variants → products`

O `customer_id` foi obtido a partir da tabela `orders`, enquanto o `product_id` foi identificado relacionando `order_items.product_variant_id` com `product_variants.id`.

A matriz usuário–produto foi construída utilizando:

- linhas: `customer_id`;
- colunas: `product_id`;
- valor 1: cliente comprou o produto ao menos uma vez;
- valor 0: cliente não comprou o produto.

Compras repetidas do mesmo produto pelo mesmo cliente foram consideradas apenas uma vez, pois o modelo utiliza somente presença ou ausência da interação.

A matriz resultante apresentou:

- **2.000 clientes**
- **500 produtos**

### Similaridade entre produtos

A similaridade entre os produtos foi calculada utilizando Similaridade de Cosseno sobre as colunas da matriz usuário–produto.

Dessa forma, cada produto é representado por um vetor binário que indica quais clientes o adquiriram.

O produto utilizado como referência foi:

**Motor de Popa 1949 — product_id 180**

O próprio produto foi removido do ranking de similaridade.

### Top 5 produtos mais similares

| Posição | Produto | Similaridade |
|---:|---|---:|
| 1 | Motor de Popa 5331 | 0,256553 |
| 2 | Cabo Náutico 2105 | 0,256239 |
| 3 | Vela Mestra 1913 | 0,255785 |
| 4 | Cabo Náutico 9048 | 0,239332 |
| 5 | GPS Plotter 6249 | 0,237744 |

O produto com maior similaridade ao `Motor de Popa 1949` foi:

**Motor de Popa 5331**, com similaridade de **0,256553**.

### Respostas para a Questão 7.3

#### 1. Como a matriz foi construída?

A matriz foi construída relacionando os pedidos aos respectivos clientes e produtos. O `customer_id` foi obtido da tabela `orders`, enquanto o produto foi identificado a partir de `order_items.product_variant_id`, relacionado a `product_variants.id` e posteriormente a `product_id`.

Após o relacionamento, cada combinação entre cliente e produto foi considerada apenas uma vez. Os clientes foram representados nas linhas e os produtos nas colunas. Cada célula recebeu valor 1 quando o cliente havia comprado o produto ao menos uma vez e 0 caso contrário, independentemente da quantidade adquirida.

#### 2. O que significa a similaridade de cosseno nesse contexto?

A similaridade de cosseno compara os vetores de interação dos produtos. Nesse contexto, ela mede o quanto dois produtos apresentam padrões semelhantes de compradores.

Quanto maior a similaridade, maior a sobreposição relativa entre os clientes que adquiriram os dois produtos. Portanto, produtos com maior similaridade ao item de referência são candidatos para recomendação com base no comportamento histórico dos clientes.

Essa métrica indica similaridade entre os conjuntos de compradores, mas não significa necessariamente que os produtos tenham sido adquiridos na mesma transação.

#### 3. Uma limitação desse método de recomendação

Uma limitação é que a abordagem considera apenas a presença ou ausência da compra. Informações como quantidade adquirida, momento da compra, preço, características do produto e contexto da transação não participam do cálculo.

Além disso, produtos com grande popularidade podem apresentar similaridade com diversos itens simplesmente por terem sido adquiridos por muitos clientes.

### Conclusão

A análise baseada na similaridade de cosseno identificou o `Motor de Popa 5331` como o produto com padrão de compradores mais semelhante ao `Motor de Popa 1949`, apresentando similaridade de 0,256553.

O resultado pode ser utilizado como base para uma estratégia simples de recomendação colaborativa, embora análises adicionais sejam necessárias para avaliar aspectos como compras realizadas na mesma transação e influência da popularidade dos produtos.