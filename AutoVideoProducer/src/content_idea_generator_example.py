"""
Auto-improved by SelfImprover on 2025-08-06 15:50:36

Improvements applied:
- Nested loops detected. Consider using list comprehensions or vectorized operations.
- Nested loops detected. Consider using list comprehensions or vectorized operations.
- Long hardcoded string detected. Consider moving to configuration file.
- Long hardcoded string detected. Consider moving to configuration file.
- Long hardcoded string detected. Consider moving to configuration file.

AI Suggestions:
Ollama request timed out...
"""

#!/usr/bin/env python3
"""
Content Idea Generator Integration Example
Shows how to integrate the content idea generator with the main AutoVideoProducer application
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from content_idea_generator import ContentIdeaGenerator
import json
from datetime import datetime

def integrate_with_main_app():
    """Example of how to integrate with the main AutoVideoProducer application"""
    
    # Initialize the content idea generator
    generator = ContentIdeaGenerator()
    
    # Load channel configuration from main app
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        channels = config.get('channels', [])
        
        print("=" * 60)
        print("CONTENT IDEA GENERATOR INTEGRATION")
        print("=" * 60)
        
        # Generate ideas for each channel
        for channel in channels:
            channel_name = channel['name']
            channel_topic = channel['topic']
            
            print(f"\n🎬 Generating ideas for channel: {channel_name}")
            print(f"📝 Topic: {channel_topic}")
            print("-" * 40)
            
            # Generate ideas
            ideas = generator.generate_ideas(channel_topic)
            
            # Display long video idea
            long_idea = ideas['long_idea']
            print(f"\n🎥 LONG VIDEO IDEA:")
            print(f"   Title: {long_idea['title']}")
            print(f"   Duration: {long_idea['duration']}")
            print(f"   Target Audience: {long_idea['target_audience']}")
            print(f"   Script Outline: {long_idea['script_outline']}")
            print(f"   Hooks: {', '.join(long_idea['hooks'])}")
            print(f"   Emotional Triggers: {', '.join(long_idea['emotional_triggers'])}")
            
            # Display short video ideas
            print(f"\n📱 SHORT VIDEO IDEAS:")
            for i, short_idea in enumerate(ideas['shorts_ideas'], 1):
                print(f"\n   {i}. {short_idea['title']}")
                print(f"      Duration: {short_idea['duration']}")
                print(f"      Target Audience: {short_idea['target_audience']}")
                print(f"      Script Outline: {short_idea['script_outline']}")
                print(f"      Hooks: {', '.join(short_idea['hooks'])}")
                print(f"      Emotional Triggers: {', '.join(short_idea['emotional_triggers'])}")
            
            print("\n" + "=" * 60)
    
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return False
    
    return True

def daily_content_schedule():
    """Example of how to schedule daily content generation"""
    
    generator = ContentIdeaGenerator()
    
    # Example channel topics for daily content
    daily_topics = [
        "AI Technology",
        "Cryptocurrency", 
        "Fitness",
        "Cooking",
        "Travel"
    ]
    
    print("\n" + "=" * 60)
    print("DAILY CONTENT SCHEDULE")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    for topic in daily_topics:
        print(f"\n📅 Generating daily content for: {topic}")
        
        # Generate ideas
        ideas = generator.generate_ideas(topic)
        
        # Display summary
        long_idea = ideas['long_idea']
        print(f"   🎥 Long Video: {long_idea['title']}")
        
        for i, short_idea in enumerate(ideas['shorts_ideas'], 1):
            print(f"   📱 Short {i}: {short_idea['title']}")
        
        print("-" * 40)

def main():
    """Main function to demonstrate the content idea generator"""
    
    print("Content Idea Generator - Integration Examples")
    print("=" * 60)
    
    # Example 1: Integration with main app
    print("\n1. INTEGRATION WITH MAIN APP")
    integrate_with_main_app()
    
    # Example 2: Daily content schedule
    print("\n2. DAILY CONTENT SCHEDULE")
    daily_content_schedule()
    
    print("\n✅ Content idea generation completed successfully!")

if __name__ == "__main__":
    main()
