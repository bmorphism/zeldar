#!/usr/bin/env python3
"""
Quick demo of the three fortune types without printer dependency
"""

import asyncio
from fortune_types import FortuneGenerator, FortuneType

async def demo_three_types():
    """Demonstrate all three fortune types"""
    print("🔮 ZELDAR THREE FORTUNE TYPES DEMO")
    print("=" * 50)
    
    generator = FortuneGenerator()
    
    # Generate one example of each type
    for fortune_type in FortuneType:
        print(f"\n🌟 {fortune_type.value.upper().replace('_', ' ')}")
        print("─" * 40)
        
        fortune = generator.generate_fortune(fortune_type)
        
        print(f"💬 Fortune: {fortune['text']}")
        print(f"📡 EMF Frequency: {fortune['electromagnetic_signature']['base_frequency']:.1f} Hz")
        print(f"🔥 Thermal Intensity: {fortune['electromagnetic_signature']['thermal_intensity']:.2f}")
        print(f"📊 Information Density: {fortune['metadata']['information_density']:.3f}")
        print(f"🧮 Complexity Score: {fortune['metadata']['complexity_score']:.3f}")
        print(f"🏷️  Session ID: {fortune['session_id']}")
    
    print(f"\n📈 FORTUNE TYPE CHARACTERISTICS:")
    print("─" * 40)
    print("1. TEMPORAL INVERSION:")
    print("   - Focuses on time paradoxes and causality loops")
    print("   - EMF Frequency: 42 Hz (temporal resonance)")
    print("   - High thermal intensity (0.85) for time distortion")
    print()
    print("2. INFORMATION FORCE:")
    print("   - Energy-matter transformation predictions")
    print("   - EMF Frequency: 137 Hz (fine structure constant)")
    print("   - Highest thermal intensity (0.92) for energy work")
    print()
    print("3. CATEGORICAL MORPHISM:")
    print("   - Structural pattern and relationship revelations")
    print("   - EMF Frequency: 272 Hz (mathematical constant e)")
    print("   - Moderate thermal intensity (0.78) for pattern recognition")
    
    print(f"\n⚖️ RECOMMENDED DISTRIBUTION:")
    distribution = generator.get_type_distribution()
    for fortune_type, percentage in distribution.items():
        print(f"   {fortune_type.replace('_', ' ').title()}: {percentage:.0%}")
    
    print(f"\n🔬 ELECTROMAGNETIC COUPLING ANALYSIS:")
    print("─" * 40)
    # Test EMF coupling for different scenarios
    test_emf_values = [42.0, 137.0, 272.0, 100.0]  # Including matching and non-matching frequencies
    
    for emf in test_emf_values:
        print(f"\nEMF Reading: {emf:.1f} Hz")
        best_type = None
        best_resonance = 0
        
        for fortune_type in FortuneType:
            analysis = generator.analyze_electromagnetic_coupling(fortune_type, emf)
            resonance = analysis['resonance_strength']
            
            if resonance > best_resonance:
                best_resonance = resonance
                best_type = fortune_type
            
            print(f"  {fortune_type.value.replace('_', ' ').title()}: "
                  f"resonance {resonance:.3f}, "
                  f"recommended: {'Yes' if analysis['recommended_for_current_emf'] else 'No'}")
        
        print(f"  → Best match: {best_type.value.replace('_', ' ').title()} "
              f"(resonance {best_resonance:.3f})")

if __name__ == "__main__":
    asyncio.run(demo_three_types())