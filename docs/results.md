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