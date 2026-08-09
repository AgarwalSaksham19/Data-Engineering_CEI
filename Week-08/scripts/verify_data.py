import pandas as pd
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

RAW_DIR = os.path.join(
    BASE_DIR,
    "data",
    "raw"
)

# Load datasets
customers = pd.read_csv(
    os.path.join(RAW_DIR, "customers.csv")
)

products = pd.read_csv(
    os.path.join(RAW_DIR, "products.csv")
)

orders = pd.read_csv(
    os.path.join(RAW_DIR, "orders.csv")
)

order_items = pd.read_csv(
    os.path.join(RAW_DIR, "order_items.csv")
)


print("=" * 50)
print("PHASE 1 DATA VERIFICATION")
print("=" * 50)


# --------------------------------------------------
# 1. ROW COUNTS
# --------------------------------------------------

print("\n1. ROW COUNTS")

print("Customers    :", len(customers))
print("Products     :", len(products))
print("Orders       :", len(orders))
print("Order Items  :", len(order_items))


# --------------------------------------------------
# 2. NULL CUSTOMER IDs
# --------------------------------------------------

print("\n2. NULL CUSTOMER IDs IN ORDERS")

null_customers = (
    orders["customer_id"]
    .isna()
    .sum()
)

empty_customers = (
    orders["customer_id"]
    .fillna("")
    .eq("")
    .sum()
)

print(
    "Missing customer IDs:",
    null_customers + empty_customers
)


# --------------------------------------------------
# 3. INVALID EMAILS
# --------------------------------------------------

print("\n3. INVALID EMAILS")

valid_email = customers["email"].str.contains(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    regex=True,
    na=False
)

invalid_emails = (
    (~valid_email)
    .sum()
)

print(
    "Invalid emails:",
    invalid_emails
)


# --------------------------------------------------
# 4. NEGATIVE QUANTITIES
# --------------------------------------------------

print("\n4. NEGATIVE QUANTITIES")

negative_quantity = (
    order_items["quantity"] < 0
).sum()

print(
    "Negative quantity records:",
    negative_quantity
)


# --------------------------------------------------
# 5. PRODUCT NAME ISSUES
# --------------------------------------------------

print("\n5. PRODUCT NAME INCONSISTENCIES")

product_issues = products[
    (products["product_name"].str.startswith(" "))
    |
    (products["product_name"].str.endswith(" "))
    |
    (
        products["product_name"]
        != products["product_name"].str.title()
    )
]

print(
    "Products with formatting issues:",
    len(product_issues)
)


# --------------------------------------------------
# 6. WRONG DATE FORMAT
# --------------------------------------------------

print("\n6. DATE FORMAT CHECK")

wrong_date_format = orders[
    orders["order_date"].str.match(
        r"^\d{2}-\d{2}-\d{4}$",
        na=False
    )
]

print(
    "Wrong-format dates:",
    len(wrong_date_format)
)


# --------------------------------------------------
# 7. REFERENTIAL INTEGRITY
# --------------------------------------------------

print("\n7. REFERENTIAL INTEGRITY")

valid_order_ids = set(
    orders["order_id"]
)

invalid_order_items = order_items[
    ~order_items["order_id"]
    .isin(valid_order_ids)
]

print(
    "Order items with invalid order IDs:",
    len(invalid_order_items)
)


# --------------------------------------------------
# 8. FINAL
# --------------------------------------------------

print("\n" + "=" * 50)
print("VERIFICATION COMPLETED")
print("=" * 50)