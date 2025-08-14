#######################################
# ✅ Machine_learning_dataset.py
#######################################

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import logging
import sys

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

# --------------------
# 📁 Chemins et dossiers
# --------------------
LOCAL_FOLDER = "logs/Machine_Learning"
PARQUET_FOLDER = "logs/Parquet_dir"
os.makedirs(LOCAL_FOLDER, exist_ok=True)
os.makedirs(PARQUET_FOLDER, exist_ok=True)

DB_PATH = "Data/taxi.db"
TABLE_NAME = "ml_dataset"
TARGET = "total_amount"

# --------------------
# 📜 Configuration du logging
# --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOCAL_FOLDER, "ML_pipeline.log"), mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

# --------------------
# 📥 Chargement des données avec limite et filtre
# --------------------
def load_data(limit=1000000, filters=None):
    logging.info(f"Tentative de connexion à la base SQLite : {DB_PATH}")
    if not os.path.exists(DB_PATH):
        logging.error(f"Fichier de base de données introuvable : {DB_PATH}")
        sys.exit(1)

    try:
        conn = sqlite3.connect(DB_PATH)
        logging.info(f"Connexion établie. Lecture de la table '{TABLE_NAME}'...")

        if filters is None:
            filters = "payment_type IN (1,2) AND tpep_pickup_datetime >= '2023-01-01'"

        query = f"SELECT * FROM {TABLE_NAME} WHERE {filters} LIMIT {limit}"
        df = pd.read_sql(query, conn)
        conn.close()
        logging.info(f"✅ Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")
        return df
    except sqlite3.Error as e:
        logging.exception(f"Erreur SQLite : {e}")
        sys.exit(1)

# --------------------
# 🧼 Nettoyage des données
# --------------------
def clean_data(df):
    logging.info("Nettoyage des données...")
    init_shape = df.shape
    df = df.dropna(how="all")

    for col in ['tpep_pickup_datetime', 'tpep_dropoff_datetime']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    if 'payment_type' in df.columns and np.issubdtype(df['payment_type'].dtype, np.number):
        df['payment_type'] = df['payment_type'].map({1: "Credit_Card", 2: "Cash"})

    df = df.dropna()
    logging.info(f"✅ Nettoyage terminé : {init_shape} → {df.shape}")
    return df

# --------------------
# 📊 Analyse exploratoire optimisée avec Parquet
# --------------------
def explore_data(df):
    logging.info("Exploration rapide des données...")

    parquet_path = os.path.join(PARQUET_FOLDER, "dataset.parquet")
    df.to_parquet(parquet_path, index=False)
    logging.info(f"💾 Dataset sauvegardé au format Parquet : {parquet_path}")

    df_fast = pd.read_parquet(parquet_path)
    logging.info("\n" + str(df_fast.describe()))

    corr = df_fast.corr(numeric_only=True)
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    heatmap_path = os.path.join(LOCAL_FOLDER, "correlation_matrix.png")
    plt.savefig(heatmap_path)
    plt.close()
    logging.info(f"📊 Heatmap sauvegardé : {heatmap_path}")

# --------------------
# 📊 Évaluation
# --------------------
def evaluate(y_true, y_pred, name):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    logging.info(f"\n📈 {name} - MAE: {mae:.4f}, MSE: {mse:.4f}, RMSE: {rmse:.4f}, R²: {r2:.4f}")
    return r2

# --------------------
# 🚀 Pipeline principal
# --------------------
if __name__ == "__main__":
    logging.info("===== DÉBUT DU PIPELINE =====")

    df = load_data(limit=1000000)
    df = clean_data(df)
    explore_data(df)

    FEATURES = ['passenger_count', 'trip_distance', 'fare_amount', 'extra',
                'mta_tax', 'tip_amount', 'tolls_amount', 'payment_type']

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    logging.info(f"Split : {X_train.shape} train / {X_test.shape} test")

    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()

    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ])

    models = {
        "Linear": LinearRegression(),
        "RandomForest": RandomForestRegressor(random_state=42),
        "KNN": KNeighborsRegressor(),
        "XGBoost": XGBRegressor(objective="reg:squarederror", random_state=42),
        "CatBoost": CatBoostRegressor(verbose=0, random_state=42)
    }

    best_model = None
    best_score = -np.inf
    best_model_name = None

    for name, model in models.items():
        logging.info(f"=== Entraînement du modèle {name} ===")
        pipeline = Pipeline([("preprocessor", preprocessor), ("model", model)])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        score = evaluate(y_test, y_pred, name)

        if score > best_score:
            best_model = pipeline
            best_score = score
            best_model_name = name

    os.makedirs("Machine_Learning", exist_ok=True)
    model_path = f"Machine_Learning/best_model_{best_model_name}.joblib"
    joblib.dump(best_model, model_path)
    logging.info(f"✅ Meilleur modèle : {best_model_name} (R²={best_score:.4f}) sauvegardé dans {model_path}")

    logging.info("===== FIN DU PIPELINE =====")
