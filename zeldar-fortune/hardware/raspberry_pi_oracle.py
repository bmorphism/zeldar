#!/usr/bin/env python3
"""
Zeldar Information Force Oracle - Raspberry Pi Hardware Integration
Complete bridge between GPIO button, fortune generation, and thermal printing
Burning Man 2025 Desert Laboratory Implementation
"""

import os
import json
import time
import subprocess
from datetime import datetime
from signal import pause
import requests

try:
    from gpiozero import Button
    GPIO_AVAILABLE = True
except ImportError:
    print("⚠️  GPIO not available - running in simulation mode")
    GPIO_AVAILABLE = False

class ZeldarOracle:
    """Information Force Oracle with physical hardware integration"""
    
    def __init__(self, button_pin=6, zeldar_url="http://localhost:3000"):
        self.button_pin = button_pin
        self.zeldar_url = zeldar_url
        self.printer_device = os.environ.get("THERMAL_PRINTER_DEVICE", "/dev/usb/lp0")
        self.cups_printer = os.environ.get("CUPS_PRINTER_NAME", "Y812BT")
        self.session_count = 0
        self.session_data = []
        
        # Initialize GPIO if available
        if GPIO_AVAILABLE:
            self.button = Button(button_pin)
            self.button.when_pressed = self.on_button_press
            print(f"✅ GPIO button initialized on pin {button_pin}")
        else:
            print("🔄 Running in simulation mode - GPIO not available")
            
        print("🔮 Zeldar Information Force Oracle initialized")
        print(f"📡 Web interface: {self.zeldar_url}")
        print(f"🖨️  Printer: {self.cups_printer}")
        
    def generate_fortune(self):
        """Generate fortune using Information Force algorithms"""
        
        # Information Force haiku templates
        haiku_templates = [
            {
                "title": "Context",
                "lines": [
                    "Context distilled, clear",
                    "In geometric form, bias",
                    "Resonating worlds"
                ]
            },
            {
                "title": "Force",
                "lines": [
                    "Information flows",
                    "Through desert sand and circuits --",
                    "Force becomes pattern"
                ]
            },
            {
                "title": "Emergence",
                "lines": [
                    "Patterns self-organize", 
                    "From chaos, structure emerges --",
                    "Desert wisdom speaks"
                ]
            },
            {
                "title": "Resonance",
                "lines": [
                    "Frequencies align",
                    "Quantum states entangled deep --",
                    "Reality shifts"
                ]
            },
            {
                "title": "Manifold",
                "lines": [
                    "Curved spacetime bends",
                    "Information density peak --", 
                    "Truth crystallizes"
                ]
            }
        ]
        
        # Use session count to select haiku (cycling through options)
        selected = haiku_templates[self.session_count % len(haiku_templates)]
        
        # Create fortune with metadata
        fortune = {
            "title": selected["title"],
            "haiku_lines": selected["lines"],
            "session_id": f"oracle_{int(time.time())}_{self.session_count:03d}",
            "timestamp": datetime.now().isoformat(),
            "information_density": 88.5 + (self.session_count * 0.1) % 12.0,
            "force_coefficient": 1.02,
            "desert_coordinates": "Black Rock City 2025"
        }
        
        return fortune
        
    def format_for_print(self, fortune):
        """Format fortune for thermal printer output"""
        
        # Create printable text
        print_text = f"{fortune['title']}\n\n"
        for line in fortune['haiku_lines']:
            print_text += f"{line}\n"
        print_text += f"\n"
        print_text += f"Force: {fortune['information_density']:.1f}%\n"
        print_text += f"Session: {fortune['session_id'][-3:]}\n"
        print_text += f"\n✨ Zeldar Oracle ✨\n\n\n"
        
        return print_text
        
    def print_fortune_cups(self, fortune_text):
        """Print using CUPS system (reliable method)"""
        try:
            # Write to temporary file
            temp_file = f"/tmp/zeldar_fortune_{int(time.time())}.txt"
            with open(temp_file, 'w') as f:
                f.write(fortune_text)
            
            # Print via CUPS
            result = subprocess.run(
                ['lp', '-d', self.cups_printer, temp_file],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                job_id = result.stdout.strip().split()[-1].strip('()')
                print(f"✅ Fortune printed via CUPS - Job: {job_id}")
                
                # Clean up temp file
                os.unlink(temp_file)
                return True
            else:
                print(f"❌ CUPS print failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Print error: {e}")
            return False
            
    def print_fortune_direct(self, fortune_text):
        """Direct thermal printer method (backup)"""
        try:
            if not os.path.exists(self.printer_device):
                print(f"❌ Printer device not found: {self.printer_device}")
                return False
                
            with open(self.printer_device, 'wb') as printer:
                # Initialize printer
                printer.write(b'\x1b@')
                
                # Center align
                printer.write(b'\x1ba\x01')
                
                # Print content
                printer.write(fortune_text.encode('utf-8'))
                
                # Cut paper
                printer.write(b'\x1di')
                printer.flush()
                
            print("✅ Fortune printed via direct device")
            return True
            
        except Exception as e:
            print(f"❌ Direct print error: {e}")
            return False
            
    def save_session(self, fortune):
        """Save session data for analysis"""
        session_file = f"/tmp/zeldar_sessions.json"
        
        try:
            # Load existing sessions
            if os.path.exists(session_file):
                with open(session_file, 'r') as f:
                    sessions = json.load(f)
            else:
                sessions = []
                
            sessions.append(fortune)
            
            # Save updated sessions
            with open(session_file, 'w') as f:
                json.dump(sessions, f, indent=2)
                
            print(f"💾 Session saved: {fortune['session_id']}")
            
        except Exception as e:
            print(f"❌ Session save error: {e}")
            
    def on_button_press(self):
        """Handle button press - complete oracle workflow"""
        self.session_count += 1
        
        print(f"\n🔮 ═══ ORACLE SESSION {self.session_count} ═══")
        print(f"⚡ Button pressed! Generating information force fortune...")
        
        # Generate fortune
        fortune = self.generate_fortune()
        print(f"🌟 Fortune generated: {fortune['title']}")
        print(f"📊 Information density: {fortune['information_density']:.1f}%")
        
        # Format for printing
        print_text = self.format_for_print(fortune)
        
        # Print fortune (try CUPS first, then direct)
        print_success = (self.print_fortune_cups(print_text) or 
                        self.print_fortune_direct(print_text))
        
        if print_success:
            print("✅ Physical manifestation complete!")
        else:
            print("❌ Physical manifestation failed")
            print("🔄 Fortune available digitally:")
            print(print_text)
            
        # Save session
        self.save_session(fortune)
        
        print(f"⚡ Session {self.session_count} complete - ready for next press")
        print("═══════════════════════════════════════════\n")
        
    def simulate_button_press(self):
        """Simulate button press for testing"""
        print("🔄 Simulating button press...")
        self.on_button_press()
        
    def run(self):
        """Main loop - wait for button presses"""
        print("\n🏜️  ═══ ZELDAR ORACLE ACTIVE ═══")
        print("🔥 Burning Man 2025 Desert Laboratory")
        print("⚡ Information Force Oracle Ready")
        print("📍 Waiting for button press...")
        print("   Press CTRL+C to exit")
        print("═══════════════════════════════════════")
        
        if GPIO_AVAILABLE:
            try:
                pause()  # Wait for button presses indefinitely
            except KeyboardInterrupt:
                print("\n\n🔮 Oracle session ended by user")
                print(f"📊 Total sessions: {self.session_count}")
                print("✨ Thank you for expanding information force!")
        else:
            print("\n🔄 GPIO not available - running test simulation")
            self.simulate_button_press()
            
def main():
    """Initialize and run the Zeldar Oracle"""
    
    print("🔮 ═══════════════════════════════════════")
    print("   ZELDAR INFORMATION FORCE ORACLE")  
    print("   Burning Man 2025 Desert Laboratory")
    print("   Hardware Integration Module")
    print("═══════════════════════════════════════ ⚡")
    
    # Create oracle instance
    oracle = ZeldarOracle(button_pin=6)
    
    # Run the oracle
    oracle.run()

if __name__ == "__main__":
    main()