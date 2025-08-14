#######################################
# ✅ Machine_learning_dataset.py
#######################################

import sqlite3
import pandas as pd
import logging
import io
import os
from pathlib import Path

# 📁 Configuration
LOCAL_FOLDER = "logs/Machine_Learning"
os.makedirs(LOCAL_FOLDER, exist_ok=True)

DB_PATH = "Data/taxi.db"  # chemin vers ta base SQLite principale
TRANSFORMED_TABLE = "cleaned_taxi"
ML_TABLE = "ml_dataset"  # nom de la table ML dans la DB
LOG_FILE = "logs/ml_dataset_log.txt"
Path("logs").mkdir(exist_ok=True)

# 🔧 Logging
log_stream = io.StringIO()
logging.basicConfig(
    stream=log_stream,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_ml_dataset():
    """
    Crée une table filtrée 'ml_dataset' à partir de 'cleaned_taxi' pour les usages Machine Learning.
    - Courses à partir du 1er janvier 2023
    - Année de la course entre 2023 et aujourd'hui
    - Type de paiement : carte (1) ou espèces (2)
    """
    try:
        logging.info("🚀 Début de la création du dataset pour Machine Learning...")

        conn = sqlite3.connect(DB_PATH)

        # Supprime la table existante
        conn.execute(f"DROP TABLE IF EXISTS {ML_TABLE}")

        # Création de la table filtrée
        query = f"""
        CREATE TABLE {ML_TABLE} AS
        SELECT *
        FROM {TRANSFORMED_TABLE}
        WHERE 
            tpep_pickup_datetime >= '2023-01-01'
            AND CAST(strftime('%Y', tpep_pickup_datetime) AS INTEGER) 
                BETWEEN 2023 AND CAST(strftime('%Y', 'now') AS INTEGER)
            AND payment_type IN (1, 2)
        """
        conn.execute(query)
        conn.commit()

        # Vérification
        count = pd.read_sql(f"SELECT COUNT(*) AS total FROM {ML_TABLE}", conn)["total"][0]
        logging.info(f"✅ Table `{ML_TABLE}` créée avec succès : {count} lignes.")

        conn.close()

    except Exception as e:
        logging.error(f"❌ Échec : {e}")

    finally:
        # Sauvegarde du log
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(log_stream.getvalue())
        logging.info(f"📝 Log enregistré dans {LOG_FILE}")

if __name__ == "__main__":
    create_ml_dataset()
