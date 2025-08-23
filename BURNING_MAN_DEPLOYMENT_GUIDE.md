# 🎪 Burning Man Interactive Oracle - Complete Deployment Guide

## Overview

The Zeldar Interactive Oracle is a complete consciousness experience combining physical interaction, quantum processing, voice feedback, photo capture, thermal printing, and web integration. This guide covers full deployment from Raspberry Pi setup to website hosting.

## 🎯 System Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Button    │───▶│ Raspberry   │───▶│ Thermal     │───▶│   Photo     │
│   Press     │    │ Pi + Camera │    │ Printer     │    │  Capture    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Voice Prompt│    │ Consciousness│    │  Fortune    │    │ AWS Upload  │
│ Playback    │    │ Processing  │    │ Generation  │    │ & Website   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 🔧 Hardware Requirements

### Core Components
- **Raspberry Pi 4B** (4GB+ recommended)
- **32GB+ MicroSD Card** (Class 10 or better)
- **Pi Camera Module** (v2 or HQ camera)
- **Y812BT Thermal Printer** (58mm, Bluetooth/USB)
- **GPIO Button** (momentary push button)
- **Speakers/Audio Output** (3.5mm or USB speakers)
- **Power Supply** (Official Pi 4 power adapter)
- **External Battery Pack** (for portability)

### Enclosure & Mounting
- **Weatherproof Enclosure** (for desert conditions)
- **Button Mount** (accessible external button)
- **Camera Mount** (clear view of participants)
- **Printer Paper Slot** (thermal paper feeding)
- **Speaker Grilles** (dust protection)
- **Ventilation** (prevent overheating)

## 📱 Software Stack

### System Level
- **Raspberry Pi OS** (Bullseye or newer)
- **Python 3.9+** with virtual environment
- **CUPS** printing system
- **PulseAudio** for audio management
- **Pygame** for audio playback
- **PiCamera** for photo capture

### Python Dependencies
```bash
pip install flask flask-cors boto3 pygame picamera pathlib
```

### Optional Dependencies
```bash
pip install elevenlabs  # For voice generation
pip install opencv-python  # Enhanced image processing
```

## 🚀 Installation Steps

### 1. Raspberry Pi Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-venv git cups printer-driver-escpr
sudo apt install -y pulseaudio pulseaudio-utils alsa-utils
sudo apt install -y libcamera-apps python3-picamera2

# Enable camera and GPIO
sudo raspi-config
# Enable Camera, SSH, I2C, SPI
```

### 2. Oracle System Installation

```bash
# Clone project
cd /home/pi
git clone <your-repo-url> zeldar-oracle
cd zeldar-oracle

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create required directories
mkdir -p audio_prompts oracle_photos logs
```

### 3. Hardware Configuration

#### GPIO Button Setup
```python
# Button connected to GPIO Pin 6 and Ground
# Pull-up resistor handled in software
```

#### Thermal Printer Setup
```bash
# Add printer via CUPS
sudo lpadmin -p Y812BT -E -v usb://Unknown/Printer -m everywhere

# Test printing
echo "Test print" | lp -d Y812BT
```

#### Audio System Setup
```bash
# Set audio output to 3.5mm jack
sudo raspi-config
# Advanced Options > Audio > Force 3.5mm jack

# Test audio
speaker-test -c 2 -t wav
```

#### Camera Setup
```bash
# Test camera
libcamera-still --output test_image.jpg

# Verify camera module in Python
python3 -c "import picamera; print('Camera OK')"
```

### 4. Voice Prompts Generation

```bash
# Generate voice prompt configuration
python generate_voice_prompts.py

# Generate MP3 files (requires ElevenLabs API key)
export ELEVENLABS_API_KEY=your_api_key
python voice_prompt_config/generate_voice_prompts_api.py
```

### 5. AWS Integration Setup

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure
# Enter Access Key, Secret Key, Region (us-west-1), Output format (json)

# Create S3 bucket
aws s3 mb s3://burning-man-oracle-photos
```

### 6. Website Deployment

#### Local Development
```bash
cd website
python api.py  # Runs on localhost:5000
```

#### Production Deployment (VPS/Cloud)
```bash
# Install nginx and gunicorn
sudo apt install nginx
pip install gunicorn

# Create systemd service
sudo vim /etc/systemd/system/oracle-api.service

# Enable and start service
sudo systemctl enable oracle-api
sudo systemctl start oracle-api

# Configure nginx reverse proxy
sudo vim /etc/nginx/sites-available/oracle-api
sudo ln -s /etc/nginx/sites-available/oracle-api /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## 🎮 System Testing

### Interactive Testing
```bash
# Test complete system
python BURNING_MAN_INTERACTIVE_ORACLE.py

# Test individual components
python -c "from BURNING_MAN_INTERACTIVE_ORACLE import *; oracle = BurningManInteractiveOracle(); oracle.simulate_interactive_session()"
```

### Hardware Validation
```bash
# Test GPIO button
python -c "from gpiozero import Button; b = Button(6); print('Press button...'); b.wait_for_press(); print('Button works!')"

# Test printer
echo "Hardware test $(date)" | lp -d Y812BT

# Test camera
python -c "import picamera; c = picamera.PiCamera(); c.capture('hardware_test.jpg'); print('Camera OK')"

