# Content Idea Generator Module

## Overview

The `content_idea_generator.py` module is a comprehensive content generation system that scrapes trending topics from various sources and generates unique video ideas using AI. It's designed to work with the AutoVideoProducer application to automatically generate content ideas for multiple channels.

## Features

### 🔍 **Multi-Source Scraping**
- **Reddit**: Scrapes trending posts from r/popular and r/trending
- **News Sites**: BBC, CNBC, Reuters for breaking news and trends
- **YouTube Trending**: Fallback scraping of trending videos
- **Google Trends**: Fallback trending topics when other sources fail

### 🤖 **AI-Powered Content Generation**
- **Ollama Integration**: Uses local LLM for content generation
- **Subliminal Hooks**: Implements NLP techniques and psychological triggers
- **Emotional Triggers**: Curiosity gaps, fear of missing out, social proof
- **Addictive Content**: Designed to maximize engagement and retention

### 📊 **Smart Caching System**
- **24-hour cache**: Prevents redundant scraping
- **Fallback mechanisms**: Works offline with cached data
- **Error handling**: Graceful degradation when sources fail

### 🎯 **Content Types Generated**
- **Long Videos**: 10+ minute comprehensive content ideas
- **Short Videos**: 30-60 second viral content ideas
- **Targeted Audiences**: Specific audience segmentation
- **Script Outlines**: Detailed content structure

## Installation

### Prerequisites
```bash
pip install requests beautifulsoup4
```

### Optional: Ollama Setup
For AI-powered content generation:
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download the model
ollama pull llama3
```

## Usage

### Basic Usage

```python
from content_idea_generator import ContentIdeaGenerator

# Initialize the generator
generator = ContentIdeaGenerator()

# Generate ideas for a channel topic
ideas = generator.generate_ideas("AI Technology")

# Access the results
long_idea = ideas['long_idea']
shorts_ideas = ideas['shorts_ideas']

print(f"Long Video: {long_idea['title']}")
for i, short in enumerate(shorts_ideas, 1):
    print(f"Short {i}: {short['title']}")
```

### Integration with Main App

```python
# Load configuration from main app
config_path = "config/config.json"
generator = ContentIdeaGenerator(config_path)

# Generate ideas for all channels
with open(config_path, 'r') as f:
    config = json.load(f)

for channel in config['channels']:
    ideas = generator.generate_ideas(channel['topic'])
    # Process ideas for video production
```

### Daily Content Schedule

```python
# Generate daily content for multiple topics
daily_topics = ["AI Technology", "Cryptocurrency", "Fitness", "Cooking"]

for topic in daily_topics:
    ideas = generator.generate_ideas(topic)
    # Schedule content production
```

## Configuration

The module uses the main application's `config.json` file with additional settings:

```json
{
    "channels": [
        {"name": "CKLegends", "topic": "History"},
        {"name": "CKFinanceCore", "topic": "Finance"}
    ],
    "scraping": {
        "timeout": 10,
        "max_retries": 3,
        "delay_between_requests": 1
    },
    "ollama": {
        "model": "llama3",
        "temperature": 0.8,
        "max_tokens": 2000
    },
    "sources": {
        "reddit": ["https://www.reddit.com/r/popular/"],
        "news": ["https://www.bbc.com/news"],
        "youtube_trending": "https://www.youtube.com/feed/trending"
    }
}
```

## Output Format

### Long Video Idea
```json
{
    "title": "Breaking: Latest AI Technology Trends You Can't Miss",
    "script_outline": "Introduction with hook → Main trend analysis → Expert insights → Future predictions → Call to action",
    "target_audience": "AI Technology enthusiasts and industry professionals",
    "hooks": ["You won't believe what's happening", "This changes everything"],
    "emotional_triggers": ["Fear of missing out", "Curiosity gap", "Social proof"],
    "duration": "10-15 minutes"
}
```

### Short Video Ideas
```json
[
    {
        "title": "Quick AI Technology Tip That Will Shock You",
        "script_outline": "Hook → Quick tip → Surprise reveal → Call to action",
        "target_audience": "AI Technology beginners and enthusiasts",
        "hooks": ["This one trick", "You'll be shocked"],
        "emotional_triggers": ["Curiosity", "Surprise"],
        "duration": "30-60 seconds"
    }
]
```

## Advanced Features

### Subliminal Hooks & NLP Techniques

The module implements advanced psychological triggers:

- **Curiosity Gaps**: "You won't believe what's happening..."
- **Fear of Missing Out**: "This changes everything..."
- **Social Proof**: "What experts are hiding..."
- **Urgency**: "Breaking news you can't miss..."
- **Controversy**: "The secret they don't want you to know..."

### Error Handling & Fallbacks

1. **Network Failures**: Falls back to cached trending topics
2. **Ollama Unavailable**: Uses pre-generated fallback responses
3. **Scraping Blocked**: Uses Google Trends fallback
4. **Cache Corruption**: Regenerates from scratch

### Caching System

- **Trending Topics**: Cached for 24 hours
- **Generated Ideas**: Cached per channel topic
- **Automatic Cleanup**: Old cache files are ignored
- **Deduplication**: Removes similar topics

## Testing

### Run Basic Test
```bash
cd AutoVideoProducer/src
python content_idea_generator.py
```

### Run Integration Example
```bash
python content_idea_generator_example.py
```

## Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   - Ensure Ollama is installed and running
   - Check if the model is downloaded: `ollama list`
   - The module works without Ollama using fallbacks

2. **Scraping Failures**
   - Network connectivity issues
   - Rate limiting from sources
   - Module falls back to cached data

3. **Configuration Errors**
   - Check `config.json` format
   - Ensure all required fields are present
   - Module uses defaults if config is missing

### Performance Optimization

- **Parallel Scraping**: Sources are scraped sequentially to avoid rate limiting
- **Smart Caching**: Reduces redundant API calls
- **Timeout Handling**: Prevents hanging requests
- **Memory Management**: Efficient data structures

## Integration with AutoVideoProducer

The module is designed to integrate seamlessly with the main AutoVideoProducer application:

1. **Configuration Sharing**: Uses the same config.json
2. **Logging Integration**: Compatible with main app logging
3. **Error Handling**: Graceful degradation
4. **Cache Management**: Shared cache directory

## Future Enhancements

- **More Sources**: Twitter, Instagram, TikTok trends
- **Advanced AI**: Better prompt engineering
- **Analytics**: Track idea performance
- **A/B Testing**: Compare different content approaches
- **Multi-language**: Support for different languages

## License

This module is part of the AutoVideoProducer project and follows the same licensing terms.
