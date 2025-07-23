#######################################
# ✅  # Extract_data.py
######################################

import requests
import os
import logging
import time
import io
from datetime import datetime

# CONFIGURATION LOCALE UNIQUEMENT
USE_GCS = False  # Doit rester False
LOCAL_FOLDER = "Data/raw"

# Création du dossier local si nécessaire
os.makedirs(LOCAL_FOLDER, exist_ok=True)

# Configuration du logging
log_stream = io.StringIO()
logging.basicConfig(
    stream=log_stream,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def download_histo_data(start_year=2022):
    """Télécharge les fichiers Parquet de Yellow Taxi de start_year à l'année en cours."""
    current_year = datetime.now().year

    try:
        for year in range(start_year, current_year + 1):
            for month in range(1, 13):
                file_name = f"yellow_tripdata_{year}-{month:02d}.parquet"
                local_path = os.path.join(LOCAL_FOLDER, file_name)
                url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}"

                # Skip si fichier déjà présent localement
                if os.path.exists(local_path):
                    logging.info(f"{file_name} déjà téléchargé, skip.")
                    continue

                logging.info(f"Téléchargement de {file_name} depuis {url}...")
                response = requests.get(url, stream=True)

                if response.status_code == 200:
                    with open(local_path, "wb") as f:
                        f.write(response.content)
                    logging.info(f"✅ {file_name} téléchargé avec succès.")
                elif response.status_code == 404:
                    logging.warning(f"❌ {file_name} non trouvé (404).")
                else:
                    logging.error(f"⚠️ Erreur HTTP {response.status_code} pour {file_name}.")

                time.sleep(1)

    except Exception as e:
        logging.error(f"🚨 Erreur inattendue : {str(e)}")

    finally:
        # Écriture du log local
        log_filename = f"download_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_path = os.path.join(LOCAL_FOLDER, log_filename)
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(log_stream.getvalue())
        logging.info(f"📝 Log sauvegardé localement : {log_path}")

if __name__ == "__main__":
    logging.info(f"📥 Démarrage du téléchargement à {datetime.today()}")
    download_histo_data(start_year=2022)
