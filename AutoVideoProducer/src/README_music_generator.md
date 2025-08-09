# Music Generator Module

The Music Generator module creates professional background music tracks for video production using AI-powered composition and intelligent style matching.

## Features

### 🎵 **AI-Powered Music Generation**
- **Audiocraft MusicGen**: Advanced AI music generation with natural-sounding compositions
- **Music21 Integration**: Professional music theory-based composition
- **MIDI Generation**: Fallback system for simple but effective music creation
- **Style Matching**: Automatically matches music style to video content

### 🎼 **Intelligent Style Selection**
- **Video Type Analysis**: Determines appropriate music style based on video content
- **Emotional Mapping**: Maps video types to emotional musical responses
- **Professional Styles**: Epic, upbeat, calm, and corporate music styles
- **Hans Zimmer Inspiration**: Epic orchestral compositions with dramatic dynamics

### 🎯 **Quality Assurance**
- **Self-Improvement**: Uses Ollama to assess music quality (1-10 scale)
- **Composition Suggestions**: AI-powered recommendations for musical elements
- **Professional Standards**: Mimics top composers like Hans Zimmer
- **Emotional Appropriateness**: Ensures music matches video mood and content

### 🔄 **Fallback Systems**
- **Multiple Generation Methods**: Audiocraft → Music21 → Simple MIDI
- **Error Handling**: Graceful degradation when services are unavailable
- **Format Conversion**: Automatic MIDI to MP3 conversion
- **Quality Assessment**: Continuous improvement through feedback

### 🎭 **Advanced Features**
- **Duration Control**: Configurable track lengths for different video types
- **Instrument Selection**: Appropriate instruments for each music style
- **Tempo Matching**: BPM optimization for video pacing
- **Key Selection**: Musical key optimization for emotional impact

## Installation

### Prerequisites
```bash
# Install music generation dependencies
pip install music21 torch audiocraft pydub midiutil

# Install additional dependencies
pip install requests beautifulsoup4

# Install Ollama (for composition suggestions and quality assessment)
# Follow instructions at: https://ollama.ai/
```

### Quick Setup
```bash
# Install all dependencies
pip install -r requirements.txt

# Download Audiocraft models (first run)
python -c "from audiocraft.models import MusicGen; MusicGen.get_pretrained('medium')"
```

## Usage

### Basic Usage
```python
from music_generator import MusicGenerator

# Initialize generator
generator = MusicGenerator()

# Generate music for different video types
video_types = ["history", "motivation", "corporate", "nature"]

for video_type in video_types:
    music_path = generator.generate_music(video_type)
    print(f"Generated music for {video_type}: {music_path}")
```

### Advanced Usage
```python
# Custom configuration
config = {
    "default_duration": 120,  # 2 minutes
    "music_styles": {
        "epic": {
            "tempo": 120,
            "key": "C",
            "scale": "major",
            "instruments": ["strings", "brass", "percussion"],
            "mood": "dramatic and powerful"
        }
    }
}

generator = MusicGenerator(config_path="custom_config.json")

# Generate with quality assessment
music_path = generator.generate_music("epic_history")

# Assess quality
quality = generator.assess_music_quality(music_path, "epic_history")
print(f"Music quality: {quality}/10")

# Get composition suggestions
suggestions = generator.get_composition_suggestions("epic_history", "epic")
print(f"Composition suggestions: {suggestions}")
```

### Configuration Options

The music generator supports extensive configuration:

```json
{
  "music_generator": {
    "default_duration": 60,
    "sample_rate": 44100,
    "bit_depth": 16,
    "music_styles": {
      "epic": {
        "tempo": 120,
        "key": "C",
        "scale": "major",
        "instruments": ["strings", "brass", "percussion"],
        "mood": "dramatic and powerful"
      },
      "upbeat": {
        "tempo": 140,
        "key": "G",
        "scale": "major",
        "instruments": ["piano", "drums", "bass"],
        "mood": "energetic and motivational"
      },
      "calm": {
        "tempo": 80,
        "key": "D",
        "scale": "minor",
        "instruments": ["piano", "strings", "ambient"],
        "mood": "peaceful and contemplative"
      },
      "corporate": {
        "tempo": 100,
        "key": "F",
        "scale": "major",
        "instruments": ["piano", "strings", "soft_percussion"],
        "mood": "professional and confident"
      }
    },
    "hans_zimmer_style": "Epic orchestral composition with dramatic dynamics",
    "self_improve": true,
    "use_audiocraft": true
  }
}
```

## Music Styles

### Epic Style
- **Use Case**: History, documentaries, dramatic content
- **Tempo**: 120 BPM
- **Key**: C Major
- **Instruments**: Strings, brass, percussion
- **Mood**: Dramatic and powerful

### Upbeat Style
- **Use Case**: Motivation, sports, technology, entertainment
- **Tempo**: 140 BPM
- **Key**: G Major
- **Instruments**: Piano, drums, bass
- **Mood**: Energetic and motivational

### Calm Style
- **Use Case**: Nature, travel, meditation, peaceful content
- **Tempo**: 80 BPM
- **Key**: D Minor
- **Instruments**: Piano, strings, ambient
- **Mood**: Peaceful and contemplative

