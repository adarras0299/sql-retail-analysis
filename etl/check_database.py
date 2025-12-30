import sqlite3
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.paths import BASE_DIR

DB_PATH = BASE_DIR / "database" / "retail.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Liste des tables
print("=== Tables ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
for table in tables:
    print(table[0])

print("\n")

# Schéma de chaque table
for table_name, in tables:
    print(f"=== Schema for {table_name} ===")
    cursor.execute(f"PRAGMA table_info({table_name})")
    for col in cursor.fetchall():
        print(col)
    print("\n")

conn.close()