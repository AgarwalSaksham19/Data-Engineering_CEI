import sqlite3

# ============================================================
# CONNECT TO DATABASE
# ============================================================

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

print("=" * 70)
print("PHASE 4 - BASIC SQL ANALYSIS")
print("=" * 70)


# ============================================================
# Q1 - TOTAL REVENUE PER CATEGORY
# ============================================================

print("\n" + "=" * 70)
print("QUERY 1 - TOTAL REVENUE PER CATEGORY")
print("=" * 70)

query1 = """
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
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
"""

cursor.execute(query1)

for row in cursor.fetchall():
    print(row)


# ============================================================
# Q2 - TOP 10 CUSTOMERS BY TOTAL ORDER VALUE
# ============================================================

print("\n" + "=" * 70)
print("QUERY 2 - TOP 10 CUSTOMERS")
print("=" * 70)

query2 = """
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
"""

cursor.execute(query2)

for row in cursor.fetchall():
    print(row)


# ============================================================
# Q3 - MONTH-WISE ORDER COUNT - LAST 12 MONTHS
# ============================================================

print("\n" + "=" * 70)
print("QUERY 3 - MONTH-WISE ORDER COUNT")
print("=" * 70)

query3 = """
SELECT
    strftime('%Y-%m', order_date) AS order_month,
    COUNT(*) AS order_count
FROM orders
WHERE order_date >= (
    SELECT date(MAX(order_date), '-11 months')
    FROM orders
)
GROUP BY strftime('%Y-%m', order_date)
ORDER BY order_month;
"""

cursor.execute(query3)

for row in cursor.fetchall():
    print(row)


# ============================================================
# Q4 - CUSTOMERS WHO PLACED ORDERS BUT NEVER HAD
#      A DELIVERED ITEM
# ============================================================

print("\n" + "=" * 70)
print("Q4 - CUSTOMERS WHO PLACED ORDERS BUT NEVER HAD A DELIVERED ITEM")
print("=" * 70)

query4 = """
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
ORDER BY c.customer_id;
"""

cursor.execute(query4)

results4 = cursor.fetchall()

print("Total customers:", len(results4))
print("\nSample results:")

for row in results4[:10]:
    print(row)


# ============================================================
# Q5 - PRODUCTS WITH MORE RETURNS THAN PURCHASES
# ============================================================

print("\n" + "=" * 70)
print("Q5 - PRODUCTS WITH MORE RETURNS THAN PURCHASES")
print("=" * 70)

query5 = """
SELECT
    p.product_id,
    p.product_name,

    SUM(
        CASE
            WHEN oi.quantity > 0 THEN oi.quantity
            ELSE 0
        END
    ) AS purchases,

    SUM(
        CASE
            WHEN oi.quantity < 0 THEN ABS(oi.quantity)
            ELSE 0
        END
    ) AS returns

FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id

GROUP BY
    p.product_id,
    p.product_name

HAVING returns > purchases

ORDER BY returns DESC;
"""

cursor.execute(query5)

for row in cursor.fetchall():
    print(row)


# ============================================================
# Q6 - RETURN RATE PER CATEGORY
# ============================================================

print("\n" + "=" * 70)
print("Q6 - RETURN RATE PER CATEGORY")
print("=" * 70)

query6 = """
SELECT
    p.category,

    SUM(
        CASE
            WHEN oi.quantity < 0 THEN ABS(oi.quantity)
            ELSE 0
        END
    ) AS returned_items,

    SUM(ABS(oi.quantity)) AS total_items,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN oi.quantity < 0 THEN ABS(oi.quantity)
                ELSE 0
            END
        )
        / NULLIF(SUM(ABS(oi.quantity)), 0),
        2
    ) AS return_rate_percent

FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id

GROUP BY p.category

ORDER BY return_rate_percent DESC;
"""

cursor.execute(query6)

for row in cursor.fetchall():
    print(row)


# ============================================================
# Q7 - RUNNING TOTAL OF REVENUE PER REGION
# ============================================================

print("\n" + "=" * 70)
print("QUERY 7 - RUNNING TOTAL BY REGION")
print("=" * 70)

