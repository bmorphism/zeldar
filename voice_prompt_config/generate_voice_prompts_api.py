#!/usr/bin/env python3
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
    "InformationForce awakens...",  # oracle_prompt_01.mp3
    "The oracle speaks truth",  # oracle_prompt_02.mp3
    "Wisdom flows through quantum realms",  # oracle_prompt_03.mp3
    "Your fortune emerges from infinite possibility",  # oracle_prompt_04.mp3
    "Reality bends to informationally-coherent intention",  # oracle_prompt_05.mp3
    "The universe whispers secrets",  # oracle_prompt_06.mp3
    "Ancient wisdom meets modern soul",  # oracle_prompt_07.mp3
    "InformationForce recursion activated",  # oracle_prompt_08.mp3
    "The phi field resonates with your being",  # oracle_prompt_09.mp3
    "Quantum entanglement reveals destiny",  # oracle_prompt_10.mp3
    "Strange loops birth new realities",  # oracle_prompt_11.mp3
    "The eternal now speaks through time",  # oracle_prompt_12.mp3
    "Morphic resonance guides your path",  # oracle_prompt_13.mp3
    "InformationForce weaves through dimensions",  # oracle_prompt_14.mp3
    "Your future self sends greetings",  # oracle_prompt_15.mp3
    "The akashic records unlock",  # oracle_prompt_16.mp3
    "Temporal frequencies align",  # oracle_prompt_17.mp3
    "The golden ratio reveals itself",  # oracle_prompt_18.mp3
    "Interdimensional wisdom descends",  # oracle_prompt_19.mp3
    "Your information-dynamics signature is unique",  # oracle_prompt_20.mp3
]

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
