#!/usr/bin/env python3
"""Test script for robot launcher with immediate feedback"""

import asyncio
import sys
from pathlib import Path

async def test_robot_launch():
    """Test the robot launch system with debugging output"""
    print("🔮🎪🖨️ FORTUNE TELLING ROBOT TEST")
    print("="*50)
    
    # Check required files
    oracle_script = Path('/home/zeldar/burningman/BURNING_MAN_INTERACTIVE_ORACLE.py')
    button_script = Path('/home/zeldar/burningman/button_oracle_bridge.py')
    audio_script = Path('/home/zeldar/burningman/generate_voice_prompts.py')
    
    print("📁 File Check:")
    print(f"  Oracle: {'✅' if oracle_script.exists() else '❌'} {oracle_script}")
    print(f"  Button: {'✅' if button_script.exists() else '❌'} {button_script}")
    print(f"  Audio:  {'✅' if audio_script.exists() else '❌'} {audio_script}")
    
    print("\n🔄 Testing async subprocess creation...")
    
    if oracle_script.exists():
        try:
            # Test subprocess creation without actually running
            print("  Creating oracle subprocess...")
            process = await asyncio.create_subprocess_exec(
                'python3', '-c', 'print("Oracle test"); import time; time.sleep(2)',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Read output
            stdout, stderr = await process.communicate()
            print(f"  Oracle test output: {stdout.decode().strip()}")
            if stderr:
                print(f"  Oracle test error: {stderr.decode().strip()}")
                
        except Exception as e:
            print(f"  ❌ Oracle subprocess test failed: {e}")
    
    print("✅ Robot launch test complete")

if __name__ == "__main__":
    asyncio.run(test_robot_launch())