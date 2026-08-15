WITH date_range AS (
    SELECT
        MIN(created_at::date) AS data_inicial,
        MAX(created_at::date) AS data_final
    FROM orders
),

calendar AS (
    SELECT
        generate_series(
            data_inicial,
            data_final,
            INTERVAL '1 day'
        )::date AS data
    FROM date_range
),

date_dimension AS (
    SELECT
        data,
        EXTRACT(ISODOW FROM data) AS numero_dia_semana,
        CASE EXTRACT(ISODOW FROM data)
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
            WHEN 7 THEN 'Domingo'
        END AS dia_semana
    FROM calendar
),

daily_sales AS (
    SELECT
        created_at::date AS data,
        SUM(total) AS valor_venda
    FROM orders
    WHERE channel = 'pos'
    GROUP BY created_at::date
),

calendar_sales AS (
    SELECT
        d.data,
        d.numero_dia_semana,
        d.dia_semana,
        COALESCE(s.valor_venda, 0) AS vendas_diarias
    FROM date_dimension d
    LEFT JOIN daily_sales s
        ON s.data = d.data
),

weekday_average AS (
    SELECT
        numero_dia_semana,
        dia_semana,
        AVG(vendas_diarias) AS media_vendas
    FROM calendar_sales
    GROUP BY
        numero_dia_semana,
        dia_semana
)

SELECT
    dia_semana,
    ROUND(media_vendas, 2) AS media_vendas
FROM weekday_average
ORDER BY media_vendas ASC;