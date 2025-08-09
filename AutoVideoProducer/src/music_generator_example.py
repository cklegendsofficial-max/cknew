#!/usr/bin/env python3
"""
Music Generator Example
Demonstrates how to use the MusicGenerator module
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from music_generator import MusicGenerator

def main():
    """Example usage of the MusicGenerator"""
    print("=== Music Generator Example ===\n")
    
    # Initialize the music generator
    print("Initializing music generator...")
    generator = MusicGenerator()
    
    # Test different video types
    video_types = [
        "history",
        "motivation", 
        "corporate",
        "nature",
        "technology",
        "sports"
    ]
    
    print("Testing music generation for different video types:\n")
    
    for video_type in video_types:
        print(f"Generating music for '{video_type}' video...")
        
        # Generate music
        music_path = generator.generate_music(video_type)
        
        if music_path:
            print(f"  ✓ Generated: {os.path.basename(music_path)}")
            
            # Assess quality
            quality = generator.assess_music_quality(music_path, video_type)
            print(f"  ✓ Quality rating: {quality}/10")
            
            # Show style info
            style = generator.determine_music_style(video_type)
            style_config = generator.config['music_styles'][style]
            print(f"  ✓ Style: {style} ({style_config['mood']})")
            print(f"  ✓ Tempo: {style_config['tempo']} BPM")
            print(f"  ✓ Key: {style_config['key']} {style_config['scale']}")
        else:
            print(f"  ✗ Failed to generate music for {video_type}")
        
        print()
    
    # Show generation statistics
    stats = generator.get_generation_stats()
    print("Generation Statistics:")
    print(f"  Total tracks generated: {stats['total_tracks_generated']}")
    print(f"  Music21 available: {stats['music21_available']}")
    print(f"  Audiocraft available: {stats['audiocraft_available']}")
    print(f"  Ollama available: {stats['ollama_available']}")
    print(f"  Cache size: {stats['cache_size']}")
    
    # Test composition suggestions
    print("\nTesting composition suggestions...")
    test_video_type = "epic_history"
    test_style = "epic"
    
    suggestions = generator.get_composition_suggestions(test_video_type, test_style)
    print(f"Composition suggestions for {test_video_type}:")
    print(f"  {suggestions}")
    
    print("\n=== Example completed ===")

if __name__ == "__main__":
    main()
