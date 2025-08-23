#!/usr/bin/env python3
"""List all available fortune files"""
import os
import glob

print("📚 Available fortunes:")
for fortune_file in sorted(glob.glob("fortunes/*.txt")):
    name = os.path.basename(fortune_file).replace('.txt', '')
    try:
        with open(fortune_file, 'r') as f:
            content = f.read()
            lines = len(content.split('\n'))
            chars = len(content)
    except:
        lines = 0
        chars = 0
    
    print(f"   {name:<25} {lines:2d} lines, {chars:3d} chars")