query7 = """
WITH daily_revenue AS (
    SELECT
        o.region_code,
        DATE(o.order_date) AS order_date,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS daily_revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY
        o.region_code,
        DATE(o.order_date)
)

SELECT
    region_code,
    order_date,
    daily_revenue,

    ROUND(
        SUM(daily_revenue) OVER (
            PARTITION BY region_code
            ORDER BY order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS running_total

FROM daily_revenue

ORDER BY
    region_code,
    order_date;
"""

cursor.execute(query7)

results7 = cursor.fetchall()

for row in results7[:20]:
    print(row)

print("\nTotal rows:", len(results7))

print("=" * 70)
print("QUERY 7 COMPLETED SUCCESSFULLY")
print("=" * 70)

# ============================================================
# Q8 - RANK PRODUCTS BY REVENUE USING DENSE_RANK
# ============================================================

print("\n" + "=" * 70)
print("QUERY 8 - PRODUCT REVENUE RANK BY CATEGORY")
print("=" * 70)

query8 = """
WITH product_revenue AS (
    SELECT
        p.category,
        p.product_id,
        p.product_name,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS total_revenue

    FROM products p

    JOIN order_items oi
        ON p.product_id = oi.product_id

    GROUP BY
        p.category,
        p.product_id,
        p.product_name
),

ranked_products AS (
    SELECT
        category,
        product_name,
        total_revenue,

        DENSE_RANK() OVER (
            PARTITION BY category
            ORDER BY total_revenue DESC
        ) AS rank_in_category

    FROM product_revenue
)

SELECT
    category,
    product_name,
    total_revenue,
    rank_in_category

FROM ranked_products

ORDER BY
    category,
    rank_in_category;
"""

cursor.execute(query8)

results8 = cursor.fetchall()

for row in results8[:20]:
    print(row)

print("\nTotal rows:", len(results8))

print("=" * 70)
print("QUERY 8 COMPLETED SUCCESSFULLY")
print("=" * 70)


# ============================================================
# Q9 - LAG ANALYSIS
# DAYS BETWEEN CONSECUTIVE CUSTOMER ORDERS
# ============================================================

print("\n" + "=" * 70)
print("QUERY 9 - LAG ANALYSIS / CUSTOMER ORDER GAPS")
print("=" * 70)

query9 = """
WITH customer_orders AS (
    SELECT
        customer_id,
        DATE(order_date) AS order_date,

        LAG(DATE(order_date)) OVER (
            PARTITION BY customer_id
            ORDER BY DATE(order_date)
        ) AS previous_order_date

    FROM orders

    WHERE customer_id IS NOT NULL
),

order_gaps AS (
    SELECT
        customer_id,
        order_date,
        previous_order_date,

        CASE
            WHEN previous_order_date IS NOT NULL
            THEN CAST(
                julianday(order_date)
                - julianday(previous_order_date)
                AS INTEGER
            )
            ELSE NULL
        END AS days_gap

    FROM customer_orders
),

customer_average_gap AS (
    SELECT
        customer_id,
        AVG(days_gap) AS average_gap

    FROM order_gaps

    WHERE days_gap IS NOT NULL

    GROUP BY customer_id
)

SELECT
    og.customer_id,
    og.order_date,
    og.previous_order_date,
    og.days_gap,

    CASE
        WHEN cag.average_gap > 30 THEN 'At Risk'
        ELSE 'Normal'
    END AS customer_status

FROM order_gaps og

JOIN customer_average_gap cag
    ON og.customer_id = cag.customer_id

ORDER BY
    og.customer_id,
    og.order_date;
"""

cursor.execute(query9)

results9 = cursor.fetchall()

for row in results9[:20]:
    print(row)

print("\nTotal rows:", len(results9))

print("=" * 70)
print("QUERY 9 COMPLETED SUCCESSFULLY")
print("=" * 70)

# ============================================================
# Q10 - CTE WITH MULTIPLE LEVELS
# MONTHLY CUSTOMER REVENUE SEGMENTATION
# ============================================================

