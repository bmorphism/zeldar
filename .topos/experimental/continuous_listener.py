#!/usr/bin/env python3
"""
Continuous GPIO State Monitor
Tests both pull-up and pull-down to determine correct wiring
"""
import time
from gpiozero import DigitalInputDevice

def test_both_configs():
    """Test both pull configurations to see which gives stable readings"""
    
    print("🔧 Testing both pull configurations...")
    
    configs = [
        ("PULL-UP", True),
        ("PULL-DOWN", False)
    ]
    
    for name, pull_up in configs:
        print(f"\n📌 Testing {name} configuration:")
        
        try:
            pin = DigitalInputDevice(6, pull_up=pull_up)
            
            # Sample for 3 seconds, count changes
            start_time = time.time()
            last_value = pin.value
            changes = 0
            readings = []
            
            while time.time() - start_time < 3.0:
                current_value = pin.value
                readings.append(current_value)
                
                if current_value != last_value:
                    changes += 1
                    last_value = current_value
                    
                time.sleep(0.01)  # 10ms sampling
                
            # Analysis
            total_readings = len(readings)
            high_count = sum(readings)
            low_count = total_readings - high_count
            
            print(f"  📊 Results over 3 seconds:")
            print(f"     Total readings: {total_readings}")
            print(f"     HIGH (1) readings: {high_count} ({high_count/total_readings*100:.1f}%)")
            print(f"     LOW (0) readings: {low_count} ({low_count/total_readings*100:.1f}%)")
            print(f"     State changes: {changes}")
            print(f"     Changes per second: {changes/3:.1f}")
            
            if changes < 10:
                print(f"  ✅ {name}: STABLE - likely correct configuration")
            else:
                print(f"  ❌ {name}: UNSTABLE - likely wrong configuration")
                
            pin.close()
            
        except Exception as e:
            print(f"  ❌ {name}: Error - {e}")
            
    print(f"\n🎯 Press button now and watch for value changes...")

if __name__ == "__main__":
    test_both_configs()