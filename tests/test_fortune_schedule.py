#!/usr/bin/env python3
"""
Test fortune schedule system with mock dates
Prevents actual printing during development testing
"""

import os
import sys
import datetime
from unittest.mock import patch, MagicMock

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fortune_selector import get_daily_fortune

def test_burning_man_fortune_schedule():
    """Test each day of Burning Man 2025 fortune selection"""
    
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
    
    for test_date, expected_fortune, description in test_cases:
        with patch('fortune_selector.datetime.date') as mock_date:
            mock_date.today.return_value = test_date
            
            result = get_daily_fortune()
            status = "✅" if result == expected_fortune else "❌"
            
            print(f"{status} {description} ({test_date}): {result}")
    
    print("\n📅 Fortune Schedule Test Complete")
    return True

def test_print_script_integration():
    """Test print script with different fortune types (no actual printing)"""
    
    fortune_types = [
        "sunday_opening_fortunes",
        "monday_sequence", 
        "tuesday_sequence",
        "wednesday_sequence",
        "thursday_sequence",
        "friday_sequence",
        "saturday_closing",
        "special_fortunes",
        "default_fortune"
    ]
    
    print("\n🖨️  Testing Print Script Fortune Loading")
    print("=" * 40)
    
    for fortune_type in fortune_types:
        fortune_file = f"/home/zeldar/burningman/fortunes/{fortune_type}.txt"
        
        if os.path.exists(fortune_file):
            with open(fortune_file, 'r') as f:
                content = f.read().strip()
                lines = len(content.split('\n'))
                chars = len(content)
                status = "✅"
        else:
            lines = 0 
            chars = 0
            status = "⚠️ "
        
        print(f"{status} {fortune_type}: {lines} lines, {chars} chars")
    
    print("\n📄 Fortune File Test Complete")
    return True

if __name__ == "__main__":
    print("🎯 Burning Man Fortune Schedule Testing")
    print("No actual printing will occur during testing")
    print("")
    
    test_burning_man_fortune_schedule()
    test_print_script_integration()
    
    print("\n🎉 All fortune schedule tests completed!")