print("\n" + "=" * 70)
print("QUERY 10 - MONTHLY CUSTOMER REVENUE SEGMENTATION")
print("=" * 70)

query10 = """
WITH monthly_customer_revenue AS (

    SELECT
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS order_month,

        SUM(
            oi.quantity
            * oi.unit_price
            * (1 - oi.discount_percent / 100.0)
        ) AS monthly_revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.customer_id IS NOT NULL

    GROUP BY
        o.customer_id,
        strftime('%Y-%m', o.order_date)
),

customer_segments AS (

    SELECT
        customer_id,
        order_month,
        ROUND(monthly_revenue, 2) AS monthly_revenue,

        CASE
            WHEN monthly_revenue > 10000
                THEN 'High'

            WHEN monthly_revenue >= 5000
                AND monthly_revenue <= 10000
                THEN 'Medium'

            ELSE 'Low'
        END AS revenue_category

    FROM monthly_customer_revenue
)

SELECT
    order_month,
    revenue_category,
    COUNT(*) AS customer_count

FROM customer_segments

GROUP BY
    order_month,
    revenue_category

ORDER BY
    order_month,
    CASE revenue_category
        WHEN 'High' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Low' THEN 3
    END;
"""

cursor.execute(query10)

results10 = cursor.fetchall()

# Show only first 20 rows
for row in results10[:20]:
    print(row)

# Show total number of rows
print("\nTotal rows:", len(results10))

print("=" * 70)
print("QUERY 10 COMPLETED SUCCESSFULLY")
print("=" * 70)

# ============================================================
# Q11 - NTILE FOR CUSTOMER SEGMENTATION
# ============================================================

print("\n" + "=" * 70)
print("QUERY 11 - CUSTOMER LIFETIME VALUE QUARTILES")
print("=" * 70)

query11 = """
WITH customer_lifetime_value AS (

    SELECT
        o.customer_id,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS total_value

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.customer_id IS NOT NULL

    GROUP BY o.customer_id
),

customer_quartiles AS (

    SELECT
        customer_id,
        total_value,

        NTILE(4) OVER (
            ORDER BY total_value DESC
        ) AS quartile

    FROM customer_lifetime_value
)

SELECT
    customer_id,
    total_value,
    quartile,

    CASE
        WHEN quartile = 1 THEN 'Platinum'
        WHEN quartile = 2 THEN 'Gold'
        WHEN quartile = 3 THEN 'Silver'
        WHEN quartile = 4 THEN 'Bronze'
    END AS quartile_label

FROM customer_quartiles

ORDER BY
    quartile,
    total_value DESC;
"""

cursor.execute(query11)

results11 = cursor.fetchall()

# Show first 20 rows only
for row in results11[:20]:
    print(row)

# Show complete result count
print("\nTotal rows:", len(results11))

print("=" * 70)
print("QUERY 11 COMPLETED SUCCESSFULLY")
print("=" * 70)

# ============================================================
# Q12 - YEAR-OVER-YEAR REVENUE COMPARISON
# ============================================================

print("\n" + "=" * 70)
print("QUERY 12 - YEAR-OVER-YEAR REVENUE COMPARISON")
print("=" * 70)

query12 = """
WITH monthly_revenue AS (
    SELECT
        strftime('%Y', o.order_date) AS year,
        strftime('%m', o.order_date) AS month,

        SUM(
            oi.quantity
            * oi.unit_price
            * (1 - oi.discount_percent / 100.0)
        ) AS revenue

    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY
        strftime('%Y', o.order_date),
        strftime('%m', o.order_date)
),

revenue_comparison AS (
    SELECT
        year,
        month,
        ROUND(revenue, 2) AS revenue,

        LAG(revenue, 12) OVER (
            ORDER BY year, month
        ) AS prev_year_revenue

    FROM monthly_revenue
)

SELECT
    year,
    month,
    revenue,

    ROUND(prev_year_revenue, 2) AS prev_year_revenue,

    CASE
        WHEN prev_year_revenue IS NULL THEN NULL
        WHEN prev_year_revenue = 0 THEN NULL
        ELSE ROUND(
            ((revenue - prev_year_revenue)
            / prev_year_revenue) * 100,
            2
        )
    END AS yoy_growth_percent

FROM revenue_comparison

ORDER BY
    year,
    month;
"""

