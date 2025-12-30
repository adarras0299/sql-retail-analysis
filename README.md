# 📊 SQL Portfolio – Business Intelligence & Customer Analytics

This project is a **data analytics portfolio** showcasing SQL and Python skills applied to real-world Business Intelligence use cases.

It covers **descriptive analytics, KPI computation, customer behavior analysis, and customer segmentation (RFM)** using a relational database and reproducible ETL pipelines.

---

## 🎯 Project Objectives

- Demonstrate strong **SQL analytics capabilities**
- Apply **Business Intelligence use cases** on transactional data
- Showcase **Python + SQL complementarity**
- Produce **actionable business insights**, not only queries

---

## 🛠 Tech Stack

- **SQL (SQLite)**
  - CTEs (`WITH`)
  - Aggregations
  - Time-based analysis
- **Python**
  - pandas
  - matplotlib
  - sqlite3
- **Data Engineering**
  - ETL scripts
  - Reproducible pipelines
- **Business Intelligence concepts**
  - KPIs
  - RFM segmentation
  - Revenue concentration (Pareto)

---

## 🔄 Data Preparation & Database Modeling
The **raw CSV file dataset** is from Ali Prasla : Online Retail Sales: Product Transactions and Customer Details
(available on Kaggle : https://www.kaggle.com/datasets/thedevastator/online-retail-transaction-records ).
The original dataset was provided as **raw CSV files** containing transactional e-commerce data at different granularities.

To enable efficient SQL analysis and Business Intelligence use cases, the data was **cleaned, normalized, and structured into a relational SQLite database** following a classic analytical model.

---

## 🏗 ETL Overview

### Step 1 – Raw Data Cleaning
- Removal of invalid rows (missing IDs, negative quantities, invalid prices)
- Parsing of date columns
- Basic type normalization

📄 `etl/clean_retail_data.py`  
Cleaned files are stored in the `data_clean/` directory.

---

### Step 2 – Database Creation

A SQLite database (`retail.db`) is created using a predefined schema:

- Primary keys
- Foreign keys
- Correct data types
- Referential integrity between tables

📄 `etl/create_database.py`  
📄 `sql/schema.sql`

---

### Step 3 – Data Loading

Cleaned CSV files are loaded into SQLite tables using pandas:

📄 `etl/load_data.py`

This step populates the analytical database used for all SQL and BI analyses.

---

## 🧩 Database Schema

The database follows a **normalized relational structure** with three core tables.

---

### 📦 customers

**One row per customer**

This table contains customer-level information and serves as the main entity for customer analytics and segmentation.

| Column | Type | Description |
|------|------|------------|
| customer_id | INTEGER (PK) | Unique customer identifier |
| country | TEXT | Customer country |
| first_order_date | DATE | Date of first purchase |

**Use cases**
- Geographic analysis
- Customer segmentation
- Cohort analysis
- RFM analysis

---

### 🧾 orders

**One row per order**

This table represents each transaction placed by a customer.

| Column | Type | Description |
|------|------|------------|
| order_id | INTEGER (PK) | Unique order identifier |
| customer_id | INTEGER (FK) | Reference to customers.customer_id |
| order_date | DATETIME | Date and time of the order |
| order_amount | FLOAT | Total monetary value of the order |
| country | TEXT | Order country (derived from customer) |

**Use cases**
- Revenue analysis
- Time-series analysis
- Order frequency
- Outlier detection

➡️ **A customer can have multiple orders**, enabling repeat purchase analysis.

---

### 🛒 order_items

**One row per product per order**

This table contains the detailed composition of each order.

| Column | Type | Description |
|------|------|------------|
| order_item_id | INTEGER (PK) | Unique line item identifier |
| order_id | INTEGER (FK) | Reference to orders.order_id |
| product_id | TEXT | Product identifier |
| product_name | TEXT | Product description |
| quantity | INTEGER | Number of units purchased |
| unit_price | FLOAT | Price per unit |

**Use cases**
- Product performance analysis
- Volume vs value analysis
- Revenue contribution per product
- Basket composition analysis

---

## 🗂 Final Dataset Overview

The database simulates an e-commerce transactional system with:

- **customers** (~4,300)
- **orders** (~22,000)
- **order_items** (order-level product details)

Each customer can place **multiple orders**, enabling cohort, frequency, and segmentation analysis.

---


## 📈 Global Analyses Performed

📄 `sql/analysis.sql`  
▶ Executed via `etl/run_and_export_analysis_sql.py`

### Global Business KPIs (SQL)

- Total revenue
- Average basket value
- Revenue growth over time
- Revenue concentration (Pareto 80/20)

---

### Customer & Revenue Analysis (SQL)

- Customer geographic distribution
- Temporal analysis of first orders
- Revenue by region
- Order frequency per customer

---

### Product Performance Analysis (SQL)

- Product contribution to revenue
- Volume vs value analysis
- Detection of outliers (high-value orders)

---

### Outputs
Each query gives a CSV file `analysis/*.csv`
For each query where a simple plot is possible (2 columns), a png file shows the analysis

---

## 📈Customer Segmentation – RFM (SQL + Python)

A dedicated **RFM (Recency, Frequency, Monetary)** analysis was implemented.
📄 `sql/rfm_analysis.sql`  
▶ Executed via `etl/run_rfm_analysis.py`

### Process

- SQL extraction of customer-level metrics
- Python computation of RFM scores
- Business segmentation into meaningful customer groups

### Customer Segments

- **Best Customers**
- **Loyal Customers**
- **Big Spenders**
- **Need Attention**
- **At Risk**


### Outputs

- `analysis/rfm_segmentation.csv`
- `analysis/rfm_segments_distribution.png`

---

## 📊 Example Insights

- ~30% of customers are **loyal repeat buyers**
- ~30% are **at risk of churn**
- ~8% are **high-value customers**
- Revenue shows strong concentration among top customers

These insights can directly support **marketing, CRM, and retention strategies**.

---



## Additional ETL Scripts

The project also includes three auxiliary scripts in the `etl/` folder:

- **`check_database.py`**: Checks that the SQLite database has been created correctly and that the tables `customers`, `orders`, and `order_items` exist. Useful for a quick console check.

- **`explore_data.py`**: Data exploration script for raw or cleaned datasets. It provides descriptive statistics and helps understand the structure of the data before any analysis.

- **`run_sql.py`**: Legacy script for running SQL queries. Can be used to test queries or understand the process, but the main script for analysis is now `run_and_export_analysis_sql.py`.

💡 **Note**: These scripts are optional and intended to be run in the console to verify different steps of the project. They are not required to reproduce the final analysis or the outputs generated by the main scripts.

