# Video Editor - Professional Video Editing with MoviePy

A comprehensive video editing system built with MoviePy that handles both long videos (10+ minutes) and shorts (15-60 seconds) with advanced effects, subtitles, and psychological manipulation techniques.

## Features

### 🎬 Video Types
- **Long Videos**: 10+ minute content with detailed storytelling
- **Shorts**: 15-60 second punchy content optimized for social media
- **Automatic Detection**: Determines video type based on script length

### 🎨 Advanced Effects
- **Transitions**: Fade in/out, crossfade, zoom effects
- **Particle Effects**: Custom confetti particles using numpy arrays
- **Text Overlays**: Motivational quotes and captions
- **Subliminal Effects**: 25th frame inserts (0.04 sec duration)
- **Zoom Effects**: Dynamic zoom with customizable parameters

### 🌍 Multi-Language Subtitles
- **Supported Languages**: English, French, German, Spanish, Japanese, Korean
- **Automatic Translation**: Using deep-translator library
- **SRT Generation**: Creates subtitle files with proper timing
- **Burned Subtitles**: Embeds subtitles directly into video

### 🧠 Psychological Manipulation
- **Addiction Effects**: Fast cuts to increase engagement
- **State Affirmations**: Embedded positive messages
- **Subliminal Messaging**: Hidden text frames for subconscious impact

### ⚡ Multi-Threading
- **Parallel Processing**: Edit multiple videos simultaneously
- **Thread Safety**: Proper resource management
- **Progress Tracking**: Real-time status updates

## Installation

### Dependencies
```bash
pip install moviepy deep-translator opencv-python numpy
```

### Required System Dependencies
- **FFmpeg**: For video processing
- **ImageMagick**: For text rendering (optional)

## Usage

### Basic Video Editing

```python
from video_editor import edit_video

# Simple usage
final_video_path = edit_video(
    script="Your video script text here...",
    voiceover_mp3="path/to/voiceover.mp3",
    visuals_list=["path/to/image1.jpg", "path/to/image2.jpg"],
    music_mp3="path/to/background_music.mp3",
    channel_topic="CKLegends"
)
```

### Advanced Configuration

```python
from video_editor import VideoEditor, VideoConfig, EffectConfig, SubtitleConfig

# Configure video settings
config = VideoConfig(
    resolution=(1920, 1080),
    fps=30,
    video_type="long",  # or "short"
    target_duration=600  # 10 minutes
)

# Configure effects
effect_config = EffectConfig(
    enable_transitions=True,
    enable_text_overlays=True,
    enable_particles=True,
    enable_subliminal=True,
    transition_duration=0.5
)

# Configure subtitles
subtitle_config = SubtitleConfig(
    enabled=True,
    languages=["en", "fr", "de", "es"],
    font_size=24
)

# Create editor
editor = VideoEditor(config, effect_config, subtitle_config)

# Edit video
final_path = editor.edit_video(
    script=script_text,
    voiceover_mp3=voiceover_path,
    visuals_list=visuals_list,
    music_mp3=music_path,
    channel_topic="CKLegends"
)
```

### Multiple Video Processing

```python
# Process multiple videos in parallel
video_tasks = [
    {
        'script': "First video script...",
        'voiceover_mp3': "voiceover1.mp3",
        'visuals_list': ["visual1.jpg", "visual2.jpg"],
        'music_mp3': "music1.mp3",
        'channel_topic': "Channel1"
    },
    {
        'script': "Second video script...",
        'voiceover_mp3': "voiceover2.mp3",
        'visuals_list': ["visual3.jpg", "visual4.jpg"],
        'music_mp3': "music2.mp3",
        'channel_topic': "Channel2"
    }
]

results = editor.edit_multiple_videos(video_tasks)
```

## Configuration Classes

### VideoConfig
Controls video output settings:
- `resolution`: Video resolution (width, height)
- `fps`: Frames per second
- `video_type`: "long" or "short"
- `target_duration`: Target video length in seconds
- `channel_topic`: Channel name for customization

