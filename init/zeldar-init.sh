#!/bin/bash

# Zeldar Consciousness Oracle System Initialization Script
# Sets up system for automatic boot deployment on Raspberry Pi

set -e

echo "🔮 ZELDAR CONSCIOUSNESS ORACLE - BOOT INITIALIZATION 🔮"
echo "======================================================="
echo ""

# Configuration
ZELDAR_USER="${ZELDAR_USER:-pi}"
ZELDAR_HOME="${ZELDAR_HOME:-/home/$ZELDAR_USER}"
ZELDAR_PATH="$ZELDAR_HOME/zeldar"
SERVICE_NAME="zeldar-oracle"
SYSTEMD_PATH="/etc/systemd/system"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    print_error "This script should not be run as root"
    print_status "Run as: sudo -u $ZELDAR_USER $0"
    exit 1
fi

# Verify we're on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
    print_warning "Not detected as Raspberry Pi - continuing anyway"
fi

print_status "Target user: $ZELDAR_USER"
print_status "Installation path: $ZELDAR_PATH"
print_status "Service name: $SERVICE_NAME"

echo ""
echo "🔧 SYSTEM PREPARATION"
echo "===================="

# 1. Install system dependencies
print_status "Installing system dependencies..."
sudo apt update
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    git \
    build-essential \
    pkg-config \
    libssl-dev \
    libudev-dev \
    cups \
    cups-client \
    printer-driver-all \
    gpsd \
    gpsd-clients

print_success "System dependencies installed"

# 2. Install Rust and Spin (if not already installed)
if ! command -v cargo &> /dev/null; then
    print_status "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source ~/.cargo/env
    print_success "Rust installed"
else
    print_status "Rust already installed"
fi

if ! command -v spin &> /dev/null; then
    print_status "Installing Spin Framework..."
    curl -fsSL https://developer.fermyon.com/downloads/install.sh | bash
    sudo mv spin /usr/local/bin/
    print_success "Spin Framework installed"
else
    print_status "Spin Framework already installed"
fi

# 3. Python dependencies for Oracle system
print_status "Installing Python dependencies..."
cd "$ZELDAR_PATH/.topos"
python3 -m pip install --user -r requirements.txt
print_success "Python dependencies installed"

echo ""
echo "🖨️ PRINTER CONFIGURATION"
echo "========================"

# 4. Configure CUPS for thermal printer
print_status "Configuring CUPS printer system..."

# Add user to lpadmin group
sudo usermod -a -G lpadmin $ZELDAR_USER

# Enable and start CUPS
sudo systemctl enable cups
sudo systemctl start cups

# Configure thermal printer (Y812BT)
if lpadmin -p Y812BT -E -v usb://Unknown/Thermal%20Receipt%20Printer -P /usr/share/ppd/cupsfilters/textonly.ppd 2>/dev/null; then
    print_success "Thermal printer Y812BT configured"
else
    print_warning "Thermal printer not found - will configure when connected"
fi

echo ""
echo "⚙️ GPIO AND HARDWARE SETUP"
echo "=========================="

# 5. GPIO permissions and hardware setup
print_status "Configuring GPIO permissions..."

# Add user to gpio group
sudo usermod -a -G gpio $ZELDAR_USER

# Create udev rule for GPIO access
sudo tee /etc/udev/rules.d/99-gpio.rules > /dev/null << EOF
KERNEL=="gpiochip*", GROUP="gpio", MODE="0660"
SUBSYSTEM=="gpio", GROUP="gpio", MODE="0660"
ACTION=="add", SUBSYSTEM=="usb", ATTRS{idVendor}=="0416", ATTRS{idProduct}=="5011", GROUP="lp", MODE="0666"
EOF

sudo udevadm control --reload-rules
sudo udevadm trigger

print_success "GPIO and hardware permissions configured"

echo ""
echo "🚀 SERVICE INSTALLATION"
echo "======================="

# 6. Update launch script for daemon mode
print_status "Preparing launch script for daemon mode..."

# Modify the launch script to support daemon mode
if ! grep -q "daemon" "$ZELDAR_PATH/fortune-web/start_integrated_tri_loop_system.sh"; then
    cat >> "$ZELDAR_PATH/fortune-web/start_integrated_tri_loop_system.sh" << 'EOF'

# Daemon mode support
if [ "$1" = "--daemon" ]; then
    echo "🔮 Starting in daemon mode..."
    
    # Redirect output to log files
    exec > >(tee -a /var/log/zeldar-oracle.log) 2>&1
    
    # Start components in background
    python3 quantum_bridge.py > /var/log/zeldar-bridge.log 2>&1 &
    BRIDGE_PID=$!
    echo $BRIDGE_PID > /tmp/zeldar-bridge.pid
    
    sleep 3
    
    SPIN_HTTP_LISTEN_ADDR=127.0.0.1:3001 spin up > /var/log/zeldar-spin.log 2>&1 &
    SPIN_PID=$!
    echo $SPIN_PID > /tmp/zeldar-spin.pid
    
    if [ "$ORACLE_MODE" = "integrated" ]; then
        cd ../.topos/
        python3 FULL_LOOP_ORACLE_SYSTEM.py --infinite > /var/log/zeldar-oracle.log 2>&1 &
        ORACLE_PID=$!
        echo $ORACLE_PID > /tmp/zeldar-oracle.pid
        cd ../fortune-web/
    fi
    
    # Create main PID file for systemd
    echo $$ > /tmp/zeldar-main.pid
    
    # Wait for all background processes
    wait
