# Script PowerShell pour démarrer PGI-IA avec Docker
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " DEMARRAGE PGI-IA AVEC DOCKER WINDOWS" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Aller dans le bon dossier
Set-Location C:\Users\fvegi\dev\pgi-ia

# Utiliser le Dockerfile minimal
Write-Host "[1] Construction de l'image Docker..." -ForegroundColor Yellow
docker build -f Dockerfile.minimal -t pgi-ia-backend .

Write-Host ""
Write-Host "[2] Démarrage du backend..." -ForegroundColor Yellow
docker run -d `
    --name pgi-ia-backend `
    -p 5000:5000 `
    -e DEEPSEEK_API_KEY=sk-ccc37a109afb461989af8cf994a8bc60 `
    -v ${PWD}/backend:/app/backend `
    -v ${PWD}/frontend:/app/frontend `
    pgi-ia-backend

Write-Host ""
Write-Host "[3] Démarrage du frontend avec Python simple..." -ForegroundColor Yellow
Start-Process python -ArgumentList "-m", "http.server", "8000", "--directory", "frontend"

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host " SERVICES DISPONIBLES:" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host " - Backend API: http://localhost:5000" -ForegroundColor White
Write-Host " - Frontend: http://localhost:8000/dashboard.html" -ForegroundColor White
Write-Host " - Health: http://localhost:5000/health" -ForegroundColor White
Write-Host ""
Write-Host "Pour arrêter: docker stop pgi-ia-backend && docker rm pgi-ia-backend" -ForegroundColor Gray
Write-Host ""
Write-Host "Appuyez sur une touche pour continuer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")