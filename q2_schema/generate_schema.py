import csv
import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


# Diretórios do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "data" / "raw"
OUTPUT_FILE = BASE_DIR / "q2_schema" / "schema.sql"


def is_integer(value):
    """Verifica se o valor pode ser representado como inteiro."""
    return bool(re.fullmatch(r"[+-]?\d+", value))


def has_leading_zero(value):
    """
    Evita interpretar códigos numéricos com zero à esquerda como números.
    Exemplo: '00123' deve permanecer como TEXT.
    """
    unsigned_value = value.lstrip("+-")

    return (
        len(unsigned_value) > 1
        and unsigned_value.startswith("0")
        and unsigned_value.isdigit()
    )


def is_numeric(value):
    """Verifica se o valor pode ser representado como número decimal."""
    try:
        Decimal(value)
        return True
    except InvalidOperation:
        return False


def is_boolean(value):
    """Reconhece representações booleanas explícitas."""
    return value.lower() in {"true", "false"}


def is_date(value):
    """Verifica datas no padrão ISO YYYY-MM-DD."""
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def looks_like_timestamp(value):
    """
    Verifica se o valor possui data e horário em formato
    compatível com ISO.
    """
    if "T" not in value and " " not in value:
        return False

    try:
        datetime.fromisoformat(value)
        return True
    except ValueError:
        return False


def is_text_identifier(column_name):
    """
    Identifica colunas que representam códigos ou identificadores
    e que devem ser preservadas como texto, mesmo quando contêm
    apenas caracteres numéricos.
    """
    exact_names = {
        "tax_id",
        "state_registration",
        "sku",
        "barcode_ean",
        "phone",
        "postal_code",
        "zip_code",
    }

    column_lower = column_name.lower()

    return (
        column_lower in exact_names
        or column_lower.endswith("_code")
        or column_lower.endswith("_number")
    )


def infer_column_type(column_name, values):
    """
    Infere o tipo PostgreSQL de uma coluna.

    Valores vazios são ignorados durante a inferência,
    pois representam ausência de informação e não um tipo.
    """
    non_empty_values = [
        value.strip()
        for value in values
        if value is not None and value.strip() != ""
    ]

    # Coluna totalmente vazia
    if not non_empty_values:
        return "TEXT"

    # Códigos e identificadores textuais
    if is_text_identifier(column_name):
        return "TEXT"

    # Booleano
    if all(is_boolean(value) for value in non_empty_values):
        return "BOOLEAN"

    # Data e horário
    if all(looks_like_timestamp(value) for value in non_empty_values):
        return "TIMESTAMP"

    # Data
    if all(is_date(value) for value in non_empty_values):
        return "DATE"

    # Preserva números com zero à esquerda
    if any(has_leading_zero(value) for value in non_empty_values):
        return "TEXT"

    # Inteiro
    if all(is_integer(value) for value in non_empty_values):
        return "BIGINT"

    # Decimal
    if all(is_numeric(value) for value in non_empty_values):
        return "NUMERIC"

    # Demais casos
    return "TEXT"


def quote_identifier(identifier):
    """
    Protege nomes de tabelas e colunas para uso no PostgreSQL.
    """
    escaped = identifier.replace('"', '""')
    return f'"{escaped}"'


def analyze_csv(csv_file):
    """
    Analisa um arquivo CSV e retorna:
    - nome da tabela;
    - nomes das colunas;
    - tipos PostgreSQL inferidos.
    """
    with csv_file.open(
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(
                f"O arquivo {csv_file.name} não possui cabeçalho."
            )

        columns = reader.fieldnames

        column_values = {
            column: []
            for column in columns
        }

        for row in reader:
            for column in columns:
                column_values[column].append(row[column])

    inferred_types = {
        column: infer_column_type(
            column,
            column_values[column]
        )
        for column in columns
    }

    table_name = csv_file.stem

    return table_name, columns, inferred_types


def generate_create_table(table_name, columns, inferred_types):
    """
    Gera uma instrução CREATE TABLE para PostgreSQL.
    """
    definitions = []

    for column in columns:
        column_name = quote_identifier(column)
        column_type = inferred_types[column]

        definitions.append(
            f"    {column_name} {column_type}"
        )

    columns_sql = ",\n".join(definitions)

    return (
        f"CREATE TABLE {quote_identifier(table_name)} (\n"
        f"{columns_sql}\n"
        f");"
    )


def generate_schema():
    """
    Processa todos os arquivos CSV presentes em data/raw
    e gera um único arquivo schema.sql.
    """
    csv_files = sorted(INPUT_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"Nenhum arquivo CSV encontrado em: {INPUT_DIR}"
        )

    create_statements = []

    print("=== GERAÇÃO DO SCHEMA POSTGRESQL ===")
    print()

    for csv_file in csv_files:
        table_name, columns, inferred_types = analyze_csv(csv_file)

        statement = generate_create_table(
            table_name,
            columns,
            inferred_types
        )

        create_statements.append(statement)

        print(
            f"{csv_file.name}: "
            f"{len(columns)} colunas -> tabela {table_name}"
        )

    schema_header = (
        "-- LH Nautical Data Challenge\n"
        "-- Schema gerado automaticamente a partir dos arquivos CSV\n"
        "-- Banco de destino: PostgreSQL\n\n"
    )

    schema_content = (
        schema_header
        + "\n\n".join(create_statements)
        + "\n"
    )

    OUTPUT_FILE.write_text(
        schema_content,
        encoding="utf-8"
    )

    print()
    print(f"Total de tabelas geradas: {len(csv_files)}")
    print(f"Arquivo criado em: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_schema()