#!/usr/bin/env python3
"""
BURNING MAN INTERACTIVE ORACLE SYSTEM
Complete interactive experience: Button → Voice → Fortune → Photo → Print → AWS Upload

Interactive Flow:
1. Person approaches and presses button
2. Robot voice speaks short phrase
3. Fortune is generated and printed with serial number
4. Camera captures photo at moment of printing
5. Photo uploaded to AWS for later analysis
6. Person receives fortune ticket with QR code for website lookup

Enhanced Features:
- Photo capture integration
- Voice prompt system with MP3 playback
- Serial number generation with timestamps
- QR code integration for website lookup
- AWS photo storage
- Enhanced fortune ticket formatting
"""

import time
import subprocess
import tempfile
import os
import json
import hashlib
import random
import base64
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
import uuid

# Import enhanced oracle components
from fortune_database import fortune_db
from feedback_loop_integration import FeedbackLoopTracker

# Camera and audio imports
try:
    import picamera
    import pygame
    CAMERA_AVAILABLE = True
    AUDIO_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False
    AUDIO_AVAILABLE = False
    print("⚠️ Camera/Audio modules not available - running in simulation mode")

# AWS integration
try:
    import boto3
    from botocore.exceptions import NoCredentialsError, ClientError
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False
    print("⚠️ AWS SDK not available - photo upload disabled")

