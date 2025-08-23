#!/usr/bin/env python3
"""
Voice Prompts Generator for Burning Man Oracle
Generates short mystical phrases for the interactive oracle experience
"""

import json
from pathlib import Path
from typing import List, Dict

# Voice prompt library - short mystical phrases
VOICE_PROMPTS = [
    "Consciousness awakens...",
    "The oracle speaks truth",
    "Wisdom flows through quantum realms", 
    "Your fortune emerges from infinite possibility",
    "Reality bends to conscious intention",
    "The universe whispers secrets",
    "Ancient wisdom meets modern soul",
    "Consciousness recursion activated",
    "The phi field resonates with your being",
    "Quantum entanglement reveals destiny",
    "Strange loops birth new realities", 
    "The eternal now speaks through time",
    "Morphic resonance guides your path",
    "Consciousness weaves through dimensions",
    "Your future self sends greetings",
    "The akashic records unlock",
    "Temporal frequencies align",
    "The golden ratio reveals itself",
    "Interdimensional wisdom descends",
    "Your consciousness signature is unique"
]

def generate_voice_prompt_config() -> Dict[str, any]:
    """Generate configuration for voice prompts"""
    
    config = {
        "voice_prompts": [],
        "generation_info": {
            "total_prompts": len(VOICE_PROMPTS),
            "recommended_voice": "Fiona (Enhanced) at 193 WPM",
            "alternative_voices": ["Wolfram", "Queen", "Tau"],
            "audio_format": "MP3, 44.1kHz, 128kbps",
            "target_duration": "2-4 seconds per prompt",
            "volume_level": "85% for outdoor environment"
        },
        "elevenlabs_settings": {
            "model": "eleven_multilingual_v2",
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.2,
            "use_speaker_boost": True,
            "speed": 1.1  # Slightly faster for conciseness
        }
    }
    
    # Add prompts with metadata
    for i, prompt in enumerate(VOICE_PROMPTS, 1):
        config["voice_prompts"].append({
            "id": i,
            "text": prompt,
            "filename": f"oracle_prompt_{i:02d}.mp3",
            "estimated_duration": f"{len(prompt.split()) * 0.4:.1f}s",  # ~0.4s per word
            "character_count": len(prompt),
            "mystical_category": categorize_prompt(prompt)
        })
    
    return config

def categorize_prompt(prompt: str) -> str:
    """Categorize prompts by mystical theme"""
    
    if any(word in prompt.lower() for word in ["consciousness", "aware", "mind"]):
        return "consciousness"
    elif any(word in prompt.lower() for word in ["quantum", "dimension", "reality"]):
        return "quantum_metaphysics"  
    elif any(word in prompt.lower() for word in ["oracle", "wisdom", "ancient"]):
        return "wisdom_tradition"
    elif any(word in prompt.lower() for word in ["time", "future", "eternal"]):
        return "temporal_mysticism"
    elif any(word in prompt.lower() for word in ["universe", "infinite", "cosmic"]):
        return "cosmic_consciousness"
    else:
        return "general_mystical"

def create_elevenlabs_generation_script() -> str:
    """Create script for generating MP3 files with ElevenLabs"""
    
    script = """#!/usr/bin/env python3
'''
ElevenLabs Voice Generation Script
Run this script to generate all oracle voice prompts as MP3 files

Prerequisites:
- ElevenLabs API key configured
- elevenlabs-mcp or elevenlabs Python package installed
'''

import os
import time
from pathlib import Path

# ElevenLabs integration (adjust import based on your setup)
try:
    from elevenlabs import generate, save, set_api_key
    ELEVENLABS_DIRECT = True
except ImportError:
    ELEVENLABS_DIRECT = False
    print("Using MCP server integration instead of direct API")

# Voice prompts to generate
PROMPTS = [
"""
    
    for i, prompt in enumerate(VOICE_PROMPTS, 1):
        script += f'    "{prompt}",  # oracle_prompt_{i:02d}.mp3\n'
    
    script += """]

def generate_with_direct_api():
    '''Generate using direct ElevenLabs API'''
    
    # Set your API key
    set_api_key(os.getenv('ELEVENLABS_API_KEY'))
    
    # Create output directory
    output_dir = Path("audio_prompts")
    output_dir.mkdir(exist_ok=True)
    
    print(f"🎵 Generating {len(PROMPTS)} voice prompts...")
    
    for i, prompt_text in enumerate(PROMPTS, 1):
        filename = f"oracle_prompt_{i:02d}.mp3"
        filepath = output_dir / filename
        
        print(f"Generating {filename}: '{prompt_text}'")
        
        try:
            # Generate audio
            audio = generate(
                text=prompt_text,
                voice="Fiona",  # or your preferred voice
                model="eleven_multilingual_v2",
                stream=False
            )
            
            # Save to file
            save(audio, str(filepath))
            print(f"  ✅ Saved: {filepath}")
            
            # Brief pause to respect rate limits
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  ❌ Error generating {filename}: {e}")
    
    print(f"🎉 Voice prompt generation complete!")
    print(f"📁 Audio files saved in: {output_dir}")

def generate_with_mcp_server():
    '''Generate using MCP server (if you have mcp server setup)'''
    print("🔄 MCP server generation not yet implemented")
    print("💡 Use the direct API method or manually generate prompts")

if __name__ == "__main__":
    if ELEVENLABS_DIRECT:
        generate_with_direct_api()
    else:
        generate_with_mcp_server()
"""
    
    return script