### Corporate Style
- **Use Case**: Business, educational, professional content
- **Tempo**: 100 BPM
- **Key**: F Major
- **Instruments**: Piano, strings, soft percussion
- **Mood**: Professional and confident

## Video Type Mapping

The generator automatically maps video types to music styles:

| Video Type | Music Style | Characteristics |
|------------|-------------|-----------------|
| history | epic | Dramatic orchestral |
| motivation | upbeat | Energetic and driving |
| corporate | corporate | Professional and confident |
| nature | calm | Peaceful and ambient |
| technology | upbeat | Modern and energetic |
| sports | upbeat | High-energy and dynamic |
| news | corporate | Professional and trustworthy |
| entertainment | upbeat | Fun and engaging |

## Output Structure

Generated music is saved to `assets/music/` with the following naming convention:
- `audiocraft_[type]_[timestamp].mp3` - Audiocraft generated music
- `music21_[type]_[timestamp].mp3` - Music21 generated music
- `simple_[type]_[timestamp].mp3` - Simple MIDI generated music

## Quality Assessment

The module uses Ollama to assess music quality based on:
- **Emotional Appropriateness**: How well music matches video content
- **Professional Quality**: Production standards and technical quality
- **Video Synchronization**: Potential for video accompaniment
- **Overall Impact**: Emotional and technical effectiveness

## Performance Optimization

### Hardware Requirements
- **Recommended**: GPU with 4GB+ VRAM for Audiocraft
- **Minimum**: CPU with 8GB RAM for Music21
- **Fallback**: Any system for simple MIDI generation

### Memory Management
- Automatic model loading/unloading
- Efficient audio processing
- Temporary file cleanup

## Error Handling

The module includes robust error handling:
- **Audiocraft Failures**: Falls back to Music21
- **Music21 Failures**: Falls back to simple MIDI
- **Ollama Unavailable**: Uses default composition suggestions
- **Format Issues**: Automatic conversion and fallback

## Integration with Main Application

The music generator is integrated into the main AutoVideoProducer workflow:

1. **Video Type Analysis**: Determines music style from script content
2. **Music Generation**: Creates appropriate background tracks
3. **Quality Control**: Assesses and improves generated music
4. **Video Integration**: Provides music for video composition

## Example Output

```
Generated music for history: audiocraft_history_1703123456.mp3
  ✓ Quality rating: 9/10
  ✓ Style: epic (dramatic and powerful)
  ✓ Tempo: 120 BPM
  ✓ Key: C major

Generated music for motivation: music21_motivation_1703123457.mp3
  ✓ Quality rating: 8/10
  ✓ Style: upbeat (energetic and motivational)
  ✓ Tempo: 140 BPM
  ✓ Key: G major

Generation Statistics:
  Total tracks generated: 4
  Music21 available: True
  Audiocraft available: True
  Ollama available: True
```

## Troubleshooting

### Common Issues

1. **Audiocraft Model Download**
   - Ensure stable internet connection
   - Check available disk space (2GB+ required)
   - Verify Hugging Face access

2. **Music21 Setup Issues**
   - Install required system dependencies
   - Configure music21 environment
   - Check for MuseScore installation

3. **Ollama Integration Issues**
   - Ensure Ollama is installed and running
   - Check `ollama --version` command
   - Verify llama3 model is downloaded

4. **Audio Quality Issues**
   - Adjust sample rate in configuration
   - Check audio format compatibility
   - Verify audio processing libraries

### Performance Tips

- Use GPU acceleration for Audiocraft when available
- Configure appropriate music styles for your content
- Enable quality assessment for better results
- Use batch processing for multiple tracks

## Advanced Features

### Custom Music Styles
```python
# Define custom music style
custom_style = {
    "tempo": 110,
    "key": "A",
    "scale": "minor",
    "instruments": ["guitar", "drums", "bass"],
    "mood": "mysterious and intriguing"
}

# Add to configuration
generator.config['music_styles']['custom'] = custom_style
```

### Composition Suggestions
```python
# Get AI-powered composition suggestions
suggestions = generator.get_composition_suggestions("mystery", "custom")
print(f"AI suggestions: {suggestions}")
```

### Quality Improvement
```python
# Assess and improve music quality
quality = generator.assess_music_quality(music_path, "mystery")
if quality < 8:
    print("Regenerating music for better quality...")
    improved_music = generator.generate_music("mystery")
```

## Future Enhancements

- **Real-time Generation**: Live music creation during video production
- **Style Transfer**: Apply specific composer styles
- **Video Synchronization**: Automatic music-video timing
- **Advanced Harmonies**: Complex chord progressions
- **Multi-track Support**: Separate instrument tracks
- **Emotional Analysis**: AI-powered emotional music matching

## Contributing

To contribute to the music generator:

1. Follow the existing code structure
2. Add comprehensive error handling
3. Include unit tests for new features
4. Update documentation for changes
5. Test with various video types and styles

## License

This module is part of the AutoVideoProducer project and follows the same licensing terms.
