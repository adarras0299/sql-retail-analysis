from pathlib import Path

# Racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent


DATA_RAW = BASE_DIR / "data_raw"
DATA_CLEAN = BASE_DIR / "data_clean"
ETL_DIR = BASE_DIR / "etl"