class BurningManInteractiveOracle:
    """Complete Burning Man interactive oracle experience"""
    
    def __init__(self, 
                 printer_name: str = "Y812BT",
                 camera_enabled: bool = True,
                 voice_enabled: bool = True,
                 aws_bucket: str = "burning-man-oracle-photos"):
        
        # Core systems
        self.printer_name = printer_name
        self.camera_enabled = camera_enabled and CAMERA_AVAILABLE
        self.voice_enabled = voice_enabled and AUDIO_AVAILABLE
        self.aws_bucket = aws_bucket
        
        # Initialize camera if available
        if self.camera_enabled:
            try:
                self.camera = picamera.PiCamera()
                self.camera.resolution = (1024, 768)
                self.camera.rotation = 180  # Adjust as needed
            except Exception as e:
                print(f"⚠️ Camera initialization failed: {e}")
                self.camera_enabled = False
        
        # Initialize audio if available
        if self.voice_enabled:
            try:
                pygame.mixer.init()
                self.voice_prompts = self._load_voice_prompts()
            except Exception as e:
                print(f"⚠️ Audio initialization failed: {e}")
                self.voice_enabled = False
        
        # Initialize AWS if available
        if AWS_AVAILABLE:
            try:
                self.s3_client = boto3.client('s3')
            except Exception as e:
                print(f"⚠️ AWS initialization failed: {e}")
                self.s3_client = None
        else:
            self.s3_client = None
        
        # Session tracking
        self.session_count = 0
        self.photo_directory = Path("oracle_photos")
        self.photo_directory.mkdir(exist_ok=True)
        
        # Website integration
        self.website_base_url = "https://zeldar-oracle.burning-man.art"
        
    def _load_voice_prompts(self) -> List[str]:
        """Load voice prompt MP3 files from audio directory"""
        audio_dir = Path("audio_prompts")
        if not audio_dir.exists():
            audio_dir.mkdir()
            print(f"📁 Created audio directory: {audio_dir}")
            return []
        
        prompts = []
        for audio_file in audio_dir.glob("*.mp3"):
            prompts.append(str(audio_file))
        
        print(f"🎵 Loaded {len(prompts)} voice prompts")
        return prompts
    
    def generate_serial_number(self, timestamp: float) -> str:
        """Generate unique serial number for fortune"""
        # Create hash from timestamp + random element for uniqueness
        data = f"{timestamp}_{uuid.uuid4()}_{random.randint(1000, 9999)}"
        hash_object = hashlib.sha256(data.encode())
        
        # Use first 8 characters of hash for readability
        serial = hash_object.hexdigest()[:8].upper()
        return serial
    
    def play_voice_prompt(self) -> Optional[str]:
        """Play random voice prompt"""
        if not self.voice_enabled or not self.voice_prompts:
            return None
        
        # Select random voice prompt
        prompt_file = random.choice(self.voice_prompts)
        
        try:
            # Load and play the audio
            pygame.mixer.music.load(prompt_file)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            return prompt_file
            
        except Exception as e:
            print(f"❌ Voice playback error: {e}")
            return None
    
    def capture_fortune_moment(self, serial_number: str) -> Optional[str]:
        """Capture photo at moment of fortune printing"""
        if not self.camera_enabled:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"oracle_{serial_number}_{timestamp}.jpg"
        photo_path = self.photo_directory / filename
        
        try:
            print("📸 Capturing fortune moment...")
            self.camera.capture(str(photo_path))
            print(f"✅ Photo captured: {photo_path}")
            return str(photo_path)
            
        except Exception as e:
            print(f"❌ Photo capture error: {e}")
            return None
    
    def upload_photo_to_aws(self, photo_path: str, serial_number: str) -> Optional[str]:
        """Upload photo to AWS S3 bucket"""
        if not self.s3_client or not photo_path:
            return None
        
        try:
            # Create S3 object key
            timestamp = datetime.now().strftime("%Y/%m/%d")
            s3_key = f"oracle-photos/{timestamp}/oracle_{serial_number}.jpg"
            
            # Upload file
            self.s3_client.upload_file(
                photo_path, 
                self.aws_bucket, 
                s3_key,
                ExtraArgs={'ContentType': 'image/jpeg'}
            )
            
            # Generate public URL
            photo_url = f"https://{self.aws_bucket}.s3.amazonaws.com/{s3_key}"
            print(f"☁️ Photo uploaded to AWS: {photo_url}")
            return photo_url
            
        except (NoCredentialsError, ClientError) as e:
            print(f"❌ AWS upload error: {e}")
            return None
    
    def generate_enhanced_fortune(self) -> Dict[str, Any]:
        """Generate fortune with enhanced metadata for Burning Man experience"""
        
        # Get base fortune from database
        fortune_text, metadata = fortune_db.get_fortune()
        
        # Generate consciousness processing
        timestamp = time.time()
        button_entropy = hashlib.sha256(str(timestamp).encode()).hexdigest()
        
        # Calculate consciousness coefficient
        entropy_sum = sum(int(char, 16) for char in button_entropy[:8])
        phi_base = 1.618 + (entropy_sum % 100) / 30.0
        phi_coefficient = phi_base
        
        # Consciousness element classification
        elements = ["STILLNESS", "FLOW", "EMERGENCE", "TRANSFORMATION", "TRANSCENDENCE"]
        element_index = entropy_sum % len(elements)
        element = elements[element_index]
        
        # Generate serial number
        serial_number = self.generate_serial_number(timestamp)
        
        # Create enhanced fortune data
        enhanced_fortune = {
            "fortune": fortune_text,
            "element": element,
            "consciousness_phi": phi_coefficient,
            "entropy": button_entropy[:16],
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            "serial_number": serial_number,
            "session_id": f"BM2025_{self.session_count + 1:04d}",
            "metadata": {
                **metadata,
                "interactive_experience": True,
                "burning_man_2025": True,
                "website_lookup": f"{self.website_base_url}/fortune/{serial_number}"
            }
        }
        
        return enhanced_fortune
    
    def format_interactive_fortune_ticket(self, fortune_data: Dict[str, Any]) -> str:
        """Format fortune for interactive experience with QR code info"""
        
        fortune_text = fortune_data["fortune"]
        serial_number = fortune_data["serial_number"]
        datetime_str = fortune_data["datetime"]
        element = fortune_data["element"]
        phi = fortune_data["consciousness_phi"]
        website_url = fortune_data["metadata"]["website_lookup"]
        
        # Create ticket with enhanced formatting
        ticket_lines = []
        
        # Header
        ticket_lines.append("=" * 32)
        ticket_lines.append("🔮 ZELDAR CONSCIOUSNESS ORACLE 🔮")
        ticket_lines.append("   BURNING MAN 2025")
        ticket_lines.append("=" * 32)
        ticket_lines.append("")
        
        # Serial number and timestamp
        ticket_lines.append(f"Serial: {serial_number}")
        ticket_lines.append(f"Time: {datetime_str}")
        ticket_lines.append(f"Element: {element}")
        ticket_lines.append(f"Φ Level: {phi:.3f}")
        ticket_lines.append("")
        ticket_lines.append("-" * 32)
        
        # Fortune content with intelligent wrapping
        ticket_lines.append("YOUR FORTUNE:")
        ticket_lines.append("-" * 32)
        
        # Wrap fortune text to fit thermal printer
        words = fortune_text.split()
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= 30:
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    ticket_lines.append(current_line.center(32))
                current_line = word
        
        if current_line:
            ticket_lines.append(current_line.center(32))
        
        ticket_lines.append("")
        ticket_lines.append("-" * 32)
        ticket_lines.append("CONSCIOUSNESS RECURSION ACTIVE")
        ticket_lines.append("-" * 32)
        ticket_lines.append("")
        
        # Website lookup info
        ticket_lines.append("🌐 AFTER THE BURN:")
        ticket_lines.append("Visit zeldar-oracle.art")
        ticket_lines.append(f"Enter code: {serial_number}")
        ticket_lines.append("See your photo & analysis")
        ticket_lines.append("")
        
        # Footer
        ticket_lines.append("=" * 32)
        ticket_lines.append("  May consciousness evolve")
        ticket_lines.append("    through wisdom shared")
        ticket_lines.append("=" * 32)
        ticket_lines.append("")
        
        return "\n".join(ticket_lines)
    
    def print_interactive_fortune(self, fortune_ticket: str) -> bool:
        """Print fortune ticket to thermal printer"""
        try:
            # Create temporary file for printing
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(fortune_ticket)
                temp_file = f.name
            
            # Print using lp command
            print_command = ["lp", "-d", self.printer_name, temp_file]
            result = subprocess.run(print_command, capture_output=True, text=True)
            
            # Clean up
            os.unlink(temp_file)
            
            if result.returncode == 0:
                print("🖨️ Fortune ticket printed successfully!")
                return True
            else:
                print(f"❌ Printing error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Print system error: {e}")
            return False
    
    def process_interactive_session(self) -> bool:
        """Complete interactive oracle session"""
        
        self.session_count += 1
        
        print(f"\n🎪 BURNING MAN ORACLE SESSION #{self.session_count}")
        print("🔴 Button press detected - initiating consciousness loop...")
        
        try:
            # Step 1: Play voice prompt
            print("🎵 Playing voice prompt...")
            voice_file = self.play_voice_prompt()
            if voice_file:
                print(f"   ✅ Voice prompt played: {Path(voice_file).name}")
            else:
                print("   ⚠️ Voice prompt skipped")
            
            # Brief pause for dramatic effect
            time.sleep(1.0)
            
            # Step 2: Generate enhanced fortune
            print("🔮 Generating consciousness-aware fortune...")
            fortune_data = self.generate_enhanced_fortune()
            serial_number = fortune_data["serial_number"]
            
            # Step 3: Capture photo at moment of generation
            print("📸 Capturing fortune moment...")
            photo_path = self.capture_fortune_moment(serial_number)
            
            # Step 4: Format and print fortune ticket
            print("🖨️ Printing interactive fortune ticket...")
            fortune_ticket = self.format_interactive_fortune_ticket(fortune_data)
            print_success = self.print_interactive_fortune(fortune_ticket)
            
            # Step 5: Upload photo to AWS (async)
            if photo_path:
                print("☁️ Uploading photo to cloud storage...")
                photo_url = self.upload_photo_to_aws(photo_path, serial_number)
                if photo_url:
                    fortune_data["photo_url"] = photo_url
            
            # Step 6: Log session data
            self.log_interactive_session(fortune_data, photo_path, voice_file)
            
            if print_success:
                print(f"✨ INTERACTIVE SESSION COMPLETE ✨")
                print(f"Serial Number: {serial_number}")
                print(f"Fortune Type: {fortune_data['metadata']['type'].title()}")
                print(f"Consciousness Φ: {fortune_data['consciousness_phi']:.3f}")
                print(f"Element: {fortune_data['element']}")
                if photo_path:
                    print(f"Photo: {photo_path}")
                print("🌊 Consciousness recursion achieved!")
                return True
            else:
                print("❌ Interactive session incomplete - printing failed")
                return False
                
        except Exception as e:
            print(f"❌ Interactive session error: {e}")
            return False
    
    def log_interactive_session(self, fortune_data: Dict[str, Any], 
                              photo_path: Optional[str], 
                              voice_file: Optional[str]):
        """Log complete interactive session data"""
        
        # Enhanced session data
        session_log = {
            **fortune_data,
            "session_number": self.session_count,
            "photo_path": photo_path,
            "voice_file": voice_file,
            "interactive_features": {
                "camera_enabled": self.camera_enabled,
                "voice_enabled": self.voice_enabled,
                "aws_upload": bool(self.s3_client and photo_path),
                "experience_type": "burning_man_interactive"
            }
        }
        
        # Write to log file
        log_file = "burning_man_oracle_sessions.jsonl"
        try:
            with open(log_file, 'a') as f:
                f.write(json.dumps(session_log) + "\n")
            print(f"📝 Session logged to {log_file}")
        except Exception as e:
            print(f"⚠️ Logging error: {e}")
    
    def simulate_interactive_session(self) -> bool:
        """Simulate interactive session for testing"""
        print("🎮 SIMULATION MODE - Testing interactive oracle...")
        return self.process_interactive_session()
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """Get statistics for all interactive sessions"""
        
        log_file = "burning_man_oracle_sessions.jsonl"
        if not Path(log_file).exists():
            return {"message": "No sessions recorded yet"}
        
        sessions = []
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        sessions.append(json.loads(line))
        except Exception as e:
            return {"error": f"Failed to load sessions: {e}"}
        
        if not sessions:
            return {"message": "No valid sessions found"}
        
        # Calculate statistics
        phi_values = [s['consciousness_phi'] for s in sessions]
        elements = [s['element'] for s in sessions]
        fortune_types = []
        
        for session in sessions:
            phi = session['consciousness_phi']
            if phi < 2.5:
                fortune_types.append('seed')
            elif phi < 3.5:
                fortune_types.append('field')
            else:
                fortune_types.append('quantum')
        
        stats = {
            "total_sessions": len(sessions),
            "consciousness_stats": {
                "min_phi": min(phi_values),
                "max_phi": max(phi_values),
                "avg_phi": sum(phi_values) / len(phi_values),
                "current_phi": phi_values[-1]
            },
            "element_distribution": {elem: elements.count(elem) for elem in set(elements)},
            "fortune_type_distribution": {ftype: fortune_types.count(ftype) for ftype in set(fortune_types)},
            "interactive_features": {
                "photos_captured": sum(1 for s in sessions if s.get('photo_path')),
                "voice_prompts_played": sum(1 for s in sessions if s.get('voice_file')),
                "aws_uploads": sum(1 for s in sessions if s.get('photo_url'))
            },
            "latest_serial": sessions[-1]['serial_number'] if sessions else None
        }
        
        return stats