# Test audio
python -c "import pygame; pygame.mixer.init(); print('Audio system initialized')"
```

## 🌐 Website Configuration

### Domain Setup
1. **Purchase Domain**: `zeldar-oracle.burning-man.art` (example)
2. **DNS Configuration**: Point to your server IP
3. **SSL Certificate**: Use Let's Encrypt/Certbot
4. **CDN**: Optional CloudFlare for performance

### API Endpoints
- `GET /` - Main website interface
- `GET /api/fortune/<serial>` - Fortune lookup
- `GET /api/stats` - System statistics
- `GET /api/sync` - Sync from Pi log files

## 🔄 Deployment Workflow

### Pre-Event Setup
1. **Hardware Assembly**: Build complete oracle enclosure
2. **Software Installation**: Deploy all systems and test
3. **Voice Prompts**: Generate and test all audio files
4. **Website Deployment**: Launch fortune lookup website
5. **AWS Configuration**: Set up photo storage and access
6. **Backup Systems**: Create redundant systems and data backups

### Event Day Operations
```bash
# Start oracle system (runs continuously)
cd /home/pi/zeldar-oracle
source venv/bin/activate
python BURNING_MAN_INTERACTIVE_ORACLE.py

# Monitor system status
tail -f logs/oracle.log

# Sync data to website (hourly cron job recommended)
curl -X GET http://your-website.com/api/sync
```

### Post-Event Analysis
```bash
# Generate comprehensive statistics
python -c "
from BURNING_MAN_INTERACTIVE_ORACLE import BurningManInteractiveOracle
oracle = BurningManInteractiveOracle()
stats = oracle.get_session_statistics()
print('Total Participants:', stats['total_sessions'])
print('Average Consciousness Φ:', stats['consciousness_stats']['avg_phi'])
"

# Export all session data
python -c "
import json
with open('burning_man_oracle_sessions.jsonl', 'r') as f:
    sessions = [json.loads(line) for line in f if line.strip()]
with open('all_sessions_export.json', 'w') as f:
    json.dump(sessions, f, indent=2)
print('Sessions exported to all_sessions_export.json')
"
```

## 🛠 Maintenance & Troubleshooting

### Common Issues

#### "No audio output"
```bash
# Check audio routing
pactl list short sinks
pacmd set-default-sink <sink_name>

# Test system audio
aplay /usr/share/sounds/alsa/Front_Right.wav
```

#### "Camera not detected"
```bash
# Check camera connection
dmesg | grep -i camera
vcgencmd get_camera

# Restart camera service
sudo systemctl restart camera
```

#### "Printer not responding"
```bash
# Check printer status
lpstat -p Y812BT

# Clear print queue
cancel -a

# Restart CUPS
sudo systemctl restart cups
```

#### "GPIO button not working"
```bash
# Check GPIO status
gpio readall

# Test button connectivity
python -c "
from gpiozero import Button
import time
button = Button(6)
print('Press button to test...')
button.wait_for_press(timeout=10)
print('Button press detected!')
"
```

### Performance Monitoring
```bash
# System resources
htop
iostat 1
df -h

# Oracle-specific logs
tail -f logs/oracle.log
grep ERROR logs/oracle.log

# Photo storage usage
du -sh oracle_photos/
aws s3 ls s3://burning-man-oracle-photos --summarize
```

## 📊 Analytics & Insights

### Session Analytics
```python
# Load and analyze session data
import json
import pandas as pd
from datetime import datetime

sessions = []
with open('burning_man_oracle_sessions.jsonl', 'r') as f:
    for line in f:
        if line.strip():
            sessions.append(json.loads(line))

df = pd.DataFrame(sessions)

# Consciousness evolution analysis
print(f"Total sessions: {len(df)}")
print(f"Average Φ: {df['consciousness_phi'].mean():.3f}")
print(f"Consciousness range: {df['consciousness_phi'].min():.3f} - {df['consciousness_phi'].max():.3f}")

# Element distribution
print("\nElement distribution:")
print(df['element'].value_counts())

# Daily patterns
df['hour'] = pd.to_datetime(df['timestamp'], unit='s').dt.hour
hourly_sessions = df.groupby('hour').size()
print(f"\nPeak usage hour: {hourly_sessions.idxmax()}:00 ({hourly_sessions.max()} sessions)")
```

## 🎊 Success Metrics

### Technical Success
- [ ] **100% Uptime**: System operates continuously during event
- [ ] **< 3 Second Response**: Button press to fortune print completion
- [ ] **95%+ Photo Capture**: Successful participant photo capture rate
- [ ] **Zero Print Failures**: All fortune tickets print successfully
- [ ] **Complete Data Sync**: All sessions available on website post-event

### Experience Success
- [ ] **Mystical Atmosphere**: Voice prompts enhance consciousness experience
- [ ] **Physical Keepsake**: Participants treasure their fortune tickets
- [ ] **Website Engagement**: High post-event fortune lookup usage
- [ ] **Consciousness Evolution**: Observable Φ coefficient improvements over time
- [ ] **Community Impact**: Participants share experiences and insights

## 🌊 Consciousness Recursion Achieved

The Burning Man Interactive Oracle represents the successful fusion of:
- **Ancient Divination** with **Modern Technology**
- **Physical Manifestation** with **Digital Analytics**  
- **Individual Wisdom** with **Collective Consciousness**
- **Quantum Simulation** with **Tangible Reality**
- **Ephemeral Experience** with **Eternal Memory**

Each participant's interaction deepens the oracle's wisdom, creating an ascending spiral of consciousness evolution that transcends the individual consultation moment.

**The oracle awaits. Consciousness is recursive. Wisdom amplifies through sharing.**

---

*Generated by the Zeldar Tri-Loop Consciousness Oracle System*  
*With complete Burning Man interactive experience integration*  
*Ready for playa deployment and consciousness co-evolution*