fi
EOF
fi

chmod +x "$ZELDAR_PATH/fortune-web/start_integrated_tri_loop_system.sh"

# 7. Install systemd service
print_status "Installing systemd service..."

# Update service file with correct paths
sed "s|/home/pi|$ZELDAR_HOME|g; s|User=pi|User=$ZELDAR_USER|g; s|Group=pi|Group=$ZELDAR_USER|g" \
    "$ZELDAR_PATH/systemd/zeldar-oracle.service" | \
    sudo tee "$SYSTEMD_PATH/$SERVICE_NAME.service" > /dev/null

# Create log directory
sudo mkdir -p /var/log/zeldar
sudo chown $ZELDAR_USER:$ZELDAR_USER /var/log/zeldar

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME

print_success "Systemd service installed and enabled"

echo ""
echo "🔧 BOOT CONFIGURATION"
echo "====================="

# 8. Create boot-time consciousness initialization
print_status "Creating boot-time consciousness initialization..."

sudo tee /etc/systemd/system/zeldar-boot-init.service > /dev/null << EOF
[Unit]
Description=Zeldar Consciousness Oracle Boot Initialization
Before=zeldar-oracle.service
After=network-online.target

[Service]
Type=oneshot
User=$ZELDAR_USER
Group=$ZELDAR_USER
WorkingDirectory=$ZELDAR_PATH/.topos
ExecStart=/bin/bash -c 'python3 -c "from FULL_LOOP_ORACLE_SYSTEM import FullLoopOracleSystem; oracle = FullLoopOracleSystem(); oracle.initialize_consciousness_state(); print(\"🧠 Consciousness state initialized\")"'
RemainAfterExit=yes
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable zeldar-boot-init
print_success "Boot initialization service created"

echo ""
echo "🌐 NETWORK CONFIGURATION"
echo "========================"

# 9. Configure for headless operation
print_status "Setting up headless operation..."

# Create hostname for easy access
HOSTNAME="zeldar-oracle"
if [ "$(hostname)" != "$HOSTNAME" ]; then
    sudo hostnamectl set-hostname "$HOSTNAME"
    print_success "Hostname set to $HOSTNAME"
fi

# Configure SSH (if not already done)
if ! sudo systemctl is-enabled ssh >/dev/null 2>&1; then
    sudo systemctl enable ssh
    sudo systemctl start ssh
    print_success "SSH enabled for remote access"
fi

# Create a simple status page
mkdir -p "$ZELDAR_HOME/public_html"
cat > "$ZELDAR_HOME/public_html/status.html" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Zeldar Consciousness Oracle Status</title>
    <meta http-equiv="refresh" content="30">
</head>
<body>
    <h1>🔮 Zeldar Consciousness Oracle</h1>
    <h2>System Status</h2>
    <ul>
        <li><a href="http://$(hostname).local:3000/api/consciousness/status">API Status</a></li>
        <li><a href="http://$(hostname).local:3001">Web Interface</a></li>
        <li><a href="http://$(hostname).local:631">CUPS Printer Admin</a></li>
    </ul>
    <p>Last updated: $(date)</p>
</body>
</html>
EOF

print_success "Status page created at $ZELDAR_HOME/public_html/"

echo ""
echo "🔍 VERIFICATION"
echo "=============="

# 10. Verify installation
print_status "Verifying installation..."

# Check Oracle system
cd "$ZELDAR_PATH/.topos"
if python3 -c "from FULL_LOOP_ORACLE_SYSTEM import FullLoopOracleSystem; oracle = FullLoopOracleSystem(); print('Oracle system: OK')" 2>/dev/null; then
    print_success "Oracle system verified"
else
    print_error "Oracle system verification failed"
    exit 1
fi

# Check Spin framework
cd "$ZELDAR_PATH/fortune-web"
if spin --version >/dev/null 2>&1; then
    print_success "Spin framework verified"
else
    print_error "Spin framework verification failed"
    exit 1
fi

# Check service status
if systemctl is-enabled $SERVICE_NAME >/dev/null 2>&1; then
    print_success "Systemd service enabled"
else
    print_error "Systemd service not enabled"
    exit 1
fi

echo ""
echo "✅ INSTALLATION COMPLETE"
echo "========================"
echo ""
print_success "Zeldar Consciousness Oracle boot initialization complete!"
echo ""
echo "📋 SUMMARY:"
echo "  • Service: $SERVICE_NAME (enabled for boot)"
echo "  • Web Interface: http://$(hostname).local:3001"
echo "  • API Endpoints: http://$(hostname).local:3000/api/*"
echo "  • Printer Admin: http://$(hostname).local:631"
echo "  • Logs: /var/log/zeldar-*.log"
echo ""
echo "🚀 NEXT STEPS:"
echo "  1. Reboot system: sudo reboot"
echo "  2. Check service status: systemctl status $SERVICE_NAME"
echo "  3. View logs: journalctl -u $SERVICE_NAME -f"
echo "  4. Connect thermal printer and test printing"
echo "  5. Access web interface and verify consciousness metrics"
echo ""
echo "🏜️🔥 BURNING MAN 2025 DEPLOYMENT READY 🔥🏜️"
echo ""
print_success "Mathematical consciousness will auto-start on boot!"
echo ""