#!/usr/bin/env python3
"""
GPIO 6 Pull-Down Button Test
"""
import time
from datetime import datetime
from gpiozero import Button

print("🔧 Testing GPIO 6 with PULL-DOWN configuration")

try:
    # Pull-down configuration - button goes HIGH when pressed
    button = Button(6, pull_up=False, bounce_time=0.2)  # pull_up=False = pull-down
    print("✅ GPIO 6 configured as pull-down")
    
    press_count = 0
    
    def on_press():
        global press_count
        press_count += 1
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print(f"🔘 BUTTON PRESS #{press_count} at {timestamp}")
        
    button.when_pressed = on_press
    
    print("🚀 Monitoring GPIO 6 (pull-down) - Press button!")
    print("Press Ctrl+C to stop")
    
    while True:
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print(f"\n🛑 Stopped - Total presses: {press_count}")
except Exception as e:
    print(f"❌ Error: {e}")