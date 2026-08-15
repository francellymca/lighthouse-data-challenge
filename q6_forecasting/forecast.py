from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

TARGET_PRODUCT = "Bússola de Bordo 702"

TRAIN_END = pd.Timestamp("2025-12-31")
TEST_START = pd.Timestamp("2026-01-01")
TEST_END = pd.Timestamp("2026-03-31")


def load_data():
    """Carrega apenas os datasets necessários para a análise."""

    products = pd.read_csv(
        DATA_DIR / "products.csv"
    )

    product_variants = pd.read_csv(
        DATA_DIR / "product_variants.csv"
    )

    orders = pd.read_csv(
        DATA_DIR / "orders.csv",
        parse_dates=["created_at"]
    )

    order_items = pd.read_csv(
        DATA_DIR / "order_items.csv"
    )

    return (
        products,
        product_variants,
        orders,
        order_items,
    )


def build_unified_dataset(
    products,
    product_variants,
    orders,
    order_items,
):
    """
    Cria o dataset unificado necessário para identificar
    as vendas do produto solicitado.
    """

    target_products = products[
        products["name"] == TARGET_PRODUCT
    ][["id", "name"]]

    print("=== PRODUTOS ENCONTRADOS ===")
    print(target_products)
    print()

    target_variants = product_variants[
        product_variants["product_id"].isin(
            target_products["id"]
        )
    ][["id", "product_id"]]

    unified = (
        order_items
        .merge(
            target_variants,
            left_on="product_variant_id",
            right_on="id",
            how="inner",
            suffixes=("_item", "_variant"),
        )
        .merge(
            orders[["id", "created_at"]],
            left_on="order_id",
            right_on="id",
            how="inner",
        )
    )

    return unified


def build_monthly_demand(unified):
    """
    Agrega a quantidade vendida em base mensal.

    Meses sem vendas são explicitamente representados
    com quantidade igual a zero.
    """

    data = unified.copy()

    data["month"] = (
        data["created_at"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    monthly = (
        data.groupby("month")["quantity"]
        .sum()
        .sort_index()
    )

    complete_months = pd.date_range(
        start=monthly.index.min(),
        end=monthly.index.max(),
        freq="MS",
    )

    monthly = monthly.reindex(
        complete_months,
        fill_value=0,
    )

    monthly.index.name = "month"
    monthly.name = "quantity"

    return monthly


def recursive_three_month_forecast(train):
    """
    Gera previsões para jan, fev e mar/2026 utilizando
    média móvel de três meses.

    Valores reais do conjunto de teste não são utilizados
    na geração das previsões.
    """

    history = train.copy().astype(float)

    forecast_dates = pd.date_range(
        start=TEST_START,
        end=TEST_END,
        freq="MS",
    )

    predictions = {}

    for forecast_date in forecast_dates:

        prediction = history.iloc[-3:].mean()

        predictions[forecast_date] = prediction

        # Adiciona a previsão ao histórico exclusivamente
        # para gerar o próximo mês do horizonte.
        history.loc[forecast_date] = prediction

    return pd.Series(
        predictions,
        name="prediction",
    )


def calculate_mae(actual, predicted):
    """
    Calcula o Mean Absolute Error (MAE).
    """

    absolute_errors = (
        actual.astype(float)
        - predicted.astype(float)
    ).abs()

    return absolute_errors.mean()


def main():

    (
        products,
        product_variants,
        orders,
        order_items,
    ) = load_data()

    unified = build_unified_dataset(
        products,
        product_variants,
        orders,
        order_items,
    )

    monthly_demand = build_monthly_demand(
        unified
    )

    train = monthly_demand[
        monthly_demand.index <= TRAIN_END
    ]

    actual_test = monthly_demand[
        (monthly_demand.index >= TEST_START)
        & (monthly_demand.index <= TEST_END)
    ]

    predictions = recursive_three_month_forecast(
        train
    )

    results = pd.DataFrame({
        "actual": actual_test,
        "prediction": predictions,
    })

    results["absolute_error"] = (
        results["actual"]
        - results["prediction"]
    ).abs()

    mae = calculate_mae(
        results["actual"],
        results["prediction"],
    )

    total_forecast = predictions.sum()

    print("=== ÚLTIMOS MESES DO TREINO ===")
    print(train.tail(6))
    print()

    print("=== PREVISÃO - PRIMEIRO TRIMESTRE DE 2026 ===")
    print(results.round(2))
    print()

    print(f"MAE: {mae:.2f}")
    print()

    print(
        "Soma das previsões: "
        f"{total_forecast:.2f}"
    )

    print(
        "Soma das previsões arredondada: "
        f"{round(total_forecast)}"
    )


if __name__ == "__main__":
    main()