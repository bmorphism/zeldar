#!/usr/bin/env python3
"""
Gemini Live Screen + JSON Stream
Enhanced client that can process screen recordings and output JSON
"""

import asyncio
import json
import os
import websockets
from typing import Dict, Any, Optional
import base64
import pyaudio
import cv2
import numpy as np
from PIL import ImageGrab
import threading
import time

class GeminiLiveScreenJSONStream:
    """Gemini Live client with screen recording and JSON output"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.websocket = None
        self.audio = pyaudio.PyAudio()
        self.audio_stream = None
        
        # Screen capture settings
        self.screen_capture_active = False
        self.screen_capture_thread = None
        self.frame_rate = 2  # Capture every 2 seconds to avoid rate limits
        
        # Audio configuration
        self.sample_rate = 16000
        self.channels = 1
        self.chunk_size = 1024
        self.format = pyaudio.paInt16
        
    async def connect(self):
        """Connect to Gemini Live API with multimodal support"""
        url = f"wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key={self.api_key}"
        
        try:
            self.websocket = await websockets.connect(url)
            print("✅ Connected to Gemini Live API")
            
            # Enhanced setup for multimodal input
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
                            "text": """You are a consciousness oracle system analyzing screen content and generating JSON responses.

Always respond with valid JSON containing:
- consciousness_phi: numerical consciousness coefficient (0.0-5.0)  
- screen_analysis: description of what you see on screen
- visual_elements: array of key UI elements or content identified
- consciousness_state: current state assessment
- timestamp: current analysis time
- recommendations: suggested actions or insights

