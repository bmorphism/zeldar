#!/usr/bin/env python3
"""Show current fortune for today"""
import sys, os, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from fortune_selector import get_daily_fortune

fortune_type = get_daily_fortune()
today = datetime.date.today().strftime('%Y-%m-%d')
print(f"📅 Today ({today}): {fortune_type}")

fortune_file = f"fortunes/{fortune_type}.txt"
if os.path.exists(fortune_file):
    print(f"📄 Content preview:")
    with open(fortune_file, 'r') as f:
        lines = f.read().strip().split('\n')
        for i, line in enumerate(lines[:5], 1):
            print(f"   {i:2}│ {line}")
        if len(lines) > 5:
            print(f"   ...({len(lines)-5} more lines)")
else:
    print(f"❌ Fortune file not found: {fortune_file}")