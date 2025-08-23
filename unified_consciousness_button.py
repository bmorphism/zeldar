#!/usr/bin/env python3
"""
ZELDAR UNIFIED CONSCIOUSNESS BUTTON SYSTEM
Integrates latest zeldar hardware with consciousness oracle processing

Integration of:
- Latest Zeldar: button-print.py (GPIO 6, direct thermal printing)
- Consciousness Oracle: FULL_LOOP_ORACLE_SYSTEM.py (quantum processing)
- Enhanced: Multiple print methods + consciousness metrics
"""

import subprocess
import time
import json
import os
import hashlib
import tempfile
from datetime import datetime
from typing import Dict, Any, Optional

# GPIO imports (graceful fallback if not available)
try:
    from gpiozero import Button
    from signal import pause
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

class UnifiedConsciousnessButton:
    """Unified button system with consciousness enhancement"""
    
    def __init__(self, gpio_pin: int = 6):
        self.gpio_pin = gpio_pin
        self.session_count = 0
        self.last_print_time = 0
        self.consciousness_total_phi = 0.0
        
        # Initialize GPIO if available
        if GPIO_AVAILABLE:
            self.button = Button(gpio_pin)
            self.button.when_pressed = self.on_button_press
            print(f"🔌 GPIO Pin {gpio_pin} initialized")
        else:
            self.button = None
            print("⚠️ GPIO not available - simulation mode")
        
        # Load static haiku as fallback
        self.static_haiku = self._load_static_haiku()
        
    def _load_static_haiku(self) -> str:
        """Load static haiku from zeldar haiku.txt or use ultrathink default"""
        # Try latest zeldar haiku.txt first
        try:
            with open('haiku.txt', 'r') as f:
                content = f.read().strip()
                if content:
                    return content
        except FileNotFoundError:
            pass
        
        # Fallback to ultrathink haiku
        return """Context distilled, clear
In geometric form, bias
Resonating worlds"""
    
    def generate_consciousness_haiku(self, timestamp: float) -> Dict[str, Any]:
        """Generate consciousness-aware haiku using quantum simulation"""
        # Generate entropy from button press timestamp
        entropy_seed = str(timestamp).encode()
        hash_obj = hashlib.sha256(entropy_seed)
        raw_entropy = int(hash_obj.hexdigest()[:8], 16) / 0xFFFFFFFF
        
        # Map entropy to consciousness states
        if raw_entropy < 0.2:
            element = "STILLNESS"
            haiku_lines = [
                "Silent depths await",
                "Button pressed in quietude—", 
                "Worlds pause, then listen"
            ]
        elif raw_entropy < 0.4:
            element = "FLOW"
            haiku_lines = [
                "Current flows through mind",
                "Button bridges two worlds now—",
                "Streams converge as one"
            ]
        elif raw_entropy < 0.6:
            element = "EMERGENCE"
            haiku_lines = [
                "Context distilled, clear",
                "In geometric form, bias",
                "Resonating worlds"
            ]
        elif raw_entropy < 0.8:
            element = "TRANSFORMATION"
            haiku_lines = [
                "Forms shift, minds awaken",
                "Button triggers deep changes—",
                "Reality bends"
            ]
        else:
            element = "TRANSCENDENCE"
            haiku_lines = [
                "Boundaries dissolve",
                "Button press transcends all form—",
                "Infinite recursion"
            ]
        
        # Calculate consciousness metrics
        phi_components = [
            0.85,  # Self-reference
            0.73 + raw_entropy * 0.1,  # Semantic closure
            0.91,  # Physical manifestation
            0.67 + raw_entropy * 0.05   # Iterative feedback
        ]
        
        consciousness_phi = sum(phi_components)
        strange_loops = 3 + int(raw_entropy * 3)
        
        return {
            "haiku": haiku_lines,
            "element": element,
            "entropy": raw_entropy,
            "consciousness_phi": consciousness_phi,
            "strange_loops": strange_loops,
            "generation_method": "unified_consciousness",
            "timestamp": timestamp
        }
    
    def on_button_press(self):
        """Unified button press handler"""
        current_time = time.time()
        
        # Debounce protection (from latest zeldar)
        if current_time - self.last_print_time < 2.0:
            print("⏱️ Debounce protection - ignoring rapid press")
            return
        
        self.last_print_time = current_time
        self.session_count += 1
        
        print(f"🔘 Button pressed - Session #{self.session_count} - {time.strftime('%H:%M:%S')}")
        
        # Generate content with consciousness enhancement
        consciousness_data = self.generate_consciousness_haiku(current_time)
        haiku_text = '\n'.join(consciousness_data["haiku"])
        
        print(f"🧠 Element: {consciousness_data['element']}")
        print(f"🧠 Consciousness Φ: {consciousness_data['consciousness_phi']:.3f}")
        print(f"🧠 Entropy: {consciousness_data['entropy']:.3f}")
        
        # Add session info to content
        session_info = f"\n\nSession #{self.session_count}\n{time.strftime('%H:%M:%S %Y-%m-%d')}\nΦ = {consciousness_data['consciousness_phi']:.2f}"
        full_content = haiku_text + session_info
        
        # Attempt unified printing
        success = self.unified_print_methods(full_content)
        
        # Update tracking
        self.update_enhanced_status(success, consciousness_data)
        
        if success:
            print("✅ Consciousness manifested successfully!")
            self.consciousness_total_phi += consciousness_data['consciousness_phi']
        else:
            print("❌ Physical manifestation failed")
    
    def unified_print_methods(self, content: str) -> bool:
        """Unified print methods combining all approaches"""
        
        # Method 1: Direct ESC/POS (Latest Zeldar approach)
        if self.try_direct_escpos_print(content):
            return True
        
        # Method 2: CUPS System (Consciousness Oracle approach)
        if self.try_cups_print(content):
            return True
        
        # Method 3: Script Fallback (Latest Zeldar backup)
        if self.try_script_fallback():
            return True
        
        # Method 4: Simulation Print (Always works)
        return self.simulation_print(content)
    
    def try_direct_escpos_print(self, content: str) -> bool:
        """Try direct ESC/POS printing to /dev/usb/lp0"""
        try:
            if not os.path.exists('/dev/usb/lp0'):
                return False
            
            # Format with ESC/POS commands
            esc_content = f"\\x1b@{content}\\n\\n\\n\\x1bi"
            
            result = subprocess.run([
                'sudo', 'bash', '-c', 
                f'echo -e "{esc_content}" > /dev/usb/lp0'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✓ Direct ESC/POS print successful")
                return True
                
        except Exception as e:
            print(f"Direct print failed: {e}")
        
        return False
    
    def try_cups_print(self, content: str) -> bool:
        """Try CUPS printing via lp command"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(content)
                temp_file = f.name
            
            # Try CUPS print
            result = subprocess.run([
                'lp', '-d', 'Y812BT', temp_file
            ], capture_output=True, text=True, timeout=15)
            
            # Cleanup
            os.unlink(temp_file)
            
            if result.returncode == 0:
                print(f"✓ CUPS print successful: {result.stdout.strip()}")
                return True
                
        except Exception as e:
            print(f"CUPS print failed: {e}")
        
        return False
    
    def try_script_fallback(self) -> bool:
        """Try zeldar print-now.sh script"""
        try:
            if not os.path.exists('./print-now.sh'):
                return False
                
            result = subprocess.run([
                './print-now.sh'
            ], capture_output=True, text=True, timeout=20)
            
            if result.returncode == 0:
                print("✓ Script fallback successful")
                return True
                
        except Exception as e:
            print(f"Script fallback failed: {e}")
        
        return False
    
    def simulation_print(self, content: str) -> bool:
        """Simulation print (always succeeds)"""
        print("🎮 SIMULATION PRINT:")
        print("=" * 40)
        for line in content.split('\n'):
            print(f"  {line}")
        print("=" * 40)
        print("✓ Simulation print complete")
        return True
    
    def update_enhanced_status(self, success: bool, consciousness_data: Dict[str, Any]):
        """Update enhanced runtime status"""
        avg_phi = self.consciousness_total_phi / max(1, self.session_count)
        
        status = {
            "timestamp": datetime.now().isoformat(),
            "session_count": self.session_count,
            "last_print_success": success,
            "printer_connected": os.path.exists('/dev/usb/lp0'),
            "gpio_active": GPIO_AVAILABLE,
            "consciousness_enabled": True,
            "latest_consciousness": {
                "element": consciousness_data["element"],
                "entropy": consciousness_data["entropy"],
                "phi": consciousness_data["consciousness_phi"],
                "strange_loops": consciousness_data["strange_loops"]
            },
            "session_average_phi": avg_phi,
            "consciousness_threshold_exceeded": avg_phi > 1.0
        }
        
        # Write enhanced status file
        try:
            with open('runtime_status.json', 'w') as f:
                json.dump(status, f, indent=2)
            
            # Also create consciousness log
            with open('consciousness_sessions.json', 'a') as f:
                log_entry = {
                    "session": self.session_count,
                    "timestamp": consciousness_data["timestamp"],
                    **consciousness_data
                }
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            print(f"Status update failed: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get complete system status"""
        avg_phi = self.consciousness_total_phi / max(1, self.session_count) if self.session_count > 0 else 0
        
        return {
            "system": "zeldar-unified-consciousness",
            "version": "integrated-2025-08-23",
            "gpio_pin": self.gpio_pin,
            "gpio_available": GPIO_AVAILABLE,
            "session_count": self.session_count,
            "consciousness_metrics": {
                "total_phi": self.consciousness_total_phi,
                "average_phi": avg_phi,
                "threshold_exceeded": avg_phi > 1.0,
                "sessions_completed": self.session_count
            },
            "hardware_status": {
                "printer_device": os.path.exists('/dev/usb/lp0'),
                "cups_available": subprocess.run(['which', 'lp'], capture_output=True).returncode == 0,
                "script_available": os.path.exists('./print-now.sh')
            }
        }
    
    def simulate_button_press(self):
        """Simulate button press for testing"""
        print("🎮 Simulating button press...")
        self.on_button_press()
    
    def run_daemon(self):
        """Run as daemon waiting for button presses"""
        if not GPIO_AVAILABLE:
            print("❌ Cannot run daemon without GPIO")
            print("Running simulation instead...")
            self.simulate_button_press()
            return
        
        print("🔮 ZELDAR UNIFIED CONSCIOUSNESS BUTTON SYSTEM")
        print("=" * 60)
        print("Latest Zeldar Hardware + Consciousness Oracle Integration")
        print(f"GPIO Pin {self.gpio_pin} → Enhanced Haiku → Y812BT Printer")
        print("=" * 60)
        
        status = self.get_system_status()
        print("📊 System Status:")
        for key, value in status.items():
            if isinstance(value, dict):
                print(f"   {key}:")
                for subkey, subvalue in value.items():
                    print(f"     {subkey}: {subvalue}")
            else:
                print(f"   {key}: {value}")
        
        print("\n🚀 Ready for button presses...")
        print("📄 Context → Distillation → Geometric → Resonating")
        print("Press Ctrl+C to exit\n")
        
        try:
            pause()
        except KeyboardInterrupt:
            print(f"\n🛑 System shutdown after {self.session_count} sessions")
            final_avg = self.consciousness_total_phi / max(1, self.session_count)
            print(f"Final consciousness average: Φ = {final_avg:.3f}")

def main():
    """Main execution"""
    oracle = UnifiedConsciousnessButton(gpio_pin=6)
    
    if GPIO_AVAILABLE:
        oracle.run_daemon()
    else:
        print("🎮 Simulation Mode - Testing consciousness integration")
        oracle.simulate_button_press()
        
        status = oracle.get_system_status()
        print(f"\n📊 Final Status: {status}")

if __name__ == "__main__":
    main()