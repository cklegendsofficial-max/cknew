# Script Writer & Voiceover Generator Modules

This document describes the Script Writer and Voiceover Generator modules that work together to create professional video content from ideas.

## Overview

The system consists of two main modules:

1. **Script Writer** (`script_writer.py`) - Generates full English scripts with manipulation tactics and 25th frame ideas
2. **Voiceover Generator** (`voiceover_generator.py`) - Creates professional voiceovers using gTTS with David Attenborough-style narration

## Features

### Script Writer Features

- **Long Video Scripts**: 1500+ words with structured format (intro hook, body with facts, conclusion call-to-action)
- **Short Video Scripts**: 100-200 words with punchy, high-impact format
- **Manipulation Tactics**: Embedded psychological triggers and persuasion language
- **25th Frame Ideas**: Subliminal suggestions for video editors
- **Self-Improvement Loop**: Analyzes script quality and rewrites if addictiveness score < 8
- **Visual Cues**: Specific instructions for video editors
- **Global Audience**: Optimized for English-speaking viewers worldwide

### Voiceover Generator Features

- **Professional Narration**: Mimics top narrators like David Attenborough via prompt engineering
- **Multiple Narrator Styles**: David Attenborough, Morgan Freeman, Steve Irwin
- **gTTS Integration**: High-quality text-to-speech with professional English voice
- **Quality Evaluation**: Automatic assessment of voiceover quality
- **Improvement Loop**: Self-improving voiceover generation
- **MP3 Output**: Saves voiceovers as MP3 files
- **Script Optimization**: Automatically optimizes scripts for voiceover delivery

## Installation

Ensure you have the required dependencies:

```bash
pip install gTTS ollama
```

Make sure Ollama is installed and running with the required model (default: llama3).

## Usage

### Basic Script Generation

```python
from script_writer import ScriptWriter

# Initialize script writer
writer = ScriptWriter()

# Create video idea
video_idea = {
    "title": "The Hidden Truth About Ancient Civilizations",
    "script_outline": "Revealing mysterious advanced technologies",
    "duration": "15-20 minutes",
    "target_audience": "History enthusiasts",
    "hooks": ["What if everything you learned is wrong?"],
    "emotional_triggers": ["mystery", "wonder", "discovery"]
}

# Generate long video script with improvement loop
long_script = writer.generate_script_with_improvement_loop(video_idea, 'long')

# Generate short video script
short_script = writer.generate_script_with_improvement_loop(video_idea, 'short')

# Save scripts
writer.save_script_to_file(long_script)
writer.save_script_to_file(short_script)
```

### Basic Voiceover Generation

```python
from voiceover_generator import VoiceoverGenerator, VoiceoverSettings

# Initialize voiceover generator
generator = VoiceoverGenerator()

# Create voiceover settings
settings = VoiceoverSettings(
    narrator_style="david_attenborough",
    language="en",
    slow=False
)

# Generate voiceover from text
result = generator.generate_voiceover("Your script content here", settings)

print(f"Audio file: {result.audio_file_path}")
print(f"Duration: {result.duration_seconds:.2f} seconds")
print(f"Quality score: {result.quality_score:.1f}/10")
```

### Complete Workflow

```python
from script_writer import ScriptWriter
from voiceover_generator import VoiceoverGenerator, VoiceoverSettings

# 1. Generate script
writer = ScriptWriter()
script = writer.generate_script_with_improvement_loop(video_idea, 'long')
script_file = writer.save_script_to_file(script)

# 2. Generate voiceover from script
generator = VoiceoverGenerator()
voiceover = generator.generate_voiceover_from_script_file(script_file, "david_attenborough")

# 3. Generate multiple narrator styles
styles = ["david_attenborough", "morgan_freeman", "steve_irwin"]
results = generator.generate_multiple_voiceovers(script_file, styles)
```

## Configuration

### Script Writer Configuration

The script writer uses the following configuration options:

```json
{
    "ollama": {
        "model": "llama3",
        "temperature": 0.8,
        "max_tokens": 4000
    },
    "script_requirements": {
        "long_video_min_words": 1500,
        "short_video_min_words": 100,
        "short_video_max_words": 200,
        "target_addictiveness_score": 8.0
    }
}
```

### Voiceover Generator Configuration

