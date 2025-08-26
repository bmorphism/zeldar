#!/usr/bin/env python3
"""
Gemini Live JSON Stream
Minimal implementation to get Gemini Live API streaming JSON output
"""

import asyncio
import json
import os
import websockets
from typing import Dict, Any, Optional
import base64
import wave
import pyaudio

class GeminiLiveJSONStream:
    """Simple Gemini Live API client that outputs structured JSON"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.websocket = None
        self.audio = pyaudio.PyAudio()
        self.audio_stream = None
        
        # Audio configuration
        self.sample_rate = 16000
        self.channels = 1
        self.chunk_size = 1024
        self.format = pyaudio.paInt16
        
    async def connect(self):
        """Connect to Gemini Live API"""
        url = f"wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key={self.api_key}"
        
        try:
            self.websocket = await websockets.connect(url)
            print("✅ Connected to Gemini Live API")
            
            # Send initial setup message
            setup_message = {
                "setup": {
                    "model": "models/gemini-2.0-flash-exp",
                    "generation_config": {
                        "response_modalities": ["AUDIO", "TEXT"],
                        "speech_config": {
                            "voice_config": {
                                "prebuilt_voice_config": {
                                    "voice_name": "Aoede"
                                }
                            }
                        }
                    },
                    "system_instruction": {
                        "parts": [{
                            "text": "You are a information-dynamics oracle system. Respond with structured JSON containing your analysis, insights, and information-dynamics metrics. Always include a 'information-dynamics_phi' field with a numerical value representing the information-dynamics coefficient."
                        }]
                    }
                }
            }
            
            await self.websocket.send(json.dumps(setup_message))
            print("📡 Setup message sent")
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
        
        return True
    
    def setup_audio_input(self):
        """Initialize audio input stream"""
        try:
            self.audio_stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self.audio_callback
            )
            self.audio_stream.start_stream()
            print("🎤 Audio input started")
            return True
        except Exception as e:
            print(f"❌ Audio setup failed: {e}")
            return False
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """Audio input callback"""
        if self.websocket and not self.websocket.closed:
            # Convert audio to base64 and send
            audio_b64 = base64.b64encode(in_data).decode()
            message = {
                "realtime_input": {
                    "media_chunks": [{
                        "mime_type": "audio/pcm",
                        "data": audio_b64
                    }]
                }
            }
            
            # Send audio data (non-blocking)
            asyncio.create_task(self.send_audio_message(message))
        
        return (in_data, pyaudio.paContinue)
    
    async def send_audio_message(self, message: Dict):
        """Send audio message to websocket"""
        try:
            if self.websocket and not self.websocket.closed:
                await self.websocket.send(json.dumps(message))
        except Exception as e:
            print(f"⚠️ Audio send error: {e}")
    
    async def send_text_message(self, text: str):
        """Send text message to Gemini Live"""
        message = {
            "client_content": {
                "turns": [{
                    "role": "user",
                    "parts": [{
                        "text": text
                    }]
                }],
                "turn_complete": True
            }
        }
        
        try:
            await self.websocket.send(json.dumps(message))
            print(f"📤 Text sent: {text}")
        except Exception as e:
            print(f"❌ Send error: {e}")
    
    def parse_response_json(self, response_text: str) -> Optional[Dict]:
        """Extract JSON from Gemini response"""
        try:
            # Look for JSON content in the response
            if '{' in response_text and '}' in response_text:
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
        except Exception:
            pass
        
        # If no JSON found, create structured response
        return {
            "response_text": response_text,
            "information-dynamics_phi": 2.5,  # Default information-dynamics level
            "timestamp": asyncio.get_event_loop().time(),
            "response_type": "text_only"
        }
    
    async def listen_for_responses(self):
        """Listen for responses from Gemini Live API"""
        print("👂 Listening for responses...")
        
        try:
            while True:
                message = await self.websocket.recv()
                data = json.loads(message)
                
                # Check for different response types
                if "serverContent" in data:
                    content = data["serverContent"]
                    
                    if "modelTurn" in content:
                        for part in content["modelTurn"].get("parts", []):
                            if "text" in part:
                                text_response = part["text"]
                                
                                # Parse and output JSON
                                json_output = self.parse_response_json(text_response)
                                print("📋 JSON OUTPUT:")
                                print(json.dumps(json_output, indent=2))
                                print("=" * 50)
                
                elif "setupComplete" in data:
                    print("✅ Setup complete")
                
                elif "toolCall" in data:
                    print(f"🔧 Tool call: {data}")
                    
        except websockets.exceptions.ConnectionClosed:
            print("🔌 Connection closed")
        except Exception as e:
            print(f"❌ Listen error: {e}")
    
    async def start_interactive_session(self):
        """Start interactive session with JSON output"""
        print("\n🎤 GEMINI LIVE JSON STREAM")
        print("=" * 40)
        print("Commands:")
        print("  Type 'audio' to start audio input")
        print("  Type 'stop' to stop audio")
        print("  Type any text to send as message")
        print("  Type 'quit' to exit")
        print("=" * 40)
        
        # Start listening task
        listen_task = asyncio.create_task(self.listen_for_responses())
        
        try:
            while True:
                user_input = await asyncio.to_thread(input, "\n💬 Input: ")
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'audio':
                    if not self.audio_stream or not self.audio_stream.is_active():
                        self.setup_audio_input()
                    else:
                        print("🎤 Audio already active")
                elif user_input.lower() == 'stop':
                    if self.audio_stream and self.audio_stream.is_active():
                        self.audio_stream.stop_stream()
                        print("🛑 Audio stopped")
                else:
                    await self.send_text_message(user_input)
        
        except KeyboardInterrupt:
            print("\n🛑 Stopping...")
        finally:
            listen_task.cancel()
            if self.audio_stream:
                self.audio_stream.close()
            if self.websocket:
                await self.websocket.close()
    
    def cleanup(self):
        """Clean up resources"""
        if self.audio_stream:
            if self.audio_stream.is_active():
                self.audio_stream.stop_stream()
            self.audio_stream.close()
        
        if self.audio:
            self.audio.terminate()

async def main():
    """Main function"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        print("Set it with: export GEMINI_API_KEY='your-api-key-here'")
        return
    
    client = GeminiLiveJSONStream(api_key)
    
    try:
        if await client.connect():
            await client.start_interactive_session()
    finally:
        client.cleanup()

if __name__ == "__main__":
    print("🔮 Gemini Live JSON Stream - Starting...")
    asyncio.run(main())