#!/usr/bin/env python3
"""
Simple GPIO Debug Script
Tests GPIO pins and button detection with minimal complexity
"""

import time
import sys
from datetime import datetime

try:
    from gpiozero import Button, Device
    print("✅ gpiozero imported successfully")
except ImportError as e:
    print(f"❌ Failed to import gpiozero: {e}")
    sys.exit(1)

def test_gpio_pin(pin_number):
    """Test a specific GPIO pin for button presses"""
    print(f"\n🔍 Testing GPIO pin {pin_number}")
    print("Press Ctrl+C to stop")
    
    last_press = 0
    cooldown = 0.0  # No cooldown - all presses detected
    
    try:
        # Create button with minimal configuration
        button = Button(pin_number, pull_up=True, bounce_time=None)  # No debounce filtering
        print(f"✅ Button created on GPIO {pin_number}")
        
        def on_press():
            nonlocal last_press
            current_time = time.time()
            
            # Cooldown disabled - detect all presses
            # if current_time - last_press < cooldown:
            #     print(f"⏱️  Ignoring press (cooldown: {cooldown - (current_time - last_press):.1f}s remaining)")
            #     return
                
            last_press = current_time
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"🔘 BUTTON PRESSED! GPIO {pin_number} at {timestamp}")
            
            # Simple feedback
            print("   └─ Press detected and processed")
            
        button.when_pressed = on_press
        
        print(f"🚀 Monitoring GPIO {pin_number} - Press the button...")
        print(f"⏱️  Cooldown between presses: {cooldown}s")
        
        # Keep alive loop
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Stopped monitoring GPIO {pin_number}")
    except Exception as e:
        print(f"❌ Error with GPIO {pin_number}: {e}")

def scan_common_pins():
    """Test common GPIO pins to find working buttons"""
    common_pins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    
    print("🔍 Scanning common GPIO pins for button detection...")
    print("This will test each pin briefly. Press your button during each test.")
    
    for pin in common_pins:
        try:
            print(f"\n📌 Testing GPIO {pin} (5 second window)...")
            button = Button(pin, pull_up=True, bounce_time=None)  # No debounce filtering
            
            pressed = False
            def detect_press():
                nonlocal pressed
                pressed = True
                print(f"🔘 DETECTED on GPIO {pin}!")
                
            button.when_pressed = detect_press
            
            # Wait 5 seconds for press
            for i in range(50):
                if pressed:
                    break
                time.sleep(0.1)
                
            button.close()
            
            if pressed:
                print(f"✅ GPIO {pin} is working! Press detected.")
            else:
                print(f"   No press detected on GPIO {pin}")
                
        except Exception as e:
            print(f"   ❌ GPIO {pin} failed: {e}")
            
        time.sleep(0.5)  # Brief pause between tests

if __name__ == "__main__":
    print("🚀 GPIO Button Debug Tool")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "scan":
            scan_common_pins()
        else:
            try:
                pin = int(sys.argv[1])
                test_gpio_pin(pin)
            except ValueError:
                print("❌ Invalid pin number")
    else:
        print("Usage:")
        print(f"  {sys.argv[0]} <pin_number>  # Test specific pin")
        print(f"  {sys.argv[0]} scan          # Scan all common pins")
        print("\nTesting GPIO 6 by default...")
        test_gpio_pin(6)