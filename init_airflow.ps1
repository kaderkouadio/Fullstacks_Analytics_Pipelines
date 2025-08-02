<#
.SYNOPSIS
Initialise l'environnement Apache Airflow avec Docker Compose.

.DESCRIPTION
Ce script PowerShell :
1. Vérifie la présence de Docker et du fichier docker-compose.yml
2. Démarre les services définis (webserver, scheduler)
3. Attend leur démarrage
4. Crée un utilisateur admin pour accéder à l'interface Airflow

.AUTEUR
Kader Kouadio
#>

# ------------------- CONFIGURATION -------------------

# Dossier du projet (chemin courant)
$projectPath = Get-Location

# Nom du fichier Docker Compose attendu
$dockerComposeFile = "$projectPath\docker-compose.yml"

# Informations utilisateur admin
$adminUser = "admin"
$adminPass = "admin"
$adminEmail = "kkaderkouadio@gmail.com"
$adminFirstname = "Kader"
$adminLastname = "Kouadio"

# ------------------- ÉTAPE 0 : Vérification de Docker -------------------

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker n'est pas installé ou n'est pas accessible depuis PowerShell." -ForegroundColor Red
    exit 1
}

# ------------------- ÉTAPE 1 : Vérification du fichier docker-compose -------------------

if (-Not (Test-Path $dockerComposeFile)) {
    Write-Host "❌ Fichier docker-compose.yml introuvable dans le dossier courant !" -ForegroundColor Red
    exit 1
}

# ------------------- ÉTAPE 2 : Lancement des services Airflow -------------------

Write-Host "`n[1/4] 🚀 Lancement de Docker Compose..." -ForegroundColor Cyan
docker-compose up -d

# ------------------- ÉTAPE 3 : Pause pour laisser le temps aux conteneurs de démarrer -------------------

Write-Host "`n[2/4] ⏳ Attente du démarrage des containers (10 secondes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# ------------------- ÉTAPE 4 : Création de l'utilisateur admin -------------------

Write-Host "`n[3/4] 👤 Création de l'utilisateur admin..." -ForegroundColor Cyan

docker-compose run --rm airflow-webserver airflow users create `
  --username $adminUser `
  --firstname $adminFirstname `
  --lastname $adminLastname `
  --role Admin `
  --email $adminEmail `
  --password $adminPass

Write-Host "`n[4/4] ✅ Utilisateur créé (ou déjà existant)." -ForegroundColor Green

# ------------------- INFOS SUPPLÉMENTAIRES -------------------

Write-Host "`n🎉 Airflow est prêt ! Accédez à l'interface web sur : http://localhost:8080" -ForegroundColor Green

Write-Host "`n🧾 Identifiants de connexion :" -ForegroundColor Cyan
Write-Host "   ➤ Utilisateur : $adminUser"
Write-Host "   ➤ Mot de passe : $adminPass"

Write-Host "`n📋 Pour consulter les logs en temps réel : docker-compose logs -f" -ForegroundColor DarkGray
