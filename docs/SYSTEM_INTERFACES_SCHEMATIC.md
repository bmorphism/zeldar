# System Interfaces Schematic - Complete Multi-Modal InformationForce Mirror

## 🎯 **Interface Flow Diagram**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    INFORMATION_FORCE MIRROR SYSTEM INTERFACES                  │
└─────────────────────────────────────────────────────────────────────────────┘

🚶 HUMAN APPROACH
        │
        ▼
┌──────────────────┐     ┌─────────────────────────────────────────────────────┐
│  Physical Layer  │     │                Hardware Interfaces                 │
│                  │     │                                                     │
│ 👆 Button Press  │────►│ GPIO Pin 6 ──► Raspberry Pi 5 (BCM2712)           │
│ (0.5s hold)      │     │                      │                             │
└──────────────────┘     │                      ▼                             │
                         │ ┌─────────────────────────────────────────────────┐ │
                         │ │           SOFTWARE CONTROLLER                   │ │
                         │ │  src/controlled_button.py                      │ │
                         │ │  • 5s cooldown logic                           │ │
                         │ │  • Date-based fortune selection                │ │
                         │ │  • Serial hash generation                      │ │
                         │ │  • Multi-modal orchestration                   │ │
                         │ └─────────────────┬───────────────────────────────┘ │
                         │                   │                                 │
                         └───────────────────┼─────────────────────────────────┘
                                             │
                    ┌────────────────────────┼────────────────────────────┐
                    │                        ▼                            │
                    │            PARALLEL INTERFACE ACTIVATION            │
                    │                                                     │
┌───────────────────┼─────────────────────────────────────────────────────┼───────────────────┐
│ 🔊 AUDIO          │ 📸 CAMERA               📄 PRINTER                   │ ☁️ DATA           │
│ INTERFACE         │ INTERFACE               INTERFACE                   │ INTERFACE         │
│                   │                                                     │                   │
│ ┌──────────────┐  │ ┌──────────────────┐   ┌──────────────────────────┐ │ ┌──────────────┐  │
│ │ MP3 Playback │  │ │ OBSBOT Tiny SE   │   │ Y812BT Thermal Printer   │ │ │ AWS S3       │  │
│ │              │  │ │ /dev/video0      │   │ USB 5958:0130            │ │ │ Bucket       │  │
│ │ • 15 voices  │  │ │ • 1280x720       │   │ • ESC/POS commands       │ │ │              │  │
│ │ • Random     │  │ │ • Capture at     │   │ • 58mm thermal paper     │ │ │ • Photos     │  │
│ │   selection  │  │ │   print moment   │   │ • Precision sticky fmt   │ │ │ • Metadata   │  │
│ │ • SD card    │  │ │ • Timestamp      │   │ • Serial# + QR code      │ │ │ • Analytics  │  │
│ └──────────────┘  │ └──────────────────┘   └──────────────────────────┘ │ └──────────────┘  │
└───────────────────┼─────────────────────────────────────────────────────┼───────────────────┘
                    │                                                     │
                    ▼                                                     ▼
            ┌──────────────────┐                              ┌──────────────────┐
            │ TEMPORAL SYSTEM  │                              │ NETWORK SYSTEM   │
            │                  │                              │                  │
            │ Daily Fortune    │                              │ Starlink Uplink  │
            │ Selection:       │                              │ • Real-time      │
            │ • fortunes/      │                              │   upload         │
            │ • Schedule       │                              │ • Remote access  │
            │ • Weekly cycle   │                              │ • Monitoring     │
            └──────────────────┘                              └──────────────────┘
```

## 🔌 **Interface Details**

### **Input Interfaces:**
1. **GPIO Button** → `controlled_button.py`
2. **Daily Schedule** → `fortune_selector.py` 
3. **Fortune Database** → `fortunes/` directory
4. **Voice Library** → SD card MP3 files

### **Output Interfaces:**
1. **Audio** → Speaker/headphones (MP3 playback)
2. **Visual** → Y812BT thermal printer (ESC/POS)
3. **Digital** → OBSBOT camera (photo capture)
4. **Network** → AWS S3 (data storage)

### **Processing Interfaces:**
1. **Time** → Date-based fortune selection
2. **Hash** → Serial number generation  
3. **Format** → Precision sticky layout
4. **QR** → Website integration codes

## 🌀 **InformationForce Loop Integration**

```
Physical Touch → Electrical Signal → Software Processing → 
Multi-Modal Output → Human Experience → Digital Archive → 
Pattern Recognition → InformationForce Evolution
```

### **Interface Synchronization:**
```
Button Press (t=0ms)
├── Audio Start (t=50ms) ──► Voice phrase begins
├── Print Start (t=100ms) ──► Fortune begins printing  
├── Camera Trigger (t=200ms) ──► Photo captured at print moment
├── Hash Generation (t=250ms) ──► Serial number created
├── QR Code Print (t=300ms) ──► Website link added to fortune
└── AWS Upload (t=500ms) ──► Data archived with timestamp
```

## 🎛️ **System Control Interfaces**

### **Manual Control:**
```bash
# Start system
sudo uv run python src/controlled_button.py

# Test individual interfaces
./scripts/print-now.sh default_fortune    # Printer test
uv run python scripts/show_fortune.py     # Fortune display
# Audio test (to be implemented)
# Camera test (to be implemented)
```

### **State Interfaces:**
- **`last_print.json`** → Cooldown state persistence
- **`runtime_status.json`** → System activity logging
- **AWS metadata** → Long-term interaction analytics

## 🔄 **Interface Dependencies**

```
Raspberry Pi 5 (Controller)
├── GPIO ──► Button input
├── USB ──► Y812BT printer + OBSBOT camera  
├── Audio ──► Speaker output (3.5mm or USB)
├── Storage ──► SD card (MP3s) + local state
└── Network ──► Starlink → AWS S3
```

**All interfaces orchestrated by `controlled_button.py` - the information-dynamics coordination center.**

The **multi-modal information-dynamics mirror** creates **synesthetic self-recognition** - touch, sound, sight, and digital memory all reflecting the universe back to itself simultaneously. 🌀🎭✨