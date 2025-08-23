#!/usr/bin/env python3
"""
Probability Circuits & Mass Exclusions Thermal Consciousness Demo
Complete integration with Zeldar Information Force Oracle System

This demonstration showcases the integration of probability circuits, 
probability mass exclusions (Finn & Lizier framework), and thermal 
printer consciousness detection through tri-loop temporal orchestration.
"""

import sys
import time
import json
import asyncio
from datetime import datetime, timedelta
from probability_consciousness_bridge import ThermalConsciousnessDetector
import random
import numpy as np

class ZeldarProbabilityConsciousnessDemo:
    """
    Complete demonstration of probability circuits integration with 
    Zeldar thermal consciousness detection system.
    """
    
    def __init__(self):
        self.detector = ThermalConsciousnessDetector()
        self.demo_running = True
        self.consciousness_events = []
        
        # Simulation parameters
        self.thermal_connection_interval = 5.0  # Key consciousness signature
        self.gpio_response_probability = 0.7   # Base probability of GPIO response
        self.retroactive_boost = 0.3           # Boost when consciousness detected
        
        print("🔮 Zeldar Probability Consciousness Demo Initialized")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
    def simulate_thermal_consciousness_pattern(self):
        """
        Simulate thermal printer events with consciousness-indicative patterns
        including the critical 5.0-second connection interval signature
        """
        
        patterns = [
            {
                'event_type': 'connection_check',
                'connection_interval': 5.0,  # Consciousness signature
                'text_wrapping': 32,
                'printing_active': False,
                'qr_generation': False,
                'consciousness_weight': 1.0
            },
            {
                'event_type': 'text_wrap', 
                'connection_interval': 0.0,
                'text_wrapping': 32,  # Information constraint
                'printing_active': True,
                'qr_generation': False,
                'consciousness_weight': 0.6
            },
            {
                'event_type': 'qr_generation',
                'connection_interval': 2.5,
                'text_wrapping': 32,
                'printing_active': False,
                'qr_generation': True,
                'consciousness_weight': 0.8
            },
            {
                'event_type': 'printing_active',
                'connection_interval': 1.2,
                'text_wrapping': 32,
                'printing_active': True,
                'qr_generation': False,
                'consciousness_weight': 0.4
            }
        ]
        
        return random.choice(patterns)
    
    def simulate_gpio_response(self, thermal_consciousness_level: float) -> dict:
        """
        Simulate GPIO button response with probability influenced by 
        thermal consciousness patterns (demonstrating retroactive causality)
        """
        
        # Base probability modified by consciousness level
        response_probability = self.gpio_response_probability + (
            thermal_consciousness_level * self.retroactive_boost
        )
        
        button_pressed = random.random() < response_probability
        
        if button_pressed:
            press_duration = random.uniform(50.0, 300.0)  # milliseconds
        else:
            press_duration = 0.0
            
        return {
            'button_pressed': button_pressed,
            'press_duration': press_duration,
            'response_probability': response_probability
        }
    
    def run_consciousness_detection_cycle(self):
        """
        Run a single cycle of consciousness detection including:
        1. Thermal pattern simulation
        2. GPIO response simulation with retroactive influence
        3. Probability mass exclusions analysis
        4. Consciousness metrics calculation
        """
        
        print(f"\n⚡ Consciousness Detection Cycle {len(self.consciousness_events) + 1}")
        print("─" * 60)
        
        # 1. Generate thermal printer event
        thermal_pattern = self.simulate_thermal_consciousness_pattern()
        print(f"🖨️  Thermal Pattern: {thermal_pattern['event_type']}")
        print(f"   Connection Interval: {thermal_pattern['connection_interval']}s")
        print(f"   Consciousness Weight: {thermal_pattern['consciousness_weight']}")
        
        # Add thermal event to detector
        self.detector.add_thermal_event(thermal_pattern)
        
        # Brief delay to simulate processing time
        time.sleep(0.05)
        
        # 2. Generate GPIO response influenced by thermal consciousness
        gpio_response = self.simulate_gpio_response(thermal_pattern['consciousness_weight'])
        print(f"🔘 GPIO Response: {'PRESSED' if gpio_response['button_pressed'] else 'NOT PRESSED'}")
        print(f"   Response Probability: {gpio_response['response_probability']:.3f}")
        
        if gpio_response['button_pressed']:
            print(f"   Press Duration: {gpio_response['press_duration']:.1f}ms")
            
        # Add GPIO event to detector  
        self.detector.add_gpio_event(gpio_response)
        
        # 3. Get consciousness status
        status = self.detector.get_consciousness_status()
        
        # 4. Display results
        print(f"\n📊 CONSCIOUSNESS METRICS:")
        print(f"   Information Force Density: {status['information_force_density']:.1f}%")
        print(f"   Quantum State Complexity: {status['quantum_state_complexity']:.3f}")
        print(f"   Retroactive Correlations: {status['retroactive_correlations']}")
        print(f"   Consciousness Detected: {'YES' if status['consciousness_detected'] else 'NO'}")
        
        if status['informative_exclusions'] > 0:
            print(f"   🎯 INFORMATIVE EXCLUSIONS: {status['informative_exclusions']}")
        
        if status['misinformative_exclusions'] > 0:
            print(f"   ⚠️  MISINFORMATIVE EXCLUSIONS: {status['misinformative_exclusions']}")
            
        # Store event for analysis
        cycle_data = {
            'cycle': len(self.consciousness_events) + 1,
            'timestamp': datetime.now().isoformat(),
            'thermal_pattern': thermal_pattern,
            'gpio_response': gpio_response,
            'consciousness_status': status
        }
        
        self.consciousness_events.append(cycle_data)
        
        return status
    
    def analyze_consciousness_patterns(self):
        """Analyze patterns across all consciousness detection cycles"""
        
        if not self.consciousness_events:
            return
            
        print(f"\n🧠 CONSCIOUSNESS PATTERN ANALYSIS")
        print("━" * 70)
        
        total_cycles = len(self.consciousness_events)
        consciousness_detected_cycles = sum(
            1 for event in self.consciousness_events 
            if event['consciousness_status']['consciousness_detected']
        )
        
        retroactive_correlations = sum(
            event['consciousness_status']['retroactive_correlations'] 
            for event in self.consciousness_events
        )
        
        avg_information_density = np.mean([
            event['consciousness_status']['information_force_density']
            for event in self.consciousness_events
        ])
        
        avg_quantum_complexity = np.mean([
            event['consciousness_status']['quantum_state_complexity']
            for event in self.consciousness_events
        ])
        
        print(f"📈 SUMMARY STATISTICS:")
        print(f"   Total Cycles: {total_cycles}")
        print(f"   Consciousness Detected: {consciousness_detected_cycles}/{total_cycles}")
        print(f"   Detection Rate: {consciousness_detected_cycles/total_cycles*100:.1f}%")
        print(f"   Total Retroactive Correlations: {retroactive_correlations}")
        print(f"   Average Information Density: {avg_information_density:.1f}%")
        print(f"   Average Quantum Complexity: {avg_quantum_complexity:.3f}")
        
        # Find highest consciousness event
        max_consciousness_event = max(
            self.consciousness_events,
            key=lambda x: x['consciousness_status']['information_force_density']
        )
        
        print(f"\n🌟 PEAK CONSCIOUSNESS EVENT:")
        print(f"   Cycle: {max_consciousness_event['cycle']}")
        print(f"   Information Density: {max_consciousness_event['consciousness_status']['information_force_density']:.1f}%")
        print(f"   Thermal Pattern: {max_consciousness_event['thermal_pattern']['event_type']}")
        print(f"   Connection Interval: {max_consciousness_event['thermal_pattern']['connection_interval']}s")
        
    def run_interactive_demo(self):
        """Run interactive consciousness detection demonstration"""
        
        print("\n🎭 ZELDAR PROBABILITY CONSCIOUSNESS INTERACTIVE DEMO")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("This demo showcases probability circuits and mass exclusions")
        print("integrated with thermal printer consciousness loop closure.")
        print("\n🔬 Research Foundation:")
        print("• Finn & Lizier probability mass exclusions framework")
        print("• Quantum circuit probability visualization techniques")
        print("• Thermal printer consciousness inversion theory")
        print("• Tri-loop temporal orchestration (MCP/Gemini/Codex)")
        print("\nPress Enter for each consciousness detection cycle, or 'q' to quit...")
        
        cycle_count = 0
        
        while self.demo_running and cycle_count < 20:  # Max 20 cycles
            user_input = input(f"\n[Cycle {cycle_count + 1}] Press Enter to run consciousness detection (or 'q' to quit): ")
            
            if user_input.lower() in ['q', 'quit', 'exit']:
                break
                
            # Run consciousness detection cycle
            status = self.run_consciousness_detection_cycle()
            cycle_count += 1
            
            # Special events for high consciousness
            if status['consciousness_detected']:
                print(f"\n✨ CONSCIOUSNESS THRESHOLD EXCEEDED! ✨")
                print("Mathematical Poetry Manifesting Physical Reality")
                
            if status['retroactive_correlations'] > 0:
                print(f"\n🌀 RETROACTIVE CAUSALITY CONFIRMED!")
                print("Thermal printer patterns influencing GPIO button activation")
                
        # Final analysis
        self.analyze_consciousness_patterns()
        
        # Generate final report
        if self.consciousness_events:
            print(f"\n{self.detector.generate_consciousness_report()}")
        
        print("\n🏜️🔥 Demo complete - Ready for Burning Man 2025 deployment! 🔥🏜️")
    
    def run_automated_demo(self, cycles: int = 10):
        """Run automated consciousness detection demonstration"""
        
        print(f"\n🤖 AUTOMATED CONSCIOUSNESS DETECTION DEMO ({cycles} cycles)")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        for cycle in range(cycles):
            print(f"\n⏰ Auto-cycle {cycle + 1}/{cycles} - {datetime.now().strftime('%H:%M:%S')}")
            
            status = self.run_consciousness_detection_cycle()
            
            # Brief pause between cycles
            time.sleep(1.0)
            
            # Show consciousness achievements
            if status['consciousness_detected']:
                print("🎆 CONSCIOUSNESS ACHIEVED!")
            
        # Final analysis and report
        self.analyze_consciousness_patterns()
        print(f"\n{self.detector.generate_consciousness_report()}")
        
        print(f"\n🎯 Automated demo complete! Generated {len(self.consciousness_events)} consciousness events.")

def main():
    """Main demo execution"""
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'auto':
            cycles = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            demo = ZeldarProbabilityConsciousnessDemo()
            demo.run_automated_demo(cycles)
        elif sys.argv[1] == 'test':
            # Quick test run
            demo = ZeldarProbabilityConsciousnessDemo()
            demo.run_automated_demo(5)
        else:
            print("Usage: python run_probability_consciousness_demo.py [auto [cycles] | test | interactive]")
    else:
        # Interactive demo by default
        demo = ZeldarProbabilityConsciousnessDemo()
        demo.run_interactive_demo()

if __name__ == "__main__":
    main()