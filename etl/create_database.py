import sqlite3
from pathlib import Path
import sys

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.paths import BASE_DIR

DB_PATH = BASE_DIR / "database" / "retail.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"

# Ensure database folder exists
DB_PATH.parent.mkdir(exist_ok=True)

# Create database and load schema
conn = sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema_sql = f.read()

conn.executescript(schema_sql)
conn.commit()
conn.close()

print("SQLite database created successfully.")
