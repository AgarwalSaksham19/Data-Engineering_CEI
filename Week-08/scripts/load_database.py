import sqlite3
import pandas as pd
import os

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CLEAN_DIR = os.path.join(
    BASE_DIR,
    "data",
    "cleaned"
)

DB_PATH = os.path.join(
    BASE_DIR,
    "ecommerce.db"
)

SCHEMA_PATH = os.path.join(
    BASE_DIR,
    "sql",
    "schema.sql"
)


# ------------------------------------------------------------
# CONNECT TO SQLITE
# ------------------------------------------------------------

connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()

cursor.execute(
    "PRAGMA foreign_keys = ON"
)


# ------------------------------------------------------------
# CREATE TABLES
# ------------------------------------------------------------

with open(
    SCHEMA_PATH,
    "r",
    encoding="utf-8"
) as file:

    schema = file.read()

connection.executescript(schema)


# ------------------------------------------------------------
# LOAD CLEANED CSV FILES
# ------------------------------------------------------------

customers = pd.read_csv(
    os.path.join(
        CLEAN_DIR,
        "customers_clean.csv"
    )
)

products = pd.read_csv(
    os.path.join(
        CLEAN_DIR,
        "products_clean.csv"
    )
)

orders = pd.read_csv(
    os.path.join(
        CLEAN_DIR,
        "orders_clean.csv"
    )
)

order_items = pd.read_csv(
    os.path.join(
        CLEAN_DIR,
        "order_items_clean.csv"
    )
)


# ------------------------------------------------------------
# INSERT DATA
# ------------------------------------------------------------

customers.to_sql(
    "customers",
    connection,
    if_exists="append",
    index=False
)

products.to_sql(
    "products",
    connection,
    if_exists="append",
    index=False
)

orders.to_sql(
    "orders",
    connection,
    if_exists="append",
    index=False
)

order_items.to_sql(
    "order_items",
    connection,
    if_exists="append",
    index=False
)


# ------------------------------------------------------------
# ROW COUNT VALIDATION
# ------------------------------------------------------------

print("=" * 60)
print("PHASE 3 - SQLITE DATABASE")
print("=" * 60)

print("\nROW COUNTS")

tables = [
    "customers",
    "products",
    "orders",
    "order_items"
]

for table in tables:

    count = cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(
        f"{table:<15}: {count}"
    )


# ------------------------------------------------------------
# FOREIGN KEY VALIDATION
# ------------------------------------------------------------

print("\nFOREIGN KEY VALIDATION")

errors = cursor.execute(
    "PRAGMA foreign_key_check"
).fetchall()

if len(errors) == 0:

    print(
        "No foreign key violations found."
    )

else:

    print(
        "Foreign key violations found:"
    )

    for error in errors:
        print(error)


# ------------------------------------------------------------
# SHOW TABLES
# ------------------------------------------------------------

print("\nDATABASE TABLES")

tables_found = cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    """
).fetchall()

for table in tables_found:
    print("-", table[0])


# ------------------------------------------------------------
# CLOSE DATABASE
# ------------------------------------------------------------

connection.commit()
connection.close()

print("\nDatabase created successfully!")
print("Database:", DB_PATH)