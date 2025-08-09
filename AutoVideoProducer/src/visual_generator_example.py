#!/usr/bin/env python3
"""
Visual Generator Example
Demonstrates how to use the VisualGenerator module
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_generator import VisualGenerator

def main():
    """Example usage of the VisualGenerator"""
    print("=== Visual Generator Example ===\n")
    
    # Initialize the visual generator
    print("Initializing visual generator...")
    generator = VisualGenerator()
    
    # Test script with various visual cues
    test_script = """
    Scene: Ancient Rome at sunset with epic architecture
    Visual: Dramatic battle scene with warriors and chariots
    Show: Modern city skyline at night with neon lights
    Describe scene: A peaceful mountain landscape with misty peaks
    Visual: Futuristic technology with holographic displays
    Scene: Corporate boardroom with professional atmosphere
    """
    
    print(f"Test script:\n{test_script}\n")
    
    # Generate visuals
    print("Generating visuals...")
    visual_paths = generator.generate_visuals(test_script)
    
    if visual_paths:
        print(f"\nGenerated {len(visual_paths)} visual assets:")
        for i, path in enumerate(visual_paths):
            print(f"  {i+1}. {os.path.basename(path)}")
            
        # Show generation statistics
        stats = generator.get_generation_stats()
        print(f"\nGeneration Statistics:")
        print(f"  Total images generated: {stats['total_images_generated']}")
        print(f"  Average quality: {stats['average_quality']:.1f}/10")
        print(f"  Stable Diffusion available: {stats['sd_available']}")
        print(f"  Ollama available: {stats['ollama_available']}")
        
        # Test subliminal embedding
        print("\nTesting subliminal image embedding...")
        if visual_paths:
            # Create a simple test logo (you would normally have a real logo file)
            test_logo_path = "assets/test_logo.png"
            if os.path.exists(test_logo_path):
                embedded_path = generator.embed_subliminal_images(visual_paths[0], test_logo_path)
                print(f"Embedded subliminal image: {os.path.basename(embedded_path)}")
            else:
                print("No test logo found, skipping subliminal embedding test")
    else:
        print("No visuals were generated.")
    
    print("\n=== Example completed ===")

if __name__ == "__main__":
    main()
