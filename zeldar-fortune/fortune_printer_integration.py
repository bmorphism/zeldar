#!/usr/bin/env python3
"""
Fortune-Printer Integration System

Integrates the three fortune types with the thermal printer system,
providing electromagnetic correlation and printing optimization.
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fortune_types import FortuneGenerator, FortuneType
from thermal_printer import ThermalPrinter

class ZeldarFortuneOracle:
    """
    Complete fortune oracle system integrating:
    - 3 fortune types with electromagnetic signatures
    - Thermal printer with type-specific formatting
    - EMF correlation and loop closure detection
    """
    
    def __init__(self, printer_device: str = "/dev/usb/lp0"):
        self.generator = FortuneGenerator()
        self.printer = ThermalPrinter(device_path=printer_device)
        self.logger = logging.getLogger('ZeldarOracle')
        
        # Session tracking
        self.session_counter = 0
        self.fortune_history = []
        self.type_usage_stats = {t.value: 0 for t in FortuneType}
        
        # EMF monitoring
        self.current_emf = 0.0
        self.emf_history = []
        
        self.logger.info("Zeldar Fortune Oracle initialized")
    
    def select_optimal_fortune_type(self, current_emf: float = None, 
                                  user_preference: str = None) -> FortuneType:
        """Select optimal fortune type based on EMF conditions and preferences"""
        
        if user_preference:
            # Direct user selection
            try:
                return FortuneType(user_preference)
            except ValueError:
                self.logger.warning(f"Invalid fortune type: {user_preference}")
        
        # EMF-based selection if available
        if current_emf is not None:
            self.current_emf = current_emf
            
            # Calculate resonance with each type
            resonances = {}
            for fortune_type in FortuneType:
                analysis = self.generator.analyze_electromagnetic_coupling(fortune_type, current_emf)
                resonances[fortune_type] = analysis['resonance_strength']
            
            # Select type with highest resonance
            optimal_type = max(resonances, key=resonances.get)
            
            if resonances[optimal_type] > 0.6:
                self.logger.info(f"EMF-guided selection: {optimal_type.value} (resonance: {resonances[optimal_type]:.3f})")
                return optimal_type
        
        # Fallback: balanced distribution with slight randomization
        distribution = self.generator.get_type_distribution()
        current_stats = self._get_usage_statistics()
        
        # Weight against overused types
        weights = {}
        for fortune_type in FortuneType:
            ideal_ratio = distribution[fortune_type.value]
            actual_ratio = current_stats.get(fortune_type.value, 0)
            
            # Boost underused types, reduce overused types
            if actual_ratio < ideal_ratio:
                weights[fortune_type] = 1.5  # Boost underused
            elif actual_ratio > ideal_ratio * 1.3:
                weights[fortune_type] = 0.7  # Reduce overused
            else:
                weights[fortune_type] = 1.0  # Normal weight
        
        # Weighted random selection
        import random
        choices = []
        for fortune_type, weight in weights.items():
            choices.extend([fortune_type] * int(weight * 10))
        
        selected = random.choice(choices)
        self.logger.info(f"Distribution-balanced selection: {selected.value}")
        return selected
    
    async def generate_and_print_fortune(self, fortune_type: FortuneType = None, 
                                       current_emf: float = None) -> Dict:
        """Generate and print fortune with full electromagnetic correlation"""
        
        # Select fortune type
        if fortune_type is None:
            fortune_type = self.select_optimal_fortune_type(current_emf)
        
        # Generate fortune
        fortune = self.generator.generate_fortune(fortune_type)
        
        # Update session tracking
        self.session_counter += 1
        session_id = f"ZELDAR_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.session_counter:03d}"
        fortune['session_id'] = session_id
        
        # Analyze EMF coupling if available
        if current_emf is not None:
            coupling_analysis = self.generator.analyze_electromagnetic_coupling(
                fortune_type, current_emf
            )
            fortune['emf_coupling'] = coupling_analysis
        
        # Format for thermal printer
        formatted_content = self._format_fortune_for_printer(fortune)
        
        # Connect to printer if not connected
        if not self.printer.is_connected():
            if not self.printer.connect():
                self.logger.error("Failed to connect to printer")
                return {'success': False, 'error': 'Printer connection failed', 'fortune': fortune}
        
        # Print the fortune
        print_success = self.printer.print_raw_text(formatted_content)
        
        if print_success:
            # Update statistics
            self.type_usage_stats[fortune_type.value] += 1
            self.fortune_history.append(fortune)
            
            # Log the successful print
            self.logger.info(f"Fortune printed: {fortune_type.value} - Session {session_id}")
            
            # Save to file for tracking
            self._save_fortune_record(fortune)
        
        return {
            'success': print_success,
            'fortune': fortune,
            'session_id': session_id,
            'printer_connected': self.printer.is_connected()
        }
    
    def _format_fortune_for_printer(self, fortune: Dict) -> str:
        """Format fortune for thermal printer with type-specific styling"""
        
        fortune_type = fortune['type']
        text = fortune['text']
        metadata = fortune['metadata']
        signature = fortune['electromagnetic_signature']
        
        # Type-specific headers
        headers = {
            'temporal_inversion': '⏰ TEMPORAL INVERSION ORACLE',
            'information_force': '⚡ INFORMATION FORCE ORACLE',
            'categorical_morphism': '🔗 CATEGORICAL MORPHISM ORACLE'
        }
        
        # Type-specific symbols
        symbols = {
            'temporal_inversion': '⟲ ⟳ ⟲',
            'information_force': '⚡ ∿ ⚡',
            'categorical_morphism': '→ ≅ ←'
        }
        
        header = headers.get(fortune_type, '🔮 ZELDAR ORACLE')
        symbol = symbols.get(fortune_type, '✦ ✧ ✦')
        
        # Format the complete ticket
        formatted = f"""
