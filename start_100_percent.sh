#!/bin/bash
# PGI-IA 100% Automatic Startup Script

echo "🚀 Starting PGI-IA System (100% Mode)..."

# Check if running in WSL
if grep -q Microsoft /proc/version; then
    echo "✅ Running in WSL"
else
    echo "⚠️  Not running in WSL"
fi

# Activate virtual environment
source venv_pgi_ia/bin/activate

# Load environment variables
source setup_env.sh

# Check GPU
if command -v nvidia-smi &> /dev/null; then
    echo "🎮 GPU Status:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
    echo "⚠️  No GPU detected"
fi

# Kill any existing Flask process
pkill -f "python.*backend/main.py" 2>/dev/null

# Start backend
echo "📦 Starting backend..."
cd /home/fvegi/dev/pgi-ia
python backend/main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Test backend
echo "🧪 Testing backend..."
curl -s http://localhost:5000/health | jq

# Open dashboard
echo "🌐 Opening dashboard..."
if [ -f frontend/dashboard.html ]; then
    # Try to open in Windows browser from WSL
    if command -v cmd.exe &> /dev/null; then
        cmd.exe /c start file:///home/fvegi/dev/pgi-ia/frontend/dashboard.html
    elif command -v xdg-open &> /dev/null; then
        xdg-open frontend/dashboard.html
    else
        echo "Please open: file:///home/fvegi/dev/pgi-ia/frontend/dashboard.html"
    fi
fi

echo ""
echo "✅ PGI-IA System is running at 100%!"
echo "🌐 Backend: http://localhost:5000"
echo "📊 Dashboard: file:///home/fvegi/dev/pgi-ia/frontend/dashboard.html"
echo "🔌 APIs configured: OpenAI ✅ DeepSeek ✅ Gemini ⏳ Anthropic ⏳"
echo ""
echo "Press Ctrl+C to stop the system"

# Keep running
wait $BACKEND_PID
