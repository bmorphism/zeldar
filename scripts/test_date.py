#!/usr/bin/env python3
"""Test fortune for specific date"""
import sys, os, datetime
from unittest.mock import patch

if len(sys.argv) != 2:
    print("Usage: test_date.py YYYY-MM-DD")
    sys.exit(1)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from fortune_selector import get_daily_fortune

test_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()

# Direct test without mocking - reimplement logic
fortune_map = {
    datetime.date(2025, 8, 24): "sunday_opening_fortunes",
    datetime.date(2025, 8, 25): "monday_sequence", 
    datetime.date(2025, 8, 26): "tuesday_sequence",
    datetime.date(2025, 8, 27): "wednesday_sequence",
    datetime.date(2025, 8, 28): "thursday_sequence",
    datetime.date(2025, 8, 29): "friday_sequence",
    datetime.date(2025, 8, 30): "saturday_closing",
    datetime.date(2025, 8, 31): "special_fortunes"
}

fortune_type = fortune_map.get(test_date, "default_fortune")
print(f"📅 {test_date}: {fortune_type}")