import pandas as pd
import os


# ============================================================
# PATH CONFIGURATION
# ============================================================

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

CLEAN_DIR = os.path.join(
    BASE_DIR,
    "data",
    "cleaned"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)

# Create folders if they don't exist
os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("PHASE 2 - DATA CLEANING")
print("=" * 60)

print("\nLoading datasets...")

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

print("Customers loaded    :", len(customers))
print("Products loaded     :", len(products))
print("Orders loaded       :", len(orders))
print("Order items loaded  :", len(order_items))


# ============================================================
# CLEAN CUSTOMERS
# ============================================================

print("\n" + "-" * 60)
print("1. CLEANING CUSTOMERS")
print("-" * 60)

customers_original_count = len(customers)


# Remove duplicate customer records
customers = customers.drop_duplicates(
    subset=["customer_id"]
)


# Clean customer names
customers["customer_name"] = (
    customers["customer_name"]
    .astype(str)
    .str.strip()
)


# Clean emails
customers["email"] = (
    customers["email"]
    .astype(str)
    .str.strip()
    .str.lower()
)


print(
    "Duplicate customers removed:",
    customers_original_count - len(customers)
)


# ============================================================
# VALIDATE EMAILS
# ============================================================

def validate_emails(df):

    email_pattern = (
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )

    valid = df["email"].str.match(
        email_pattern,
        na=False
    )

    invalid_customer_ids = (
        df.loc[~valid, "customer_id"]
        .tolist()
    )

    return invalid_customer_ids


invalid_customer_ids = validate_emails(
    customers
)

print(
    "Invalid emails found:",
    len(invalid_customer_ids)
)

print(
    "Invalid customer IDs:",
    invalid_customer_ids[:10]
)


# Replace invalid emails with missing value
if invalid_customer_ids:

    customers.loc[
        customers["customer_id"].isin(
            invalid_customer_ids
        ),
        "email"
    ] = pd.NA


# ============================================================
# CLEAN PRODUCTS
# ============================================================

print("\n" + "-" * 60)
print("2. CLEANING PRODUCTS")
print("-" * 60)

products_original_count = len(products)


# Remove duplicate products
products = products.drop_duplicates(
    subset=["product_id"]
)


# Normalize product names
products["product_name"] = (
    products["product_name"]
    .astype(str)
    .str.strip()
    .str.title()
)


# Clean category and subcategory
products["category"] = (
    products["category"]
    .astype(str)
    .str.strip()
    .str.title()
)

products["subcategory"] = (
    products["subcategory"]
    .astype(str)
    .str.strip()
    .str.title()
)


# Make cost price numeric
products["cost_price"] = pd.to_numeric(
    products["cost_price"],
    errors="coerce"
)


print(
    "Duplicate products removed:",
    products_original_count - len(products)
)

print(
    "Product names normalized successfully."
)


# ============================================================
# CLEAN ORDERS
# ============================================================

print("\n" + "-" * 60)
print("3. CLEANING ORDERS")
print("-" * 60)

orders_original_count = len(orders)


# ------------------------------------------------------------
# Handle missing customer IDs
# ------------------------------------------------------------

missing_customer_mask = (
    orders["customer_id"]
    .isna()
    |
    orders["customer_id"]
    .astype(str)
    .str.strip()
    .eq("")
)

missing_customer_count = (
    missing_customer_mask.sum()
)

print(
    "Orders with missing customer ID:",
    missing_customer_count
)


# Remove orders without customer IDs
orders = orders[
    ~missing_customer_mask
].copy()


# ------------------------------------------------------------
# Clean customer ID
# ------------------------------------------------------------

orders["customer_id"] = (
    orders["customer_id"]
    .astype(str)
    .str.strip()
)


# ------------------------------------------------------------
# Fix order dates
# ------------------------------------------------------------

def fix_order_date(value):

    if pd.isna(value):
        return pd.NaT

    value = str(value).strip()

    # DD-MM-YYYY
    try:

        if (
            len(value) == 10
            and value[2] == "-"
            and value[5] == "-"
        ):

            return pd.to_datetime(
                value,
                format="%d-%m-%Y"
            )

    except:

        pass


    # YYYY-MM-DD HH:MM:SS
    try:

        return pd.to_datetime(
            value,
            format="%Y-%m-%d %H:%M:%S"
        )

    except:

        return pd.NaT


orders["order_date"] = (
    orders["order_date"]
    .apply(fix_order_date)
)


invalid_date_count = (
    orders["order_date"]
    .isna()
    .sum()
)

print(
    "Invalid dates after conversion:",
    invalid_date_count
)


# Remove rows where date could not be fixed
orders = orders.dropna(
    subset=["order_date"]
)


# ------------------------------------------------------------
# Remove duplicate orders
# ------------------------------------------------------------

orders = orders.drop_duplicates(
    subset=["order_id"]
)


print(
    "Duplicate orders removed:",
    orders_original_count
    - missing_customer_count
    - len(orders)
)


# ============================================================
# CLEAN ORDER ITEMS
# ============================================================

print("\n" + "-" * 60)
print("4. CLEANING ORDER ITEMS")
print("-" * 60)

