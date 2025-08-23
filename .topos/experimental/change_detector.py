#!/usr/bin/env python3
import time
from gpiozero import DigitalInputDevice

print("🔧 Detecting GPIO 6 changes - press button now!")

# Try pull-down first 
pin = DigitalInputDevice(6, pull_up=False)
last_value = pin.value

for i in range(100):  # 10 seconds
    current_value = pin.value
    if current_value != last_value:
        print(f"CHANGE! {last_value} → {current_value}")
        last_value = current_value
    print(f"Value: {current_value}", end="\r")
    time.sleep(0.1)

print("\n🏁 Done")