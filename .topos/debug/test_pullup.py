#!/usr/bin/env python3
import time
from gpiozero import DigitalInputDevice

print("🔧 Testing GPIO 6 with PULL-UP")
pin = DigitalInputDevice(6, pull_up=True)

for i in range(50):
    value = pin.value  
    print(f"GPIO 6 (pull-up): {value}", end="\r")
    time.sleep(0.1)
print("\n🏁 Done")