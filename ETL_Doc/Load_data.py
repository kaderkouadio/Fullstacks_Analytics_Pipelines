#######################################
# ✅  # Load_data.py
######################################
import os
import sqlite3
import pandas as pd
import logging
import io
from datetime import datetime
from pathlib import Path

# CONFIGURATION
LOCAL_FOLDER = "Data/raw"
DB_PATH = "Data/taxi.db"
TABLE_NAME = "taxi"

# Logging setup
log_stream = io.StringIO()
logging.basicConfig(stream=log_stream, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Colonnes attendues
EXPECTED_COLUMNS = [
    "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count",
    "trip_distance", "RatecodeID", "store_and_fwd_flag", "PULocationID", "DOLocationID",
    "payment_type", "fare_amount", "extra", "mta_tax", "tip_amount", "tolls_amount",
    "improvement_surcharge", "total_amount", "congestion_surcharge", "Airport_fee"
]

def init_sqlite():
    """Crée la base SQLite et la table si nécessaire."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            VendorID INTEGER,
            tpep_pickup_datetime TEXT,
            tpep_dropoff_datetime TEXT,
            passenger_count REAL,
            trip_distance REAL,
            RatecodeID REAL,
            store_and_fwd_flag TEXT,
            PULocationID INTEGER,
            DOLocationID INTEGER,
            payment_type INTEGER,
            fare_amount REAL,
            extra REAL,
            mta_tax REAL,
            tip_amount REAL,
            tolls_amount REAL,
            improvement_surcharge REAL,
            total_amount REAL,
            congestion_surcharge REAL,
            Airport_fee REAL,
            source_file TEXT
        )
    ''')
    conn.commit()
    return conn

def get_loaded_files(conn):
    """Liste les fichiers déjà chargés dans la base."""
    try:
        df = pd.read_sql(f"SELECT DISTINCT source_file FROM {TABLE_NAME}", conn)
        return set(df["source_file"].tolist())
    except Exception:
        return set()

def load_files_to_sqlite():
    """Charge les fichiers Parquet dans la base SQLite locale."""
    conn = init_sqlite()
    existing_files = get_loaded_files(conn)
    files = Path(LOCAL_FOLDER).glob("*.parquet")

    for file_path in files:
        if file_path.name in existing_files:
            logging.info(f"{file_path.name} déjà chargé, skip.")
            continue

        try:
            df = pd.read_parquet(file_path, engine="pyarrow")
            available_columns = list(set(df.columns) & set(EXPECTED_COLUMNS))
            df = df[available_columns]

            if "tpep_pickup_datetime" in df.columns:
                df["tpep_pickup_datetime"] = df["tpep_pickup_datetime"].astype(str)
            if "tpep_dropoff_datetime" in df.columns:
                df["tpep_dropoff_datetime"] = df["tpep_dropoff_datetime"].astype(str)
            if "store_and_fwd_flag" in df.columns:
                df["store_and_fwd_flag"] = df["store_and_fwd_flag"].astype(str)

            df["source_file"] = file_path.name

            df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
            logging.info(f"{file_path.name} inséré avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors du chargement de {file_path.name}: {str(e)}")

    conn.close()

    # Sauvegarde du log localement
    log_file = f"Data/load_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(log_stream.getvalue())
    logging.info(f"Log sauvegardé dans : {log_file}")

if __name__ == "__main__":
    logging.info("🚀 Début du chargement des fichiers parquet dans SQLite...")
    load_files_to_sqlite()
