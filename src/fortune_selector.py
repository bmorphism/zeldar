#!/usr/bin/env python3
"""
Fortune selection logic separated from GPIO hardware
Allows testing without hardware dependencies
"""

import datetime

def get_daily_fortune():
    """Select fortune based on current date during Burning Man 2025"""
    today = datetime.date.today()
    
    fortune_map = {
        # Burning Man 2025 Schedule
        datetime.date(2025, 8, 24): "sunday_opening_fortunes",
        datetime.date(2025, 8, 25): "monday_sequence", 
        datetime.date(2025, 8, 26): "tuesday_sequence",
        datetime.date(2025, 8, 27): "wednesday_sequence",
        datetime.date(2025, 8, 28): "thursday_sequence",
        datetime.date(2025, 8, 29): "friday_sequence",
        datetime.date(2025, 8, 30): "saturday_closing",
        datetime.date(2025, 8, 31): "special_fortunes"  # Upload later
    }
    
    return fortune_map.get(today, "default_fortune")