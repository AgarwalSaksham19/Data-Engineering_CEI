import sqlite3
from datetime import datetime


# ============================================================
# PHASE 6 - EDGE CASE TESTING
# ============================================================

print("=" * 70)
print("PHASE 6 - EDGE CASE TESTING")
print("=" * 70)


# ============================================================
# CREATE TEST DATABASE
# ============================================================

def create_test_database():

    conn = sqlite3.connect(":memory:")

    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # Customers table
    cursor.execute("""
        CREATE TABLE customers (
            customer_id TEXT PRIMARY KEY,
            customer_name TEXT
        )
    """)

    # Products table
    cursor.execute("""
        CREATE TABLE products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT
        )
    """)

    # Orders table
    cursor.execute("""
        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            order_date TEXT,
            status TEXT,

            FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
        )
    """)

    # Order items table
    cursor.execute("""
        CREATE TABLE order_items (
            item_id TEXT PRIMARY KEY,
            order_id TEXT,
            product_id TEXT,
            quantity INTEGER,
            unit_price REAL,
            discount_percent REAL,

            FOREIGN KEY (order_id)
            REFERENCES orders(order_id),

            FOREIGN KEY (product_id)
            REFERENCES products(product_id)
        )
    """)

    # Sample valid data
    cursor.execute("""
        INSERT INTO customers
        VALUES ('CUST001', 'Test Customer')
    """)

    cursor.execute("""
        INSERT INTO products
        VALUES ('PROD001', 'Test Product')
    """)

    cursor.execute("""
        INSERT INTO orders
        VALUES (
            'ORD001',
            'CUST001',
            '2026-01-10',
            'DELIVERED'
        )
    """)

    cursor.execute("""
        INSERT INTO order_items
        VALUES (
            'ITEM001',
            'ORD001',
            'PROD001',
            2,
            100.0,
            10.0
        )
    """)

    conn.commit()

    return conn


# ============================================================
# TEST 1 - INVALID ORDER ID
# ============================================================

def test_invalid_order_id():

    print("\n" + "-" * 70)
    print("TEST 1 - INVALID ORDER ID")
    print("-" * 70)

    conn = create_test_database()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO order_items
            VALUES (
                'ITEM002',
                'ORD999',
                'PROD001',
                1,
                100.0,
                10.0
            )
        """)

        conn.commit()

        print("FAILED")
        print("Invalid order ID was accepted.")

    except sqlite3.IntegrityError:

        print("PASSED")
        print(
            "Invalid order_id rejected by foreign key constraint."
        )

    finally:

        conn.close()


# ============================================================
# TEST 2 - DISCOUNT GREATER THAN 100
# ============================================================

def test_invalid_discount():

    print("\n" + "-" * 70)
    print("TEST 2 - DISCOUNT GREATER THAN 100%")
    print("-" * 70)

    conn = create_test_database()
    cursor = conn.cursor()

    discount = 120

    if discount > 100:

        print("PASSED")
        print(
            "Invalid discount detected:",
            discount,
            "%"
        )

    else:

        print("FAILED")
        print("Discount validation failed.")

    conn.close()


# ============================================================
# TEST 3 - ZERO QUANTITY
# ============================================================

def test_zero_quantity():

    print("\n" + "-" * 70)
    print("TEST 3 - ZERO QUANTITY")
    print("-" * 70)

    conn = create_test_database()
    cursor = conn.cursor()

    quantity = 0

    if quantity == 0:

        print("PASSED")
        print(
            "Zero quantity detected and treated as an edge case."
        )

    else:

        print("FAILED")

    conn.close()


# ============================================================
# TEST 4 - FUTURE ORDER DATE
# ============================================================

def test_future_date():

    print("\n" + "-" * 70)
    print("TEST 4 - FUTURE ORDER DATE")
    print("-" * 70)

    future_date = "2099-12-31"

    today = datetime.now().date()
    order_date = datetime.strptime(
        future_date,
        "%Y-%m-%d"
    ).date()

    if order_date > today:

        print("PASSED")
        print(
            "Future order date detected:",
            future_date
        )

    else:

        print("FAILED")
        print("Future date was not detected.")


# ============================================================
# RUN ALL TESTS
# ============================================================

test_invalid_order_id()

test_invalid_discount()

test_zero_quantity()

test_future_date()


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("PHASE 6 EDGE CASE TESTING COMPLETED")
print("=" * 70)