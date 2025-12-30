import sys
import sqlite3
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.paths import BASE_DIR
DB_PATH = BASE_DIR / "database" / "retail.db"
SQL_PATH = BASE_DIR / "sql" / "analysis.sql"

# Connecter à la base SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Lire le fichier SQL
with open(SQL_PATH, "r", encoding="utf-8") as f:
    sql_script = f.read()

# Attention : ici on exécute toutes les requêtes séparément
queries = [q.strip() for q in sql_script.split(";") if q.strip()]

for i, query in enumerate(queries, 1):
    print(f"\n--- Requête {i} ---\n{query}\n")
    try:
        cursor.execute(query)
        # Si la requête retourne des résultats, les afficher
        rows = cursor.fetchall()
        if rows:
            for row in rows[:10]:  # Affiche les 10 premières lignes
                print(row)
    except Exception as e:
        print(f"Erreur : {e}")

conn.close()