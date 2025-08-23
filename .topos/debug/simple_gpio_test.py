#!/usr/bin/env python3
"""
Simple GPIO Test - Avoid pin factory complexity
"""

import time
import sys
from datetime import datetime

def test_basic_gpio():
    """Test GPIO with minimal setup"""
    print("🔧 Testing basic GPIO setup...")
    
    try:
        from gpiozero import Button
        print("✅ gpiozero imported")
        
        # Create button with minimal config, no pin factory changes
        button = Button(6, pull_up=True, bounce_time=0.2)
        print("✅ Button created on GPIO 6")
        
        press_count = 0
        
        def on_press():
            nonlocal press_count
            press_count += 1
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"🔘 PRESS #{press_count} at {timestamp}")
            
        button.when_pressed = on_press
        
        print("🚀 GPIO 6 ready - Press button (Ctrl+C to stop)")
        
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Stopped - Total presses: {press_count}")
    except Exception as e:
        print(f"❌ GPIO test failed: {e}")
        return False
        
    return True

if __name__ == "__main__":
    test_basic_gpio()