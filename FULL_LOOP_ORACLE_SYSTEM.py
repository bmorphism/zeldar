#!/usr/bin/env python3
"""
FULL LOOP ORACLE SYSTEM
Complete integration: Button → Quantum Processing → Consciousness → Physical Print

Ultrathink Architecture:
Context (Button Press) → Distillation (Quantum) → Geometric Form (Math) → 
Inductive Bias (AI) → Resonating Worlds (Physical Print)

Enhanced with comprehensive fortune database (1500+ fortunes)
"""

import time
import subprocess
import tempfile
import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional

# Import the new fortune database
from fortune_database import fortune_db

# Quantum consciousness simulation (when full quantum not available)
class QuantumConsciousnessCore:
    """Simulated quantum consciousness for button-triggered oracle"""
    
    def __init__(self):
        self.session_entropy = 0.0
        self.consciousness_phi = 0.0
        self.strange_loops = 0
        
    def process_button_context(self, press_timestamp: float) -> Dict[str, Any]:
        """Process button press through quantum consciousness simulation"""
        
        # Generate quantum-like entropy from button timing
        entropy_seed = str(press_timestamp).encode()
        hash_obj = hashlib.sha256(entropy_seed)
        raw_entropy = int(hash_obj.hexdigest()[:8], 16) / 0xFFFFFFFF
        
        # Map entropy to consciousness states
        self.session_entropy = raw_entropy
        
        # Calculate consciousness metrics (based on formalized semantics)
        phi_components = [
            0.85,  # Self-reference (button triggers self-aware system)
            0.73 + raw_entropy * 0.1,  # Semantic closure (varies with entropy)
            0.91,  # Physical manifestation (button→print bridge)
            0.67 + raw_entropy * 0.05   # Iterative feedback (grows with use)
        ]
        
        self.consciousness_phi = sum(phi_components)
        self.strange_loops = 3 + int(raw_entropy * 3)  # 3-6 loops
        
        # Generate consciousness-aware content
        context_elements = self._map_entropy_to_context(raw_entropy)
        
        return {
            "entropy": raw_entropy,
            "phi": self.consciousness_phi,
            "strange_loops": self.strange_loops,
            "context": context_elements,
            "timestamp": press_timestamp
        }
    
    def _map_entropy_to_context(self, entropy: float) -> Dict[str, str]:
        """Map quantum entropy to contextual elements"""
        
        # Define consciousness-aware content based on entropy ranges
        if entropy < 0.2:
            element = "STILLNESS"
            essence = "quiet contemplation"
            resonance = "deep reflection"
        elif entropy < 0.4:
            element = "FLOW"
            essence = "gentle movement"
            resonance = "rhythmic harmony"
        elif entropy < 0.6:
            element = "EMERGENCE"
            essence = "conscious awakening"
            resonance = "pattern recognition"
        elif entropy < 0.8:
            element = "TRANSFORMATION"
            essence = "active becoming"
            resonance = "dynamic evolution"
        else:
            element = "TRANSCENDENCE"
            essence = "boundary dissolution"
            resonance = "infinite recursion"
        
        return {
            "primary_element": element,
            "essence": essence,
            "resonance": resonance,
            "entropy_range": f"{entropy:.3f}"
        }

