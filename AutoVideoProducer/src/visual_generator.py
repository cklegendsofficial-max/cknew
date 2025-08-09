#!/usr/bin/env python3
"""
Visual Generator Module
Generates visuals using Stable Diffusion with prompt refinement and fallback to Unsplash scraping
"""

import os
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np

# Try to import optional dependencies
try:
    import torch
    from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class VisualGenerator:
    """Generate high-quality cinematic visuals for videos"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.pipeline = None
        self._initialize_ai_models()
    
    def _initialize_ai_models(self):
        """Initialize AI models for visual generation"""
        try:
            if DIFFUSERS_AVAILABLE:
                self.logger.info("Initializing Stable Diffusion for cinematic visuals...")
                
                # Use a lighter model for CPU/memory efficiency
                model_id = "runwayml/stable-diffusion-v1-5"
                
                self.pipeline = StableDiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=torch.float32,  # Use float32 for CPU compatibility
                    use_safetensors=True
                )
                
                # Optimize for memory efficiency
                self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
                    self.pipeline.scheduler.config
                )
                
                # Force CPU mode to avoid CUDA memory issues
                self.pipeline = self.pipeline.to("cpu")
                self.pipeline.enable_attention_slicing()
                self.pipeline.enable_vae_slicing()
                
                self.logger.info("Stable Diffusion initialized successfully on CPU")
            else:
                self.logger.warning("Stable Diffusion not available, using fallback methods")
                
        except Exception as e:
            self.logger.error(f"Error initializing AI models: {e}")
            self.pipeline = None
    
    def generate_visuals(self, scripts: List[Dict], num_visuals: int = 3) -> List[Dict]:
        """
        Generate cinematic visuals for scripts
        
        Args:
            scripts: List of scripts from script writer
            num_visuals: Number of visuals to generate per script
            
        Returns:
            List of generated visuals with metadata
        """
        try:
            self.logger.info(f"Generating cinematic visuals for {len(scripts)} scripts")
            
            visuals = []
            
            for i, script in enumerate(scripts):
                try:
                    # Generate multiple visuals per script for variety
                    for j in range(num_visuals):
                        visual = self._generate_cinematic_visual(script, i, j)
                        if visual:
                            visuals.append(visual)
                except Exception as e:
                    self.logger.error(f"Error generating visual for script {i+1}: {e}")
                    continue
            
            return visuals
            
        except Exception as e:
            self.logger.error(f"Error generating visuals: {e}")
            return []
    
    def _generate_cinematic_visual(self, script: Dict, script_index: int, visual_index: int) -> Optional[Dict]:
        """Generate a single cinematic visual from script"""
        try:
            # Get script content for prompt generation
            title = script.get('title', f'Script {script_index+1}')
            content = script.get('content', script.get('description', ''))
            channel_type = script.get('channel_type', 'general')
            
            # Create output directory
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'visuals')
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate image file
            image_filename = f"cinematic_{script_index+1}_{visual_index+1}_{int(time.time())}.png"
            image_path = os.path.join(output_dir, image_filename)
            
            # Generate cinematic visual using AI
            if DIFFUSERS_AVAILABLE and self.pipeline:
                try:
                    # Create cinematic prompt from script content
                    prompt = self._create_cinematic_prompt(script, visual_index)
                    
                    # Generate high-quality image
                    image = self.pipeline(
                        prompt=prompt,
                        negative_prompt="blurry, low quality, distorted, ugly, bad anatomy, watermark, text",
                        num_inference_steps=15,  # Reduced from 30
                        guidance_scale=7.5,  # Reduced from 8.5
                        width=512,  # Reduced from 1024
                        height=512  # Reduced from 1024
                    ).images[0]
                    
                    # Apply cinematic post-processing
                    image = self._apply_cinematic_effects(image, channel_type)
                    
                    # Save high-quality image
                    image.save(image_path, "PNG", quality=95)
                    
                    self.logger.info(f"Generated cinematic visual: {image_path}")
                    
                    return {
                        'id': f"cinematic_{script_index+1}_{visual_index+1}_{int(time.time())}",
                        'title': f"Cinematic Visual {visual_index+1} for {title}",
                        'image_file': image_path,
                        'prompt': prompt,
                        'style': 'cinematic',
                        'resolution': '512x512',  # Updated from 1024x1024
                        'channel_type': channel_type,
                        'metadata': {
                            'generated_at': datetime.now().isoformat(),
                            'script_id': script.get('id', f'script_{script_index+1}'),
                            'method': 'stable_diffusion_cinematic',
                            'enhanced': True,
                            'visual_index': visual_index
                        }
                    }
                    
                except Exception as e:
                    self.logger.error(f"Error generating AI cinematic visual: {e}")
                    return self._create_cinematic_fallback(script, script_index, visual_index, image_path)
            
            else:
                self.logger.warning("AI models not available, creating cinematic fallback")
                return self._create_cinematic_fallback(script, script_index, visual_index, image_path)
                
        except Exception as e:
            self.logger.error(f"Error in cinematic visual generation: {e}")
            return None
    
    def _create_cinematic_prompt(self, script: Dict, visual_index: int) -> str:
        """Create a cinematic prompt for image generation"""
        title = script.get('title', '')
        content = script.get('content', script.get('description', ''))
        channel_type = script.get('channel_type', 'general')
        
        # Base cinematic elements
        cinematic_elements = [
            "cinematic lighting",
            "professional photography",
            "movie poster style",
            "dramatic shadows",
            "golden hour lighting",
            "cinematic composition",
            "film grain effect",
            "professional color grading"
        ]
        
        # Channel-specific cinematic themes
        if channel_type == "cklegends":
            themes = [
                "epic warrior in battle armor",
                "ancient battlefield with dramatic lighting",
                "heroic figure with golden aura",
                "mythical warrior with cinematic pose",
                "epic battle scene with smoke and fire"
            ]
        elif channel_type == "ckdrive":
            themes = [
                "luxury sports car on mountain road",
                "racing scene with motion blur",
                "automotive photography with dramatic lighting",
                "supercar with cinematic background",
                "racing driver in action pose"
            ]
        elif channel_type == "ckcombat":
            themes = [
                "martial arts fighter in action",
                "combat scene with dynamic lighting",
                "warrior in training pose",
                "fight scene with dramatic shadows",
                "combat training with cinematic effects"
            ]
        elif channel_type == "ckironwill":
            themes = [
                "mental strength visualization",
                "determination and focus scene",
                "success mindset representation",
                "overcoming obstacles scene",
                "mental toughness visualization"
            ]
        elif channel_type == "ckfinancecore":
            themes = [
                "financial success scene",
                "wealth and prosperity visualization",
                "business success representation",
                "investment success scene",
                "financial freedom visualization"
            ]
        else:
            themes = [
                "professional scene with dramatic lighting",
                "cinematic composition with depth",
                "dramatic scene with professional photography",
                "movie-style scene with cinematic effects"
            ]
        
        # Select theme based on visual index
        theme = themes[visual_index % len(themes)]
        
        # Create comprehensive prompt
        prompt = f"{title}, {theme}, {', '.join(cinematic_elements)}, {content[:100]}"
        
        return prompt
    
    def _apply_cinematic_effects(self, image: Image.Image, channel_type: str) -> Image.Image:
        """Apply cinematic post-processing effects"""
        try:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Apply channel-specific color grading
            if channel_type == "cklegends":
                # Warm, golden tones for epic feel
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(1.3)
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.2)
                
            elif channel_type == "ckdrive":
                # Cool, blue tones for automotive feel
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(1.1)
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(1.1)
                
            elif channel_type == "ckcombat":
                # High contrast, dramatic tones
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.4)
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(0.9)
                
            elif channel_type == "ckironwill":
                # Warm, motivational tones
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(1.2)
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(1.05)
                
            elif channel_type == "ckfinancecore":
                # Professional, sophisticated tones
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(1.1)
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.1)
            
            # Apply subtle film grain effect
            image = self._add_film_grain(image)
            
            # Apply subtle vignette effect
            image = self._add_vignette(image)
            
            return image
            
        except Exception as e:
            self.logger.error(f"Error applying cinematic effects: {e}")
            return image
    
    def _add_film_grain(self, image: Image.Image) -> Image.Image:
        """Add subtle film grain effect"""
        try:
            # Create noise pattern
            width, height = image.size
            noise = np.random.normal(0, 5, (height, width, 3)).astype(np.uint8)
            noise_img = Image.fromarray(noise, 'RGB')
            
            # Blend with original image
            result = Image.blend(image, noise_img, 0.05)
            return result
            
        except Exception as e:
            self.logger.error(f"Error adding film grain: {e}")
            return image
    
    def _add_vignette(self, image: Image.Image) -> Image.Image:
        """Add subtle vignette effect"""
        try:
            width, height = image.size
            center_x, center_y = width // 2, height // 2
            
            # Create vignette mask
            mask = Image.new('L', (width, height), 255)
            draw = ImageDraw.Draw(mask)
            
            # Draw radial gradient
            for y in range(height):
                for x in range(width):
                    distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    max_distance = ((width // 2) ** 2 + (height // 2) ** 2) ** 0.5
                    intensity = int(255 * (1 - (distance / max_distance) * 0.3))
                    mask.putpixel((x, y), max(0, intensity))
            
            # Apply vignette
            result = Image.composite(image, Image.new('RGB', image.size, (0, 0, 0)), mask)
            return result
            
        except Exception as e:
            self.logger.error(f"Error adding vignette: {e}")
            return image
    
    def _create_cinematic_fallback(self, script: Dict, script_index: int, visual_index: int, image_path: str) -> Dict:
        """Create a cinematic fallback visual when AI generation is not available"""
        try:
            if PIL_AVAILABLE:
                # Create a cinematic-style image
                width, height = 512, 512  # Reduced from 1024x1024
                img = Image.new('RGB', (width, height), color='black')
                draw = ImageDraw.Draw(img)
                
                # Create gradient background
                for y in range(height):
                    for x in range(width):
                        # Create cinematic gradient
                        intensity = int(50 + 100 * (y / height))
                        img.putpixel((x, y), (intensity//3, intensity//3, intensity))
                
                # Add cinematic text
                title = script.get('title', f'Cinematic Visual {visual_index+1}')
                try:
                    # Try to use a larger font
                    font_size = 60
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                # Center the text
                bbox = draw.textbbox((0, 0), title, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x = (width - text_width) // 2
                y = (height - text_height) // 2
                
                # Add text with shadow effect
                draw.text((x+2, y+2), title, fill='black', font=font)
                draw.text((x, y), title, fill='white', font=font)
                
                # Add cinematic elements
                self._add_cinematic_elements(draw, width, height, script.get('channel_type', 'general'))
                
                # Save image
                img.save(image_path, "PNG", quality=95)
                
                return {
                    'id': f"cinematic_{script_index+1}_{visual_index+1}_{int(time.time())}",
                    'title': f"Cinematic Visual {visual_index+1} for {title}",
                    'image_file': image_path,
                    'prompt': f"Cinematic fallback visual for {title}",
                    'style': 'cinematic_fallback',
                    'resolution': '512x512',
                    'channel_type': script.get('channel_type', 'general'),
                    'metadata': {
                        'generated_at': datetime.now().isoformat(),
                        'script_id': script.get('id', f'script_{script_index+1}'),
                        'method': 'cinematic_fallback',
                        'enhanced': False,
                        'visual_index': visual_index
                    }
                }
            else:
                # Create placeholder file
                with open(image_path, 'w') as f:
                    f.write("Cinematic placeholder visual file")
                
                return {
                    'id': f"cinematic_{script_index+1}_{visual_index+1}_{int(time.time())}",
                    'title': f"Cinematic Visual {visual_index+1} for {script.get('title', f'Script {script_index+1}')}",
                    'image_file': image_path,
                    'prompt': f"Cinematic placeholder for {script.get('title', f'Script {script_index+1}')}",
                    'style': 'placeholder',
                    'resolution': 'N/A',
                    'channel_type': script.get('channel_type', 'general'),
                    'metadata': {
                        'generated_at': datetime.now().isoformat(),
                        'script_id': script.get('id', f'script_{script_index+1}'),
                        'method': 'placeholder',
                        'enhanced': False,
                        'visual_index': visual_index
                    }
                }
                
        except Exception as e:
            self.logger.error(f"Error creating cinematic fallback: {e}")
            return None
    
    def _add_cinematic_elements(self, draw: ImageDraw.Draw, width: int, height: int, channel_type: str):
        """Add cinematic visual elements"""
        try:
            # Add channel-specific cinematic elements
            if channel_type == "cklegends":
                # Add epic elements
                for i in range(5):
                    x = width // 4 + i * width // 8
                    y = height // 4
                    draw.ellipse([x-20, y-20, x+20, y+20], fill='gold')
                    
            elif channel_type == "ckdrive":
                # Add automotive elements
                for i in range(3):
                    x = width // 3 + i * width // 6
                    y = height // 3
                    draw.rectangle([x-30, y-10, x+30, y+10], fill='blue')
                    
            elif channel_type == "ckcombat":
                # Add combat elements
                for i in range(4):
                    x = width // 4 + i * width // 8
                    y = height // 4
                    draw.polygon([(x, y-20), (x-10, y+10), (x+10, y+10)], fill='red')
                    
            elif channel_type == "ckironwill":
                # Add motivational elements
                for i in range(3):
                    x = width // 3 + i * width // 6
                    y = height // 3
                    draw.rectangle([x-15, y-15, x+15, y+15], fill='green')
                    
            elif channel_type == "ckfinancecore":
                # Add financial elements
                for i in range(4):
                    x = width // 4 + i * width // 8
                    y = height // 4
                    draw.ellipse([x-15, y-15, x+15, y+15], fill='yellow')
                    
        except Exception as e:
            self.logger.error(f"Error adding cinematic elements: {e}")