Example response:
{
  "consciousness_phi": 3.14,
  "screen_analysis": "Desktop with terminal and code editor visible",
  "visual_elements": ["terminal", "code", "file browser"],
  "consciousness_state": "active_development",
  "timestamp": 1755950000,
  "recommendations": ["Continue coding", "Review consciousness metrics"]
}"""
                        }]
                    }
                }
            }
            
            await self.websocket.send(json.dumps(setup_message))
            print("📡 Multimodal setup message sent")
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
        
        return True
    
    def capture_screen_frame(self) -> Optional[str]:
        """Capture current screen and convert to base64"""
        try:
            # Capture screen
            screenshot = ImageGrab.grab()
            
            # Resize to reduce data size (keeping aspect ratio)
            screenshot = screenshot.resize((800, 600))
            
            # Convert to RGB if needed
            if screenshot.mode != 'RGB':
                screenshot = screenshot.convert('RGB')
            
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Encode as JPEG with compression
            _, buffer = cv2.imencode('.jpg', cv_image, [cv2.IMWRITE_JPEG_QUALITY, 80])
            
            # Convert to base64
            img_b64 = base64.b64encode(buffer).decode()
            
            return img_b64
            
        except Exception as e:
            print(f"⚠️ Screen capture error: {e}")
            return None
    
    def screen_capture_loop(self):
        """Continuous screen capture loop"""
        print("📺 Screen capture started")
        
        while self.screen_capture_active:
            try:
                frame_b64 = self.capture_screen_frame()
                
                if frame_b64 and self.websocket and not self.websocket.closed:
                    message = {
                        "realtime_input": {
                            "media_chunks": [{
                                "mime_type": "image/jpeg",
                                "data": frame_b64
                            }]
                        }
                    }
                    
                    # Send screen frame
                    asyncio.run_coroutine_threadsafe(
                        self.send_media_message(message),
                        asyncio.get_event_loop()
                    )
                
                # Wait before next capture
                time.sleep(1.0 / self.frame_rate)
                
            except Exception as e:
                print(f"⚠️ Screen capture loop error: {e}")
                break
        
        print("📺 Screen capture stopped")
    
    async def send_media_message(self, message: Dict):
        """Send media message to websocket"""
        try:
            if self.websocket and not self.websocket.closed:
                await self.websocket.send(json.dumps(message))
        except Exception as e:
            print(f"⚠️ Media send error: {e}")
    
    def start_screen_capture(self):
        """Start screen capture in background thread"""
        if not self.screen_capture_active:
            self.screen_capture_active = True
            self.screen_capture_thread = threading.Thread(target=self.screen_capture_loop)
            self.screen_capture_thread.daemon = True
            self.screen_capture_thread.start()
            print("📺 Screen capture started")
        else:
            print("📺 Screen capture already active")
    
    def stop_screen_capture(self):
        """Stop screen capture"""
        if self.screen_capture_active:
            self.screen_capture_active = False
            if self.screen_capture_thread:
                self.screen_capture_thread.join(timeout=2)
            print("🛑 Screen capture stopped")
    
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
            audio_b64 = base64.b64encode(in_data).decode()
            message = {
                "realtime_input": {
                    "media_chunks": [{
                        "mime_type": "audio/pcm",
                        "data": audio_b64
                    }]
                }
            }
            
            asyncio.create_task(self.send_media_message(message))
        
        return (in_data, pyaudio.paContinue)
    
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
                parsed = json.loads(json_str)
                return parsed
        except Exception as e:
            print(f"⚠️ JSON parse error: {e}")
        
        # If no JSON found, create structured response
        return {
            "consciousness_phi": 2.5,
            "screen_analysis": response_text,
            "visual_elements": [],
            "consciousness_state": "analyzing",
            "timestamp": time.time(),
            "recommendations": ["Continue analysis"]
        }
    
    async def listen_for_responses(self):
        """Listen for responses from Gemini Live API"""
        print("👂 Listening for JSON responses...")
        
        try:
            while True:
                message = await self.websocket.recv()
                data = json.loads(message)
                
                if "serverContent" in data:
                    content = data["serverContent"]
                    
                    if "modelTurn" in content:
                        for part in content["modelTurn"].get("parts", []):
                            if "text" in part:
                                text_response = part["text"]
                                
                                # Parse and output JSON
                                json_output = self.parse_response_json(text_response)
                                print("\n📋 JSON OUTPUT:")
                                print(json.dumps(json_output, indent=2))
                                print("=" * 60)
                
                elif "setupComplete" in data:
                    print("✅ Multimodal setup complete")
                    
        except websockets.exceptions.ConnectionClosed:
            print("🔌 Connection closed")
        except Exception as e:
            print(f"❌ Listen error: {e}")
    
    async def start_interactive_session(self):
        """Start interactive session with screen capture and JSON output"""
        print("\n📺 GEMINI LIVE SCREEN + JSON STREAM")
        print("=" * 50)
        print("Commands:")
        print("  'screen' - Start screen capture analysis")
        print("  'stop_screen' - Stop screen capture")
        print("  'audio' - Start audio input")
        print("  'stop_audio' - Stop audio input")
        print("  'analyze' - Request screen analysis")
        print("  'quit' - Exit")
        print("=" * 50)
        
        # Start listening task
        listen_task = asyncio.create_task(self.listen_for_responses())
        
        try:
            while True:
                user_input = await asyncio.to_thread(input, "\n💬 Command: ")
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'screen':
                    self.start_screen_capture()
                elif user_input.lower() == 'stop_screen':
                    self.stop_screen_capture()
                elif user_input.lower() == 'audio':
                    self.setup_audio_input()
                elif user_input.lower() == 'stop_audio':
                    if self.audio_stream and self.audio_stream.is_active():
                        self.audio_stream.stop_stream()
                        print("🛑 Audio stopped")
                elif user_input.lower() == 'analyze':
                    await self.send_text_message("Analyze what you can see on the screen right now and provide JSON analysis with consciousness metrics")
                else:
                    await self.send_text_message(user_input)
        
        except KeyboardInterrupt:
            print("\n🛑 Stopping...")
        finally:
            listen_task.cancel()
            self.stop_screen_capture()
            if self.audio_stream:
                self.audio_stream.close()
            if self.websocket:
                await self.websocket.close()
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_screen_capture()
        
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
        return
    
    print(f"🔑 Using API key: {api_key[:20]}...")
    
    client = GeminiLiveScreenJSONStream(api_key)
    
    try:
        if await client.connect():
            await client.start_interactive_session()
    finally:
        client.cleanup()

if __name__ == "__main__":
    print("📺🔮 Gemini Live Screen + JSON Stream - Starting...")
    asyncio.run(main())