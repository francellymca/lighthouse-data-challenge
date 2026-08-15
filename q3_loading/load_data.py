import csv
import os
from pathlib import Path

import psycopg
from psycopg import sql


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
SCHEMA_FILE = BASE_DIR / "q2_schema" / "schema.sql"


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "lh_nautical"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}


def get_connection():
    return psycopg.connect(**DB_CONFIG)


def create_schema(connection):
    """
    Executa o schema.sql gerado na Questão 2.
    """
    schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")

    with connection.cursor() as cursor:
        cursor.execute(schema_sql)

    connection.commit()


def get_csv_columns(csv_file):
    """
    Retorna os nomes das colunas presentes no cabeçalho do CSV.
    """
    with csv_file.open(
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.reader(file)
        return next(reader)


def count_csv_rows(csv_file):
    """
    Conta as linhas de dados do CSV, desconsiderando apenas o cabeçalho.
    Nenhum tratamento é realizado.
    """
    with csv_file.open(
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.reader(file)
        next(reader, None)
        return sum(1 for _ in reader)


def load_csv(connection, csv_file):
    """
    Carrega o CSV na tabela de mesmo nome utilizando COPY FROM STDIN.
    """
    table_name = csv_file.stem
    columns = get_csv_columns(csv_file)

    copy_query = sql.SQL(
        "COPY {} ({}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
    ).format(
        sql.Identifier(table_name),
        sql.SQL(", ").join(
            sql.Identifier(column)
            for column in columns
        ),
    )

    with connection.cursor() as cursor:
        with cursor.copy(copy_query) as copy:
            with csv_file.open(mode="rb") as file:
                while data := file.read(1024 * 1024):
                    copy.write(data)

    connection.commit()


def count_database_rows(connection, table_name):
    """
    Retorna a quantidade de registros presentes na tabela.
    """
    query = sql.SQL(
        "SELECT COUNT(*) FROM {}"
    ).format(
        sql.Identifier(table_name)
    )

    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()[0]


def main():
    csv_files = sorted(DATA_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"Nenhum arquivo CSV encontrado em: {DATA_DIR}"
        )

    print("=== CARREGAMENTO DOS CSVs ===")
    print()

    with get_connection() as connection:

        print("Criando tabelas...")
        create_schema(connection)
        print("Schema criado com sucesso.")
        print()

        validation_results = {}

        for csv_file in csv_files:

            table_name = csv_file.stem

            print(f"Carregando {csv_file.name}...")

            csv_rows = count_csv_rows(csv_file)

            load_csv(
                connection,
                csv_file
            )

            database_rows = count_database_rows(
                connection,
                table_name
            )

            validation_results[table_name] = {
                "csv": csv_rows,
                "database": database_rows
            }

            status = (
                "OK"
                if csv_rows == database_rows
                else "DIVERGENTE"
            )

            print(
                f"  CSV: {csv_rows} | "
                f"PostgreSQL: {database_rows} | "
                f"{status}"
            )

        print()
        print("=== VALIDAÇÃO DA CARGA ===")

        valid_tables = 0

        for table_name, counts in validation_results.items():

            if counts["csv"] == counts["database"]:
                valid_tables += 1

        print(
            f"Tabelas validadas: "
            f"{valid_tables}/{len(csv_files)}"
        )

        print()
        print("=== QUESTÃO 3.2 ===")

        target_tables = [
            "customers",
            "orders",
            "order_items",
            "payments",
        ]

        total_rows = 0

        for table_name in target_tables:

            count = count_database_rows(
                connection,
                table_name
            )

            total_rows += count

            print(
                f"{table_name}: {count}"
            )

        print()
        print(
            "Soma total de linhas: "
            f"{total_rows}"
        )


if __name__ == "__main__":
    main()