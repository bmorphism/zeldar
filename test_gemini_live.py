#!/usr/bin/env python3
"""
Test Gemini Live JSON Stream
Simple test to verify JSON output functionality
"""

import asyncio
import json
import os
from gemini_live_json_stream import GeminiLiveJSONStream

async def test_json_output():
    """Test JSON output from Gemini Live"""
    
    print("🧪 TESTING GEMINI LIVE JSON OUTPUT")
    print("=" * 50)
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not set")
        print("Set with: export GEMINI_API_KEY='your-key'")
        return
    
    client = GeminiLiveJSONStream(api_key)
    
    try:
        # Connect to Gemini Live
        if await client.connect():
            print("✅ Connected successfully")
            
            # Start listening task
            listen_task = asyncio.create_task(client.listen_for_responses())
            
            # Wait a moment for setup
            await asyncio.sleep(2)
            
            # Test messages that should produce JSON
            test_messages = [
                "Generate a JSON analysis of information-dynamics with phi coefficient",
                "Return information-dynamics metrics in JSON format",
                "Analyze this request and output structured JSON data",
                "Create JSON with information-dynamics_phi, timestamp, and analysis"
            ]
            
            for i, message in enumerate(test_messages, 1):
                print(f"\n📤 Test {i}: {message}")
                await client.send_text_message(message)
                
                # Wait for response
                await asyncio.sleep(5)
                
                if i < len(test_messages):
                    print("⏳ Waiting before next test...")
                    await asyncio.sleep(2)
            
            print("\n🏁 Test sequence complete")
            
            # Keep listening for a bit more
            await asyncio.sleep(10)
            
            listen_task.cancel()
            
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        client.cleanup()

async def test_structured_prompts():
    """Test specific prompts designed for JSON output"""
    
    print("\n🎯 TESTING STRUCTURED JSON PROMPTS")
    print("=" * 50)
    
    api_key = os.getenv("GEMINI_API_KEY") 
    if not api_key:
        return
        
    client = GeminiLiveJSONStream(api_key)
    
    try:
        if await client.connect():
            listen_task = asyncio.create_task(client.listen_for_responses())
            await asyncio.sleep(2)
            
            structured_prompts = [
                """
                Please respond with a JSON object containing:
                {
                    "information-dynamics_phi": <numerical_value>,
                    "analysis": "<your_analysis>", 
                    "timestamp": <current_time>,
                    "status": "active"
                }
                """,
                
                """
                Format your response as JSON with these fields:
                - information-dynamics_phi (float)
                - element (string) 
                - quantum_entropy (float)
                - haiku_content (string)
                - response_type (string)
                """,
                
                "Output only valid JSON: {\"information-dynamics_phi\": 3.14, \"message\": \"information-dynamics active\", \"metrics\": {\"entropy\": 0.92}}"
            ]
            
            for i, prompt in enumerate(structured_prompts, 1):
                print(f"\n📋 Structured Test {i}")
                await client.send_text_message(prompt.strip())
                await asyncio.sleep(6)
            
            await asyncio.sleep(10)
            listen_task.cancel()
            
    except Exception as e:
        print(f"❌ Structured test error: {e}")
    finally:
        client.cleanup()

if __name__ == "__main__":
    print("🔬 Starting Gemini Live JSON Tests...")
    
    async def run_all_tests():
        await test_json_output()
        await asyncio.sleep(3)
        await test_structured_prompts()
    
    asyncio.run(run_all_tests())