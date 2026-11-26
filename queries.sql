-- 1. Monthly revenue (delivered orders)
SELECT DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
       COUNT(DISTINCT o.order_id) AS orders,
       ROUND(SUM(oi.price), 2) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY month
ORDER BY month;

-- 2. Top 10 categories by revenue
SELECT p.product_category_name, ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY revenue DESC
LIMIT 10;

-- 3. State ranking (window function)
SELECT customer_state, revenue,
       RANK() OVER (ORDER BY revenue DESC) AS state_rank
FROM (
    SELECT c.customer_state, ROUND(SUM(oi.price), 2) AS revenue
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_state
) t;

-- 4. Late delivery % by state
SELECT c.customer_state,
       COUNT(*) AS delivered_orders,
       SUM(o.order_delivered_customer_date > o.order_estimated_delivery_date) AS late_orders,
       ROUND(100 * SUM(o.order_delivered_customer_date > o.order_estimated_delivery_date) / COUNT(*), 2) AS late_pct
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY late_pct DESC;
