# Visual Generator Module

The Visual Generator module creates high-quality visual assets for video production using AI-powered image generation and intelligent prompt refinement.

## Features

### 🎨 **AI-Powered Visual Generation**
- **Stable Diffusion Integration**: Uses `stabilityai/stable-diffusion-2-1` for high-quality image generation
- **Cinematic Style**: Automatically applies cinematic lighting and composition styles
- **High Resolution**: Generates 1024x576 images optimized for video production
- **GPU Acceleration**: Supports CUDA for fast generation on compatible hardware

### 🧠 **Intelligent Prompt Processing**
- **Script Parsing**: Automatically extracts visual cues from script outlines
- **Ollama Integration**: Uses AI to refine and improve visual prompts
- **Pattern Recognition**: Identifies visual cues like "Scene:", "Visual:", "Show:", etc.
- **Content Analysis**: Generates visuals from script content when no explicit cues are found

### 🎯 **Quality Assurance**
- **Self-Improvement**: Uses Ollama to rate visual quality (1-10 scale)
- **Automatic Regeneration**: Re-generates images that score below quality threshold
- **Prompt Optimization**: Suggests improvements based on quality assessment
- **Cinematic Standards**: Mimics top directors like Christopher Nolan

### 🔄 **Fallback Systems**
- **Unsplash API**: Fetches high-quality stock photos when AI generation fails
- **Local Caching**: Caches generated images for reuse
- **Error Handling**: Graceful degradation when services are unavailable

### 🎭 **Advanced Features**
- **Subliminal Embedding**: Embeds brand logos at 1/25 frame size for video editing
- **Style Customization**: Configurable cinematic styles and visual preferences
- **Batch Processing**: Generates multiple images per visual cue
- **Statistics Tracking**: Monitors generation quality and performance

## Installation

### Prerequisites
```bash
# Install Stable Diffusion dependencies
pip install diffusers transformers accelerate torch pillow

# Install additional dependencies
pip install requests beautifulsoup4

# Install Ollama (for prompt refinement and quality assessment)
# Follow instructions at: https://ollama.ai/
```

### Quick Setup
```bash
# Install all dependencies
pip install -r requirements.txt

# Download Stable Diffusion model (first run)
python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('stabilityai/stable-diffusion-2-1')"
```

## Usage

### Basic Usage
```python
from visual_generator import VisualGenerator

# Initialize generator
generator = VisualGenerator()

# Generate visuals from script
script_outline = """
Scene: Ancient Rome at sunset with epic architecture
Visual: Dramatic battle scene with warriors and chariots
Show: Modern city skyline at night with neon lights
"""

visual_paths = generator.generate_visuals(script_outline)
print(f"Generated {len(visual_paths)} visual assets")
```

### Advanced Usage
```python
# Custom configuration
config = {
    "image_width": 1024,
    "image_height": 576,
    "num_images_per_video": 15,
    "cinematic_style": "Cinematic style like Spielberg, with epic composition",
    "quality_threshold": 8,
    "self_improve": True
}

generator = VisualGenerator(config_path="custom_config.json")

# Generate with quality assessment
visual_paths = generator.generate_visuals(script_outline)

# Assess quality of generated images
for path in visual_paths:
    quality = generator.assess_visual_quality(path, "epic scene")
    print(f"Quality: {quality}/10")

# Embed subliminal images
brand_logo = "assets/brand_logo.png"
embedded_path = generator.embed_subliminal_images(visual_paths[0], brand_logo)
```

### Configuration Options

The visual generator supports extensive configuration:

```json
{
  "visual_generator": {
    "image_width": 1024,
    "image_height": 576,
    "num_images_per_video": 10,
    "cinematic_style": "Cinematic style like Christopher Nolan, with dramatic lighting and epic composition",
    "quality_threshold": 9,
    "unsplash_api_key": "your_unsplash_api_key",
    "fallback_to_unsplash": true,
    "cache_images": true,
    "self_improve": true
  }
}
```

## Script Cue Patterns

The generator recognizes these patterns in scripts:

- `Scene: [description]`
- `Visual: [description]`
- `Show: [description]`
- `Describe scene: [description]`
- `Depict: [description]`
- `Imagine: [description]`

## Output Structure

Generated assets are saved to `assets/visuals/` with the following naming convention:
- `visual_XX_YY_timestamp.png` - Stable Diffusion generated images
- `unsplash_XX_YY_timestamp.jpg` - Unsplash fetched images
- `visual_XX_YY_timestamp_embedded.png` - Images with subliminal embeddings

## Quality Assessment

The module uses Ollama to assess visual quality based on:
- **Visual Composition**: Balance, framing, and visual hierarchy
- **Lighting Quality**: Dramatic lighting and cinematic appeal
- **Cinematic Appeal**: Professional film-like quality
- **Technical Quality**: Resolution, clarity, and technical standards

## Performance Optimization

### GPU Requirements
- **Recommended**: NVIDIA GPU with 8GB+ VRAM
- **Minimum**: 4GB VRAM for smaller models
- **CPU Fallback**: Available but significantly slower

### Memory Management
- Automatic model loading/unloading
- Batch processing for efficiency
- Image caching to reduce regeneration

## Error Handling

The module includes robust error handling:
- **Stable Diffusion Failures**: Falls back to Unsplash API
- **Ollama Unavailable**: Uses default prompts and quality assessment
- **Network Issues**: Continues with cached or generated content
- **Memory Issues**: Automatically reduces batch size

## Integration with Main Application

The visual generator is integrated into the main AutoVideoProducer workflow:

1. **Script Analysis**: Parses generated scripts for visual cues
2. **Asset Generation**: Creates visuals based on script content
3. **Quality Control**: Assesses and improves generated assets
4. **Video Integration**: Provides assets for video composition

## Example Output

```
Generated 12 visual assets:
  visual_00_00_1703123456.png (Quality: 9/10)
  visual_00_01_1703123457.png (Quality: 8/10)
  visual_01_00_1703123458.png (Quality: 9/10)
  ...

Generation Statistics:
  Total images generated: 12
  Average quality: 8.7/10
  Stable Diffusion available: True
  Ollama available: True
```

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory**
   - Reduce batch size in configuration
   - Use CPU fallback mode
   - Close other GPU applications

2. **Stable Diffusion Model Download**
   - Ensure stable internet connection
   - Check available disk space (3GB+ required)
   - Verify Hugging Face access

3. **Ollama Integration Issues**
   - Ensure Ollama is installed and running
   - Check `ollama --version` command
   - Verify llama3 model is downloaded

4. **Image Quality Issues**
   - Adjust quality threshold in configuration
   - Modify cinematic style prompts
   - Enable self-improvement mode

### Performance Tips

- Use GPU acceleration when available
- Enable image caching for repeated generations
- Configure appropriate quality thresholds
- Use batch processing for multiple assets

## Future Enhancements

- **Style Transfer**: Apply specific artistic styles
- **Video Integration**: Direct video composition
- **Real-time Generation**: Live visual creation
- **Advanced Caching**: Smart asset management
- **Multi-model Support**: Additional AI models

## Contributing

To contribute to the visual generator:

1. Follow the existing code structure
2. Add comprehensive error handling
3. Include unit tests for new features
4. Update documentation for changes
5. Test with various script formats

## License

This module is part of the AutoVideoProducer project and follows the same licensing terms.
