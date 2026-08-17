# Dashboard de Vendas — Lighthouse Data Challenge

Dashboard desenvolvido em Power BI para consolidar e explorar os principais indicadores
comerciais do conjunto de dados do Lighthouse Data Challenge.

A solução foi estruturada para permitir uma leitura executiva do desempenho das vendas e,
ao mesmo tempo, análises específicas de produtos, clientes e distribuição geográfica.

## Estrutura do Dashboard

O dashboard é composto por quatro páginas analíticas:

### 1. Visão Executiva de Vendas

Apresenta uma visão consolidada do desempenho comercial entre 2020 e 2026, reunindo
os principais indicadores do negócio:

- Faturamento total;
- Pedidos;
- Ticket médio por pedido;
- Clientes;
- Quantidade vendida;
- Evolução temporal do faturamento;
- Participação do faturamento por canal;
- Evolução anual dos pedidos;
- Evolução anual do ticket médio;
- Faturamento por estado.

A evolução do faturamento utiliza uma visualização temporal dinâmica. Quando nenhum ano
específico está selecionado, o desempenho é apresentado por semestre. Ao selecionar um
único ano, o gráfico passa automaticamente para a granularidade mensal.

---

### 2. Análise de Produtos

Permite avaliar o desempenho do portfólio por diferentes perspectivas, incluindo:

- Produtos vendidos;
- Categorias vendidas;
- Preço médio por item;
- Categorias com maior faturamento;
- Produtos com maior faturamento;
- Categorias com maior quantidade vendida;
- Produtos com maior quantidade vendida.

Os indicadores e rankings respondem aos filtros de ano e canal, permitindo comparar
mudanças no desempenho e na composição das vendas ao longo do período analisado.

---

### 3. Análise de Clientes

Concentra indicadores relacionados ao comportamento e ao valor da base de clientes:

- Total de clientes;
- Pedidos por cliente;
- Ticket médio por pedido;
- Faturamento médio por cliente;
- Clientes com maior faturamento;
- Clientes com maior quantidade de pedidos;
- Distribuição entre pessoa física e pessoa jurídica;
- Concentração do faturamento nos 10% de clientes de maior contribuição.

A análise de concentração permite avaliar quanto do faturamento depende dos clientes de
maior valor e como essa participação varia de acordo com os filtros aplicados.

---

### 4. Análise Geográfica

Apresenta a distribuição territorial das vendas e da operação por meio de indicadores,
rankings e visualização geográfica:

- Estados atendidos;
- Cidades atendidas;
- Faturamento médio por localidade;
- Pedidos médios por localidade;
- Faturamento por estado e cidade;
- Pedidos por estado e cidade;
- Concentração do faturamento nos dois estados de maior contribuição;
- Distribuição geográfica das localidades.

No conjunto de dados atual, existe uma localidade por cidade. Entretanto, os conceitos
foram mantidos separadamente no modelo. Dessa forma, as métricas por localidade continuam
válidas caso uma mesma cidade passe a possuir mais de uma unidade operacional.

---

## Filtros e Interatividade

As páginas possuem filtros de Ano e Canal, permitindo analisar o desempenho comercial
em diferentes contextos.

As medidas foram estruturadas para preservar o contexto dos filtros e atualizar
dinamicamente os indicadores, rankings, distribuições e análises de concentração.

---

## Validação dos Indicadores

Durante o desenvolvimento, os indicadores foram testados em diferentes combinações de
ano e canal para verificar a propagação dos filtros e a consistência entre as páginas.

Entre as validações realizadas:

- O faturamento total foi confrontado com as distribuições por canal, estado e cidade;
- A quantidade de pedidos foi validada em diferentes níveis de agregação;
- O ticket médio por pedido foi confrontado com faturamento e quantidade de pedidos;
- O faturamento médio por cliente foi verificado em conjunto com pedidos por cliente e
  ticket médio;
- As métricas geográficas foram confrontadas com a quantidade de localidades atendidas;
- As análises de concentração dos Top 10% de clientes e dos Top 2 estados foram testadas
  sob diferentes contextos de filtro.

### Validação das Categorias Vendidas

Durante os testes da página de produtos, o indicador de categorias vendidas permaneceu
em 14 nas diferentes combinações de ano e canal avaliadas.

Como os demais indicadores e rankings apresentavam variações, foi realizada uma
verificação adicional para determinar se o comportamento estava relacionado à propagação
dos filtros.

A análise do faturamento por categoria confirmou que todas as 14 categorias registram
vendas nos contextos avaliados. Portanto, a permanência do indicador em 14 representa
uma característica do conjunto de dados e não uma falha na lógica da medida ou na
propagação dos filtros.

---

## Arquivo

O dashboard está disponível neste diretório:

`lh_nautical_dashboard.pbix`

Para visualizar e explorar todas as interações, filtros e páginas analíticas, abra o
arquivo utilizando o Microsoft Power BI Desktop.