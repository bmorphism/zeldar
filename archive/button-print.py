#!/usr/bin/env python3
# Button Print Loop - Unified
# Context distilled in geometric form

from gpiozero import Button
from signal import pause
import subprocess
import time
import os

# Enhanced GPIO configuration with explicit pull-up and bounce time
button = Button(6, pull_up=True, bounce_time=0.1)

def print_haiku():
    """Print haiku - try direct first, fallback to CUPS"""
    # Clean subprocess environment
    clean_env = {
        'PATH': '/usr/bin:/bin:/usr/sbin:/sbin',
        'USER': 'zeldar',
        'HOME': '/home/zeldar'
    }
    try:
        # Direct method
        subprocess.run(['./print-now.sh'], 
                      check=True, 
                      env=clean_env,
                      close_fds=True,
                      preexec_fn=os.setsid)
        print("✓ Haiku printed (direct)")
    except:
        try:
            # CUPS fallback  
            subprocess.run(['lp', '-d', 'Y812BT', 'haiku.txt'],
                      check=True,
                      env=clean_env,
                      close_fds=True)
            print("✓ Haiku printed (CUPS)")
        except:
            print("✗ Print failed")

def on_press():
    print(f"🔘 Button pressed - {time.strftime('%H:%M:%S')}")
    print_haiku()

button.when_pressed = on_press

print("🚀 Ready: GPIO 6 → Thermal Print")
print("📄 Context distilled, geometric form, resonating worlds")

pause()