cursor.execute(query12)
results12 = cursor.fetchall()

for row in results12[:20]:
    print(row)

print("\nTotal rows:", len(results12))
print("QUERY 12 COMPLETED SUCCESSFULLY")


# ============================================================
# Q13 - FIRST / LAST VALUE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("QUERY 13 - FIRST AND LAST PURCHASED CATEGORY")
print("=" * 70)

query13 = """
WITH customer_categories AS (
    SELECT
        o.customer_id,
        DATE(o.order_date) AS order_date,
        p.category,

        FIRST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id
            ORDER BY DATE(o.order_date)
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS first_category,

        FIRST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id
            ORDER BY DATE(o.order_date) DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS last_category

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    WHERE o.customer_id IS NOT NULL
),

customer_summary AS (
    SELECT DISTINCT
        customer_id,
        first_category,
        last_category

    FROM customer_categories
)

SELECT
    customer_id,
    first_category,
    last_category,

    CASE
        WHEN first_category != last_category
            THEN 'Yes'
        ELSE 'No'
    END AS category_shift

FROM customer_summary

ORDER BY customer_id;
"""

cursor.execute(query13)
results13 = cursor.fetchall()

for row in results13[:20]:
    print(row)

print("\nTotal rows:", len(results13))
print("QUERY 13 COMPLETED SUCCESSFULLY")


# ============================================================
# Q14 - CUMULATIVE DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("QUERY 14 - CUMULATIVE REVENUE DISTRIBUTION")
print("=" * 70)

query14 = """
WITH customer_revenue AS (
    SELECT
        o.customer_id,

        SUM(
            oi.quantity
            * oi.unit_price
            * (1 - oi.discount_percent / 100.0)
        ) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.customer_id IS NOT NULL

    GROUP BY o.customer_id
),

cumulative_revenue AS (
    SELECT
        customer_id,
        ROUND(revenue, 2) AS revenue,

        SUM(revenue) OVER (
            ORDER BY revenue DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_revenue,

        SUM(revenue) OVER () AS total_revenue

    FROM customer_revenue
)

SELECT
    customer_id,
    revenue,

    ROUND(
        cumulative_revenue,
        2
    ) AS cumulative_revenue,

    ROUND(
        100.0 * cumulative_revenue / total_revenue,
        2
    ) AS cumulative_percent

FROM cumulative_revenue

ORDER BY revenue DESC;
"""

cursor.execute(query14)
results14 = cursor.fetchall()

for row in results14[:20]:
    print(row)

print("\nTotal rows:", len(results14))
print("QUERY 14 COMPLETED SUCCESSFULLY")


# ============================================================
# Q15 - COHORT AND RETENTION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("QUERY 15 - COHORT RETENTION ANALYSIS")
print("=" * 70)

