<#
.SYNOPSIS
Initialise l'environnement Apache Airflow avec Docker Compose.

.DESCRIPTION
Ce script PowerShell :
1. Vérifie la présence de Docker et du fichier docker-compose.yml
2. Démarre les services définis (webserver, scheduler)
3. Attend leur démarrage
4. Crée un utilisateur admin pour accéder à l'interface Airflow

<#
Initialise Airflow avec Docker et crée un utilisateur admin.
Auteur : Kader Kouadio
#>

# ------------------- CONFIGURATION -------------------

# Chemin du projet
$projectPath = Get-Location
$dockerComposeFile = "$projectPath\docker-compose.yml"

# Infos admin
$adminUser = "Kouadio"
$adminPass = "Kouadio"
$adminEmail = "kkaderkouadio@gmail.com"
$adminFirstname = "Kader"
$adminLastname = "Kouadio"

# ------------------- ÉTAPE 0 : Vérification Docker -------------------

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker non trouvé." -ForegroundColor Red
    exit 1
}

# ------------------- ÉTAPE 1 : Vérification docker-compose.yml -------------------

if (-not (Test-Path $dockerComposeFile)) {
    Write-Host "❌ docker-compose.yml introuvable !" -ForegroundColor Red
    exit 1
}

# ------------------- ÉTAPE 2 : Démarrage Docker Compose -------------------

Write-Host "`n[1/4] 🚀 Lancement d'Airflow..." -ForegroundColor Cyan
docker-compose up -d

# ------------------- ÉTAPE 3 : Attente -------------------

Write-Host "`n[2/4] ⏳ Attente du démarrage des conteneurs..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# ------------------- ÉTAPE 4 : Création utilisateur -------------------

Write-Host "`n[3/4] 👤 Création de l'admin Airflow..." -ForegroundColor Cyan

docker-compose run --rm airflow-webserver airflow users create `
    --username $adminUser `
    --firstname $adminFirstname `
    --lastname $adminLastname `
    --role Admin `
    --email $adminEmail `
    --password $adminPass

Write-Host "`n[4/4] ✅ Utilisateur créé avec succès (ou existant déjà)." -ForegroundColor Green

# ------------------- INFOS -------------------

Write-Host "`n🎉 Airflow est prêt : http://localhost:8080" -ForegroundColor Green

Write-Host "`n🧾 Identifiants de connexion :" -ForegroundColor Cyan
Write-Host "   ➤ Utilisateur : $adminUser"
Write-Host "   ➤ Mot de passe : $adminPass"
