# LH Nautical — Data & AI Challenge

Solução desenvolvida para o **Desafio Lighthouse — Dados e IA**, contemplando diferentes
etapas de uma jornada de dados: análise exploratória, modelagem e carga em banco de dados,
análises de negócio, previsão de demanda, sistema de recomendação e visualização analítica
em Power BI.

O projeto foi estruturado de forma modular, mantendo separados os dados de origem, os
scripts de cada questão, os resultados obtidos e a camada de visualização.

---

## Estrutura do Projeto

```text
lighthouse-challenge/
│
├── data/
│   └── raw/                    # 24 arquivos CSV originais
│
├── q1_eda/                     # Análise Exploratória de Dados
├── q2_schema/                  # Geração automática do schema PostgreSQL
├── q3_loading/                 # Carregamento dos dados
├── q4_customers/               # Análise de clientes
├── q5_calendar/                # Dimensão de calendário
├── q6_forecasting/             # Previsão de demanda
├── q7_recommendation/          # Sistema de recomendação
│
├── dashboard/
│   ├── lh_nautical_dashboard.pbix
│   └── README.md
│
├── docs/
│   └── results.md
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

Os arquivos em `data/raw/` correspondem aos dados originais fornecidos para o desafio
e foram preservados sem alterações.

---

## Etapas Desenvolvidas

### Q1 — Análise Exploratória de Dados

Análise inicial da tabela `orders`, incluindo estrutura dos dados, valores ausentes,
consistência das variáveis financeiras e identificação de possíveis outliers.

### Q2 — Geração do Schema PostgreSQL

Desenvolvimento de um script em Python para identificar automaticamente os arquivos CSV,
inferir os tipos das colunas e gerar o arquivo `schema.sql` com as instruções
`CREATE TABLE`.

### Q3 — Carregamento dos Dados

Carga automatizada dos 24 arquivos CSV no PostgreSQL, com validação da quantidade de
registros entre os arquivos de origem e as tabelas carregadas.

### Q4 — Análise de Clientes

Identificação dos clientes com maior ticket médio entre aqueles que atendem ao critério
mínimo de diversidade de categorias, seguida da análise das categorias mais adquiridas
por esse grupo.

### Q5 — Dimensão de Calendário

Construção de uma dimensão de datas para calcular corretamente a média diária de vendas
das lojas físicas, incluindo no cálculo os dias sem registros de vendas.

### Q6 — Previsão de Demanda

Construção de um modelo baseline baseado em média móvel para previsão da demanda mensal
do produto `Bússola de Bordo 702`, com separação temporal entre treino e teste para evitar
data leakage.

### Q7 — Sistema de Recomendação

Construção de uma matriz usuário–produto e aplicação de similaridade de cosseno para
identificar produtos com padrões de compradores semelhantes ao item de referência.

---

## Dashboard Power BI

Como camada complementar de análise, foi desenvolvido um dashboard interativo em
**Microsoft Power BI**, organizado em quatro páginas:

- **Visão Executiva de Vendas** — visão consolidada dos principais indicadores comerciais;
- **Análise de Produtos** — desempenho de categorias e produtos por faturamento e volume;
- **Análise de Clientes** — comportamento, valor e concentração da base de clientes;
- **Análise Geográfica** — distribuição territorial das vendas, pedidos e localidades.

Os indicadores foram validados em diferentes combinações de ano e canal para verificar
a propagação dos filtros e a consistência entre métricas e visualizações.

A documentação específica do dashboard está disponível em
[`dashboard/README.md`](dashboard/README.md).

---

## Tecnologias

- **Python 3** — automação, análise de dados, previsão e recomendação;
- **PostgreSQL** — armazenamento e consultas relacionais;
- **SQL** — análises e construção das consultas de negócio;
- **Pandas** — manipulação e preparação dos dados;
- **NumPy** — operações numéricas;
- **Docker / Docker Compose** — execução do ambiente PostgreSQL;
- **Microsoft Power BI** — construção do dashboard analítico.

---

## Resultados

Os resultados detalhados das questões, incluindo metodologia, validações e respostas,
estão documentados em:

[`docs/results.md`](docs/results.md)

Entre os resultados obtidos estão:

- geração automática das 24 tabelas do schema PostgreSQL;
- validação da carga dos 24 arquivos de dados;
- identificação dos clientes de maior ticket médio dentro dos critérios definidos;
- análise da média diária de vendas considerando dias sem movimentação;
- construção e avaliação de um baseline de previsão de demanda;
- desenvolvimento de um sistema de recomendação baseado em similaridade de cosseno;
- construção e validação de um dashboard interativo para exploração dos principais
  indicadores comerciais.

---

## Execução

### 1. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 2. Iniciar o PostgreSQL

```bash
docker compose up -d
```

### 3. Gerar o schema

```bash
python q2_schema/generate_schema.py
```

### 4. Carregar os dados

```bash
python q3_loading/load_data.py
```

As demais análises podem ser executadas a partir dos scripts disponíveis nos diretórios
correspondentes a cada questão.

---

## Status

**Concluído e validado.**