#!/usr/bin/env python3
"""
Script Writer and Voiceover Generator Example
Demonstrates the complete workflow from video idea to voiceover generation
"""

import os
import sys
import json
import time
from datetime import datetime

# Add the src directory to the path
sys.path.append(os.path.dirname(__file__))

from script_writer import ScriptWriter
from voiceover_generator import VoiceoverGenerator, VoiceoverSettings

def main():
    """Main function demonstrating the complete workflow"""
    
    print("="*60)
    print("SCRIPT WRITER & VOICEOVER GENERATOR WORKFLOW")
    print("="*60)
    
    # Initialize modules
    print("\n1. Initializing modules...")
    script_writer = ScriptWriter()
    voiceover_generator = VoiceoverGenerator()
    
    # Test video idea
    test_idea = {
        "title": "The Hidden Truth About Ancient Civilizations",
        "script_outline": "Revealing the mysterious advanced technologies and knowledge of ancient civilizations that mainstream archaeology ignores",
        "duration": "15-20 minutes",
        "target_audience": "History enthusiasts, conspiracy theorists, curious minds",
        "hooks": ["What if everything you learned about history is wrong?", "Ancient civilizations had technology we can't replicate today"],
        "emotional_triggers": ["mystery", "wonder", "skepticism", "discovery"]
    }
    
    print(f"Test idea: {test_idea['title']}")
    
    # Step 1: Generate long video script with improvement loop
    print("\n2. Generating long video script...")
    start_time = time.time()
    
    long_script = script_writer.generate_script_with_improvement_loop(test_idea, 'long')
    
    script_time = time.time() - start_time
    print(f"Script generation completed in {script_time:.2f} seconds")
    print(f"Script details:")
    print(f"  - Title: {long_script.title}")
    print(f"  - Type: {long_script.script_type}")
    print(f"  - Total Words: {long_script.total_words}")
    print(f"  - Addictiveness Score: {long_script.addictiveness_score:.1f}/10")
    print(f"  - Improvement Suggestions: {len(long_script.improvement_suggestions)}")
    
    # Save script to file
    script_file_path = script_writer.save_script_to_file(long_script)
    print(f"Script saved to: {script_file_path}")
    
    # Step 2: Generate voiceover from script
    print("\n3. Generating voiceover from script...")
    start_time = time.time()
    
    # Create voiceover settings
    voiceover_settings = VoiceoverSettings(
        narrator_style="david_attenborough",
        language="en",
        slow=False
    )
    
    # Generate voiceover
    voiceover_result = voiceover_generator.generate_voiceover_from_script_file(
        script_file_path, 
        voiceover_settings.narrator_style
    )
    
    voiceover_time = time.time() - start_time
    print(f"Voiceover generation completed in {voiceover_time:.2f} seconds")
    print(f"Voiceover details:")
    print(f"  - Audio File: {voiceover_result.audio_file_path}")
    print(f"  - Duration: {voiceover_result.duration_seconds:.2f} seconds")
    print(f"  - Word Count: {voiceover_result.word_count}")
    print(f"  - Quality Score: {voiceover_result.quality_score:.1f}/10")
    print(f"  - Notes: {voiceover_result.voiceover_notes}")
    
    # Step 3: Generate short video script
    print("\n4. Generating short video script...")
    start_time = time.time()
    
    short_script = script_writer.generate_script_with_improvement_loop(test_idea, 'short')
    
    script_time = time.time() - start_time
    print(f"Short script generation completed in {script_time:.2f} seconds")
    print(f"Short script details:")
    print(f"  - Title: {short_script.title}")
    print(f"  - Type: {short_script.script_type}")
    print(f"  - Total Words: {short_script.total_words}")
    print(f"  - Addictiveness Score: {short_script.addictiveness_score:.1f}/10")
    
    # Save short script
    short_script_file_path = script_writer.save_script_to_file(short_script)
    print(f"Short script saved to: {short_script_file_path}")
    
    # Step 4: Generate multiple voiceover styles
    print("\n5. Generating multiple voiceover styles...")
    start_time = time.time()
    
    narrator_styles = ["david_attenborough", "morgan_freeman", "steve_irwin"]
    voiceover_results = voiceover_generator.generate_multiple_voiceovers(
        short_script_file_path, 
        narrator_styles
    )
    
    voiceover_time = time.time() - start_time
    print(f"Multiple voiceover generation completed in {voiceover_time:.2f} seconds")
    
    print(f"Multiple voiceover results:")
    for i, result in enumerate(voiceover_results):
        print(f"  {i+1}. {narrator_styles[i]}:")
        print(f"     - File: {result.audio_file_path}")
        print(f"     - Quality: {result.quality_score:.1f}/10")
        print(f"     - Duration: {result.duration_seconds:.2f}s")
    
    # Step 5: Quality improvement demonstration
    print("\n6. Demonstrating quality improvement loop...")
    start_time = time.time()
    
    # Extract script content for improvement
    script_content = f"{long_script.intro.content}\n\n{long_script.body.content}\n\n{long_script.conclusion.content}"
    
    improved_voiceover = voiceover_generator.improve_voiceover_quality(
        script_content,
        voiceover_settings,
        target_quality=8.0
    )
    
    improvement_time = time.time() - start_time
    print(f"Quality improvement completed in {improvement_time:.2f} seconds")
    print(f"Improved voiceover:")
    print(f"  - Audio File: {improved_voiceover.audio_file_path}")
    print(f"  - Quality Score: {improved_voiceover.quality_score:.1f}/10")
    print(f"  - Generation Time: {improved_voiceover.generation_time:.2f} seconds")
    
    # Step 6: Summary and statistics
    print("\n" + "="*60)
    print("WORKFLOW SUMMARY")
    print("="*60)
    
    total_time = script_time + voiceover_time + improvement_time
    print(f"Total processing time: {total_time:.2f} seconds")
    print(f"Scripts generated: 2 (1 long, 1 short)")
    print(f"Voiceovers generated: {len(voiceover_results) + 2} (including improvement)")
    print(f"Best addictiveness score: {max(long_script.addictiveness_score, short_script.addictiveness_score):.1f}/10")
    print(f"Best voiceover quality: {max([r.quality_score for r in voiceover_results] + [improved_voiceover.quality_score]):.1f}/10")
    
    # Display script samples
    print("\n" + "="*60)
    print("SCRIPT SAMPLES")
    print("="*60)
    
    print(f"\nLONG VIDEO SCRIPT SAMPLE:")
    print(f"Intro ({long_script.intro.word_count} words):")
    print(f"  {long_script.intro.content[:200]}...")
    print(f"\nManipulation Tactics: {long_script.intro.manipulation_tactics}")
    print(f"25th Frame Notes: {long_script.intro.frame_25_notes}")
    
    print(f"\nSHORT VIDEO SCRIPT SAMPLE:")
    print(f"Intro ({short_script.intro.word_count} words):")
    print(f"  {short_script.intro.content[:100]}...")
    print(f"\nManipulation Tactics: {short_script.intro.manipulation_tactics}")
    print(f"25th Frame Notes: {short_script.intro.frame_25_notes}")
    
    # Display output file locations
    print("\n" + "="*60)
    print("OUTPUT FILES")
    print("="*60)
    
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    scripts_dir = os.path.join(output_dir, 'scripts')
    voiceovers_dir = os.path.join(output_dir, 'voiceovers')
    
    print(f"Scripts directory: {scripts_dir}")
    print(f"Voiceovers directory: {voiceovers_dir}")
    
    if os.path.exists(scripts_dir):
        script_files = [f for f in os.listdir(scripts_dir) if f.endswith('.json')]
        print(f"Script files generated: {len(script_files)}")
    
    if os.path.exists(voiceovers_dir):
        voiceover_files = [f for f in os.listdir(voiceovers_dir) if f.endswith('.mp3')]
        print(f"Voiceover files generated: {len(voiceover_files)}")
    
    print("\nWorkflow completed successfully!")
    print("Check the output directories for generated files.")

def test_individual_modules():
    """Test individual modules separately"""
    
    print("\n" + "="*60)
    print("INDIVIDUAL MODULE TESTING")
    print("="*60)
    
    # Test script writer
    print("\nTesting Script Writer...")
    script_writer = ScriptWriter()
    
    test_idea = {
        "title": "The Mystery of Lost Technologies",
        "script_outline": "Exploring ancient technologies that were lost to time",
        "duration": "10 minutes",
        "target_audience": "History buffs",
        "hooks": ["Lost technology discovered"],
        "emotional_triggers": ["curiosity", "wonder"]
    }
    
    script = script_writer.generate_script_with_improvement_loop(test_idea, 'short')
    print(f"Script generated: {script.title} ({script.total_words} words)")
    
    # Test voiceover generator
    print("\nTesting Voiceover Generator...")
    voiceover_generator = VoiceoverGenerator()
    
    test_text = "This is a test of the voiceover generation system."
    result = voiceover_generator.test_voiceover_generation(test_text)
    print(f"Voiceover generated: {result.audio_file_path}")
    print(f"Quality score: {result.quality_score:.1f}/10")

if __name__ == "__main__":
    # Run individual module tests first
    test_individual_modules()
    
    # Run complete workflow
    main()
