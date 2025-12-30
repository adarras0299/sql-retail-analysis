import sqlite3
import pandas as pd
from pathlib import Path
import sys
import matplotlib.pyplot as plt

# =====================================================
# Setup paths
# =====================================================
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.paths import BASE_DIR

DB_PATH = BASE_DIR / "database" / "retail.db"
SQL_PATH = BASE_DIR / "sql" / "rfm_analysis.sql"
OUTPUT_DIR = BASE_DIR / "analysis"
OUTPUT_DIR.mkdir(exist_ok=True)

# =====================================================
# Load RFM base from SQL
# =====================================================
print("Connecting to database...")
conn = sqlite3.connect(DB_PATH)

with open(SQL_PATH, "r", encoding="utf-8") as f:
    rfm_sql = f.read()

rfm = pd.read_sql_query(rfm_sql, conn)
conn.close()

print(f"{len(rfm)} customers loaded for RFM analysis")

# =====================================================
# Compute Recency (in days)
# =====================================================
rfm["last_order_date"] = pd.to_datetime(rfm["last_order_date"])
reference_date = rfm["last_order_date"].max()
rfm["recency"] = (reference_date - rfm["last_order_date"]).dt.days

# =====================================================
# RFM Scoring (quintiles)
# =====================================================
rfm["R_score"] = pd.qcut(rfm["recency"], 5, labels=[5,4,3,2,1])
rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm["M_score"] = pd.qcut(rfm["monetary"], 5, labels=[1,2,3,4,5])

rfm["RFM_score"] = (
    rfm["R_score"].astype(str)
    + rfm["F_score"].astype(str)
    + rfm["M_score"].astype(str)
)

# =====================================================
# Customer Segmentation
# =====================================================
def segment_customer(row):
    if row["R_score"] == 5 and row["F_score"] == 5 and row["M_score"] == 5:
        return "Best Customers"
    elif row["F_score"] >= 4:
        return "Loyal Customers"
    elif row["M_score"] >= 4:
        return "Big Spenders"
    elif row["R_score"] <= 2:
        return "At Risk"
    else:
        return "Need Attention"

rfm["segment"] = rfm.apply(segment_customer, axis=1)

# =====================================================
# Export results
# =====================================================
rfm_csv = OUTPUT_DIR / "rfm_segmentation.csv"
rfm.to_csv(rfm_csv, index=False)
print(f"RFM results exported to {rfm_csv}")

# =====================================================
# Plot segmentation
# =====================================================
rfm["segment"].value_counts().plot(kind="bar", figsize=(8,4))
plt.title("RFM Customer Segmentation")
plt.ylabel("Number of customers")
plt.tight_layout()

rfm_png = OUTPUT_DIR / "rfm_segmentation.png"
plt.savefig(rfm_png)
plt.close()

print(f"RFM segmentation plot saved to {rfm_png}")
print("RFM analysis completed successfully.")
