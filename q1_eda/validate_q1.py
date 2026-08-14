import csv
from datetime import datetime
from pathlib import Path

# Caminho do arquivo
DATA_PATH = Path("data/raw/orders.csv")

with DATA_PATH.open(mode="r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    columns = reader.fieldnames
    rows = list(reader)

# Parte 1 - Visão geral
total_rows = len(rows)
total_columns = len(columns)

created_at_values = [
    datetime.fromisoformat(row["created_at"])
    for row in rows
    if row["created_at"]
]

min_date = min(created_at_values)
max_date = max(created_at_values)

# Parte 2 - Coluna total
total_values = [
    float(row["total"])
    for row in rows
    if row["total"]
]

min_total = min(total_values)
max_total = max(total_values)
avg_total = sum(total_values) / len(total_values)

# Verificação de valores nulos
null_counts = {
    column: sum(
        1
        for row in rows
        if row[column] is None or row[column].strip() == ""
    )
    for column in columns
}

print("=== QUESTÃO 1 - EDA ===")
print()

print("PARTE 1 - VISÃO GERAL")
print(f"Quantidade de linhas: {total_rows}")
print(f"Quantidade de colunas: {total_columns}")
print(f"Data mínima: {min_date}")
print(f"Data máxima: {max_date}")

print()
print("PARTE 2 - COLUNA TOTAL")
print(f"Valor mínimo: {min_total:.2f}")
print(f"Valor máximo: {max_total:.2f}")
print(f"Valor médio: {avg_total:.2f}")

print()
print("VALORES NULOS POR COLUNA")
for column, count in null_counts.items():
    print(f"{column}: {count}")
    
# Parte 3 - Diagnóstico de qualidade

print()
print("PARTE 3 - DIAGNÓSTICO")

# Verificação de valores não positivos em total
non_positive_total = sum(
    1 for value in total_values if value <= 0
)

print(f"Valores de total <= 0: {non_positive_total}")

# Ordenação necessária apenas para cálculo dos quartis
sorted_totals = sorted(total_values)


def percentile(values, percentile_value):
    """
    Calcula percentil utilizando interpolação linear.
    """
    position = (len(values) - 1) * percentile_value
    lower = int(position)
    upper = min(lower + 1, len(values) - 1)
    weight = position - lower

    return values[lower] * (1 - weight) + values[upper] * weight


q1 = percentile(sorted_totals, 0.25)
q3 = percentile(sorted_totals, 0.75)

iqr = q3 - q1
upper_limit = q3 + 1.5 * iqr
lower_limit = q1 - 1.5 * iqr

possible_outliers = [
    value
    for value in total_values
    if value < lower_limit or value > upper_limit
]

print()
print("ANÁLISE DE POSSÍVEIS OUTLIERS - MÉTODO IQR")
print(f"Q1: {q1:.2f}")
print(f"Q3: {q3:.2f}")
print(f"IQR: {iqr:.2f}")
print(f"Limite inferior: {lower_limit:.2f}")
print(f"Limite superior: {upper_limit:.2f}")
print(f"Quantidade de possíveis outliers: {len(possible_outliers)}")

if possible_outliers:
    percentage = len(possible_outliers) / len(total_values) * 100

    print(f"Percentual de possíveis outliers: {percentage:.2f}%")
    print(f"Menor valor identificado: {min(possible_outliers):.2f}")
    print(f"Maior valor identificado: {max(possible_outliers):.2f}")
    
print()
print("VERIFICAÇÕES ADICIONAIS DE QUALIDADE")

# IDs duplicados
ids = [row["id"] for row in rows]
duplicate_ids = len(ids) - len(set(ids))

# Números de pedido duplicados
order_numbers = [row["order_number"] for row in rows]
duplicate_order_numbers = len(order_numbers) - len(set(order_numbers))

print(f"IDs duplicados: {duplicate_ids}")
print(f"Números de pedido duplicados: {duplicate_order_numbers}")

# Valores categóricos observados
channels = sorted(set(row["channel"] for row in rows))
statuses = sorted(set(row["status"] for row in rows))

print(f"Canais encontrados: {channels}")
print(f"Status encontrados: {statuses}")

# Relação básica entre valores monetários
inconsistent_totals = 0

for row in rows:
    subtotal = float(row["subtotal"])
    discount = float(row["discount_amount"])
    total = float(row["total"])

    # Verifica se subtotal - desconto corresponde ao total
    if abs((subtotal - discount) - total) > 0.01:
        inconsistent_totals += 1

print(
    f"Registros em que subtotal - desconto != total: "
    f"{inconsistent_totals}"
)

print()
print("ANÁLISE DE SALESPERSON_ID POR CANAL")

channel_analysis = {}

for row in rows:
    channel = row["channel"]

    if channel not in channel_analysis:
        channel_analysis[channel] = {
            "total": 0,
            "salesperson_null": 0
        }

    channel_analysis[channel]["total"] += 1

    if row["salesperson_id"] is None or row["salesperson_id"].strip() == "":
        channel_analysis[channel]["salesperson_null"] += 1


for channel, values in channel_analysis.items():
    total = values["total"]
    nulls = values["salesperson_null"]
    percentage = (nulls / total) * 100

    print(f"\nCanal: {channel}")
    print(f"Total de pedidos: {total}")
    print(f"salesperson_id nulos: {nulls}")
    print(f"Percentual de nulos: {percentage:.2f}%")