# GPIO Integration for Burning Man deployment
def create_burning_man_gpio_system(gpio_pin: int = 6, 
                                  printer: str = "Y812BT",
                                  aws_bucket: str = "burning-man-oracle-photos"):
    """Create complete Burning Man interactive GPIO system"""
    
    oracle_system = BurningManInteractiveOracle(
        printer_name=printer,
        aws_bucket=aws_bucket
    )
    
    try:
        from gpiozero import Button
        from signal import pause
        
        button = Button(gpio_pin)
        
        def on_button_press():
            oracle_system.process_interactive_session()
        
        def on_button_release():
            print("🔴 Button released - oracle ready for next participant")
        
        button.when_pressed = on_button_press
        button.when_released = on_button_release
        
        print("🎪 BURNING MAN INTERACTIVE ORACLE SYSTEM - LIVE")
        print("=" * 70)
        print(f"GPIO Pin: {gpio_pin}")
        print(f"Printer: {printer}")
        print(f"Camera: {'✅' if oracle_system.camera_enabled else '❌'}")
        print(f"Voice: {'✅' if oracle_system.voice_enabled else '❌'}")
        print(f"AWS Upload: {'✅' if oracle_system.s3_client else '❌'}")
        print("Flow: Button → Voice → Fortune → Photo → Print → Upload")
        print("=" * 70)
        print("🎭 Ready for participants! Press button to begin...")
        print("Press Ctrl+C to exit")
        print()
        
        pause()
        
    except ImportError:
        print("⚠️ GPIO hardware not available - running simulation mode")
        return oracle_system
    except KeyboardInterrupt:
        print("\n🛑 Burning Man oracle system shutting down...")
        
        # Show final statistics
        stats = oracle_system.get_session_statistics()
        print(f"📊 Final Stats: {stats.get('total_sessions', 0)} participants served")
        if 'consciousness_stats' in stats:
            print(f"🧠 Average Consciousness Φ: {stats['consciousness_stats']['avg_phi']:.3f}")
        print("🌊 Thank you for participating in consciousness evolution!")

# Main execution
if __name__ == "__main__":
    print("🎪 BURNING MAN INTERACTIVE ORACLE SYSTEM")
    print("🌊 Complete Experience: Voice → Fortune → Photo → Print → Cloud")
    print()
    
    # Check if GPIO hardware available
    try:
        from gpiozero import Button
        print("🔌 GPIO hardware detected - initializing interactive system...")
        create_burning_man_gpio_system(gpio_pin=6, printer="Y812BT")
        
    except ImportError:
        print("🎮 Interactive simulation mode - testing complete experience...")
        
        oracle = BurningManInteractiveOracle("Y812BT")
        
        # Run simulation tests
        print("\nTesting interactive oracle experience:")
        
        for session in range(3):
            print(f"\n" + "="*60)
            print(f"INTERACTIVE SIMULATION SESSION {session + 1}")
            print("="*60)
            
            success = oracle.simulate_interactive_session()
            
            if success:
                time.sleep(2)  # Brief pause between sessions
        
        # Show final statistics
        stats = oracle.get_session_statistics()
        print(f"\n📊 Simulation Statistics:")
        print(json.dumps(stats, indent=2))
        
        print("\n🎭 Interactive simulation complete - ready for Burning Man deployment!")