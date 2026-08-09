-- ============================================================
-- WEEK 8 - E-COMMERCE ORDER ANALYTICS
-- PHASE 4 - SQL ANALYSIS
-- ============================================================


-- ============================================================
-- QUERY 1
-- TOTAL REVENUE PER CATEGORY
-- ============================================================

SELECT
    p.category,
    ROUND(
        SUM(
            oi.quantity
            * oi.unit_price
            * (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- ============================================================
-- QUERY 2
-- TOP 10 CUSTOMERS BY TOTAL ORDER VALUE
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name,
    ROUND(
        SUM(
            oi.quantity
            * oi.unit_price
            * (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_order_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_order_value DESC
LIMIT 10;


-- ============================================================
-- QUERY 3
-- MONTH-WISE ORDER COUNT
-- LAST 12 MONTHS PRESENT IN THE DATA
-- ============================================================

WITH max_date AS (
    SELECT
        MAX(order_date) AS latest_date
    FROM orders
)

SELECT
    strftime('%Y-%m', o.order_date) AS order_month,
    COUNT(DISTINCT o.order_id) AS order_count
FROM orders o
CROSS JOIN max_date m
WHERE
    date(o.order_date) >=
    date(m.latest_date, '-11 months')
GROUP BY
    strftime('%Y-%m', o.order_date)
ORDER BY
    order_month;

-- ============================================================
-- QUERY 4
-- CUSTOMERS WHO PLACED ORDERS BUT NEVER HAD A DELIVERED ITEM
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o2
    JOIN order_items oi
        ON o2.order_id = oi.order_id
    WHERE o2.customer_id = c.customer_id
      AND o2.status = 'DELIVERED'
)
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY
    c.customer_id;

-- ============================================================
-- QUERY 5
-- PRODUCTS WITH MORE RETURNS THAN PURCHASES
-- ============================================================

SELECT
    p.product_id,
    p.product_name,

    SUM(
        CASE
            WHEN oi.quantity > 0 THEN oi.quantity
            ELSE 0
        END
    ) AS purchased_quantity,

    ABS(
        SUM(
            CASE
                WHEN oi.quantity < 0 THEN oi.quantity
                ELSE 0
            END
        )
    ) AS returned_quantity

FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id

GROUP BY
    p.product_id,
    p.product_name

HAVING returned_quantity > purchased_quantity

ORDER BY returned_quantity DESC;

-- ============================================================
-- QUERY 6
-- RETURN RATE PER CATEGORY
-- ============================================================

SELECT
    p.category,

    SUM(
        CASE
            WHEN oi.quantity < 0
            THEN ABS(oi.quantity)
            ELSE 0
        END
    ) AS returned_items,

    SUM(
        ABS(oi.quantity)
    ) AS total_items,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN oi.quantity < 0
                THEN ABS(oi.quantity)
                ELSE 0
            END
        )
        /
        NULLIF(
            SUM(ABS(oi.quantity)),
            0
        ),
        2
    ) AS return_rate_percent

FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id

GROUP BY
    p.category

ORDER BY
    return_rate_percent DESC;