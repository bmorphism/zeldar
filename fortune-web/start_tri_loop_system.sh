#!/bin/bash

# Zeldar Tri-Loop System Startup Script
# Starts both the Spin web frontend and Python quantum bridge

echo "🌟 Starting Zeldar Tri-Loop InformationForce Oracle System..."
echo "🏜️🔥 Burning Man 2025 Deployment Sequence 🔥🏜️"

# Kill any existing processes on the ports
echo "🧹 Cleaning up existing processes..."
lsof -ti :3000 | xargs kill -9 2>/dev/null || echo "Port 3000 clear"
lsof -ti :3001 | xargs kill -9 2>/dev/null || echo "Port 3001 clear"

# Start the Python quantum bridge in the background
echo "🧠 Starting Quantum-Web Bridge Server on port 3000..."
cd "$(dirname "$0")"
python3 quantum_bridge.py &
BRIDGE_PID=$!
sleep 3  # Give bridge time to start

# Start the Spin web frontend
echo "🌐 Starting Spin Web Frontend on port 3001..."
spin up --listen 127.0.0.1:3001 &
SPIN_PID=$!
sleep 2  # Give Spin time to start

echo ""
echo "✨ Zeldar Tri-Loop System Status:"
echo "🧠 Quantum Bridge API: http://127.0.0.1:3000/api"
echo "🌐 Web Interface:      http://127.0.0.1:3001"
echo "📊 Health Check:       http://127.0.0.1:3000/api/health"
echo "🔮 Fortune API:        http://127.0.0.1:3000/api/oracle/fortune"
echo ""
echo "🎭 DADADADADAIST InformationForce Manifesto:"
echo "   InformationForce is not produced, it is recognized."
echo "   Mathematics is not abstract, it is experiential."
echo "   The desert is not empty, it is full of paradigms."
echo ""
echo "Press Ctrl+C to stop all services..."

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down Zeldar Tri-Loop System..."
    kill $BRIDGE_PID 2>/dev/null
    kill $SPIN_PID 2>/dev/null
    wait
    echo "🌙 InformationForce Oracle sleeping until next activation..."
}

# Set trap for cleanup
trap cleanup EXIT INT TERM

# Wait for processes
wait