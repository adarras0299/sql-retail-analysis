import sys
from pathlib import Path
import pandas as pd

# =====================================================
# Setup paths (robuste et pro)
# =====================================================
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.paths import DATA_CLEAN

# =====================================================
# Load datasets
# =====================================================
customers = pd.read_csv(
    DATA_CLEAN / "customers.csv",
    parse_dates=["first_order_date"]
)

orders = pd.read_csv(
    DATA_CLEAN / "orders.csv",
    parse_dates=["order_date"]
)

order_items = pd.read_csv(DATA_CLEAN / "order_items.csv")

# =====================================================
# Helper function
# =====================================================
def section(title):
    print("\n" + "=" * 60)
    print(title.upper())
    print("=" * 60)

# =====================================================
# 1. Dataset overview
# =====================================================
section("Dataset overview")

print("\nCustomers:", customers.shape)
print("Orders:", orders.shape)
print("Order items:", order_items.shape)

# =====================================================
# 2. Global KPIs (CEO view)
# =====================================================
section("Global KPIs (CEO)")

total_revenue = orders["order_amount"].sum()
nb_orders = orders.shape[0]
nb_customers = customers.shape[0]
avg_order_value = orders["order_amount"].mean()

print(f"Total revenue: {total_revenue:,.2f}")
print(f"Number of orders: {nb_orders:,}")
print(f"Number of customers: {nb_customers:,}")
print(f"Average order value: {avg_order_value:,.2f}")

# =====================================================
# 3. Time analysis
# =====================================================
section("Time analysis")

orders["order_month"] = orders["order_date"].dt.to_period("M")

monthly_revenue = (
    orders.groupby("order_month")["order_amount"]
    .sum()
    .sort_index()
)

print("\nMonthly revenue (last 5 months):")
print(monthly_revenue.tail())

# =====================================================
# 4. Geographic analysis
# =====================================================
section("Geographic analysis")

revenue_by_country = (
    orders.groupby("country")["order_amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 5 countries by revenue:")
print(revenue_by_country.head())

uk_share = (
    revenue_by_country["United Kingdom"] / total_revenue * 100
    if "United Kingdom" in revenue_by_country
    else 0
)

print(f"\nUK revenue share: {uk_share:.2f}%")

# =====================================================
# 5. Customer analysis (one-shot clients)
# =====================================================
section("Customer analysis")

top_customers = (
    orders.sort_values("order_amount", ascending=False)
    .head(10)[["order_id", "order_amount", "country"]]
)

print("\nTop 10 customers by order amount:")
print(top_customers)

# Pareto 80/20
orders_sorted = orders.sort_values("order_amount", ascending=False)
orders_sorted["cum_revenue_share"] = (
    orders_sorted["order_amount"].cumsum() / total_revenue
)

top_20pct_revenue = orders_sorted[
    orders_sorted["cum_revenue_share"] <= 0.8
].shape[0]

print(
    f"\n{top_20pct_revenue} orders generate 80% of total revenue "
    f"({top_20pct_revenue / nb_orders * 100:.2f}% of orders)"
)

# =====================================================
# 6. Product analysis
# =====================================================
section("Product analysis")

product_revenue = (
    order_items.groupby("product_name")["line_amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 products by revenue:")
print(product_revenue.head(10))

product_volume = (
    order_items.groupby("product_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 products by volume:")
print(product_volume.head(10))

# =====================================================
# 7. Outliers detection
# =====================================================
section("Outliers")

high_value_orders = orders[orders["order_amount"] > 10_000]

print(f"Number of orders > 10,000: {high_value_orders.shape[0]}")
print("\nTop 5 highest orders:")
print(
    high_value_orders
    .sort_values("order_amount", ascending=False)
    .head()
)


print("\nExploration completed successfully.")

