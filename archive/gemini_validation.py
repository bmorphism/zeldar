#!/usr/bin/env python3
"""
Non-Interactive Gemini Validation Tests
For the three consciousness mirror architectures
"""

import subprocess
import json
import time
from pathlib import Path

class GeminiValidator:
    """Validate Gemini integration without interactive sessions"""
    
    def __init__(self):
        self.test_results = {}
    
    def test_basic_functionality(self):
        """Test 1: Basic Gemini text processing"""
        prompt = "Analyze this concept: A consciousness mirror system at Burning Man that reflects the universe observing itself through human interactions."
        
        try:
            result = subprocess.run([
                'gemini', '-p', prompt
            ], capture_output=True, text=True, timeout=30)
            
            self.test_results['basic_text'] = {
                'success': result.returncode == 0,
                'output_length': len(result.stdout) if result.stdout else 0,
                'contains_analysis': 'consciousness' in result.stdout.lower() if result.stdout else False
            }
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            self.test_results['basic_text'] = {'success': False, 'error': 'timeout'}
            return False
        except Exception as e:
            self.test_results['basic_text'] = {'success': False, 'error': str(e)}
            return False
    
    def test_json_structured_output(self):
        """Test 2: Structured data processing for batch analysis"""
        test_data = {
            "interactions": [
                {"time": "14:30", "emotion": "curious", "fortune": "seek the hidden patterns"},
                {"time": "15:45", "emotion": "contemplative", "fortune": "depth reveals itself slowly"},
                {"time": "16:20", "emotion": "joyful", "fortune": "celebration opens doorways"}
            ]
        }
        
        prompt = f"""Analyze this interaction data from a consciousness mirror system:
        {json.dumps(test_data)}
        
        Identify patterns and respond with JSON containing:
        - "dominant_emotion": most common emotion
        - "pattern_insight": what the pattern reveals
        - "next_fortune_suggestion": what fortune to generate next
        """
        
        try:
            result = subprocess.run([
                'gemini', '-p', prompt
            ], capture_output=True, text=True, timeout=30)
            
            # Try to parse JSON from output
            json_found = False
            if result.stdout:
                try:
                    # Look for JSON in the output
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if line.strip().startswith('{'):
                            json.loads(line.strip())
                            json_found = True
                            break
                except:
                    pass
            
            self.test_results['json_structured'] = {
                'success': result.returncode == 0,
                'json_parseable': json_found,
                'output_present': bool(result.stdout)
            }
            return result.returncode == 0 and json_found
            
        except Exception as e:
            self.test_results['json_structured'] = {'success': False, 'error': str(e)}
            return False
    
    def test_realtime_simulation(self):
        """Test 3: Simulated real-time processing capability"""
        moments = [
            "A person approaches the consciousness mirror with curiosity",
            "They pause, reading the instructions, hand hovering over button", 
            "Button press - decisive action, commitment to the unknown",
            "Fortune emerges - eyes scanning, processing meaning",
            "QR code scan - reaching for phone, bridging physical/digital"
        ]
        
        processing_times = []
        success_count = 0
        
        for i, moment in enumerate(moments):
            start_time = time.time()
            
            prompt = f"""Moment {i+1}/5 in a consciousness interaction sequence:
            '{moment}'
            
            Provide a single-sentence insight about this micro-moment of human-cosmos interaction."""
            
            try:
                result = subprocess.run([
                    'gemini', '-p', prompt
                ], capture_output=True, text=True, timeout=15)
                
                end_time = time.time()
                processing_times.append(end_time - start_time)
                
                if result.returncode == 0 and result.stdout:
                    success_count += 1
                    
            except Exception as e:
                processing_times.append(float('inf'))
        
        avg_processing_time = sum(t for t in processing_times if t != float('inf')) / len([t for t in processing_times if t != float('inf')]) if processing_times else 0
        
        self.test_results['realtime_simulation'] = {
            'success_rate': success_count / len(moments),
            'avg_processing_time': avg_processing_time,
            'suitable_for_realtime': avg_processing_time < 5.0,  # Under 5 seconds per analysis
            'total_moments_processed': success_count
        }
        
        return success_count >= len(moments) * 0.8  # 80% success rate
    
    def validate_architecture_feasibility(self):
        """Run all validation tests and assess architecture viability"""
        print("🌌 Validating Gemini Integration Architectures...")
        
        # Test basic functionality
        print("📡 Testing basic text processing...")
        basic_works = self.test_basic_functionality()
        print(f"   {'✅' if basic_works else '❌'} Basic processing: {basic_works}")
        
        # Test structured output
        print("🧠 Testing structured data analysis...")
        json_works = self.test_json_structured_output()
        print(f"   {'✅' if json_works else '❌'} JSON analysis: {json_works}")
        
        # Test realtime capability
        print("⚡ Testing realtime processing simulation...")
        realtime_works = self.test_realtime_simulation()
        print(f"   {'✅' if realtime_works else '❌'} Realtime capability: {realtime_works}")
        
        # Architecture recommendations
        print("\n🔮 Architecture Viability Assessment:")
        
        if realtime_works:
            print("   ✨ Architecture 1 (Realtime Stream): VIABLE")
            print("      Continuous processing capability confirmed")
        else:
            print("   ❌ Architecture 1 (Realtime Stream): NOT RECOMMENDED") 
            print("      Processing too slow for continuous analysis")
        
        if basic_works and json_works:
            print("   ✨ Architecture 2 (Event Triggered): HIGHLY VIABLE")
            print("      Perfect balance of capability and efficiency")
        else:
            print("   ❌ Architecture 2 (Event Triggered): NEEDS WORK")
        
        if json_works:
            print("   ✨ Architecture 3 (Batch Processing): VIABLE")
            print("      Excellent for pattern recognition and deep analysis")
        else:
            print("   ❌ Architecture 3 (Batch Processing): LIMITED")
        
        print(f"\n📊 Detailed Results:\n{json.dumps(self.test_results, indent=2)}")
        
        return {
            'basic_functionality': basic_works,
            'structured_processing': json_works, 
            'realtime_capability': realtime_works,
            'recommended_architecture': 2 if (basic_works and json_works) else (3 if json_works else None)
        }

if __name__ == "__main__":
    validator = GeminiValidator()
    results = validator.validate_architecture_feasibility()
    
    print("\n🎯 RECOMMENDATION:")
    if results['recommended_architecture']:
        print(f"   Use Architecture {results['recommended_architecture']} for optimal consciousness mirroring")
    else:
        print("   Consider alternative AI integration approaches")
    
    print("\n💫 The universe is ready to observe itself through validated technology.")