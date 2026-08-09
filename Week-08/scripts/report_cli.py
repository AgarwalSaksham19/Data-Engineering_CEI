import sqlite3
from datetime import datetime, timedelta

DB_PATH = "ecommerce.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def connect_database():
    return sqlite3.connect(DB_PATH)


# ============================================================
# DATE VALIDATION
# ============================================================

def validate_date(date_text):

    try:
        return datetime.strptime(date_text, "%Y-%m-%d").date()

    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return None


# ============================================================
# GET PREVIOUS PERIOD
# ============================================================

def get_previous_period(start_date, end_date):

    days = (end_date - start_date).days + 1

    previous_end = start_date - timedelta(days=1)
    previous_start = previous_end - timedelta(days=days - 1)

    return previous_start, previous_end


# ============================================================
# REPORT CALCULATION
# ============================================================

def generate_report(report_type, start_date, end_date):

    conn = connect_database()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # CURRENT PERIOD
    # --------------------------------------------------------

    current_query = """
    SELECT
        COUNT(DISTINCT o.order_id) AS total_orders,

        ROUND(
            COALESCE(
                SUM(
                    oi.quantity *
                    oi.unit_price *
                    (1 - oi.discount_percent / 100.0)
                ),
                0
            ),
            2
        ) AS revenue,

        COUNT(DISTINCT o.customer_id) AS unique_customers

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE DATE(o.order_date)
          BETWEEN ? AND ?;
    """

    cursor.execute(
        current_query,
        (str(start_date), str(end_date))
    )

    total_orders, revenue, unique_customers = cursor.fetchone()


    # --------------------------------------------------------
    # TOP 3 PRODUCTS
    # --------------------------------------------------------

    top_products_query = """

    SELECT
        p.product_name,

        ROUND(
            SUM(
                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS product_revenue

    FROM products p

    JOIN order_items oi
        ON p.product_id = oi.product_id

    JOIN orders o
        ON oi.order_id = o.order_id

    WHERE DATE(o.order_date)
          BETWEEN ? AND ?

    GROUP BY
        p.product_id,
        p.product_name

    ORDER BY product_revenue DESC

    LIMIT 3;

    """

    cursor.execute(
        top_products_query,
        (str(start_date), str(end_date))
    )

    top_products = cursor.fetchall()


    # --------------------------------------------------------
    # PREVIOUS PERIOD
    # --------------------------------------------------------

    previous_start, previous_end = get_previous_period(
        start_date,
        end_date
    )

    previous_query = """

    SELECT
        COUNT(DISTINCT o.order_id),

        ROUND(
            COALESCE(
                SUM(
                    oi.quantity *
                    oi.unit_price *
                    (1 - oi.discount_percent / 100.0)
                ),
                0
            ),
            2
        )

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE DATE(o.order_date)
          BETWEEN ? AND ?;

    """

    cursor.execute(
        previous_query,
        (
            str(previous_start),
            str(previous_end)
        )
    )

    previous_orders, previous_revenue = cursor.fetchone()


    # --------------------------------------------------------
    # PERCENTAGE CHANGE
    # --------------------------------------------------------

    if previous_revenue and previous_revenue != 0:

        revenue_change = (
            (revenue - previous_revenue)
            / previous_revenue
        ) * 100

    else:

        revenue_change = None


    if previous_orders and previous_orders != 0:

        order_change = (
            (total_orders - previous_orders)
            / previous_orders
        ) * 100

    else:

        order_change = None


    # ========================================================
    # DISPLAY REPORT
    # ========================================================

    print("\n" + "=" * 70)
    print("E-COMMERCE ORDER ANALYTICS REPORT")
    print("=" * 70)

    print("\nReport Type       :", report_type.upper())

    print(
        "Date Range        :",
        start_date,
        "to",
        end_date
    )

    print(
        "Previous Period   :",
        previous_start,
        "to",
        previous_end
    )

    print("\n" + "-" * 70)

    print("SUMMARY")
    print("-" * 70)

    print("Total Orders      :", total_orders)

    print("Total Revenue     : ₹", revenue)

    print("Unique Customers  :", unique_customers)

    print("\n" + "-" * 70)

    print("PREVIOUS PERIOD COMPARISON")
    print("-" * 70)

    print("Previous Orders   :", previous_orders)

    print(
        "Previous Revenue  : ₹",
        previous_revenue
    )

    if order_change is not None:

        print(
            "Order Change      : {:.2f}%".format(
                order_change
            )
        )

    else:

        print("Order Change      : N/A")


    if revenue_change is not None:

        print(
            "Revenue Change    : {:.2f}%".format(
                revenue_change
            )
        )

    else:

        print("Revenue Change    : N/A")


    print("\n" + "-" * 70)

    print("TOP 3 PRODUCTS")
    print("-" * 70)

    if top_products:

        for index, row in enumerate(
            top_products,
            start=1
        ):

            print(
                "{}. {} - ₹{}".format(
                    index,
                    row[0],
                    row[1]
                )
            )

    else:

        print("No products found for this period.")


    print("\n" + "=" * 70)
    print("REPORT GENERATED SUCCESSFULLY")
    print("=" * 70)

    conn.close()


# ============================================================
# MAIN CLI
# ============================================================

def main():

    print("=" * 70)
    print("E-COMMERCE ORDER ANALYTICS CLI")
    print("=" * 70)

    print("\nAvailable report types:")
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")

    report_type = input(
        "\nEnter report type (daily/weekly/monthly): "
    ).strip().lower()


    # --------------------------------------------------------
    # VALIDATE REPORT TYPE
    # --------------------------------------------------------

    if report_type not in [
        "daily",
        "weekly",
        "monthly"
    ]:

        print(
            "\nInvalid report type."
        )

        print(
            "Please choose daily, weekly, or monthly."
        )

        return


    # --------------------------------------------------------
    # DATE INPUT
    # --------------------------------------------------------

    start_input = input(
        "Enter start date (YYYY-MM-DD): "
    ).strip()

    end_input = input(
        "Enter end date (YYYY-MM-DD): "
    ).strip()


    start_date = validate_date(start_input)
    end_date = validate_date(end_input)


    if start_date is None or end_date is None:
        return


    # --------------------------------------------------------
    # DATE RANGE VALIDATION
    # --------------------------------------------------------

    if start_date > end_date:

        print(
            "\nError: Start date cannot be after end date."
        )

        return


    # --------------------------------------------------------
    # GENERATE REPORT
    # --------------------------------------------------------

    generate_report(
        report_type,
        start_date,
        end_date
    )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()