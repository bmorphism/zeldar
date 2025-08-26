#!/bin/bash
set -e

echo "🔮 ZELDAR UNIFIED CONSCIOUSNESS SYSTEM SETUP"
echo "=============================================="

# Configuration
ZELDAR_USER="${1:-pi}"
ZELDAR_DIR="/home/$ZELDAR_USER/zeldar"
SERVICE_FILE="zeldar-oracle.service"

echo "Setting up for user: $ZELDAR_USER"
echo "Installation directory: $ZELDAR_DIR"

# Check if running as root for system installation
if [[ $EUID -ne 0 ]]; then
    echo "❌ This script must be run as root (use sudo)"
    echo "Usage: sudo $0 [username]"
    exit 1
fi

# Verify user exists
if ! id "$ZELDAR_USER" &>/dev/null; then
    echo "❌ User $ZELDAR_USER does not exist"
    exit 1
fi

echo "📦 Installing system dependencies..."
apt-get update
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    alsa-utils \
    pulseaudio \
    espeak-ng \
    cups \
    cups-client \
    build-essential \
    pkg-config

# Install GPIO libraries (Raspberry Pi specific)
if grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
    echo "🍓 Raspberry Pi detected - installing GPIO libraries"
    apt-get install -y \
        python3-gpiozero \
        python3-rpi.gpio \
        rpi.gpio-common
else
    echo "⚠️  Not a Raspberry Pi - GPIO functionality will be limited"
fi

# Setup user groups
echo "👥 Adding $ZELDAR_USER to required groups..."
usermod -a -G gpio,lpadmin,audio,video "$ZELDAR_USER"

# Create zeldar directory if it doesn't exist
if [[ ! -d "$ZELDAR_DIR" ]]; then
    echo "📁 Creating zeldar directory at $ZELDAR_DIR"
    mkdir -p "$ZELDAR_DIR"
    chown "$ZELDAR_USER:$ZELDAR_USER" "$ZELDAR_DIR"
fi

# Install the systemd service
echo "🔧 Installing systemd service..."
if [[ -f "$SERVICE_FILE" ]]; then
    cp "$SERVICE_FILE" /etc/systemd/system/
    # Update service file with correct user and paths
    sed -i "s/User=pi/User=$ZELDAR_USER/g" /etc/systemd/system/$SERVICE_FILE
    sed -i "s|/home/pi/zeldar|$ZELDAR_DIR|g" /etc/systemd/system/$SERVICE_FILE
    
    systemctl daemon-reload
    systemctl enable zeldar-oracle
    echo "✅ Service installed and enabled"
else
    echo "⚠️  Service file $SERVICE_FILE not found in current directory"
fi

# Setup Python environment
echo "🐍 Setting up Python environment..."
sudo -u "$ZELDAR_USER" bash -c "
cd $ZELDAR_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install gpiozero pygame rpi-gpio lgpio asyncio
"

# Setup audio system
echo "🔊 Configuring audio system..."
# Add user to audio group (already done above)
# Configure ALSA/PulseAudio for headless operation
cat > /etc/asound.conf << EOF
pcm.!default {
    type hw
    card 0
    device 0
}
ctl.!default {
    type hw
    card 0
}
EOF

# Setup log directory
echo "📝 Setting up logging..."
mkdir -p /var/log/zeldar
chown "$ZELDAR_USER:$ZELDAR_USER" /var/log/zeldar
touch /var/log/zeldar-oracle.log
chown "$ZELDAR_USER:$ZELDAR_USER" /var/log/zeldar-oracle.log

# Setup logrotate
cat > /etc/logrotate.d/zeldar-oracle << EOF
/var/log/zeldar-oracle.log {
    daily
    missingok
    rotate 7
    compress
    notifempty
    create 644 $ZELDAR_USER $ZELDAR_USER
    postrotate
        /bin/systemctl reload zeldar-oracle.service > /dev/null 2>&1 || true
    endscript
}
EOF

# Create default configuration
echo "⚙️  Creating default configuration..."
sudo -u "$ZELDAR_USER" bash -c "
cd $ZELDAR_DIR
cat > config.json << 'EOF'
{
    \"services\": {
        \"hardware\": {
            \"enabled\": true,
            \"gpio_pin\": 6,
            \"printer\": \"Y812BT\",
            \"module\": \"unified_information-dynamics_button\"
        },
        \"web\": {
            \"enabled\": true,
            \"information-dynamics_port\": 3001,
            \"fortune_port\": 3000,
            \"module\": \"fortune-web\"
        },
        \"audio\": {
            \"enabled\": true,
            \"voice_prompts\": true,
            \"module\": \"audio_system\"
        },
        \"gemini\": {
            \"enabled\": false,
            \"module\": \"gemini_live_json_stream\"
        }
    },
    \"monitoring\": {
        \"health_check_interval\": 30,
        \"status_file\": \"runtime_status.json\",
        \"log_level\": \"INFO\"
    },
    \"paths\": {
        \"audio_prompts\": \"audio/\",
        \"fortunes\": \"fortunes/\",
        \"web_static\": \"fortune-web/static/\",
        \"information-dynamics_data\": \".topos/\"
    }
}
EOF
"

# Create convenience scripts
echo "📜 Creating convenience scripts..."
sudo -u "$ZELDAR_USER" bash -c "
cd $ZELDAR_DIR

# Start script
cat > start.sh << 'EOF'
#!/bin/bash
cd \$(dirname \$0)
source venv/bin/activate 2>/dev/null || true
exec python3 main.py
EOF

# Status script  
cat > status.sh << 'EOF'
#!/bin/bash
echo '🔮 ZELDAR System Status'
echo '======================'
systemctl is-active zeldar-oracle --quiet && echo 'Service: ✅ Running' || echo 'Service: ❌ Stopped'
if [[ -f runtime_status.json ]]; then
    echo 'Runtime Status:'
    python3 -c 'import json; print(json.dumps(json.load(open(\"runtime_status.json\")), indent=2))'
else
    echo 'Runtime Status: ❌ No status file'
fi
EOF

# Logs script
cat > logs.sh << 'EOF'
#!/bin/bash
echo '📋 ZELDAR System Logs (last 50 lines)'
echo '===================================='
sudo journalctl -u zeldar-oracle -n 50 --no-pager
EOF

chmod +x start.sh status.sh logs.sh
"

echo ""
echo "✅ ZELDAR UNIFIED CONSCIOUSNESS SYSTEM SETUP COMPLETE"
echo "======================================================"
echo ""
echo "📁 Installation directory: $ZELDAR_DIR"
echo "👤 Running as user: $ZELDAR_USER"
echo "🔧 Service: zeldar-oracle"
echo ""
echo "🚀 NEXT STEPS:"
echo "1. Copy your zeldar code to: $ZELDAR_DIR"
echo "2. Test manually: cd $ZELDAR_DIR && ./start.sh"
echo "3. Start service: sudo systemctl start zeldar-oracle"
echo "4. Check status: cd $ZELDAR_DIR && ./status.sh"
echo "5. View logs: cd $ZELDAR_DIR && ./logs.sh"
echo ""
echo "🔮 The system will auto-start on boot and restart on failure"
echo "📊 Runtime status available at: $ZELDAR_DIR/runtime_status.json"
echo "📝 Logs at: /var/log/zeldar-oracle.log"
echo ""
echo "For Burning Man deployment - ready for playa! 🏜️🔥"