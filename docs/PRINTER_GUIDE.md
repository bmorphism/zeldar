# Y812BT Thermal Printer - Working Setup Guide

## Hardware Configuration ✅
- **Printer**: Y812BT thermal printer (USB ID: 5958:0130)
- **Device**: /dev/usb/lp0 
- **GPIO Button**: Pin 6 for manual triggering
- **User Groups**: Add user to `lp` group for device access

## Verified Working Print Methods

### 1. Direct Raw Device Printing (Primary)
```bash
# Initialize printer and send content
sudo bash -c "echo -e '\x1b@' > /dev/usb/lp0 && cat your_file.txt > /dev/usb/lp0 && echo -e '\n\n\n\x1bi' > /dev/usb/lp0"
```
- ESC/POS commands: `\x1b@` (initialize), `\x1bi` (partial cut)
- Direct write to device node
- Fastest method, no print queue

### 2. CUPS Print Queue (Fallback)
```bash
# Print via CUPS system
lp -d Y812BT your_file.txt
```
- Requires printer configured in CUPS
- Print queue management available
- Good for multiple users/jobs

### 3. Custom Script Method
Use `./print-now.sh` script:
- Checks printer availability
- Falls back from direct to CUPS automatically
- Includes status feedback

## GPIO Button System

### Python Script (button-print.py)
- Monitors GPIO pin 6 for button press
- Dual-method printing (direct → CUPS fallback)
- Updates runtime_status.json with activity
- Runs continuously as daemon

### Button Wiring
- GPIO pin 6 to button
- Ground connection required
- Pull-up resistor handled by software

## File Structure
```
burningman/
├── button-print.py      # GPIO daemon script
├── print-now.sh        # Manual print script
├── haiku.txt           # Default content
├── dada_hyperstition.txt # ASCII art content
└── runtime_status.json # Activity tracking
```

## Troubleshooting Commands

### Check Hardware
```bash
lsusb                    # Verify USB connection
ls -la /dev/usb/         # Check device node exists
dmesg | tail -20         # Hardware messages
```

### Check Permissions
```bash
groups                   # Verify lp group membership
ls -la /dev/usb/lp0     # Check device permissions
```

### Test Printing
```bash
./print-now.sh          # Test direct method
lpstat -p               # Check CUPS printers
lp -d Y812BT test.txt   # Test CUPS method
```

### GPIO Testing
```bash
# Test button functionality (5 second timeout)
timeout 5 python3 -c "
from gpiozero import Button
from signal import pause
print('🔘 Press button on pin 6...')
Button(6).when_pressed = lambda: print('✅ Button works!')
pause()
"
```

## Content Formatting Tips
- Plain text works best
- ASCII art prints reliably
- Keep lines under 32 characters for thermal printer width
- Use `\n\n\n` for spacing between prints
- ESC/POS commands for formatting if needed

## Power Considerations
- Ensure adequate power supply (5V 3A+ recommended)
- Watch for undervoltage warnings in dmesg
- Thermal printing draws significant current

## Success Indicators
- lsusb shows device ID 5958:0130
- /dev/usb/lp0 exists with lp group write access
- Direct printing returns no errors
- CUPS shows printer as "idle" and "accepting requests"
- GPIO script runs without Python import errors

## Last Verified
- Date: 2025-08-23
- System: Raspberry Pi with Y812BT
- Methods: Direct device ✅, CUPS ✅, GPIO ✅