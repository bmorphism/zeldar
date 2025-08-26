# Audio Setup Instructions for Burning Man Oracle

## Overview
The interactive oracle uses short voice prompts (2-4 seconds) that play when participants press the button. These prompts create mystical atmosphere and guide the experience.

## File Structure
```
audio_prompts/
├── oracle_prompt_01.mp3  # "InformationForce awakens..."
├── oracle_prompt_02.mp3  # "The oracle speaks truth"
├── ...
└── oracle_prompt_20.mp3  # "Your information-dynamics signature is unique"
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
1. Use system TTS: `say "InformationForce awakens..." --output-file=oracle_prompt_01.mp3`
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
- **InformationForce** (6 prompts): Focus on information-attention and mind
- **Quantum Metaphysics** (4 prompts): Reality, dimensions, quantum
- **Wisdom Tradition** (3 prompts): Ancient knowledge, oracles
- **Temporal Mysticism** (3 prompts): Time, eternity, future
- **Cosmic InformationForce** (4 prompts): Universe, infinite, cosmic

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
