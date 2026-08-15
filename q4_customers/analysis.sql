WITH customer_metrics AS (
    SELECT
        customer_id,
        SUM(total) AS faturamento_total,
        COUNT(DISTINCT id) AS frequencia,
        SUM(total) / COUNT(DISTINCT id) AS ticket_medio
    FROM orders
    GROUP BY customer_id
),

category_diversity AS (
    SELECT
        o.customer_id,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    INNER JOIN order_items oi
        ON oi.order_id = o.id
    INNER JOIN product_variants pv
        ON pv.id = oi.product_variant_id
    INNER JOIN products p
        ON p.id = pv.product_id
    GROUP BY o.customer_id
),

top_10_customers AS (
    SELECT
        cm.customer_id,
        cm.faturamento_total,
        cm.frequencia,
        cm.ticket_medio,
        cd.diversidade_categorias
    FROM customer_metrics cm
    INNER JOIN category_diversity cd
        ON cd.customer_id = cm.customer_id
    WHERE cd.diversidade_categorias >= 13
    ORDER BY
        cm.ticket_medio DESC,
        cm.customer_id ASC
    LIMIT 10
),

category_ranking AS (
    SELECT
        p.category_id,
        c.name AS categoria,
        SUM(oi.quantity) AS quantidade_total
    FROM top_10_customers t
    INNER JOIN orders o
        ON o.customer_id = t.customer_id
    INNER JOIN order_items oi
        ON oi.order_id = o.id
    INNER JOIN product_variants pv
        ON pv.id = oi.product_variant_id
    INNER JOIN products p
        ON p.id = pv.product_id
    INNER JOIN categories c
        ON c.id = p.category_id
    GROUP BY
        p.category_id,
        c.name
)

SELECT
    category_id,
    categoria,
    quantidade_total
FROM category_ranking
ORDER BY
    quantidade_total DESC,
    category_id ASC
LIMIT 1;