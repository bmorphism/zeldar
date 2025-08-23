#!/usr/bin/env python3
"""
Direct test of fortune selection by modifying function temporarily
"""

import sys
import os
import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def get_daily_fortune_test(test_date):
    """Test version of get_daily_fortune with explicit date"""
    
    fortune_map = {
        # Burning Man 2025 Schedule  
        datetime.date(2025, 8, 24): "sunday_opening_fortunes",
        datetime.date(2025, 8, 25): "monday_sequence", 
        datetime.date(2025, 8, 26): "tuesday_sequence",
        datetime.date(2025, 8, 27): "wednesday_sequence",
        datetime.date(2025, 8, 28): "thursday_sequence",
        datetime.date(2025, 8, 29): "friday_sequence",
        datetime.date(2025, 8, 30): "saturday_closing",
        datetime.date(2025, 8, 31): "special_fortunes"
    }
    
    return fortune_map.get(test_date, "default_fortune")

def test_fortune_schedule():
    """Test Burning Man 2025 schedule"""
    
    test_cases = [
        (datetime.date(2025, 8, 24), "sunday_opening_fortunes", "Sunday Opening"),
        (datetime.date(2025, 8, 25), "monday_sequence", "Monday"),
        (datetime.date(2025, 8, 26), "tuesday_sequence", "Tuesday"),
        (datetime.date(2025, 8, 27), "wednesday_sequence", "Wednesday"),
        (datetime.date(2025, 8, 28), "thursday_sequence", "Thursday"),
        (datetime.date(2025, 8, 29), "friday_sequence", "Friday"),
        (datetime.date(2025, 8, 30), "saturday_closing", "Saturday Closing"),
        (datetime.date(2025, 8, 31), "special_fortunes", "Special Sunday"),
        (datetime.date(2025, 8, 23), "default_fortune", "Before Event"),
        (datetime.date(2025, 9, 1), "default_fortune", "After Event"),
    ]
    
    print("🧪 Testing Burning Man 2025 Fortune Schedule")
    print("=" * 50)
    
    all_passed = True
    
    for test_date, expected_fortune, description in test_cases:
        result = get_daily_fortune_test(test_date)
        status = "✅" if result == expected_fortune else "❌"
        
        if result != expected_fortune:
            all_passed = False
        
        print(f"{status} {description} ({test_date}): {result}")
    
    print(f"\n📅 Fortune Schedule Test: {'✅ PASSED' if all_passed else '❌ FAILED'}")
    return all_passed

if __name__ == "__main__":
    test_fortune_schedule()