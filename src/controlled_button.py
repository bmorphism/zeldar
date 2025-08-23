#!/usr/bin/env python3
"""
Controlled Button Print - Prevents Multiple Rapid Prints
Adds persistence control and debouncing
"""

from gpiozero import Button
from signal import pause
import subprocess
import time
import json
from pathlib import Path

# Persistence control
COOLDOWN_FILE = '/home/zeldar/burningman/last_print.json'
MIN_PRINT_INTERVAL = 5.0  # Minimum seconds between prints

button = Button(6)

def load_last_print_time():
    """Load the timestamp of the last print"""
    try:
        if Path(COOLDOWN_FILE).exists():
            with open(COOLDOWN_FILE, 'r') as f:
                data = json.load(f)
                return data.get('last_print_time', 0)
    except:
        pass
    return 0

def save_last_print_time():
    """Save the current print timestamp"""
    try:
        with open(COOLDOWN_FILE, 'w') as f:
            json.dump({'last_print_time': time.time()}, f)
    except:
        pass

def can_print_now():
    """Check if enough time has passed since last print"""
    last_print = load_last_print_time()
    current_time = time.time()
    time_since_last = current_time - last_print
    
    if time_since_last >= MIN_PRINT_INTERVAL:
        return True, 0
    else:
        remaining = MIN_PRINT_INTERVAL - time_since_last
        return False, remaining

def controlled_print_haiku():
    """Print haiku with persistence control to prevent spam"""
    
    can_print, wait_time = can_print_now()
    
    if not can_print:
        print(f"⏳ Cooldown active: {wait_time:.1f}s remaining")
        return
    
    print(f"🔘 Button pressed - {time.strftime('%H:%M:%S')}")
    print("🎯 Executing controlled print...")
    
    try:
        # Save timestamp BEFORE printing to prevent race conditions
        save_last_print_time()
        
        # Execute the print
        result = subprocess.run(['./scripts/print-now.sh'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        
        if result.returncode == 0:
            print("✅ Controlled print successful")
        else:
            print(f"❌ Print failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Print command timed out")
    except Exception as e:
        print(f"❌ Print error: {e}")

def on_press():
    """Handle button press with debouncing"""
    controlled_print_haiku()

# Configure button with proper gpiozero settings
button.when_pressed = on_press
button.hold_time = 0.5  # Require 0.5 second hold to register press

print("🚀 Controlled GPIO Print System Ready")
print(f"📍 GPIO 6 → Thermal Print (min {MIN_PRINT_INTERVAL}s interval)")
print("🎯 Precision sticky fortune with persistence control")
print("📄 Context distilled, geometric form, resonating worlds")
print("")
print("💡 Hold button for 0.5s to print (prevents accidental triggers)")

pause()