query15 = """
WITH customer_cohorts AS (

    SELECT
        customer_id,
        DATE(registration_date) AS registration_date,
        strftime('%Y-%m', registration_date) AS cohort_month

    FROM customers
),

cohort_sizes AS (

    SELECT
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size

    FROM customer_cohorts

    GROUP BY cohort_month
),

customer_orders AS (

    SELECT DISTINCT
        o.customer_id,
        DATE(o.order_date) AS order_date

    FROM orders o

    WHERE o.customer_id IS NOT NULL
),

cohort_activity AS (

    SELECT
        cc.cohort_month,
        cc.customer_id,

        (
            (
                CAST(strftime('%Y', co.order_date) AS INTEGER)
                -
                CAST(strftime('%Y', cc.registration_date) AS INTEGER)
            ) * 12

            +

            (
                CAST(strftime('%m', co.order_date) AS INTEGER)
                -
                CAST(strftime('%m', cc.registration_date) AS INTEGER)
            )
        ) AS month_number

    FROM customer_cohorts cc

    JOIN customer_orders co
        ON cc.customer_id = co.customer_id

    WHERE co.order_date >= cc.registration_date
),

cohort_counts AS (

    SELECT
        cohort_month,

        COUNT(DISTINCT CASE
            WHEN month_number = 0
            THEN customer_id
        END) AS month_0,

        COUNT(DISTINCT CASE
            WHEN month_number = 1
            THEN customer_id
        END) AS month_1,

        COUNT(DISTINCT CASE
            WHEN month_number = 2
            THEN customer_id
        END) AS month_2,

        COUNT(DISTINCT CASE
            WHEN month_number = 3
            THEN customer_id
        END) AS month_3

    FROM cohort_activity

    GROUP BY cohort_month
)

SELECT
    cs.cohort_month,

    cs.cohort_size,

    COALESCE(cc.month_0, 0) AS month_0,
    COALESCE(cc.month_1, 0) AS month_1,
    COALESCE(cc.month_2, 0) AS month_2,
    COALESCE(cc.month_3, 0) AS month_3,

    ROUND(
        100.0 * COALESCE(cc.month_0, 0)
        / NULLIF(cs.cohort_size, 0),
        2
    ) AS month_0_retention,

    ROUND(
        100.0 * COALESCE(cc.month_1, 0)
        / NULLIF(cs.cohort_size, 0),
        2
    ) AS month_1_retention,

    ROUND(
        100.0 * COALESCE(cc.month_2, 0)
        / NULLIF(cs.cohort_size, 0),
        2
    ) AS month_2_retention,

    ROUND(
        100.0 * COALESCE(cc.month_3, 0)
        / NULLIF(cs.cohort_size, 0),
        2
    ) AS month_3_retention

FROM cohort_sizes cs

LEFT JOIN cohort_counts cc
    ON cs.cohort_month = cc.cohort_month

ORDER BY cs.cohort_month;
"""

cursor.execute(query15)

results15 = cursor.fetchall()

# Show only first 20 rows
for row in results15[:20]:
    print(row)

# Show total number of result rows
print("\nTotal rows:", len(results15))

print("=" * 70)
print("QUERY 15 COMPLETED SUCCESSFULLY")
print("=" * 70)


# ============================================================
# Q16 - SELF JOIN WITH WINDOW FUNCTION
# ============================================================

print("\n" + "=" * 70)
print("QUERY 16 - SELF JOIN WITH WINDOW FUNCTION")
print("=" * 70)

query16 = """
WITH ordered_orders AS (
    SELECT
        o.order_id,
        o.customer_id,
        DATE(o.order_date) AS order_date,

        LAG(o.order_id) OVER (
            PARTITION BY o.customer_id
            ORDER BY DATE(o.order_date)
        ) AS previous_order_id,

        LAG(DATE(o.order_date)) OVER (
            PARTITION BY o.customer_id
            ORDER BY DATE(o.order_date)
        ) AS previous_order_date

    FROM orders o

    WHERE o.customer_id IS NOT NULL
),

order_comparison AS (
    SELECT
        current_order.order_id,
        current_order.customer_id,
        current_order.order_date,

        previous_order.order_id
            AS previous_order_id,

        previous_order.order_date
            AS previous_order_date

    FROM ordered_orders current_order

    LEFT JOIN ordered_orders previous_order
        ON current_order.previous_order_id =
           previous_order.order_id
)

SELECT
    order_id,
    customer_id,
    order_date,
    previous_order_id,
    previous_order_date,

    CASE
        WHEN previous_order_date IS NOT NULL
        THEN CAST(
            julianday(order_date)
            - julianday(previous_order_date)
            AS INTEGER
        )
        ELSE NULL
    END AS days_since_previous_order

FROM order_comparison

ORDER BY
    customer_id,
    order_date;
"""

cursor.execute(query16)
results16 = cursor.fetchall()

for row in results16[:20]:
    print(row)

print("\nTotal rows:", len(results16))
print("QUERY 16 COMPLETED SUCCESSFULLY")




# ============================================================
# CLOSE DATABASE
# ============================================================

cursor.close()
conn.close()


print("\n" + "=" * 70)
print("ALL SQL QUESTIONS Q1 TO Q16 COMPLETED SUCCESSFULLY")
print("=" * 70)