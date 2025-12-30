"""
- Execute analysis.sql
- Load results into pandas
- Export CSV / plots
"""

import sqlite3
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import re
import sys

# -----------------------
# Setup paths
# -----------------------
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.paths import BASE_DIR

DB_PATH = BASE_DIR / "database" / "retail.db"
SQL_FILE = BASE_DIR / "sql" / "analysis.sql"
OUTPUT_DIR = BASE_DIR / "analysis"
OUTPUT_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def load_sql_queries(sql_file: Path):
    """
    Load SQL queries from a file with their labels
    """
    queries = []
    with open(sql_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split queries sur les ;
    raw_queries = [q.strip() for q in content.split(";") if q.strip()]

    for q in raw_queries:
        # Cherche un label avec regex
        match = re.search(r"--\s*name\s*:\s*(\w+)", q, re.IGNORECASE)
        label = match.group(1) if match else f"query_{len(queries)+1}"
        queries.append({"label": label, "sql": q})

    return queries

# -----------------------
# Run queries and export
# -----------------------
def run_queries_and_export(db_path: Path, queries):
    print("Connecting to database...")
    conn = sqlite3.connect(db_path)

    for q in queries:
        label = q["label"]
        sql = q["sql"]
        print(f"\nExecuting query: {label} ...")

        try:
            df = pd.read_sql(sql, conn)
            print(f"Rows returned: {len(df)}")

            # Export CSV
            csv_path = OUTPUT_DIR / f"{label}.csv"
            df.to_csv(csv_path, index=False)
            print(f"Exported CSV: {csv_path}")

            # Simple plot if possible
            if len(df.columns) == 2 and pd.api.types.is_numeric_dtype(df.iloc[:,1]):
                plt.figure(figsize=(8,4))
                plt.bar(df.iloc[:,0].astype(str), df.iloc[:,1])
                plt.xticks(rotation=45, ha='right')
                plt.ylabel(df.columns[1])
                plt.title(label)
                plt.tight_layout()
                plt.savefig(OUTPUT_DIR / f"{label}.png")
                plt.close()
                print(f"Plot saved: {OUTPUT_DIR / label}.png")

        except Exception as e:
            print(f"Error executing {label}: {e}")

    conn.close()
    print("\nAll queries executed and exported successfully.")

# ------------------------------------------------------------
# Main execution
# ------------------------------------------------------------

if __name__ == "__main__":
    queries = load_sql_queries(SQL_FILE)
    if not queries:
        print("No SQL queries found.")
    else:
        run_queries_and_export(DB_PATH, queries)

