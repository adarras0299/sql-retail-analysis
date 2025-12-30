-- =====================================================
-- RFM BASE TABLE
-- One row per customer
-- =====================================================

WITH customer_orders AS (
    SELECT
        c.customer_id,
        MAX(o.order_date) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.quantity * oi.unit_price) AS monetary
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY c.customer_id
)

SELECT
    customer_id,
    last_order_date,
    frequency,
    monetary
FROM customer_orders
ORDER BY monetary DESC;
