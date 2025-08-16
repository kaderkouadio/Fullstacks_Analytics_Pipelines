# Fullstacks_Analytics_Pipelines
**Contexte du depot 1** : 
## 📌 Contexte

Le dépôt 1 de **Fullstacks_Analytics_Pipelines** correspond à la première étape de mise en place d’un **pipeline ELT** (Extract – Load – Transform) automatisé pour la collecte, le stockage et la préparation de données destinées à des analyses avancées et à l’entraînement de modèles de Machine Learning.

L’objectif principal de ce dépôt est de créer une **infrastructure fonctionnelle et reproductible** permettant :
- D’extraire les données brutes depuis des sources définies (API, fichiers plats, bases de données…)
- De charger ces données dans un entrepôt (Data Warehouse / Data Lake)
- D’effectuer les transformations nécessaires pour les rendre exploitables par les outils d’analyse et de modélisation

Cette étape est cruciale car elle pose les **fondations techniques** de tout le projet **Fullstacks_Analytics_Pipelines**, garantissant la fiabilité, la qualité et la disponibilité des données pour les dépôts suivants (analyses, visualisations, et prédictions).
---

## 🎯 Objectifs du Dépôt 1

1. **Mettre en place l’environnement technique**
   - Initialisation du projet avec la structure de répertoires et les dépendances requises
   - Configuration d’Airflow pour l’orchestration des tâches ELT
   - Définition des paramètres de connexion aux différentes sources et destinations de données

2. **Développer et exécuter un pipeline ELT complet**
   - **Extraction** : récupération des données brutes depuis la source
   - **Chargement** : insertion des données brutes dans la couche de stockage
   - **Transformation** : nettoyage, formatage et enrichissement des données

3. **Garantir la traçabilité et la reproductibilité**
   - Suivi des exécutions
   - Journalisation des erreurs
   - Versionnage du code
---
# - Phase 1 : Pipeline ELT + Airflow DAGs

Bienvenue dans la **Phase 1** de **Fullstacks_Analytics_Pipelines**, une solution analytique interactive pour explorer et visualiser les données taxis et limousines de la ville de New York (TLC) du jeu **Taxi & Limousine Commission(TLC)**. 
Ce partie contient l’implémentation complète de la première étape du projet, incluant :
- La construction d’un **pipeline ELT** automatisé(DAGs Airflow pour l’automatisation) pour l’ingestion, le nettoyage et la transformation des données.
- L’orchestration avec **Docker Compose Airflow** pour planifier et superviser les tâches.
- Le développement, l’entraînement et l’évaluation d’un **modèle de machine learning** pour la prédiction (classification).

Cette phase , une solution backend robuste conçue pour transformer l'expérience des données du jeu **Taxi & Limousine Commission**, constitue le socle technique sur lequel s’appuie la suite du projet, notamment l’intégration dans une application **Streamlit** pour la prédiction.

## Aperçu de la Phase 2 : Développement et Entraînement du Modèle

**Objectif** : Explorer les données TLC via le Pipeline développée en Phase 1 et présenter des insights exploitables à travers une application web interactive pour les scientifiques, analystes, et studios.

- **Extraction, transformation et chargement des données (scripts ELT)** :
  - Processus ELT pour extraire les fichiers parquets depuis le site: https://www.nyc.gov/site/tlc/about/about-tlc.page
  - DAGs Airflow pour automatiser le pipeline.
- **Visualisation Interactive** :
  - Créer des graphiques dynamiques avec **Plotly** pour illustrer les insights.
  - Crée les vues SQL
  - Exporte les Parquet pour le cache
  - Développer une application **Streamlit** avec des tableaux dynamiques et une recherche avancée.

- **Développement et Entraînement du Modèle** :
  - script d’exploration et de feature engineering..
  - Script d’entraînement du modèle.
  - Sauvegarde du modèle (.pkl ou .joblib).
  - Évaluation du modèle (MAE, MSE, RMSE, R²…).
  - Scripts pour charger un modèle et faire une prédiction.

### 🛠 Fonctionnalités principales

- **Pipeline ELT automatisé avec Airflow** :
  -Extraction des données TLC depuis CSV ou Parquet.
  -Transformation et nettoyage.
  -Chargement des données traitées dans data/processed/.

- **Exploration et visualisation** :
  -Analyse rapide avec Parquet pour réduire le temps de chargement.
  -Heatmaps de corrélation et statistiques descriptives.

- **Modélisation ML** :
 -Modèles : Linear Regression, RandomForest, KNN, XGBoost, CatBoost.
 -Prétraitement automatique : imputation, scaling, encodage.
 -Sélection du meilleur modèle selon R².
 -Logs détaillés pour suivre l’exécution et les métriques.
 -Export du modèle entraîné pour utilisation dans le Dépôt 2 (Streamlit).

