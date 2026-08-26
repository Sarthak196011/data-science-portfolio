"""Transform: dbt-style SQL transformations using DuckDB in-memory."""
import pandas as pd
import duckdb

def transform_all(raw: dict) -> dict:
    con = duckdb.connect()
    con.register('raw_orders',    raw['orders'])
    con.register('raw_customers', raw['customers'])
    con.register('raw_products',  raw['products'])

    fact_orders = con.execute("""
        SELECT
            o.order_id,
            o.customer_id,
            o.product_id,
            o.order_date,
            EXTRACT('year'  FROM o.order_date)::INT AS order_year,
            EXTRACT('month' FROM o.order_date)::INT AS order_month,
            o.quantity,
            o.unit_price,
            o.discount,
            o.revenue,
            o.status,
            o.channel,
            o.region,
            c.segment         AS customer_segment,
            c.country,
            p.category        AS product_category,
            p.cost_price,
            o.revenue - (o.quantity * p.cost_price) AS gross_profit
        FROM raw_orders o
        LEFT JOIN raw_customers c ON o.customer_id = c.customer_id
        LEFT JOIN raw_products  p ON o.product_id  = p.product_id
        WHERE o.status = 'Completed'
    """).df()

    dim_customers = con.execute("""
        SELECT
            c.customer_id,
            c.name,
            c.segment,
            c.country,
            c.signup_year,
            c.lifetime_value,
            COUNT(o.order_id)     AS total_orders,
            SUM(o.revenue)        AS total_revenue,
            AVG(o.revenue)        AS avg_order_value,
            MAX(o.order_date)     AS last_order_date
        FROM raw_customers c
        LEFT JOIN raw_orders o ON c.customer_id = o.customer_id AND o.status='Completed'
        GROUP BY c.customer_id, c.name, c.segment, c.country, c.signup_year, c.lifetime_value
    """).df()

    dim_products = con.execute("""
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            p.cost_price,
            p.list_price,
            p.supplier,
            COUNT(o.order_id)  AS total_orders,
            SUM(o.quantity)    AS total_units_sold,
            SUM(o.revenue)     AS total_revenue
        FROM raw_products p
        LEFT JOIN raw_orders o ON p.product_id = o.product_id AND o.status='Completed'
        GROUP BY p.product_id, p.product_name, p.category, p.cost_price, p.list_price, p.supplier
    """).df()

    agg_monthly = con.execute("""
        SELECT
            EXTRACT('year'  FROM order_date)::INT AS order_year,
            EXTRACT('month' FROM order_date)::INT AS order_month,
            STRFTIME(order_date, '%Y-%m')          AS year_month,
            COUNT(order_id)                        AS total_orders,
            SUM(revenue)                           AS total_revenue,
            AVG(revenue)                           AS avg_order_value,
            COUNT(DISTINCT customer_id)            AS unique_customers
        FROM raw_orders
        WHERE status='Completed'
        GROUP BY
            EXTRACT('year'  FROM order_date)::INT,
            EXTRACT('month' FROM order_date)::INT,
            STRFTIME(order_date, '%Y-%m')
        ORDER BY order_year, order_month
    """).df()

    agg_category = con.execute("""
        SELECT
            p.category,
            COUNT(o.order_id)  AS total_orders,
            SUM(o.revenue)     AS total_revenue,
            AVG(o.revenue)     AS avg_order_value,
            SUM(o.quantity)    AS total_units
        FROM raw_orders o
        JOIN raw_products p ON o.product_id = p.product_id
        WHERE o.status='Completed'
        GROUP BY p.category
        ORDER BY total_revenue DESC
    """).df()

    con.close()
    return {
        'fact_orders':  fact_orders,
        'dim_customers':dim_customers,
        'dim_products': dim_products,
        'agg_monthly':  agg_monthly,
        'agg_category': agg_category,
    }