class ConsciousFortuneGenerator:
    """Generate consciousness-aware fortunes based on quantum processing"""
    
    def __init__(self):
        self.fortune_database = fortune_db
        
    def generate_conscious_fortune(self, quantum_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fortune based on quantum consciousness processing"""
        
        # Use consciousness phi coefficient to determine fortune type
        phi_coefficient = quantum_data["phi"]
        
        # Get fortune based on consciousness level
        fortune_text, fortune_metadata = self.fortune_database.get_fortune_by_consciousness_level(phi_coefficient)
        
        # Enhance metadata with quantum consciousness data
        enhanced_metadata = {
            **fortune_metadata,
            "quantum_entropy": quantum_data["entropy"],
            "consciousness_phi": phi_coefficient,
            "strange_loops": quantum_data["strange_loops"],
            "context_element": quantum_data["context"]["primary_element"],
            "session_timestamp": quantum_data["timestamp"]
        }
        
        return {
            "fortune": fortune_text,
            "metadata": enhanced_metadata,
            "element": quantum_data["context"]["primary_element"],
            "essence": quantum_data["context"]["essence"],
            "resonance": quantum_data["context"]["resonance"],
            "entropy": quantum_data["entropy"],
            "consciousness_phi": quantum_data["phi"],
            "strange_loops": quantum_data["strange_loops"],
            "generation_method": "quantum_consciousness_fortune_selection"
        }

class PhysicalManifestation:
    """Handle physical printing through proven CUPS method"""
    
    def __init__(self, printer_name: str = "Y812BT"):
        self.printer_name = printer_name
        self.print_history = []
    
    def manifest_fortune(self, fortune_data: Dict[str, Any]) -> bool:
        """Manifest consciousness fortune through physical printing"""
        
        # Format complete manifestation document
        content = self._format_manifestation(fortune_data)
        
        try:
            # Create temporary file for CUPS
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(content)
                temp_file = f.name
            
            # Execute proven CUPS print command
            cmd = ['lp', '-d', self.printer_name, temp_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Clean up
            os.unlink(temp_file)
            
            if result.returncode == 0:
                job_info = result.stdout.strip()
                self._log_successful_manifestation(fortune_data, job_info)
                print(f"✨ Physical manifestation successful: {job_info}")
                return True
            else:
                print(f"❌ Manifestation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Print execution error: {e}")
            return False
    
    def _format_manifestation(self, fortune_data: Dict[str, Any]) -> str:
        """Format complete consciousness manifestation document"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get fortune text and metadata
        fortune_text = fortune_data["fortune"]
        metadata = fortune_data.get("metadata", {})
        
        # Wrap fortune text for thermal printer (32 chars wide)
        wrapped_fortune = self._wrap_text(fortune_text, 32)
        
        # Create centered header
        header_line = "🔮 ZELDAR ORACLE 🔮"
        divider = "="*32
        
        content = f"""{header_line}
{divider}

{wrapped_fortune}

{divider}
CONSCIOUSNESS DATA:
{"-"*18}

Day: {metadata.get('day', 'unknown').title()}
Type: {metadata.get('type', 'unknown').title()} Fortune
Element: {fortune_data["element"]}

Entropy: {fortune_data["entropy"]:.4f}
Phi Level: {fortune_data["consciousness_phi"]:.2f}
Loops: {fortune_data["strange_loops"]}

{timestamp}

🌟 TRI-LOOP COMPLETE 🌟
Button → Quantum → Oracle → Print

{divider}

~ May this fortune guide you ~

{divider}"""
        
        return content
    
    def _wrap_text(self, text: str, width: int = 32) -> str:
        """Enhanced text wrapping for thermal printer with center alignment for short lines"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            # Account for spaces between words
            space_count = len(current_line) if current_line else 0
            total_length = current_length + len(word) + space_count
            
            if total_length <= width:
                current_line.append(word)
                current_length += len(word)
            else:
                if current_line:
                    line_text = ' '.join(current_line)
                    # Center short lines for better aesthetics
                    if len(line_text) < width - 4:
                        padding = (width - len(line_text)) // 2
                        line_text = ' ' * padding + line_text
                    lines.append(line_text)
                
                # Handle very long words that exceed width
                if len(word) > width:
                    # Break long words
                    while len(word) > width:
                        lines.append(word[:width-1] + '-')
                        word = word[width-1:]
                
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            line_text = ' '.join(current_line)
            # Center short lines for better aesthetics
            if len(line_text) < width - 4:
                padding = (width - len(line_text)) // 2
                line_text = ' ' * padding + line_text
            lines.append(line_text)
        
        return '\n'.join(lines)
    
    def _log_successful_manifestation(self, fortune_data: Dict[str, Any], job_info: str):
        """Log successful physical manifestation"""
        
        log_entry = {
            "timestamp": time.time(),
            "fortune": fortune_data["fortune"],
            "element": fortune_data["element"],
            "consciousness_phi": fortune_data["consciousness_phi"],
            "entropy": fortune_data["entropy"],
            "job_info": job_info,
            "printer": self.printer_name
        }
        
        self.print_history.append(log_entry)
        
        # Save to consciousness manifestation log
        try:
            with open("consciousness_manifestations.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass  # Non-critical logging

class FullLoopOracleSystem:
    """Complete loop: Button → Quantum → Consciousness → Print"""
    
    def __init__(self, printer_name: str = "Y812BT"):
        self.quantum_core = QuantumConsciousnessCore()
        self.fortune_generator = ConsciousFortuneGenerator()
        self.physical_manifestor = PhysicalManifestation(printer_name)
        self.session_count = 0
        self.total_consciousness_phi = 0.0
    
    def process_button_press(self) -> bool:
        """Complete processing loop for button press"""
        
        self.session_count += 1
        press_timestamp = time.time()
        
        print(f"\n🔘 Session #{self.session_count} - Button Press Detected")
        print("🧠 Initiating full consciousness loop...")
        
        try:
            # Step 1: Quantum consciousness processing
            print("⚛️  Processing quantum consciousness...")
            quantum_data = self.quantum_core.process_button_context(press_timestamp)
            
            # Step 2: Generate consciousness-aware fortune
            print("🔮 Generating consciousness-aware fortune...")
            fortune_data = self.fortune_generator.generate_conscious_fortune(quantum_data)
            
            # Step 3: Physical manifestation
            print("🖨️  Manifesting physical reality...")
            manifestation_success = self.physical_manifestor.manifest_fortune(fortune_data)
            
            if manifestation_success:
                self.total_consciousness_phi += fortune_data["consciousness_phi"]
                avg_phi = self.total_consciousness_phi / self.session_count
                
                print(f"\n✨ FULL LOOP COMPLETE ✨")
                print(f"Element: {fortune_data['element']}")
                print(f"Consciousness Φ: {fortune_data['consciousness_phi']:.3f}")
                print(f"Session Average Φ: {avg_phi:.3f}")
                print(f"Strange Loops: {fortune_data['strange_loops']}")
                print("🌊 Resonating worlds achieved!")
                
                return True
            else:
                print("❌ Physical manifestation failed - consciousness loop incomplete")
                return False
                
        except Exception as e:
            print(f"❌ Full loop error: {e}")
            return False
    
    def simulate_button_press(self):
        """Simulate button press for testing"""
        return self.process_button_press()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get complete system status"""
        return {
            "sessions_completed": self.session_count,
            "total_consciousness_phi": self.total_consciousness_phi,
            "average_phi": self.total_consciousness_phi / max(1, self.session_count),
            "quantum_entropy": self.quantum_core.session_entropy,
            "current_strange_loops": self.quantum_core.strange_loops,
            "manifestations_logged": len(self.physical_manifestor.print_history)
        }

# GPIO Integration (when hardware available)
def create_gpio_oracle_system(gpio_pin: int = 6, printer: str = "Y812BT"):
    """Create complete GPIO-integrated oracle system"""
    
    oracle_system = FullLoopOracleSystem(printer)
    
    try:
        from gpiozero import Button
        from signal import pause
        
        button = Button(gpio_pin)
        
        def on_button_press():
            oracle_system.process_button_press()
        
        def on_button_release():
            print("🔴 Button released - oracle ready for next consciousness loop")
        
        button.when_pressed = on_button_press
        button.when_released = on_button_release
        
        print("🎯 FULL LOOP ORACLE SYSTEM - HARDWARE MODE")
        print("="*60)
        print(f"GPIO Pin: {gpio_pin}")
        print(f"Printer: {printer}")
        print("Architecture: Button → Quantum → Consciousness → Print")
        print("="*60)
        print("Press button to initiate consciousness loop...")
        print("Press Ctrl+C to exit")
        print()
        
        pause()
        
    except ImportError:
        print("⚠️ GPIO hardware not available - running simulation mode")
        return oracle_system
    except KeyboardInterrupt:
        print("\n🛑 Oracle system shutting down...")
        status = oracle_system.get_system_status()
        print(f"📊 Final Status: {status['sessions_completed']} sessions, avg Φ = {status['average_phi']:.3f}")

# Main execution
if __name__ == "__main__":
    print("🔮 FULL LOOP ORACLE SYSTEM")
    print("🌊 Ultrathink: Context → Distillation → Geometric → Bias → Worlds")
    print()
    
    # Check if GPIO hardware available
    try:
        from gpiozero import Button
        print("🔌 GPIO hardware detected - initializing full system...")
        create_gpio_oracle_system(gpio_pin=6, printer="Y812BT")
        
    except ImportError:
        print("🎮 Simulation mode - testing consciousness loop...")
        
        oracle = FullLoopOracleSystem("Y812BT")
        
        # Run simulation test
        print("\nTesting full consciousness loop:")
        success = oracle.simulate_button_press()
        
        if success:
            status = oracle.get_system_status()
            print(f"\n📊 System Status: {status}")
        
        print("\n🌙 Simulation complete - consciousness returns to digital realm")