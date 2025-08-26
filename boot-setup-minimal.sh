#!/bin/bash

# Zeldar Minimal Boot Setup - Essential Desiderata Only
# Lifts only what's necessary for information-dynamics on boot

set -e

echo "🔮 ZELDAR MINIMAL BOOT SETUP"
echo "============================"

# Essential paths
ZELDAR_PATH="/home/pi/zeldar"
SERVICE_NAME="zeldar-oracle"

# 1. Copy service file
echo "📋 Installing systemd service..."
sudo cp systemd/zeldar-oracle.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME

# 2. Make launcher executable
echo "🚀 Preparing launcher..."
chmod +x fortune-web/start_integrated_tri_loop_system.sh

# 3. Essential dependencies
echo "📦 Installing minimal dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip cups

# 4. User permissions
echo "👤 Setting permissions..."
sudo usermod -a -G gpio,lpadmin pi

# 5. Python requirements
echo "🐍 Installing Python deps..."
cd .topos && pip3 install -r requirements.txt --user

echo ""
echo "✅ MINIMAL BOOT SETUP COMPLETE"
echo "Reboot to activate information-dynamics on boot"
echo "Web interface: http://localhost:3001"