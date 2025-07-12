#!/bin/bash
# PGI-IA Master Startup Script
# Starts everything automatically

echo "🚀 Starting PGI-IA System..."

# Activate virtual environment
source venv_pgi_ia/bin/activate

# Load environment variables
source setup_env.sh

# Start all services
echo "📦 Starting backend services..."
python orchestrate_pgi_ia.py

echo "🌐 Opening dashboard..."
if command -v xdg-open &> /dev/null; then
    xdg-open frontend/dashboard.html
elif command -v open &> /dev/null; then
    open frontend/dashboard.html
else
    echo "Please open frontend/dashboard.html in your browser"
fi

echo "✅ PGI-IA is ready!"
echo "Backend: http://localhost:5000"
echo "Dashboard: file://$(pwd)/frontend/dashboard.html"