order_items_original_count = len(
    order_items
)


# Remove duplicate item IDs
order_items = (
    order_items
    .drop_duplicates(
        subset=["item_id"]
    )
)


# Convert numeric columns
order_items["quantity"] = pd.to_numeric(
    order_items["quantity"],
    errors="coerce"
)

order_items["unit_price"] = pd.to_numeric(
    order_items["unit_price"],
    errors="coerce"
)

order_items["discount_percent"] = pd.to_numeric(
    order_items["discount_percent"],
    errors="coerce"
)


# ============================================================
# REFERENTIAL INTEGRITY
# ============================================================

def check_referential_integrity(
    orders_df,
    order_items_df
):

    valid_order_ids = set(
        orders_df["order_id"]
    )

    invalid_items = order_items_df[
        ~order_items_df["order_id"]
        .isin(valid_order_ids)
    ]

    return invalid_items


invalid_order_items = (
    check_referential_integrity(
        orders,
        order_items
    )
)

print(
    "Invalid order references:",
    len(invalid_order_items)
)


# Remove order items referencing
# non-existent orders
if len(invalid_order_items) > 0:

    order_items = order_items[
        order_items["order_id"]
        .isin(
            set(orders["order_id"])
        )
    ].copy()


# Check product references
valid_product_ids = set(
    products["product_id"]
)

invalid_product_items = order_items[
    ~order_items["product_id"]
    .isin(valid_product_ids)
]

print(
    "Invalid product references:",
    len(invalid_product_items)
)


# Remove invalid product references
if len(invalid_product_items) > 0:

    order_items = order_items[
        order_items["product_id"]
        .isin(valid_product_ids)
    ].copy()


# ============================================================
# FINAL CLEANING
# ============================================================

# Remove rows with missing critical values
order_items = order_items.dropna(
    subset=[
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "discount_percent"
    ]
)


# Remove invalid discount values
invalid_discount = (
    (order_items["discount_percent"] < 0)
    |
    (order_items["discount_percent"] > 100)
)

print(
    "Invalid discount records:",
    invalid_discount.sum()
)

order_items = order_items[
    ~invalid_discount
].copy()


# Keep negative quantities because
# the assignment defines them as returns.


print(
    "Duplicate order items removed:",
    order_items_original_count
    - len(order_items)
)


# ============================================================
# SAVE CLEANED DATA
# ============================================================

print("\n" + "-" * 60)
print("5. SAVING CLEANED DATA")
print("-" * 60)


customers.to_csv(
    os.path.join(
        CLEAN_DIR,
        "customers_clean.csv"
    ),
    index=False
)


products.to_csv(
    os.path.join(
        CLEAN_DIR,
        "products_clean.csv"
    ),
    index=False
)


orders.to_csv(
    os.path.join(
        CLEAN_DIR,
        "orders_clean.csv"
    ),
    index=False
)


order_items.to_csv(
    os.path.join(
        CLEAN_DIR,
        "order_items_clean.csv"
    ),
    index=False
)


print(
    "customers_clean.csv saved"
)

print(
    "products_clean.csv saved"
)

print(
    "orders_clean.csv saved"
)

print(
    "order_items_clean.csv saved"
)


# ============================================================
# DATA QUALITY REPORT
# ============================================================

report_file = os.path.join(
    OUTPUT_DIR,
    "data_quality_report.txt"
)

with open(
    report_file,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "E-COMMERCE DATA QUALITY REPORT\n"
    )

    file.write(
        "=" * 50 + "\n\n"
    )

    file.write(
        f"Original customers: "
        f"{customers_original_count}\n"
    )

    file.write(
        f"Clean customers: "
        f"{len(customers)}\n\n"
    )

    file.write(
        f"Original products: "
        f"{products_original_count}\n"
    )

    file.write(
        f"Clean products: "
        f"{len(products)}\n\n"
    )

    file.write(
        f"Original orders: "
        f"{orders_original_count}\n"
    )

    file.write(
        f"Clean orders: "
        f"{len(orders)}\n"
    )

    file.write(
        f"Missing customer IDs removed: "
        f"{missing_customer_count}\n\n"
    )

    file.write(
        f"Invalid emails found: "
        f"{len(invalid_customer_ids)}\n"
    )

    file.write(
        f"Invalid order references: "
        f"{len(invalid_order_items)}\n"
    )

    file.write(
        f"Invalid product references: "
        f"{len(invalid_product_items)}\n"
    )

    file.write(
        f"Invalid dates removed: "
        f"{invalid_date_count}\n"
    )

    file.write(
        f"Clean order items: "
        f"{len(order_items)}\n"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("PHASE 2 COMPLETED SUCCESSFULLY")
print("=" * 60)

print(
    "\nFinal dataset sizes:"
)

print(
    "Customers    :",
    len(customers)
)

print(
    "Products     :",
    len(products)
)

print(
    "Orders       :",
    len(orders)
)

print(
    "Order Items  :",
    len(order_items)
)

print(
    "\nCleaned files saved in:"
)

print(CLEAN_DIR)

print(
    "\nData quality report:"
)

print(report_file)