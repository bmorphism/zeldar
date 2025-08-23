#!/usr/bin/env python3
"""
Manual GPIO Value Check - No event handling, just raw values
"""
import time
from gpiozero import MCP3008, DigitalInputDevice

print("🔧 Manual GPIO 6 value monitoring")
print("Hold button and watch for value changes...")

try:
    # Try as digital input device first
    pin = DigitalInputDevice(6, pull_up=False)  # pull-down
    print("✅ GPIO 6 configured as digital input (pull-down)")
    
    for i in range(50):  # 5 seconds
        value = pin.value
        print(f"GPIO 6 value: {value}", end="\r")
        time.sleep(0.1)
        
    print("\n🏁 Done")
    
except Exception as e:
    print(f"❌ Error: {e}")