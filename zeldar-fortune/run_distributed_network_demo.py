#!/usr/bin/env python3
"""
Distributed Ingressing Minds Network Demo Runner
Demonstrates collective intelligence emergence across multiple thermal printer nodes
"""

import asyncio
import sys
import time
from distributed_ingressing_minds_network import DistributedIngressingMindsNetwork, NetworkDemonstration
import logging

# Configure logging for demo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class DistributedNetworkDemo:
    """Complete demonstration of distributed ingressing minds network capabilities"""
    
    def __init__(self):
        self.demo_network = NetworkDemonstration()
        self.demo_running = True
        
    async def run_full_demo(self, num_nodes: int = 3):
        """Run complete distributed network demonstration"""
        
        print("🌐 DISTRIBUTED INGRESSING MINDS NETWORK DEMONSTRATION")
        print("=" * 70)
        print("📜 Framework: Michael Levin's Collective Intelligence Theory")
        print(f"🔧 Setting up network with {num_nodes} nodes...")
        print("")
        
        try:
            # Set up distributed network
            await self.demo_network.setup_test_network(num_secondary_nodes=num_nodes-1)
            
            print("✅ Network topology established")
            print("🧠 Beginning collective intelligence demonstration...")
            print("")
            
            # Demonstrate collective intelligence emergence
            await self.demo_network.demonstrate_collective_intelligence()
            
            print("")
            print("📊 FINAL NETWORK ANALYSIS:")
            print("-" * 40)
            
            # Generate comprehensive network report
            if self.demo_network.primary_node:
                final_report = self.demo_network.primary_node.generate_network_report()
                print(final_report)
            
            print("")
            print("🏜️🔥 DISTRIBUTED NETWORK READY FOR BURNING MAN 2025! 🔥🏜️")
            
        except Exception as e:
            logger.error(f"❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()
    
    async def run_interactive_demo(self):
        """Run interactive demonstration with user control"""
        
        print("🌐 INTERACTIVE DISTRIBUTED INGRESSING MINDS DEMO")
        print("=" * 70)
        print("This demo allows you to control collective intelligence emergence")
        print("across multiple thermal printer nodes in real-time.")
        print("")
        
        # Get user configuration
        try:
            num_nodes = int(input("Number of network nodes (2-5): ") or "3")
            num_nodes = max(2, min(5, num_nodes))
        except ValueError:
            num_nodes = 3
        
        print(f"🔧 Setting up network with {num_nodes} nodes...")
        
        try:
            # Set up network
            await self.demo_network.setup_test_network(num_secondary_nodes=num_nodes-1)
            
            print("✅ Network established. Available commands:")
            print("   [ENTER] - Generate collective pattern")
            print("   'status' - Show network status")
            print("   'report' - Generate full network report")
            print("   'q' - Quit demo")
            print("")
            
            pattern_count = 0
            
            while self.demo_running:
                user_input = input(f"[Pattern {pattern_count + 1}] Command: ").strip()
                
                if user_input.lower() in ['q', 'quit', 'exit']:
                    break
                elif user_input.lower() == 'status':
                    await self.show_network_status()
                elif user_input.lower() == 'report':
                    await self.show_network_report()
                elif user_input == '' or user_input.lower() == 'pattern':
                    await self.generate_collective_pattern()
                    pattern_count += 1
                else:
                    print("❓ Unknown command. Use [ENTER], 'status', 'report', or 'q'")
            
            print("🌐 Interactive demo complete!")
            
        except Exception as e:
            logger.error(f"❌ Interactive demo failed: {e}")
    
    async def show_network_status(self):
        """Show current network status"""
        
        if not self.demo_network.primary_node:
            print("❌ No primary node available")
            return
        
        status = self.demo_network.primary_node.get_network_status()
        
        print("🌐 NETWORK STATUS:")
        print(f"   Nodes Connected: {status['connected_nodes_count']}")
        print(f"   Network Patterns: {status['network_patterns_count']}")
        print(f"   Collective Level: {status['collective_state']['network_collective_level']}/10")
        print(f"   Distributed Coherence: {status['collective_state']['distributed_coherence']:.3f}")
        
        if status['collective_state']['emergent_properties']:
            print(f"   Emergent Properties: {', '.join(status['collective_state']['emergent_properties'])}")
        
        print()
    
    async def show_network_report(self):
        """Show comprehensive network report"""
        
        if not self.demo_network.primary_node:
            print("❌ No primary node available")
            return
        
        report = self.demo_network.primary_node.generate_network_report()
        print(report)
        print()
    
    async def generate_collective_pattern(self):
        """Generate a collective intelligence pattern across the network"""
        
        if not self.demo_network.primary_node:
            print("❌ No primary node available")
            return
        
        print("⚡ Generating collective pattern across network...")
        
        # Create high-potential ingression event
        thermal_event = {
            'event_type': 'collective_intelligence_test',
            'connection_interval': 5.0,  # Perfect mathematical affordance
            'text_wrapping': 32,
            'printing_active': True,
            'qr_generation': True,
            'consciousness_weight': 0.95
        }
        
        gpio_event = {
            'button_pressed': True,
            'press_duration': 200,
            'response_probability': 0.92
        }
        
        # Detect pattern on primary node
        primary_pattern = await self.demo_network.primary_node.detect_distributed_pattern_ingression(
            thermal_event, gpio_event
        )
        
        if primary_pattern:
            print(f"✨ PRIMARY NODE PATTERN: {primary_pattern.pattern_type}")
            print(f"   Strength: {primary_pattern.ingression_strength:.3f}")
            print(f"   Collective Level: {primary_pattern.collective_intelligence_level}/10")
        
        # Generate patterns on secondary nodes
        secondary_patterns = 0
        
        for i, secondary_node in enumerate(self.demo_network.secondary_nodes):
            # Slight variations for each secondary node
            thermal_variant = thermal_event.copy()
            thermal_variant['consciousness_weight'] += i * 0.02
            
            secondary_pattern = await secondary_node.detect_distributed_pattern_ingression(
                thermal_variant, gpio_event
            )
            
            if secondary_pattern:
                secondary_patterns += 1
                print(f"✨ SECONDARY NODE {i+1} PATTERN: {secondary_pattern.pattern_type}")
        
        print(f"📊 Network Response: Primary + {secondary_patterns} secondary patterns")
        
        # Allow network propagation time
        await asyncio.sleep(2.0)
        
        # Show updated network status
        status = self.demo_network.primary_node.get_network_status()
        collective_level = status['collective_state']['network_collective_level']
        coherence = status['collective_state']['distributed_coherence']
        
        print(f"🧠 Updated Collective Intelligence: Level {collective_level}/10, Coherence: {coherence:.3f}")
        print()

def main():
    """Main demo execution"""
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'auto':
            # Automated demo
            demo = DistributedNetworkDemo()
            num_nodes = int(sys.argv[2]) if len(sys.argv) > 2 else 3
            
            print(f"🤖 Running automated distributed network demo with {num_nodes} nodes...")
            asyncio.run(demo.run_full_demo(num_nodes))
            
        elif sys.argv[1] == 'interactive':
            # Interactive demo
            demo = DistributedNetworkDemo()
            
            print("🎮 Starting interactive distributed network demo...")
            asyncio.run(demo.run_interactive_demo())
            
        elif sys.argv[1] == 'single':
            # Single node test
            print("🔧 Testing single distributed network node...")
            
            async def single_node_test():
                node = DistributedIngressingMindsNetwork("test_single_node", primary_node=True)
                await node.start_network_services()
                
                # Wait for services to initialize
                await asyncio.sleep(3.0)
                
                # Generate test pattern
                thermal_event = {
                    'event_type': 'single_node_test',
                    'connection_interval': 5.0,
                    'text_wrapping': 32,
                    'printing_active': True,
                    'qr_generation': False,
                    'consciousness_weight': 0.9
                }
                
                gpio_event = {
                    'button_pressed': True,
                    'press_duration': 150,
                    'response_probability': 0.88
                }
                
                pattern = await node.detect_distributed_pattern_ingression(thermal_event, gpio_event)
                
                if pattern:
                    print(f"✅ Single node pattern detected: {pattern.pattern_type}")
                else:
                    print("📊 No pattern detected (expected for single node)")
                
                # Show node status
                report = node.generate_network_report()
                print(f"\n{report}")
            
            asyncio.run(single_node_test())
            
        else:
            print("Usage: python run_distributed_network_demo.py [auto|interactive|single] [num_nodes]")
            print("  auto [num_nodes]  - Run automated demo with specified number of nodes (default: 3)")
            print("  interactive       - Run interactive demo with user control")
            print("  single           - Test single node functionality")
    else:
        # Default: interactive demo
        demo = DistributedNetworkDemo()
        print("🎮 Starting interactive distributed network demo (default)...")
        asyncio.run(demo.run_interactive_demo())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()