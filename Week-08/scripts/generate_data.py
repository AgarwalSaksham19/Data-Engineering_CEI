import csv
import random
import os
from datetime import datetime, timedelta

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(RAW_DIR, exist_ok=True)

NUM_CUSTOMERS = 500
NUM_PRODUCTS = 500
NUM_ORDERS = 1000
NUM_ORDER_ITEMS = 2000

random.seed(42)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start_year=2023, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 8, 1)

    days = (end - start).days

    random_days = random.randint(0, days)

    date = start + timedelta(days=random_days)

    return date


def random_email(name, customer_number):

    # Around 2% invalid emails
    if customer_number % 50 == 0:

        invalid_emails = [
            f"{name}gmail.com",
            f"{name}@",
            f"{name}.com",
            f"{name}example.com"
        ]

        return random.choice(invalid_emails)

    return f"{name}{customer_number}@example.com"


# ============================================================
# 1. GENERATE CUSTOMERS
# ============================================================

print("Generating customers...")

first_names = [
    "Rahul", "Amit", "Priya", "Neha", "Rohan",
    "Ankit", "Sneha", "Karan", "Pooja", "Arjun",
    "Vikas", "Simran", "Aditya", "Kavya", "Nikhil"
]

last_names = [
    "Sharma", "Verma", "Singh", "Kumar", "Gupta",
    "Mehta", "Joshi", "Patel", "Malhotra", "Agarwal"
]

customer_types = [
    "REGULAR",
    "PREMIUM",
    "VIP"
]

customers = []

for i in range(1, NUM_CUSTOMERS + 1):

    customer_id = f"CUST{i:05d}"

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    customer_name = f"{first_name} {last_name}"

    email_name = (
        first_name.lower()
        + last_name.lower()
    )

    email = random_email(email_name, i)

    registration_date = random_date(
        2023,
        2025
    ).strftime("%Y-%m-%d")

    customer_type = random.choice(customer_types)

    customers.append([
        customer_id,
        customer_name,
        email,
        registration_date,
        customer_type
    ])


customers_file = os.path.join(
    RAW_DIR,
    "customers.csv"
)

with open(
    customers_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "customer_id",
        "customer_name",
        "email",
        "registration_date",
        "customer_type"
    ])

    writer.writerows(customers)


print(f"Customers created: {len(customers)}")


# ============================================================
# 2. GENERATE PRODUCTS
# ============================================================

print("Generating products...")

categories = {
    "Electronics": [
        "Laptop",
        "Smartphone",
        "Headphones",
        "Keyboard",
        "Mouse",
        "Monitor"
    ],

    "Clothing": [
        "T Shirt",
        "Jeans",
        "Jacket",
        "Shoes",
        "Sweater",
        "Dress"
    ],

    "Home": [
        "Chair",
        "Table",
        "Lamp",
        "Pillow",
        "Curtain",
        "Sofa"
    ],

    "Books": [
        "Novel",
        "Science Book",
        "History Book",
        "Programming Book",
        "Math Book",
        "Biography"
    ]
}

products = []

for i in range(1, NUM_PRODUCTS + 1):

    product_id = f"PROD{i:05d}"

    category = random.choice(
        list(categories.keys())
    )

    subcategory = random.choice(
        categories[category]
    )

    # Normal product name
    product_name = subcategory

    # Intentionally introduce
    # spaces and mixed case
    if i % 20 == 0:

        product_name = (
            "  "
            + subcategory.upper()
            + "  "
        )

    elif i % 25 == 0:

        product_name = subcategory.lower()

    cost_price = round(
        random.uniform(100, 50000),
        2
    )

    products.append([
        product_id,
        product_name,
        category,
        subcategory,
        cost_price
    ])


products_file = os.path.join(
    RAW_DIR,
    "products.csv"
)

with open(
    products_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "product_id",
        "product_name",
        "category",
        "subcategory",
        "cost_price"
    ])

    writer.writerows(products)


print(f"Products created: {len(products)}")


# ============================================================
# 3. GENERATE ORDERS
# ============================================================

print("Generating orders...")

statuses = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
]

regions = [
    "NORTH",
    "SOUTH",
    "EAST",
    "WEST",
    "CENTRAL"
]

orders = []

for i in range(1, NUM_ORDERS + 1):

    order_id = f"ORD{i:06d}"

    # Around 5% NULL customer IDs
    if i % 20 == 0:

        customer_id = ""

    else:

        customer_id = random.choice(
            customers
        )[0]

    order_date = random_date(
        2024,
        2026
    )

    # Some dates intentionally use
    # DD-MM-YYYY format
    if i % 25 == 0:

        order_date_value = (
            order_date.strftime(
                "%d-%m-%Y"
            )
        )

    else:

        order_date_value = (
            order_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

    status = random.choice(statuses)

    region_code = random.choice(regions)

    orders.append([
        order_id,
        customer_id,
        order_date_value,
        status,
        region_code
    ])


orders_file = os.path.join(
    RAW_DIR,
    "orders.csv"
)

with open(
    orders_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "order_id",
        "customer_id",
        "order_date",
        "status",
        "region_code"
    ])

    writer.writerows(orders)


print(f"Orders created: {len(orders)}")


# ============================================================
# 4. GENERATE ORDER ITEMS
# ============================================================

print("Generating order items...")

order_items = []

for i in range(1, NUM_ORDER_ITEMS + 1):

    item_id = f"ITEM{i:06d}"

    # Use existing orders so that
    # referential integrity mostly holds
    order_id = random.choice(
        orders
    )[0]

    product_id = random.choice(
        products
    )[0]

    # Normal quantity
    quantity = random.randint(1, 10)

    # Around 3% negative quantities
    # represent returns
    if i % 33 == 0:

        quantity = -random.randint(
            1,
            3
        )

    unit_price = round(
        random.uniform(
            100,
            60000
        ),
        2
    )

    discount_percent = round(
        random.uniform(
            0,
            100
        ),
        2
    )

    order_items.append([
        item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        discount_percent
    ])


order_items_file = os.path.join(
    RAW_DIR,
    "order_items.csv"
)

with open(
    order_items_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "discount_percent"
    ])

    writer.writerows(order_items)


print(
    f"Order items created: "
    f"{len(order_items)}"
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n====================================")
print("DATA GENERATION COMPLETED")
print("====================================")

print(f"Customers    : {customers_file}")
print(f"Products     : {products_file}")
print(f"Orders       : {orders_file}")
print(f"Order Items  : {order_items_file}")

print("\nAll raw datasets are stored in:")
print(RAW_DIR)