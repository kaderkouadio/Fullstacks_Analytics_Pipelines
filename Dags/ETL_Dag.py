#######################################
# ✅  # ETL_Dag.py
######################################

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import calendar

# ========= ⚙️ CONFIGURATION =========
default_args = {
    'owner': 'KOUADIO K. Kader | Économiste, Analyste Financier & Data/BI/IA Developer',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# ========= 🔁 FONCTION pour vérifier le dernier vendredi =========
def check_last_friday(execution_date_str, **kwargs):
    execution_date = datetime.strptime(execution_date_str, "%Y-%m-%d")
    year = execution_date.year
    month = execution_date.month

    # Dernier jour du mois
    last_day = calendar.monthrange(year, month)[1]
    last_friday = max(
        day for day in range(1, last_day + 1)
        if datetime(year, month, day).weekday() == 4  # 4 = vendredi
    )

    if execution_date.day != last_friday:
        raise ValueError(f"Ce n'est pas le dernier vendredi ({last_friday}) du mois.")

# ========= DAG =========

with DAG(
    dag_id="ELT_Pipeline_data_taxi_last_friday",
    default_args=default_args,
    description=(
        "📦 Pipeline Data Engineering pour l'analyse mensuelle des trajets taxi : "
        "automatisation complète du cycle ETL (Extract, Load, Transform) c'est a dire Extraction, Chargement et Transformation des données réelles."
        "exécuté automatiquement chaque dernier vendredi du mois à 23h. "
        "Les données sont nettoyées et sauvegardées pour les analyses ultérieures."
    ),
    schedule_interval="0 23 * * 5", # Tous les vendredis à 23
    catchup=False,
    tags=["ETL", "taxi-data", "mensuel", "cleaning", "local-dev"]
) as dag:

    verify_last_friday = PythonOperator(
        task_id="verify_last_friday",
        python_callable=check_last_friday,
        op_args=["{{ ds }}"],
    )

    Extract_data = BashOperator(
        task_id="Extract_data",
        bash_command="python C:/Users/kkade/Desktop/Fullstacks_Analytics_Pipelines/Dags/Extract_data.py",
    )

    Load_data = BashOperator(
        task_id="Load_data",
        bash_command="python C:/Users/kkade/Desktop/Fullstacks_Analytics_Pipelines/Dags/Load_data.py",
    )

    Transform_data = BashOperator(
        task_id="Transform_data",
        bash_command="python C:/Users/kkade/Desktop/Fullstacks_Analytics_Pipelines/Dags/Transform_data.py",
    )

    # Dépendances
    verify_last_friday >> Extract_data >> Load_data >> Transform_data

