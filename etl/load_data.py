import sqlite3
import pandas as pd
from pathlib import Path
import sys

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.paths import DATA_CLEAN, BASE_DIR

DB_PATH = BASE_DIR / "database" / "retail.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Clean tables before reload
cursor.execute("DELETE FROM order_items")
cursor.execute("DELETE FROM orders")
cursor.execute("DELETE FROM customers")
conn.commit()

# Load CSV files
customers = pd.read_csv(
    DATA_CLEAN / "customers.csv",
    parse_dates=["first_order_date"],
    dtype={"customer_id": str}
)

orders = pd.read_csv(
    DATA_CLEAN / "orders.csv",
    parse_dates=["order_date"],
    dtype={"order_id": str}
)

order_items = pd.read_csv(
    DATA_CLEAN / "order_items.csv",
    dtype={"order_id": str, "product_id": str}
)

# Insert data
customers.to_sql("customers", conn, if_exists="append", index=False)
orders.to_sql("orders", conn, if_exists="append", index=False)
order_items.to_sql("order_items", conn, if_exists="append", index=False)

# Check row counts
for table in ["customers", "orders", "order_items"]:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"{table}: {cursor.fetchone()[0]} rows")

conn.close()

print("Data successfully loaded into SQLite database.")