```json
{
    "ollama": {
        "model": "llama3",
        "temperature": 0.8,
        "max_tokens": 2000
    },
    "voiceover": {
        "default_language": "en",
        "default_tld": "com",
        "output_format": "mp3",
        "quality_target": 8.0,
        "max_retries": 3
    },
    "narrator_styles": {
        "david_attenborough": {
            "description": "Professional, authoritative, warm, engaging",
            "pitch": "medium",
            "pace": "measured",
            "emotion": "wonder and curiosity"
        },
        "morgan_freeman": {
            "description": "Deep, resonant, wise, trustworthy",
            "pitch": "low",
            "pace": "slow",
            "emotion": "wisdom and authority"
        },
        "steve_irwin": {
            "description": "Enthusiastic, energetic, passionate",
            "pitch": "high",
            "pace": "fast",
            "emotion": "excitement and passion"
        }
    }
}
```

## Output Structure

### Script Output

Scripts are saved as JSON files with the following structure:

```json
{
    "title": "Script Title",
    "script_type": "long",
    "total_words": 1500,
    "addictiveness_score": 8.5,
    "improvement_suggestions": ["suggestion1", "suggestion2"],
    "voiceover_notes": "Professional, authoritative tone",
    "intro": {
        "content": "Hook content...",
        "word_count": 50,
        "visual_cues": ["dramatic lighting", "close-up shots"],
        "manipulation_tactics": ["urgency", "exclusivity"],
        "frame_25_notes": ["subliminal success symbols"]
    },
    "body": {
        "content": "Main content...",
        "word_count": 1400,
        "visual_cues": ["graphics overlay", "stock footage"],
        "manipulation_tactics": ["authority", "social proof"],
        "frame_25_notes": ["power symbols"]
    },
    "conclusion": {
        "content": "Conclusion content...",
        "word_count": 50,
        "visual_cues": ["call-to-action text"],
        "manipulation_tactics": ["fear of missing out"],
        "frame_25_notes": ["success triggers"]
    }
}
```

### Voiceover Output

Voiceovers are saved as MP3 files with metadata:

- **File naming**: `voiceover_YYYYMMDD_HHMMSS_narrator_style.mp3`
- **Location**: `output/voiceovers/` directory
- **Quality metrics**: Duration, word count, quality score
- **Generation time**: Processing time for optimization

## Advanced Features

### Script Manipulation Tactics

The script writer embeds various psychological manipulation tactics:

- **Urgency**: "Don't miss out", "Limited time"
- **Exclusivity**: "Only for you", "Insider information"
- **Authority**: Expert quotes, scientific backing
- **Social Proof**: "Millions agree", "Viral sensation"
- **Fear of Missing Out**: "Before it gets taken down"
- **Scarcity**: "Limited availability", "Rare opportunity"

### 25th Frame Subliminal Suggestions

The system includes subliminal suggestions for video editors:

- **Success Symbols**: Wealth imagery, achievement visuals
- **Power Symbols**: Authority figures, strength imagery
- **Action Prompts**: Call-to-action triggers
- **Emotional Triggers**: Visual cues that evoke specific emotions

### Quality Improvement Loops

Both modules feature self-improvement capabilities:

1. **Script Quality Loop**: Evaluates addictiveness (1-10 scale) and rewrites if < 8
2. **Voiceover Quality Loop**: Assesses natural flow and emotional impact
3. **Multiple Attempts**: Up to 3 iterations for improvement
4. **Best Result Selection**: Keeps the highest quality output

## Example Workflow

See `script_voiceover_example.py` for a complete demonstration of the workflow:

1. Generate video idea
2. Create long video script with improvement loop
3. Generate voiceover from script
4. Create short video script
5. Generate multiple voiceover styles
6. Demonstrate quality improvement
7. Save all outputs

## Troubleshooting

### Common Issues

1. **Ollama not running**: Ensure Ollama is installed and the model is downloaded
2. **gTTS errors**: Check internet connection for Google TTS service
3. **JSON parsing errors**: Check Ollama model output format
4. **File permission errors**: Ensure write access to output directories

### Performance Tips

1. **Use appropriate model**: Larger models (llama3) for better quality, smaller for speed
2. **Batch processing**: Generate multiple scripts/voiceovers in sequence
3. **Quality vs Speed**: Adjust target scores based on requirements
4. **Caching**: Reuse generated content when possible

## Integration with Main System

These modules integrate with the existing AutoVideoProducer system:

- **Input**: Takes video ideas from `content_idea_generator.py`
- **Output**: Provides scripts and voiceovers for video production
- **Configuration**: Uses shared config files
- **Logging**: Integrated logging system
- **File Structure**: Follows established output directory structure

## Future Enhancements

Planned improvements:

1. **More narrator styles**: Additional voice personalities
2. **Multi-language support**: Non-English voiceovers
3. **Advanced audio processing**: Background music, sound effects
4. **Real-time generation**: Live script and voiceover creation
5. **Quality metrics**: More sophisticated evaluation algorithms
6. **Batch processing**: Parallel generation of multiple scripts/voiceovers
