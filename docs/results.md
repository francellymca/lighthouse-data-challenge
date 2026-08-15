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