#!/usr/bin/env python3
import time
from gpiozero import Button

pins_to_test = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

print("🔍 Quick GPIO scan - press button during each test:")
for pin in pins_to_test[:10]:  # Test first 10
    try:
        print(f"Testing GPIO {pin}...", end=" ", flush=True)
        button = Button(pin, pull_up=True, bounce_time=0.1)
        
        detected = False
        start_time = time.time()
        
        def on_press():
            global detected
            detected = True
            
        button.when_pressed = on_press
        
        # Wait 2 seconds
        while time.time() - start_time < 2:
            if detected:
                print("✅ FOUND!")
                button.close()
                exit()
            time.sleep(0.1)
            
        button.close()
        print("❌")
        
    except Exception as e:
        print(f"Error: {e}")
        
print("No button found on tested pins")