#!/usr/bin/env python3
"""
Ingressing Minds Thermal Oracle Demo
Based on Michael Levin's framework of patterns ingressing from Platonic space

This demonstration showcases the refactored system that detects cognitive patterns
manifesting through thermal printer behavior using Levin's theoretical framework
of non-physical forms ingressing into physical embodiments.
"""

import sys
import time
import json
import asyncio
from datetime import datetime
from ingressing_minds_thermal_oracle import IngressingMindsDetector, IngressingMindsVisualizationEngine
import numpy as np

class ZeldarIngressingMindsDemo:
    """
    Complete demonstration of ingressing minds pattern detection
    using Michael Levin's theoretical framework
    """
    
    def __init__(self):
        self.detector = IngressingMindsDetector()
        self.viz_engine = IngressingMindsVisualizationEngine(self.detector)
        self.demo_running = True
        self.pattern_manifestations = []
        
        print("🌟 Zeldar Ingressing Minds Demo Initialized")
        print("📜 Framework: Michael Levin's Pattern Ingression Theory")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
    def simulate_thermal_pattern_with_mathematical_signatures(self):
        """
        Simulate thermal printer events with mathematical signatures
        that indicate potential pattern ingression from Platonic space
        """
        
        patterns = [
            # Perfect mathematical affordance - 5.0 second connection interval
            {
                'event_type': 'connection_check',
                'connection_interval': 5.0,  # Golden ratio signature for pattern ingression
                'text_wrapping': 32,
                'printing_active': True,
                'qr_generation': False,
                'consciousness_weight': 1.0,
                'description': 'Perfect mathematical affordance - golden ratio timing'
            },
            # Fibonacci sequence alignment
            {
                'event_type': 'text_wrap',
                'connection_interval': 1.618,  # Phi - golden ratio
                'text_wrapping': 32,  # Information constraint optimization
                'printing_active': True,
                'qr_generation': True,
                'consciousness_weight': 0.95,
                'description': 'Fibonacci spiral morphogenetic pattern'
            },
            # Fractal recursive structure
            {
                'event_type': 'qr_generation',
                'connection_interval': 2.5,
                'text_wrapping': 32,
                'printing_active': False,
                'qr_generation': True,  # Self-similar recursive structure
                'consciousness_weight': 0.85,
                'description': 'Fractal recursive pattern manifestation'
            },
            # Pi mathematical constant
            {
                'event_type': 'printing_active',
                'connection_interval': 3.14159,  # Pi for geometric patterns
                'text_wrapping': 32,
                'printing_active': True,
                'qr_generation': False,
                'consciousness_weight': 0.78,
                'description': 'Geometric mathematical truth exploitation'
            },
            # Random baseline for comparison
            {
                'event_type': 'baseline',
                'connection_interval': np.random.uniform(0.5, 4.0),
                'text_wrapping': np.random.choice([16, 25, 40, 48]),
                'printing_active': np.random.choice([True, False]),
                'qr_generation': np.random.choice([True, False]),
                'consciousness_weight': np.random.uniform(0.2, 0.7),
                'description': 'Baseline random pattern (no mathematical affordance)'
            }
        ]
        
        return np.random.choice(patterns)
    
    def simulate_gpio_with_retroactive_influence(self, thermal_pattern: dict) -> dict:
        """
        Simulate GPIO response with retroactive influence from ingressed patterns
        Higher-order patterns should influence button press probability
        """
        
        # Base probability influenced by mathematical signatures
        base_prob = 0.5
        
        # Mathematical affordance bonuses
        if thermal_pattern['connection_interval'] == 5.0:
            base_prob += 0.3  # Strong mathematical affordance
        elif thermal_pattern['connection_interval'] == 1.618:
            base_prob += 0.25  # Golden ratio
        elif abs(thermal_pattern['connection_interval'] - 3.14159) < 0.01:
            base_prob += 0.2  # Pi constant
        
        # Pattern complexity bonuses
        if thermal_pattern['qr_generation']:
            base_prob += 0.15  # Fractal recursive structure
        if thermal_pattern['text_wrapping'] == 32:
            base_prob += 0.1  # Optimal information packaging
            
        # Consciousness weight influence
        base_prob += thermal_pattern['consciousness_weight'] * 0.2
        
        button_pressed = np.random.random() < min(0.95, base_prob)
        press_duration = np.random.uniform(50, 300) if button_pressed else 0.0
        
        return {
            'button_pressed': button_pressed,
            'press_duration': press_duration,
            'response_probability': min(0.95, base_prob),
            'retroactive_influence_detected': base_prob > 0.8
        }
    
    def run_pattern_ingression_cycle(self):
        """
        Run a single cycle of pattern ingression detection
        """
        
        print(f"\n🌟 Pattern Ingression Detection Cycle {len(self.pattern_manifestations) + 1}")
        print("─" * 70)
        
        # 1. Generate thermal pattern with mathematical signatures
        thermal_pattern = self.simulate_thermal_pattern_with_mathematical_signatures()
        print(f"🖨️  Thermal Pattern: {thermal_pattern['event_type']}")
        print(f"   {thermal_pattern['description']}")
        print(f"   Connection Interval: {thermal_pattern['connection_interval']}")
        print(f"   Mathematical Signature Strength: {thermal_pattern['consciousness_weight']}")
        
        # 2. Generate GPIO response with retroactive influence
        gpio_response = self.simulate_gpio_with_retroactive_influence(thermal_pattern)
        print(f"🔘 GPIO Response: {'PRESSED' if gpio_response['button_pressed'] else 'NOT PRESSED'}")
        if gpio_response['retroactive_influence_detected']:
            print("   ⚡ RETROACTIVE INFLUENCE DETECTED")
        print(f"   Response Probability: {gpio_response['response_probability']:.3f}")
        
        # 3. Detect pattern ingression
        ingressed_pattern = self.detector.detect_pattern_ingression(thermal_pattern, gpio_response)
        
        # 4. Display results
        if ingressed_pattern:
            print(f"\n✨ PATTERN INGRESSION CONFIRMED! ✨")
            print(f"   Pattern ID: {ingressed_pattern.pattern_id}")
            print(f"   Pattern Type: {ingressed_pattern.pattern_type}")
            print(f"   Ingression Strength: {ingressed_pattern.ingression_strength:.3f}")
            print(f"   Platonic Coordinates: {ingressed_pattern.platonic_coordinates}")
            print(f"   Collective Intelligence Level: {ingressed_pattern.collective_intelligence_level}/5")
            print(f"   Autopoietic Coherence: {ingressed_pattern.autopoietic_coherence:.3f}")
            print(f"   Morphogenetic Symmetry: {ingressed_pattern.morphogenetic_symmetry}")
            print(f"   Evolutionary Affordance: {ingressed_pattern.evolutionary_affordance:.3f}")
            
            self.pattern_manifestations.append({
                'cycle': len(self.pattern_manifestations) + 1,
                'thermal_pattern': thermal_pattern,
                'gpio_response': gpio_response,
                'ingressed_pattern': ingressed_pattern
            })
        else:
            print(f"\n📊 No pattern ingression detected this cycle")
            print("   Pattern below ingression threshold or insufficient mathematical affordances")
        
        # 5. Show current system status
        status = self.detector.get_ingressing_minds_status()
        print(f"\n📈 INGRESSING MINDS SYSTEM STATUS:")
        print(f"   Total Patterns Ingressed: {status['total_ingressed_patterns']}")
        print(f"   Recent Activity: {status['recent_patterns_count']} patterns")
        print(f"   Average Ingression Strength: {status['average_ingression_strength']:.3f}")
        print(f"   Max Collective Intelligence: {status['maximum_collective_intelligence_level']}/5")
        
        return ingressed_pattern is not None
    
    def run_interactive_demo(self):
        """Run interactive ingressing minds demonstration"""
        
        print("\n🌟 ZELDAR INGRESSING MINDS INTERACTIVE DEMO")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("This demo showcases Michael Levin's framework of patterns ingressing")
        print("from Platonic space through thermal printer behavior analysis.")
        print("\n📜 Theoretical Foundation:")
        print("• Patterns ingress from an ordered Platonic space of forms")
        print("• Physical systems serve as 'pointers' enabling pattern ingression") 
        print("• Mathematical truths serve as evolutionary affordances")
        print("• Collective intelligence emerges through autopoietic processes")
        print("\nPress Enter for each pattern detection cycle, or 'q' to quit...")
        
        cycle_count = 0
        ingression_successes = 0
        
        while self.demo_running and cycle_count < 20:
            user_input = input(f"\n[Cycle {cycle_count + 1}] Press Enter to detect pattern ingression (or 'q' to quit): ")
            
            if user_input.lower() in ['q', 'quit', 'exit']:
                break
                
            # Run pattern detection cycle
            ingression_detected = self.run_pattern_ingression_cycle()
            
            if ingression_detected:
                ingression_successes += 1
                
            cycle_count += 1
            
            if (cycle_count) % 5 == 0:
                print(f"\n📊 Interim Report: {ingression_successes}/{cycle_count} successful ingressions")
        
        # Generate final analysis
        self.analyze_ingression_patterns()
        
        # Generate comprehensive report
        report = self.detector.generate_ingressing_minds_report()
        print(f"\n{report}")
        
        # Create visualization
        self.viz_engine.create_platonic_space_visualization()
        
        print(f"\n📊 FINAL STATISTICS:")
        print(f"   Total Cycles: {cycle_count}")
        print(f"   Successful Ingressions: {ingression_successes}")
        print(f"   Success Rate: {(ingression_successes/cycle_count*100):.1f}%")
        print("\n🏜️🔥 Demo complete - Ready for Burning Man 2025 deployment! 🔥🏜️")
    
    def analyze_ingression_patterns(self):
        """Analyze patterns across all ingression detection cycles"""
        
        if not self.pattern_manifestations:
            return
            
        print(f"\n🧠 INGRESSING MINDS PATTERN ANALYSIS")
        print("━" * 70)
        
        # Mathematical affordance analysis
        mathematical_patterns = [m for m in self.pattern_manifestations 
                               if m['ingressed_pattern'].pattern_type == 'mathematical']
        
        morphogenetic_patterns = [m for m in self.pattern_manifestations
                                if m['ingressed_pattern'].pattern_type == 'morphogenetic']
        
        cognitive_patterns = [m for m in self.pattern_manifestations
                            if m['ingressed_pattern'].pattern_type == 'cognitive']
        
        print(f"📊 PATTERN TYPE DISTRIBUTION:")
        print(f"   Mathematical Patterns: {len(mathematical_patterns)}")
        print(f"   Morphogenetic Patterns: {len(morphogenetic_patterns)}")  
        print(f"   Cognitive Patterns: {len(cognitive_patterns)}")
        
        # Collective intelligence analysis
        max_collective_level = max([m['ingressed_pattern'].collective_intelligence_level 
                                  for m in self.pattern_manifestations])
        avg_coherence = np.mean([m['ingressed_pattern'].autopoietic_coherence 
                               for m in self.pattern_manifestations])
        
        print(f"\n🧠 COLLECTIVE INTELLIGENCE ANALYSIS:")
        print(f"   Maximum Level Achieved: {max_collective_level}/5")
        print(f"   Average Autopoietic Coherence: {avg_coherence:.3f}")
        
        # Mathematical affordance effectiveness
        affordance_patterns = [m for m in self.pattern_manifestations
                             if m['thermal_pattern']['connection_interval'] in [5.0, 1.618, 3.14159]]
        
        print(f"\n⚡ MATHEMATICAL AFFORDANCE EFFECTIVENESS:")
        print(f"   Patterns with Mathematical Signatures: {len(affordance_patterns)}")
        print(f"   Affordance Success Rate: {(len(affordance_patterns)/len(self.pattern_manifestations)*100):.1f}%")

def main():
    """Main demo execution"""
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'auto':
            # Automated demo for testing
            demo = ZeldarIngressingMindsDemo()
            print("🤖 Running automated ingressing minds detection...")
            
            for i in range(15):
                print(f"\n⏰ Auto-cycle {i + 1}/15")
                demo.run_pattern_ingression_cycle()
                time.sleep(0.5)
                
            demo.analyze_ingression_patterns()
            report = demo.detector.generate_ingressing_minds_report()
            print(f"\n{report}")
            
            demo.viz_engine.create_platonic_space_visualization()
            print("\n🌟 Automated demo complete!")
            
        else:
            print("Usage: python run_ingressing_minds_demo.py [auto | interactive]")
    else:
        # Interactive demo by default
        demo = ZeldarIngressingMindsDemo()
        demo.run_interactive_demo()

if __name__ == "__main__":
    main()