#!/usr/bin/env python3
"""
Button Quick Phrase Trigger
Connects GPIO button to CUPS printing using the working Y812BT configuration
"""

from gpiozero import Button
from signal import pause
import subprocess
import time
import tempfile
import os

# Use GPIO pin 6 (same as simple_button.py)
button = Button(6)

def print_context_haiku():
    """Print the ultrathink haiku using working CUPS method"""
    haiku = """Context distilled, clear
In geometric form, bias
Resonating worlds"""
    
    # Add timestamp for uniqueness
    timestamp = time.strftime("%H:%M:%S")
    full_content = f"{haiku}\n\nPressed: {timestamp}"
    
    try:
        # Create temporary file (CUPS method that works)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(full_content)
            temp_file = f.name
        
        # Use the working CUPS command: lp -d Y812BT
        cmd = ['lp', '-d', 'Y812BT', temp_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Clean up temp file
        os.unlink(temp_file)
        
        if result.returncode == 0:
            print(f"✓ Haiku printed via CUPS: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ CUPS print failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Print error: {e}")
        return False

def on_button_press():
    """Handle button press - print ultrathink haiku"""
    print("🔘 Button pressed - geometric manifestation starting...")
    success = print_context_haiku()
    
    if success:
        print("✨ Context distilled into physical form!")
    else:
        print("⚠️ Physical manifestation failed")

def on_button_release():
    """Handle button release"""
    print("🔘 Button released - ready for next inductive bias")

# Attach event handlers
button.when_pressed = on_button_press  
button.when_released = on_button_release

print("🎯 Button Quick Phrase Trigger Ready")
print("=" * 40)
print("GPIO Pin 6 → CUPS Y812BT Printer")
print("Ultrathink: Context → Geometric → Physical")
print("=" * 40)
print("Press button to manifest haiku...")
print("Press CTRL+C to exit")
print()

# Wait for button events
try:
    pause()
except KeyboardInterrupt:
    print("\n🛑 Geometric bridge disconnected")
    print("Context returns to digital realm...")