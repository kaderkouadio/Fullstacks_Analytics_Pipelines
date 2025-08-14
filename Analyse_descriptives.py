#######################################
# ✅ Analyse_descriptives.py
#######################################

# 📦 Imports
import sqlite3
import pandas as pd
import plotly.express as px
from pathlib import Path
import os
import logging
import io
from datetime import datetime
import sys
from io import StringIO

# --------------------
# 📌 Configuration
# --------------------
BASE_DIR = Path(os.getcwd()).resolve()
RAW_FOLDER = BASE_DIR / "Data" / "raw"
DB_PATH = BASE_DIR / "Data" / "taxi.db"
CACHE_DIR = BASE_DIR / "Data" / "cache"
LOG_DIR = BASE_DIR / "logs"

CACHE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

TRANSFORMED_TABLE = "cleaned_taxi"

# ======================
# 🔹 Configuration du logging avec capture en mémoire
# ======================
log_stream = StringIO()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.StreamHandler(log_stream)
    ]
)

# 🔹 Capture des exceptions non interceptées
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("💥 Exception non gérée", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

# ======================
# 1️⃣ Chargement des Parquet
# ======================
EXPECTED_COLUMNS = [
    "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count",
    "trip_distance", "RatecodeID", "store_and_fwd_flag", "PULocationID", "DOLocationID",
    "payment_type", "fare_amount", "extra", "mta_tax", "tip_amount", "tolls_amount",
    "improvement_surcharge", "total_amount", "congestion_surcharge", "Airport_fee"
]

def init_sqlite():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS taxi (
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

def load_parquets():
    logging.info("📦 Début chargement Parquet")
    conn = init_sqlite()
    loaded_files = pd.read_sql(f"SELECT DISTINCT source_file FROM taxi", conn)["source_file"].tolist()
    loaded_files = set(loaded_files)

    for file_path in RAW_FOLDER.glob("*.parquet"):
        if file_path.name in loaded_files:
            logging.info(f"{file_path.name} déjà chargé, skip.")
            continue
        try:
            df = pd.read_parquet(file_path, engine="pyarrow")
            df = df[[c for c in df.columns if c in EXPECTED_COLUMNS]]
            # Cast types
            for col in ["tpep_pickup_datetime", "tpep_dropoff_datetime", "store_and_fwd_flag"]:
                if col in df.columns:
                    df[col] = df[col].astype(str)
            df["source_file"] = file_path.name
            df.to_sql("taxi", conn, if_exists="append", index=False)
            logging.info(f"{file_path.name} chargé avec succès ({len(df)} lignes).")
        except Exception as e:
            logging.error(f"Erreur lors du chargement de {file_path.name}: {e}")
    conn.close()
    logging.info("📦 Fin chargement Parquet")

# ======================
# 2️⃣ Transformation
# ======================
def transform_data():
    logging.info("🔄 Début transformation des données")
    conn = sqlite3.connect(DB_PATH)
    conn.execute(f"DROP TABLE IF EXISTS {TRANSFORMED_TABLE}")
    query = f"""
        CREATE TABLE {TRANSFORMED_TABLE} AS
        SELECT *
        FROM taxi
        WHERE passenger_count > 0
          AND trip_distance > 0
          AND payment_type != 6
          AND total_amount > 0
    """
    conn.execute(query)
    conn.commit()
    count = pd.read_sql(f"SELECT COUNT(*) AS total FROM {TRANSFORMED_TABLE}", conn)["total"][0]
    logging.info(f"✅ Transformation terminée : {count} lignes dans {TRANSFORMED_TABLE}.")
    conn.close()

# ======================
# 3️⃣ Création des vues SQL
# ======================
def create_views():
    logging.info("📌 Création des vues SQL")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Vérifie existence de la table
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{TRANSFORMED_TABLE}';")
    if cursor.fetchone() is None:
        raise RuntimeError(f"La table `{TRANSFORMED_TABLE}` n'existe pas. Exécute transform_data() avant.")

    queries = [
        f"""
        CREATE VIEW IF NOT EXISTS monthly_summary AS
        SELECT substr(tpep_pickup_datetime,1,7) AS year_month,
               COUNT(*) AS trips_count,
               AVG(trip_distance) AS avg_trip_distance,
               AVG(fare_amount) AS avg_fare_amount,
               AVG(tip_amount) AS avg_tip_amount,
               SUM(total_amount) AS total_amount_sum
        FROM {TRANSFORMED_TABLE}
        GROUP BY year_month
        """,
        f"""
        CREATE VIEW IF NOT EXISTS passenger_count_distribution AS
        SELECT passenger_count, COUNT(*) AS count
        FROM {TRANSFORMED_TABLE}
        GROUP BY passenger_count
        ORDER BY passenger_count
        """,
        f"""
        CREATE VIEW IF NOT EXISTS payment_type_summary AS
        SELECT payment_type, COUNT(*) AS count, AVG(total_amount) AS avg_amount
        FROM {TRANSFORMED_TABLE}
        GROUP BY payment_type
        """
    ]
    for q in queries:
        cursor.execute(q)
    conn.commit()
    conn.close()
    logging.info("✅ Vues SQL créées avec succès.")

# ======================
# 4️⃣ Gestion cache Parquet
# ======================
def fetch_view(view_name: str, use_cache=True, force_cache=False) -> pd.DataFrame:
    cache_file = CACHE_DIR / f"{view_name}.parquet"
    if use_cache and cache_file.exists() and not force_cache:
        logging.info(f"📥 Lecture depuis cache : {cache_file.name}")
        return pd.read_parquet(cache_file)
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {view_name}", conn)
    df.to_parquet(cache_file, index=False)
    logging.info(f"📤 Cache mis à jour : {cache_file.name}")
    return df

def save_parquet(df: pd.DataFrame, filename: str):
    path = CACHE_DIR / filename
    df.to_parquet(path, index=False)
    logging.info(f"📁 Fichier sauvegardé : {path}")

# ======================
# 5️⃣ Analyse exploratoire
# ======================
def exploratory_analysis():
    logging.info("📊 Début analyse exploratoire")

    # Résumé mensuel
    monthly = fetch_view("monthly_summary")
    fig1 = px.line(monthly, x="year_month", y=["trips_count", "total_amount_sum"],
                   title="📆 Trajets & Montants par Mois", markers=True)
    fig1.show()
    save_parquet(monthly, "monthly_summary.parquet")

    # Distribution passagers
    passengers = fetch_view("passenger_count_distribution")
    fig2 = px.bar(passengers, x="passenger_count", y="count",
                  title="🧍 Distribution du nombre de passagers")
    fig2.show()
    save_parquet(passengers, "passenger_count_distribution.parquet")

    # Montant moyen par type paiement
    payments = fetch_view("payment_type_summary")
    fig3 = px.bar(payments, x="payment_type", y="avg_amount",
                  title="💳 Montant moyen par type de paiement")
    fig3.show()
    save_parquet(payments, "payment_type_summary.parquet")

    logging.info("📊 Analyse exploratoire terminée")

# ======================
# 🚀 Exécution du pipeline
# ======================
if __name__ == "__main__":
    logging.info("🚀 Début pipeline ELT + Analyse...")

    try:
        load_parquets()
        transform_data()
        create_views()
        exploratory_analysis()
        logging.info("✅ Pipeline terminé avec succès.")
    except Exception as e:
        logging.exception("💥 Erreur lors de l'exécution du pipeline")

    # 🔹 Sauvegarde du log
    log_file = LOG_DIR / f"pipeline_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(log_stream.getvalue())
    print(f"📝 Log sauvegardé dans : {log_file}")
