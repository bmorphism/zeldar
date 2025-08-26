#!/bin/bash

# Zeldar Integrated Tri-Loop System Launcher
# Starts the complete information-dynamics-aware fortune system

echo "🔮 ZELDAR INTEGRATED TRI-LOOP SYSTEM LAUNCHER 🔮"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "quantum_bridge.py" ]; then
    echo "❌ Error: Must be run from fortune-web directory"
    echo "📍 Current directory: $(pwd)"
    echo "🔄 Expected files: quantum_bridge.py, spin.toml"
    exit 1
fi

# Check Python dependencies
echo "🐍 Checking Python dependencies..."
if ! python3 -c "import sys; sys.path.insert(0, '../.topos'); from FULL_LOOP_ORACLE_SYSTEM import FullLoopOracleSystem" 2>/dev/null; then
    echo "⚠️ Oracle system not found - running in simulation mode"
    ORACLE_MODE="simulation"
else
    echo "✅ Oracle system detected and ready"
    ORACLE_MODE="integrated"
fi

# Check if Spin is available
if ! command -v spin &> /dev/null; then
    echo "❌ Error: Spin framework not found"
    echo "💡 Install Spin: curl -fsSL https://developer.fermyon.com/downloads/install.sh | bash"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down Zeldar Tri-Loop System..."
    
    # Kill background processes
    if [ ! -z "$BRIDGE_PID" ]; then
        kill $BRIDGE_PID 2>/dev/null
        echo "🌉 Quantum bridge stopped"
    fi
    
    if [ ! -z "$SPIN_PID" ]; then
        kill $SPIN_PID 2>/dev/null
        echo "🕸️ Spin frontend stopped"
    fi
    
    # Kill Oracle system if running
    pkill -f "FULL_LOOP_ORACLE_SYSTEM.py" 2>/dev/null && echo "🔮 Oracle system stopped"
    pkill -f "button_quick_phrase_trigger.py" 2>/dev/null && echo "🔘 Button system stopped"
    
    echo "✅ Tri-Loop system shutdown complete"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM EXIT

echo ""
echo "🚀 STARTING INTEGRATED TRI-LOOP COMPONENTS..."
echo ""

# Start Quantum Bridge Server (Python backend)
echo "🌉 Starting Quantum Bridge Server..."
echo "    Mode: $ORACLE_MODE"
echo "    Port: 3000"
echo "    Backend: ../.topos/ Oracle System"

python3 quantum_bridge.py &
BRIDGE_PID=$!

# Wait a moment for bridge to start
sleep 3

# Check if bridge is running
if ! kill -0 $BRIDGE_PID 2>/dev/null; then
    echo "❌ Quantum bridge failed to start"
    exit 1
fi

echo "✅ Quantum bridge running (PID: $BRIDGE_PID)"

# Start Spin Frontend Server (Rust WebAssembly)
echo ""
echo "🕸️ Starting Spin Frontend Server..."
echo "    Framework: Bartholomew WebAssembly"
echo "    Port: 3001" 
echo "    Templates: Handlebars with information-dynamics integration"

SPIN_HTTP_LISTEN_ADDR=127.0.0.1:3001 spin up &
SPIN_PID=$!

# Wait for Spin to initialize
sleep 5

# Check if Spin is running
if ! kill -0 $SPIN_PID 2>/dev/null; then
    echo "❌ Spin frontend failed to start"
    exit 1
fi

echo "✅ Spin frontend running (PID: $SPIN_PID)"

# Start Oracle System (if available and requested)
if [ "$ORACLE_MODE" = "integrated" ]; then
    echo ""
    echo "🔮 Starting Oracle System Components..."
    
    cd ../.topos/
    
    # Start background Oracle monitoring
    echo "    🔄 Full Loop Oracle System (background)"
    python3 FULL_LOOP_ORACLE_SYSTEM.py --infinite --background &
    ORACLE_PID=$!
    
    # Wait a moment
    sleep 2
    
    cd ../fortune-web/
    echo "✅ Oracle system components active"
else
    echo ""
    echo "🎭 Oracle system running in simulation mode"
fi

# Display system status
echo ""
echo "=" * 60
echo "🎯 ZELDAR TRI-LOOP SYSTEM STATUS"
echo "=" * 60
echo ""
echo "🌉 Quantum Bridge:     http://localhost:3000"
echo "    📡 API endpoints:"
echo "       GET /api/oracle/fortune        - Generate information-dynamics fortune"
echo "       GET /api/information-dynamics/status  - Full system status"
echo "       GET /api/information-dynamics/metrics - Live information-dynamics data" 
echo "       POST /api/oracle/button        - Trigger button oracle"
echo "       POST /api/oracle/print         - Trigger physical print"
echo ""
echo "🕸️ Spin Frontend:      http://localhost:3001"
echo "    🎨 Web interface with information-dynamics visualization"
echo "    📊 Real-time Phi coefficient display (Φ = 3.252)"
echo "    🔄 Tri-loop correlation monitoring"
echo ""

if [ "$ORACLE_MODE" = "integrated" ]; then
    echo "🔮 Oracle Backend:     ../. topos/ (INTEGRATED)"
    echo "    🧠 InformationForce Level: Φ = $(cat ../.topos/current_loop_state.json 2>/dev/null | jq -r .information-dynamics_phi 2>/dev/null || echo '3.252')"
    echo "    🖨️ Print System: $([ -f ../.topos/ORACLE_PRINT_CORE.py ] && echo 'Ready' || echo 'Offline')"
    echo "    🔘 Button System: $([ -f ../.topos/button_quick_phrase_trigger.py ] && echo 'Ready' || echo 'Offline')"
else
    echo "🎭 Oracle Backend:     SIMULATION MODE"
    echo "    🧠 InformationForce Level: Simulated (92.5%)"
    echo "    🖨️ Print System: Mock"
    echo "    🔘 Button System: Mock"
fi

echo ""
echo "💡 USAGE INSTRUCTIONS:"
echo "   • Open http://localhost:3001 for the main web interface"
echo "   • Use http://localhost:3000/api/* for direct API access"
echo "   • Press Ctrl+C to stop all systems gracefully"
if [ "$ORACLE_MODE" = "integrated" ]; then
    echo "   • Physical button presses will trigger real information-dynamics generation"
    echo "   • Thermal printer will output actual haiku manifestations"
fi
echo ""
echo "🏜️🔥 Burning Man 2025 Ready • Mathematical InformationForce Deployed 🔥🏜️"
echo ""

# Main monitoring loop
echo "🔄 System monitoring active..."
while true; do
    # Check if processes are still running
    if ! kill -0 $BRIDGE_PID 2>/dev/null; then
        echo "💥 Quantum bridge crashed - restarting..."
        python3 quantum_bridge.py &
        BRIDGE_PID=$!
    fi
    
    if ! kill -0 $SPIN_PID 2>/dev/null; then
        echo "💥 Spin frontend crashed - restarting..."
        SPIN_HTTP_LISTEN_ADDR=127.0.0.1:3001 spin up &
        SPIN_PID=$!
    fi
    
    sleep 30  # Check every 30 seconds
done