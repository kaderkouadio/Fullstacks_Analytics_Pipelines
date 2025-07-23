#######################################
# ✅  # Transform_data.py
######################################
import sqlite3
import pandas as pd
import logging
import io
from datetime import datetime
from pathlib import Path

# 📁 Configuration
DB_PATH = "Data/taxi.db"
TRANSFORMED_TABLE = "cleaned_taxi"
LOG_FILE = "logs/transform_log.txt"
Path("logs").mkdir(exist_ok=True)

# 🔧 Configuration du logging
log_stream = io.StringIO()
logging.basicConfig(stream=log_stream, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def transform_data():
    """Transforme les données de la table taxi vers cleaned_taxi dans SQLite."""
    try:
        logging.info("🚀 Début de la transformation des données...")

        conn = sqlite3.connect(DB_PATH)

        # Requête de transformation locale
        query = f"""
        CREATE TABLE IF NOT EXISTS {TRANSFORMED_TABLE} AS
        SELECT *
        FROM taxi
        WHERE passenger_count > 0
          AND trip_distance > 0
          AND payment_type != 6
          AND total_amount > 0
        """

        conn.execute(f"DROP TABLE IF EXISTS {TRANSFORMED_TABLE}")
        conn.execute(query)
        conn.commit()

        # Vérification du résultat
        count = pd.read_sql(f"SELECT COUNT(*) AS total FROM {TRANSFORMED_TABLE}", conn)["total"][0]
        logging.info(f"✅ Transformation terminée : {count} lignes dans `{TRANSFORMED_TABLE}`.")

        conn.close()

    except Exception as e:
        logging.error(f"❌ Échec de la transformation : {e}")
    finally:
        # Enregistre le log localement
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(log_stream.getvalue())
        logging.info(f"📝 Log enregistré dans {LOG_FILE}")


if __name__ == "__main__":
    transform_data()
