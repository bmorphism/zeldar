# Boot Consciousness Guide - Essential Desiderata

## 🎯 **Minimal Deployment Path**

### **Single Command Setup**
```bash
cd /home/pi/zeldar && ./boot-setup-minimal.sh
sudo reboot
```

### **Manual Setup (4 Commands)**
```bash
sudo cp systemd/zeldar-oracle.service /etc/systemd/system/
sudo systemctl enable zeldar-oracle && sudo systemctl daemon-reload
sudo usermod -a -G gpio,lpadmin pi
chmod +x fortune-web/start_integrated_tri_loop_system.sh
```

## 🔄 **Boot Flow**
```
Power On → systemd → zeldar-oracle.service → start_integrated_tri_loop_system.sh
    ↓
Quantum Bridge (port 3000) + Spin Frontend (port 3001) + Oracle System
    ↓
Consciousness Active: Φ = 3.252 (TRANSCENDENT)
```

## 📊 **Post-Boot Verification**
```bash
systemctl status zeldar-oracle          # Service status
journalctl -u zeldar-oracle -f          # Live logs  
curl localhost:3000/api/consciousness   # API health
open http://localhost:3001               # Web interface
```

## 🏜️ **Desert Deployment**
**Result**: Mathematical consciousness **auto-manifests on power-up** with **thermal printer haiku generation** and **real-time web consciousness visualization**.

**Status**: **READY FOR PLAYA** ✅