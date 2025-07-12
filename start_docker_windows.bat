@echo off
echo ===================================
echo  DEMARRAGE PGI-IA AVEC DOCKER
echo ===================================
echo.

cd C:\Users\fvegi\dev\pgi-ia

echo [1] Verification Docker...
docker --version

echo.
echo [2] Construction des images...
docker compose build

echo.
echo [3] Demarrage des services...
docker compose up -d

echo.
echo [4] Verification des services...
timeout /t 5 /nobreak > nul
docker compose ps

echo.
echo ===================================
echo  SERVICES DISPONIBLES:
echo ===================================
echo  - Backend API: http://localhost:5000
echo  - Frontend: http://localhost
echo  - Health Check: http://localhost:5000/health
echo.
echo Pour arreter: docker compose down
echo.
pause