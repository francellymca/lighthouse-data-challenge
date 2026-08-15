from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

TARGET_PRODUCT = "Motor de Popa 1949"


def load_data():
    """Carrega apenas os datasets necessários."""

    products = pd.read_csv(
        DATA_DIR / "products.csv"
    )

    product_variants = pd.read_csv(
        DATA_DIR / "product_variants.csv"
    )

    orders = pd.read_csv(
        DATA_DIR / "orders.csv"
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


def build_customer_product_dataset(
    products,
    product_variants,
    orders,
    order_items,
):
    """
    Relaciona clientes aos produtos adquiridos.

    Cada combinação cliente-produto é mantida apenas uma vez,
    pois o sistema considera presença ou ausência de compra.
    """

    customer_orders = orders[
        ["id", "customer_id"]
    ]

    variants = product_variants[
        ["id", "product_id"]
    ]

    interactions = (
        order_items[
            ["order_id", "product_variant_id"]
        ]
        .merge(
            customer_orders,
            left_on="order_id",
            right_on="id",
            how="inner",
        )
        .merge(
            variants,
            left_on="product_variant_id",
            right_on="id",
            how="inner",
            suffixes=("_order", "_variant"),
        )
    )

    customer_product = (
        interactions[
            ["customer_id", "product_id"]
        ]
        .drop_duplicates()
    )

    return customer_product


def build_user_item_matrix(customer_product):
    """
    Constrói a matriz binária Cliente × Produto.

    1 = cliente comprou o produto
    0 = cliente não comprou o produto
    """

    matrix = pd.crosstab(
        customer_product["customer_id"],
        customer_product["product_id"],
    )

    matrix = (matrix > 0).astype(int)

    return matrix


def cosine_similarity(vector_a, vector_b):
    """
    Calcula a similaridade de cosseno entre dois vetores.
    """

    numerator = np.dot(
        vector_a,
        vector_b,
    )

    denominator = (
        np.linalg.norm(vector_a)
        * np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return 0.0

    return numerator / denominator


def calculate_product_similarities(
    user_item_matrix,
    target_product_id,
):
    """
    Calcula a similaridade entre o produto de referência
    e todos os demais produtos.
    """

    if target_product_id not in user_item_matrix.columns:
        raise ValueError(
            "Produto de referência não possui interações."
        )

    target_vector = (
        user_item_matrix[target_product_id]
        .to_numpy()
    )

    similarities = []

    for product_id in user_item_matrix.columns:

        if product_id == target_product_id:
            continue

        product_vector = (
            user_item_matrix[product_id]
            .to_numpy()
        )

        similarity = cosine_similarity(
            target_vector,
            product_vector,
        )

        similarities.append({
            "product_id": product_id,
            "similarity": similarity,
        })

    return pd.DataFrame(similarities)


def main():

    (
        products,
        product_variants,
        orders,
        order_items,
    ) = load_data()

    target_products = products[
        products["name"] == TARGET_PRODUCT
    ]

    if target_products.empty:
        raise ValueError(
            f"Produto '{TARGET_PRODUCT}' não encontrado."
        )

    if len(target_products) > 1:
        raise ValueError(
            f"Mais de um produto encontrado com o nome "
            f"'{TARGET_PRODUCT}'."
        )

    target_product_id = int(
        target_products.iloc[0]["id"]
    )

    print("=== PRODUTO DE REFERÊNCIA ===")
    print(
        f"ID: {target_product_id} | "
        f"Nome: {TARGET_PRODUCT}"
    )
    print()

    customer_product = (
        build_customer_product_dataset(
            products,
            product_variants,
            orders,
            order_items,
        )
    )

    user_item_matrix = build_user_item_matrix(
        customer_product
    )

    print("=== MATRIZ USUÁRIO × PRODUTO ===")
    print(
        f"Clientes: "
        f"{user_item_matrix.shape[0]}"
    )
    print(
        f"Produtos: "
        f"{user_item_matrix.shape[1]}"
    )
    print()

    similarities = (
        calculate_product_similarities(
            user_item_matrix,
            target_product_id,
        )
    )

    ranking = (
        similarities
        .merge(
            products[["id", "name"]],
            left_on="product_id",
            right_on="id",
            how="left",
        )
        .sort_values(
            by=["similarity", "product_id"],
            ascending=[False, True],
        )
        .head(5)
    )

    print("=== TOP 5 PRODUTOS MAIS SIMILARES ===")
    print(
        ranking[
            ["product_id", "name", "similarity"]
        ].to_string(
            index=False,
            formatters={
                "similarity": "{:.6f}".format
            },
        )
    )

    print()
    print(
        "Produto com maior similaridade: "
        f"{ranking.iloc[0]['name']}"
    )


if __name__ == "__main__":
    main()