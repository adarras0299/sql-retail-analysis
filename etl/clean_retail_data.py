import pandas as pd
from pathlib import Path
import sys

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.paths import DATA_RAW, DATA_CLEAN

# Load raw data
df = pd.read_csv(
    DATA_RAW / "online_retail.csv",
    parse_dates=["InvoiceDate"]
)

# ============================
# CLEANING BASICS
# ============================

# Remove rows without customer_id
df = df.dropna(subset=["CustomerID"])

# Convert types
df["CustomerID"] = df["CustomerID"].astype(str)
df["InvoiceNo"] = df["InvoiceNo"].astype(str)

# Compute line amount
df["line_amount"] = df["Quantity"] * df["UnitPrice"]

# ============================
# CUSTOMERS TABLE
# ============================

customers = (
    df.groupby("CustomerID")
    .agg(
        first_order_date=("InvoiceDate", "min"),
        country=("Country", "first")
    )
    .reset_index()
    .rename(columns={"CustomerID": "customer_id"})
)

customers.to_csv(DATA_CLEAN / "customers.csv", index=False)

# ============================
# ORDERS TABLE  ✅ FIX ICI
# ============================

orders = (
    df.groupby("InvoiceNo")
    .agg(
        order_date=("InvoiceDate", "min"),
        order_amount=("line_amount", "sum"),
        customer_id=("CustomerID", "first"),
        country=("Country", "first")
    )
    .reset_index()
    .rename(columns={"InvoiceNo": "order_id"})
)

orders.to_csv(DATA_CLEAN / "orders.csv", index=False)

# ============================
# ORDER ITEMS TABLE
# ============================

order_items = df[[
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "UnitPrice",
    "line_amount"
]].rename(columns={
    "InvoiceNo": "order_id",
    "StockCode": "product_id",
    "Description": "product_name",
    "Quantity": "quantity",
    "UnitPrice": "unit_price"
})

order_items.to_csv(DATA_CLEAN / "order_items.csv", index=False)

print("Clean data successfully generated.")
