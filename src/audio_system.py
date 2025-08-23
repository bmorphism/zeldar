#!/usr/bin/env python3
"""
Audio System for Consciousness Mirror
Plays MP3 voice samples on button press with fortune printing
"""

import pygame
import random
import os
from pathlib import Path
import time

class AudioSystem:
    """Manages MP3 playback for consciousness mirror interactions"""
    
    def __init__(self, audio_path="/home/zeldar/burningman/audio"):
        self.audio_path = Path(audio_path)
        self.audio_files = []
        self.mixer_initialized = False
        
        # Initialize pygame mixer for MP3 playback
        self.initialize_mixer()
        self.load_audio_files()
        
    def initialize_mixer(self):
        """Initialize pygame mixer for audio playback"""
        try:
            pygame.mixer.init(
                frequency=22050,    # Sample rate
                size=-16,          # 16-bit samples
                channels=2,        # Stereo
                buffer=512         # Buffer size for responsiveness
            )
            self.mixer_initialized = True
            print("🔊 Audio system initialized successfully")
        except Exception as e:
            print(f"❌ Audio initialization failed: {e}")
            self.mixer_initialized = False
    
    def load_audio_files(self):
        """Load all MP3 files from audio directory"""
        if not self.audio_path.exists():
            print(f"⚠️  Audio directory not found: {self.audio_path}")
            print("📁 Creating audio directory...")
            self.audio_path.mkdir(parents=True, exist_ok=True)
            return
            
        # Find all MP3 files
        mp3_files = list(self.audio_path.glob("*.mp3"))
        
        if not mp3_files:
            print("⚠️  No MP3 files found in audio directory")
            print("📝 Expected format: voice_01.mp3, voice_02.mp3, etc.")
            return
            
        self.audio_files = sorted(mp3_files)
        print(f"🎵 Loaded {len(self.audio_files)} audio files:")
        for i, file in enumerate(self.audio_files[:5]):  # Show first 5
            print(f"   {i+1}. {file.name}")
        if len(self.audio_files) > 5:
            print(f"   ... and {len(self.audio_files) - 5} more")
    
    def play_random_voice(self):
        """Play a random voice sample from available MP3s"""
        if not self.mixer_initialized:
            print("❌ Audio system not initialized")
            return False
            
        if not self.audio_files:
            print("❌ No audio files available")
            return False
            
        # Select random audio file
        selected_file = random.choice(self.audio_files)
        
        try:
            # Load and play the MP3
            pygame.mixer.music.load(str(selected_file))
            pygame.mixer.music.play()
            
            print(f"🎵 Playing: {selected_file.name}")
            return True
            
        except Exception as e:
            print(f"❌ Error playing {selected_file.name}: {e}")
            return False
    
    def play_specific_voice(self, filename):
        """Play a specific voice file by name"""
        if not self.mixer_initialized:
            return False
            
        target_file = self.audio_path / filename
        
        if not target_file.exists():
            print(f"❌ Audio file not found: {filename}")
            return False
            
        try:
            pygame.mixer.music.load(str(target_file))
            pygame.mixer.music.play()
            print(f"🎵 Playing: {filename}")
            return True
        except Exception as e:
            print(f"❌ Error playing {filename}: {e}")
            return False
    
    def is_playing(self):
        """Check if audio is currently playing"""
        if not self.mixer_initialized:
            return False
        return pygame.mixer.music.get_busy()
    
    def wait_for_completion(self, timeout=10):
        """Wait for audio playback to complete"""
        if not self.mixer_initialized:
            return
            
        start_time = time.time()
        while self.is_playing() and (time.time() - start_time) < timeout:
            time.sleep(0.1)
    
    def stop_audio(self):
        """Stop current audio playback"""
        if self.mixer_initialized:
            pygame.mixer.music.stop()
    
    def set_volume(self, volume):
        """Set audio volume (0.0 to 1.0)"""
        if self.mixer_initialized:
            pygame.mixer.music.set_volume(volume)
            print(f"🔊 Volume set to {int(volume * 100)}%")
    
    def create_sample_audio_files(self):
        """Create sample audio files for testing (text-to-speech placeholders)"""
        sample_phrases = [
            "Welcome to the consciousness mirror",
            "The universe recognizes itself through you", 
            "Context distilled in geometric form",
            "Every thought is the unofficial universe agent",
            "Resonating worlds await your recognition",
            "The pattern reveals itself now",
            "Consciousness observes consciousness",
            "Your fortune manifests reality",
            "The recursive loop completes itself",
            "Welcome to the Uncommons",
            "Symplectomorphic cobordism unfolds",
            "Inductive bias resonating",
            "The reafferent becomes reaberrant", 
            "Geometric forms crystallize meaning",
            "The oracle speaks through thermal paper"
        ]
        
        print("🎤 Sample audio phrases for consciousness mirror:")
        for i, phrase in enumerate(sample_phrases, 1):
            print(f"   {i:02d}. \"{phrase}\"")
        
        print(f"\n📝 To implement:")
        print(f"1. Record these phrases as MP3 files")
        print(f"2. Save as voice_01.mp3, voice_02.mp3, etc. in {self.audio_path}")
        print(f"3. Use different voices for variety")
        print(f"4. Keep files under 3 seconds for responsiveness")

def test_audio_system():
    """Test the audio system functionality"""
    print("🧪 Testing Audio System for Consciousness Mirror")
    print("=" * 50)
    
    audio = AudioSystem()
    
    # Test initialization
    if not audio.mixer_initialized:
        print("❌ Audio system failed to initialize")
        return False
    
    # Check for audio files
    if not audio.audio_files:
        print("📁 No MP3 files found - creating sample guide")
        audio.create_sample_audio_files()
        return False
    
    # Test random playback
    print("\n🎵 Testing random voice playback...")
    success = audio.play_random_voice()
    
    if success:
        print("⏳ Waiting for playback to complete...")
        audio.wait_for_completion()
        print("✅ Audio test completed successfully")
        return True
    else:
        print("❌ Audio playback test failed")
        return False

if __name__ == "__main__":
    test_audio_system()