### EffectConfig
Controls visual effects:
- `enable_transitions`: Enable fade/transition effects
- `enable_text_overlays`: Enable motivational text overlays
- `enable_particles`: Enable particle effects
- `enable_subliminal`: Enable subliminal messaging
- `transition_duration`: Duration of transitions
- `text_duration`: Duration of text overlays

### SubtitleConfig
Controls subtitle generation:
- `enabled`: Enable subtitle generation
- `languages`: List of target languages
- `font_size`: Subtitle font size
- `font_color`: Text color
- `stroke_color`: Outline color
- `stroke_width`: Outline thickness

## Effects and Manipulation

### Particle Effects
```python
from video_editor import ParticleEffect

# Create confetti particles
particle_clip = ParticleEffect.create_confetti_particles(
    width=1920, height=1080, duration=5.0
)

# Apply zoom effect
zoomed_clip = ParticleEffect.create_zoom_effect(
    clip=video_clip, zoom_factor=1.2, duration=2.0
)
```

### Subliminal Effects
```python
from video_editor import SubliminalEffect

# Create subliminal frame
subliminal_clip = SubliminalEffect.create_subliminal_frame(
    text="SUCCESS", width=1920, height=1080, duration=0.04
)
```

### Manipulation Techniques
```python
# Apply addiction effects (fast cuts)
addiction_video = editor.create_manipulation_effects(
    video_clip, manipulation_type="addiction"
)

# Apply state affirmations
affirmation_video = editor.create_manipulation_effects(
    video_clip, manipulation_type="state"
)
```

## Subtitle Generation

### Multi-Language Support
```python
from video_editor import SubtitleGenerator, SubtitleConfig

config = SubtitleConfig(
    enabled=True,
    languages=["en", "fr", "de", "es", "jp", "kr"]
)

generator = SubtitleGenerator(config)

# Generate SRT content
srt_content = generator.create_srt_content(script, language="fr")

# Burn subtitles into video
video_with_subs = generator.burn_subtitles(video_clip, script, "en")
```

## Integration with Main Application

The video editor is integrated into the main AutoVideoProducer application:

```python
# In main.py production pipeline
elif step_num == 7:  # Video editing
    self.log_to_gui("Editing video for CKLegends...")
    
    final_video_path = video_editor.edit_video(
        script=script_text,
        voiceover_mp3=voiceover_path,
        visuals_list=visuals_list,
        music_mp3=music_file,
        channel_topic="CKLegends"
    )
```

## Output Structure

Videos are saved to the `assets/` directory with timestamped filenames:
```
assets/
├── final_video_CKLegends_20231201_143022.mp4
├── final_video_CKShorts_20231201_143045.mp4
└── subtitles_en.srt
```

## Error Handling

The video editor includes comprehensive error handling:
- **File Validation**: Checks for valid audio/video files
- **Resolution Validation**: Ensures compatible video dimensions
- **Audio Sync**: Maintains proper audio-video synchronization
- **Resource Cleanup**: Properly closes video/audio clips
- **Thread Safety**: Handles concurrent video processing

## Performance Optimization

- **Multi-threading**: Parallel video processing
- **Memory Management**: Efficient clip handling
- **Caching**: Reuses processed effects
- **Progress Tracking**: Real-time status updates

## Example Usage

See `video_editor_example.py` for comprehensive examples of:
- Long video creation
- Short video creation
- Manipulation effects
- Multiple video processing
- Subtitle generation

## Dependencies

### Required
- `moviepy>=1.0.3`: Video editing framework
- `deep-translator>=1.11.0`: Multi-language translation
- `opencv-python>=4.8.0`: Computer vision for effects
- `numpy>=1.24.0`: Numerical computing for particles

### Optional
- `ffmpeg-python>=0.2.0`: Advanced video processing
- `librosa>=0.10.0`: Audio analysis

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: Install FFmpeg system-wide
2. **Memory errors**: Reduce video resolution or duration
3. **Audio sync issues**: Check audio file format compatibility
4. **Translation errors**: Verify internet connection for deep-translator

### Performance Tips

- Use SSD storage for faster file I/O
- Close other applications during video processing
- Use appropriate video resolution for target platform
- Enable hardware acceleration if available

## License

This video editor is part of the AutoVideoProducer system for CK Empire.