═══════════════════════════════════
{header}
═══════════════════════════════════

{symbol}

{self._wrap_text_for_printer(text, 35)}

{symbol}

SESSION: {fortune['session_id']}
TYPE: {fortune_type.replace('_', ' ').title()}
TIME: {fortune['datetime'][:19]}

═══════════════════════════════════
EMF SIGNATURE
───────────────────────────────────
Frequency: {signature['base_frequency']:.1f} Hz
Thermal: {signature['thermal_intensity']:.2f}
Phase: {signature['phase_modulation']:.3f}

INFORMATION METRICS
───────────────────────────────────
Density: {metadata['information_density']:.3f}
Complexity: {metadata['complexity_score']:.3f}
Markers: {metadata['temporal_markers']}
Words: {metadata['word_count']}

═══════════════════════════════════
"The future prints the past"
═══════════════════════════════════

"""
        return formatted.strip()
    
    def _wrap_text_for_printer(self, text: str, width: int = 35) -> str:
        """Wrap text for thermal printer width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= width:
                current_line = current_line + " " + word if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return "\n".join(lines)
    
    def _save_fortune_record(self, fortune: Dict):
        """Save fortune record to file"""
        records_file = Path("/tmp/zeldar_fortune_records.json")
        
        # Load existing records
        records = []
        if records_file.exists():
            try:
                with open(records_file, 'r') as f:
                    records = json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load fortune records: {e}")
        
        # Add new record
        records.append(fortune)
        
        # Keep only last 100 records
        records = records[-100:]
        
        # Save updated records
        try:
            with open(records_file, 'w') as f:
                json.dump(records, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Failed to save fortune record: {e}")
    
    def _get_usage_statistics(self) -> Dict[str, float]:
        """Get current usage statistics as ratios"""
        total = sum(self.type_usage_stats.values())
        if total == 0:
            return {t.value: 0.0 for t in FortuneType}
        
        return {
            fortune_type: count / total 
            for fortune_type, count in self.type_usage_stats.items()
        }
    
    def get_session_report(self) -> Dict:
        """Get comprehensive session report"""
        current_stats = self._get_usage_statistics()
        ideal_distribution = self.generator.get_type_distribution()
        
        return {
            'total_fortunes_printed': self.session_counter,
            'type_distribution': {
                'actual': current_stats,
                'ideal': ideal_distribution
            },
            'recent_fortunes': self.fortune_history[-5:],  # Last 5 fortunes
            'current_emf': self.current_emf,
            'printer_connected': self.printer.is_connected(),
            'session_start': datetime.now().isoformat()
        }
    
    def cleanup(self):
        """Cleanup printer connection"""
        try:
            self.printer.disconnect()
            self.logger.info("Oracle cleanup completed")
        except Exception as e:
            self.logger.warning(f"Cleanup error: {e}")

async def run_interactive_oracle():
    """Interactive oracle session"""
    print("🔮 ZELDAR INTERACTIVE FORTUNE ORACLE")
    print("=" * 50)
    
    oracle = ZeldarFortuneOracle()
    
    try:
        while True:
            print(f"\n📊 Session: {oracle.session_counter} fortunes printed")
            
            # Show type distribution
            stats = oracle._get_usage_statistics()
            for fortune_type, ratio in stats.items():
                print(f"  {fortune_type.replace('_', ' ').title()}: {ratio:.1%}")
            
            print(f"\n🔮 Fortune Types:")
            print("  1. Temporal Inversion (time paradox)")  
            print("  2. Information Force (energy dynamics)")
            print("  3. Categorical Morphism (structural patterns)")
            print("  4. Auto-select optimal type")
            print("  5. Show session report")
            print("  6. Exit")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == '1':
                result = await oracle.generate_and_print_fortune(FortuneType.TEMPORAL_INVERSION)
            elif choice == '2':
                result = await oracle.generate_and_print_fortune(FortuneType.INFORMATION_FORCE)
            elif choice == '3':
                result = await oracle.generate_and_print_fortune(FortuneType.CATEGORICAL_MORPHISM)
            elif choice == '4':
                # Auto-select with simulated EMF
                import random
                simulated_emf = random.uniform(30, 300)  # Simulate EMF reading
                result = await oracle.generate_and_print_fortune(current_emf=simulated_emf)
                print(f"📡 Simulated EMF: {simulated_emf:.1f} Hz")
            elif choice == '5':
                report = oracle.get_session_report()
                print(f"\n📈 SESSION REPORT")
                print(f"Total fortunes: {report['total_fortunes_printed']}")
                print(f"Printer connected: {report['printer_connected']}")
                continue
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please select 1-6.")
                continue
            
            if 'result' in locals():
                if result['success']:
                    print(f"✅ Fortune printed successfully!")
                    print(f"Session ID: {result['session_id']}")
                    print(f"Type: {result['fortune']['type'].replace('_', ' ').title()}")
                    print(f"Text: {result['fortune']['text'][:80]}...")
                else:
                    print(f"❌ Printing failed: {result.get('error', 'Unknown error')}")
                    print(f"Fortune text: {result['fortune']['text']}")
    
    except KeyboardInterrupt:
        print("\n🛑 Oracle session interrupted")
    
    finally:
        oracle.cleanup()
        print("Oracle session ended.")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🌟 ZELDAR FORTUNE ORACLE SYSTEM")
    print("Three types of electromagnetic fortune generation")
    print()
    
    asyncio.run(run_interactive_oracle())