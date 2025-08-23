#!/usr/bin/env python3
"""
Multi-GPIO Pin Listener with Voice Feedback
Each pin gets a unique voice to identify which one was pressed
"""

import sys
import time
import subprocess
from datetime import datetime
from gpiozero import Button

class VoiceGPIOListener:
    def __init__(self, pin, voice_name, haiku):
        self.pin = pin
        self.voice_name = voice_name
        self.haiku = haiku
        self.last_press = 0
        self.cooldown = 3.0
        self.press_count = 0
        
    def speak_haiku(self):
        """Speak the haiku using text-to-speech"""
        try:
            # Use espeak on Linux (cross-platform TTS)
            subprocess.run([
                'espeak', 
                '-s', '150',  # Speaking rate
                '-p', str(30 + self.pin * 10),  # Unique pitch per pin
                f"GPIO {self.pin}: {self.haiku}"
            ], check=False, timeout=10)
            print(f"🗣️  Spoke haiku for GPIO {self.pin} with voice {self.voice_name}")
        except FileNotFoundError:
            # Fallback to simple print if espeak not available
            print(f"🗣️  GPIO {self.pin} ({self.voice_name}): {self.haiku}")
        except Exception as e:
            print(f"❌ Speech failed for GPIO {self.pin}: {e}")
            print(f"🗣️  GPIO {self.pin} ({self.voice_name}): {self.haiku}")
            
    def on_press(self):
        """Handle button press with cooldown and voice feedback"""
        current_time = time.time()
        
        if current_time - self.last_press < self.cooldown:
            remaining = self.cooldown - (current_time - self.last_press)
            print(f"⏱️  GPIO {self.pin} cooldown: {remaining:.1f}s remaining")
            return
            
        self.last_press = current_time
        self.press_count += 1
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        
        print(f"🔘 GPIO {self.pin} PRESSED! ({self.press_count}) at {timestamp}")
        print(f"   └─ Voice: {self.voice_name}")
        
        # Speak haiku in background
        self.speak_haiku()
        
    def start_listening(self):
        """Start listening on this GPIO pin"""
        try:
            button = Button(self.pin, pull_up=False, bounce_time=0.2)  # pull-down, detects falling edge
            button.when_pressed = self.on_press
            
            print(f"✅ GPIO {self.pin} ready - Voice: {self.voice_name}")
            return button
        except Exception as e:
            print(f"❌ GPIO {self.pin} failed: {e}")
            return None

def main():
    # GPIO pin configurations with unique voices and haikus
    gpio_configs = [
        {
            'pin': 2, 
            'voice': 'Alex',
            'haiku': 'GPIO two speaks, with clarity and depth, button press confirmed'
        },
        {
            'pin': 3,
            'voice': 'Victoria', 
            'haiku': 'Pin three awakens, feminine voice responds, third connection made'
        },
        {
            'pin': 4,
            'voice': 'Daniel',
            'haiku': 'Fourth pin activated, British accent clear, four corners of truth'
        },
        {
            'pin': 5,
            'voice': 'Karen',
            'haiku': 'Five senses align, Australian voice rings, fifth element found'
        },
        {
            'pin': 6,
            'voice': 'Moira',
            'haiku': 'Sixth sense detected, Irish lilt confirms, six degrees apart'
        },
        {
            'pin': 7,
            'voice': 'Rishi',
            'haiku': 'Seven sacred sounds, Indian wisdom speaks, lucky number pressed'
        },
        {
            'pin': 8,
            'voice': 'Tessa',
            'haiku': 'Eighth note harmony, South African tone, infinite loop closed'
        }
    ]
    
    print("🚀 Multi-GPIO Voice Listener Starting...")
    print("=" * 50)
    
    listeners = []
    active_buttons = []
    
    # Create listeners for each pin
    for config in gpio_configs:
        listener = VoiceGPIOListener(
            config['pin'], 
            config['voice'], 
            config['haiku']
        )
        button = listener.start_listening()
        
        if button:
            listeners.append(listener)
            active_buttons.append(button)
    
    print(f"\n✅ {len(listeners)} GPIO pins active and listening")
    print("🔘 Press any connected button to hear unique voice")
    print("⏱️  3-second cooldown between presses per pin")
    print("\nPress Ctrl+C to stop all listeners")
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"\n🛑 Stopping all {len(listeners)} GPIO listeners...")
        for button in active_buttons:
            button.close()
        print("🏁 All GPIO listeners stopped")

if __name__ == "__main__":
    main()