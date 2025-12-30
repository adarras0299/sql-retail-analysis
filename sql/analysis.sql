-- =====================================
-- 1. KPIs GLOBAUX
-- =====================================

-- name : CA_total_&_volume
SELECT
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS total_customers,
    SUM(oi.quantity * oi.unit_price) AS total_revenue,
    AVG(oi.quantity * oi.unit_price) AS avg_item_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id;

-- name : Panier_Moyen
WITH order_totals AS (
    SELECT
        o.order_id,
        SUM(oi.quantity * oi.unit_price) AS order_amount
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id
)
SELECT
    AVG(order_amount) AS avg_basket_value
FROM order_totals;
 
-- =====================================
-- 2. ANALYSE TEMPORELLE
-- =====================================

-- name : Croissance_du_CA
SELECT
    strftime('%Y-%m', o.order_date) AS month,
    SUM(oi.quantity * oi.unit_price) AS monthly_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;

-- name : Nouveaux_clients_par_cohorte_mensuelle
SELECT
    strftime('%Y-%m', first_order_date) AS mois_cohorte,
    COUNT(*) AS nouveaux_clients
FROM customers
GROUP BY mois_cohorte
ORDER BY mois_cohorte;

-- =====================================
-- 3. ANALYSE CLIENT
-- =====================================

-- name : Nombre_de_clients_par_pays
SELECT
    country,
    COUNT(*) AS customers
FROM customers
GROUP BY country
ORDER BY customers DESC;

-- name : CA_par_Pays
SELECT
    c.country,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.country
ORDER BY revenue DESC;

-- name : Contribution_des_clients_au_CA (80/20 Pareto)
WITH customer_revenue AS (
    SELECT
        c.customer_id,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id
),
ranked_customers AS (
    SELECT
        customer_id,
        revenue,
        SUM(revenue) OVER () AS total_revenue,
        SUM(revenue) OVER (
            ORDER BY revenue DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_revenue
    FROM customer_revenue
)
SELECT
    customer_id,
    revenue,
    ROUND(cumulative_revenue / total_revenue, 3) AS cumulative_share
FROM ranked_customers
ORDER BY revenue DESC;

-- name : Distribution_des_commandes_clients
SELECT
    order_count,
    COUNT(*) AS number_of_customers
FROM (
    SELECT
        customer_id,
        COUNT(order_id) AS order_count
    FROM orders
    GROUP BY customer_id
)
GROUP BY order_count
ORDER BY order_count;

-- name : Nombre_de_commandes_moyennes_par_client 
SELECT
    COUNT(order_id) * 1.0 / COUNT(DISTINCT customer_id) AS avg_orders_per_customer
FROM orders;



-- =====================================
-- 4. ANALYSE PRODUIT
-- =====================================

-- name : CA_par_Produit
SELECT
    product_id,
    SUM(quantity) AS units_sold,
    SUM(quantity * unit_price) AS revenue
FROM order_items
GROUP BY product_id
ORDER BY revenue DESC;

-- name : Volume_vs_Valeur 
SELECT
    product_id,
    SUM(quantity) AS units_sold,
    AVG(unit_price) AS avg_price,
    SUM(quantity * unit_price) AS revenue
FROM order_items
GROUP BY product_id
ORDER BY units_sold DESC;

-- name : Outliers
WITH product_stats AS (
    SELECT
        product_id,
        AVG(unit_price) AS avg_price,
        COUNT(*) AS sales_count
    FROM order_items
    GROUP BY product_id
)
SELECT
    oi.product_id,
    oi.unit_price,
    ps.avg_price
FROM order_items oi
JOIN product_stats ps ON oi.product_id = ps.product_id
WHERE oi.unit_price > ps.avg_price * 3;