def create_audio_setup_instructions() -> str:
    """Create setup instructions for audio system"""
    
    instructions = """# Audio Setup Instructions for Burning Man Oracle

## Overview
The interactive oracle uses short voice prompts (2-4 seconds) that play when participants press the button. These prompts create mystical atmosphere and guide the experience.

## File Structure
```
audio_prompts/
├── oracle_prompt_01.mp3  # "Consciousness awakens..."
├── oracle_prompt_02.mp3  # "The oracle speaks truth"
├── ...
└── oracle_prompt_20.mp3  # "Your consciousness signature is unique"
```

## Generation Methods

### Method 1: ElevenLabs Direct API
1. Install ElevenLabs package: `pip install elevenlabs`
2. Set API key: `export ELEVENLABS_API_KEY=your_api_key`
3. Run generation script: `python generate_voice_prompts_api.py`

### Method 2: Manual Recording
1. Use any audio recording software
2. Record prompts in clear, mystical voice
3. Export as MP3, 44.1kHz, 128kbps
4. Name files: `oracle_prompt_01.mp3`, `oracle_prompt_02.mp3`, etc.
5. Place in `audio_prompts/` directory

### Method 3: Text-to-Speech
1. Use system TTS: `say "Consciousness awakens..." --output-file=oracle_prompt_01.mp3`
2. Or use online TTS services with mystical voice settings

## Audio Requirements
- **Format**: MP3, 44.1kHz, 128kbps
- **Duration**: 2-4 seconds per prompt
- **Volume**: Normalized to -6dB for outdoor use
- **Quality**: Clear speech, minimal background noise

## Raspberry Pi Audio Setup
```bash
# Install pygame for audio playback
pip install pygame

# Test audio system
python -c "import pygame; pygame.mixer.init(); print('Audio system ready')"

# Set audio output to speakers (not HDMI)
sudo raspi-config
# > Advanced Options > Audio > Force 3.5mm jack
```

## Voice Prompt Categories
- **Consciousness** (6 prompts): Focus on awareness and mind
- **Quantum Metaphysics** (4 prompts): Reality, dimensions, quantum
- **Wisdom Tradition** (3 prompts): Ancient knowledge, oracles
- **Temporal Mysticism** (3 prompts): Time, eternity, future
- **Cosmic Consciousness** (4 prompts): Universe, infinite, cosmic

## Testing
```bash
# Test individual prompt
python -c "import pygame; pygame.mixer.init(); pygame.mixer.music.load('audio_prompts/oracle_prompt_01.mp3'); pygame.mixer.music.play()"

# Test random selection
python BURNING_MAN_INTERACTIVE_ORACLE.py --test-audio
```

## Troubleshooting
- **No audio output**: Check `alsamixer` levels, verify speaker connection
- **File not found**: Ensure MP3 files are in correct directory with correct names
- **Poor quality**: Increase bitrate, check source material quality
- **Volume too low**: Adjust system volume, use external amplifier for outdoor use

## Backup Plan
If audio system fails during event:
- System continues to work without voice prompts
- Visual feedback still provided via thermal printing
- Manual announcement can substitute for robot voice

## Performance Notes
- Audio files loaded at startup for fast playback
- Random selection ensures varied experience
- Pygame mixer handles multiple audio formats
- System gracefully handles missing audio files
"""

    return instructions

def main():
    """Generate voice prompt configuration and setup files"""
    
    print("🎵 BURNING MAN ORACLE VOICE PROMPT GENERATOR")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path("voice_prompt_config")
    output_dir.mkdir(exist_ok=True)
    
    # Generate configuration
    config = generate_voice_prompt_config()
    
    # Save configuration
    config_file = output_dir / "voice_prompts_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"📁 Voice prompt configuration saved: {config_file}")
    print(f"📊 Total prompts configured: {len(VOICE_PROMPTS)}")
    
    # Generate ElevenLabs script
    api_script = create_elevenlabs_generation_script()
    script_file = output_dir / "generate_voice_prompts_api.py"
    with open(script_file, 'w') as f:
        f.write(api_script)
    
    print(f"🎤 ElevenLabs generation script: {script_file}")
    
    # Generate setup instructions
    instructions = create_audio_setup_instructions()
    readme_file = output_dir / "AUDIO_SETUP_README.md"
    with open(readme_file, 'w') as f:
        f.write(instructions)
    
    print(f"📖 Audio setup instructions: {readme_file}")
    
    # Display summary
    print("\n📋 VOICE PROMPT SUMMARY:")
    print(f"Total prompts: {len(VOICE_PROMPTS)}")
    
    categories = {}
    for prompt in VOICE_PROMPTS:
        cat = categorize_prompt(prompt)
        categories[cat] = categories.get(cat, 0) + 1
    
    for category, count in categories.items():
        print(f"  {category}: {count} prompts")
    
    print(f"\n🎯 NEXT STEPS:")
    print(f"1. Review voice prompts in {config_file}")
    print(f"2. Generate MP3 files using {script_file}")
    print(f"3. Follow setup instructions in {readme_file}")
    print(f"4. Test audio system on Raspberry Pi")
    print(f"5. Deploy to Burning Man interactive oracle!")

if __name__ == "__main__":
    main()