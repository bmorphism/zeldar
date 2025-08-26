# 🔮 AI Fortune Teller (The Ingressing Robot)

**Press button → AI speaks → Fortune prints → Photo captures → QR code connects**

## Core Mission

Create a **simple, magical experience** where:
1. Person **presses crystal-ball button** 
2. Robot **speaks AI-generated phrases** 
3. **Fortune prints** on thermal printer
4. **Camera snaps photo** at moment of printing
5. **QR code** on ticket connects to website with photo and fortune

## Quick Start

```bash
./boot-setup-minimal.sh  # Essential setup
sudo reboot
python3 FULL_LOOP_ORACLE_SYSTEM.py  # Start the magic
```

## Hardware Needed

- **Raspberry Pi** + power supply
- **Y812BT thermal printer** (USB)  
- **Button** (GPIO Pin 6)
- **USB camera**
- **SD card** with AI-generated MP3 phrases

## The Experience

**User**: *Approaches and presses button*
**Robot**: *Plays AI-generated opener phrase (1 of 15)*  
**Printer**: *Starts printing fortune with timestamp + QR code*
**Camera**: *Snaps photo at exact moment of printing*
**Robot**: *Plays AI-generated ending phrase*

**Result**: Person gets physical ticket with:
- AI-generated fortune
- Timestamp & serial number
- QR code → website with their photo and fortune

## AI Content

- **15 AI-generated opener MP3s** (robot voice, not human)
- **AI-generated fortunes** 
- **Modular phrases** uploaded to SD card
- **Photos + timestamps** saved to AWS for analysis

## Technical Core

- **`FULL_LOOP_ORACLE_SYSTEM.py`** - Main system
- **`button_oracle_bridge.py`** - Button → action
- **`thermal_information_force_bridge.py`** - Printing
- **Y812BT printer setup** via CUPS

## Gift Economy Integration

Perfect for Burning Man:
- **Interactive**: Immediate physical gift (printed fortune)
- **Digital connection**: QR code extends experience beyond the playa
- **Unique**: Every interaction generates personalized content
- **Simple**: Just press button, get magic

---

*One button press. AI speaks. Fortune manifests. Photo captured. Connection made.* ✨