### 📦 Livrables**
À l’issue de ce dépôt 1, les livrables attendus sont :
- **1.Pipeline ELT opérationnel**
  -DAG Airflow fonctionnel avec tâches ordonnancées
  -Scripts d’extraction, chargement et transformation validés
- **2.Base de données alimentée**
  -Données brutes disponibles dans la couche de stockage
  -Données transformées prêtes pour exploitation
- **3.Documentation technique**
  -README détaillant l’architecture, les technologies, la procédure d’installation et d’exécution
  -Schéma du pipeline ELT
- **4.Fichiers de configuration**
  -Paramétrage des connexions et variables d’environnement
  -Instructions pour adapter le pipeline à d’autres sources/destinations

## Structure du Projet


## Technologies Utilisées

### 🚀Technologies utilisées
- **Langage** : Python 3.x
- **Orchestration** : Apache Airflow
- **Stockage** : SQLite  
- **ETL/ELT** : Pandas, SQLAlchemy
- **Gestion des dépendances** : pip et requirements.txt
- **Versionnage** : Git / GitHub
- **Docker** : Conteneurisation pour déploiements locaux.
- **Docker compose**
---
## Mise en Place de l’Environnement

### Prérequis
- Python 3.11+
- VSCode (recommandé)
- Git
- Compte GitHub pour le contrôle de version
- Compte Render (pour déploiement cloud, gratuit)

### Étapes d’Installation

1. **Cloner le Répertoire**
   ```bash
   git clone https://github.com/kaderkouadio/Fullstacks_Analytics_Pipelines
   cd Fullstacks_Analytics_Pipelines
   ```

2. **Créer et Activer un Environnement Virtuel**
   ```bash
   python3 -m venv .venv
   .\venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

3. **Ouvrir dans VSCode**
   ```bash
   code .
   ```
   Sélectionnez l’interpréteur Python du `.venv` si demandé.

4. **Installer les Dépendances**
   Assurez-vous que `requirements.txt` contient :
   ```text
   pandas
   plotly
   streamlit
   requests
   python-dotenv
   ```
   Installez :
   ```bash
   pip install requirements.txt
   ```
   ```
---
## Déploiement

### github
1. Poussez `Fullstacks_Analytics_Pipelines` dans un répertoire GitHub.
2. Créez un service Web sur Render :
   - Langage : `Python 3`
   - Commande de Build : `pip install -r requirements.txt`
   - Instance Type : `Free`
3. Ajoutez les variables d’environnement :

---

### 🔍 Points clés de l’architecture

- **Séparation claire des étapes du pipeline** :  
  Les DAGs Airflow orchestrent les scripts Python situés dans `scripts/`.
- **Gestion optimisée des données** :  
  Fichiers bruts → traités → cache Parquet pour optimiser les EDA et la modélisation.
- **Suivi complet par logs** :  
  Chaque étape est tracée dans `logs/` avec horodatage et niveau de détail.
- **Compatibilité ML et déploiement** :  
  Les modèles entraînés dans `models/` sont prêts à être intégrés à l’application Streamlit du **Dépôt 2**.
---

## 🚀 Pourquoi Ce Projet Se Démarque
Ce projet illustre ma capacité à mettre en place une chaîne de traitement de données **de bout en bout** allant de l’extraction à la mise à disposition d’un modèle prêt pour la prédiction :  

- **Expertise Technique** : Maîtrise d’Airflow pour l’orchestration, Pandas pour la transformation de données, SQL pour la création de vues, et scikit-learn / XGBoost / CatBoost pour la modélisation.  
- **Pipeline ELT Professionnel** : Automatisation complète du chargement, nettoyage, transformation et stockage des données dans une base SQLite optimisée.  
- **Modélisation Avancée** : Entraînement, évaluation et sélection du meilleur modèle sur un dataset structuré, prêt pour intégration dans une application de prédiction.  
- **Professionnalisme** : Code structuré, journalisation (logs) complète, scripts modulaires et reproductibles, livrables exploitables pour déploiement.

---

## 🔮 Améliorations Futures
- **Connexion à un Data Warehouse** : Migrer vers PostgreSQL, BigQuery ou Snowflake pour plus de scalabilité.  
- **Automatisation CI/CD** : Déploiement automatisé des DAGs et des modèles via GitHub Actions ou GitLab CI.  
- **Surveillance du Modèle** : Implémenter du monitoring (drift de données, performances en production).  
- **Optimisation des Performances** : Utilisation de formats de stockage haute performance (ex. : Delta Lake, Parquet partitionné) et cache Redis.  
- **Extension des Modèles** : Tester des modèles de deep learning pour améliorer la précision prédictive.
---

## 📬 Contact

Pour toute question ou collaboration, n’hésitez pas à me contacter :

**Kader KOUADIO**  
- **LinkedIn** :👨‍💻[Koukou Kader Kouadio](https://www.linkedin.com/in/koukou-kader-kouadio-2a32371a4/)
- **Email** :📧 [kkaderkouadio@gmail.com](mailto:kkaderkouadio@gmail.com)

---