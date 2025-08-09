"""
Video Editor Module
Edits videos using MoviePy with effects, 25th frame insertion, and multi-language subtitles
"""

import os
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime
import subprocess
import tempfile
import time # Added for time.time()

# Try to import optional dependencies
try:
    import moviepy.editor as mp
    from moviepy.video.fx import resize, crop, fadein, fadeout
    from moviepy.audio.fx import volumex
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    logging.warning("MoviePy not available for video editing")

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    logging.warning("Deep translator not available for multi-language subtitles")

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL not available for image processing")

class VideoEditor:
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the video editor with configuration"""
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self.video_cache = {}
        
        # Load configuration
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            "video": {
                "width": 1920,
                "height": 1080,
                "fps": 30,
                "duration": 120,
                "format": "mp4",
                "codec": "libx264"
            },
            "effects": {
                "use_25th_frame": True,
                "use_psychological_effects": True,
                "use_transitions": True,
                "use_color_grading": True
            },
            "subtitles": {
                "enabled": True,
                "languages": ["en", "es", "fr", "de", "tr"],
                "font_size": 24,
                "font_color": "white",
                "background_color": "black",
                "position": "bottom"
            },
            "output_directory": "videos",
            "use_manipulation_techniques": True,
            "enhance_psychological_impact": True
        }
    
    def edit_videos(self, voiceovers: List[Dict], visuals: List[Dict], music: List[Dict]) -> List[Dict]:
        """
        Edit videos from voiceovers, visuals, and music
        
        Args:
            voiceovers: List of voiceovers from voiceover generator
            visuals: List of visuals from visual generator
            music: List of music from music generator
            
        Returns:
            List of edited videos with metadata
        """
        edited_videos = []
        
        try:
            for i, voiceover in enumerate(voiceovers):
                visual = visuals[i] if i < len(visuals) else None
                music_track = music[i] if i < len(music) else None
                
                edited_video = self.edit_video(voiceover, visual, music_track)
                if edited_video:
                    edited_videos.append(edited_video)
                    
        except Exception as e:
            self.logger.error(f"Error editing videos: {e}")
            
        return edited_videos
    
    def edit_video(self, voiceover: Dict, visual: Optional[Dict] = None, music: Optional[Dict] = None) -> Optional[Dict]:
        """
        Edit a single video from voiceover, visual, and music
        
        Args:
            voiceover: Voiceover data from voiceover generator
            visual: Visual data from visual generator (optional)
            music: Music data from music generator (optional)
            
        Returns:
            Edited video metadata or None if failed
        """
        try:
            self.logger.info(f"Starting video editing for voiceover: {voiceover.get('title', 'Unknown')}")
            
            # Get channel type from voiceover or default
            channel_type = voiceover.get('channel_type', 'general')
            
            # Create channel-specific output directory
            output_dir = os.path.join(self.config.get('output_directory', 'videos'), channel_type)
            os.makedirs(output_dir, exist_ok=True)
            
            # Create subdirectories for different video types
            long_videos_dir = os.path.join(output_dir, 'long_videos')
            shorts_dir = os.path.join(output_dir, 'shorts')
            os.makedirs(long_videos_dir, exist_ok=True)
            os.makedirs(shorts_dir, exist_ok=True)
            
            # Generate video filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            title_safe = "".join(c for c in voiceover.get('title', 'Unknown') if c.isalnum() or c in (' ', '-', '_')).rstrip()
            title_safe = title_safe.replace(' ', '_')[:50]  # Limit length
            
            # Create both long video and short video
            videos_created = []
            
            # 1. Create Long Video (16:9 - 1920x1080 - 10+ minutes)
            long_video_filename = f"long_{title_safe}_{timestamp}.mp4"
            long_video_path = os.path.join(long_videos_dir, long_video_filename)
            
            long_video_result = self._create_real_video(
                voiceover, visual, music, 
                long_video_path, 
                width=1920, height=1080, 
                duration=600,  # 10 minutes for long videos
                video_type="long"
            )
            if long_video_result:
                videos_created.append(long_video_result)
            
            # 2. Create Short Video (9:16 - 1080x1920 - 30 seconds)
            short_video_filename = f"short_{title_safe}_{timestamp}.mp4"
            short_video_path = os.path.join(shorts_dir, short_video_filename)
            
            short_video_result = self._create_real_video(
                voiceover, visual, music, 
                short_video_path, 
                width=1080, height=1920, 
                duration=30,  # 30 seconds for shorts
                video_type="short"
            )
            if short_video_result:
                videos_created.append(short_video_result)
            
            # Return the first video result for compatibility
            return videos_created[0] if videos_created else None
                
        except Exception as e:
            self.logger.error(f"Error editing video: {e}")
            return None
    
    def _create_real_video(self, voiceover: Dict, visual: Dict, music: Dict, video_type: str) -> str:
        """Create a real cinematic video with multiple visuals, transitions, and effects"""
        try:
            self.logger.info(f"Creating {video_type} cinematic video with real content...")
            
            # Video settings based on type
            if video_type == "short":
                duration = 30
                size = (1080, 1920)  # 9:16 for shorts
                fps = 30
            else:
                duration = 600  # 10 minutes for long videos
                size = (1920, 1080)  # 16:9 for long videos
                fps = 30
            
            # Create multiple cinematic visuals for variety
            visual_clips = self._create_multiple_cinematic_visuals(visual, duration, size, video_type)
            
            # Create cinematic background
            background_clip = self._create_cinematic_background(size, duration, video_type)
            
            # Add cinematic voiceover with proper audio
            if voiceover and voiceover.get('audio_file'):
                voiceover_clip = self._add_cinematic_voiceover(background_clip, voiceover['audio_file'], duration)
            else:
                self.logger.warning("No voiceover available, using background music only")
                voiceover_clip = background_clip
            
            # Add cinematic music with proper mixing
            if music and music.get('audio_file'):
                video_clip = self._add_cinematic_music(voiceover_clip, music['audio_file'], duration)
            else:
                self.logger.warning("No music available, using voiceover only")
                video_clip = voiceover_clip
            
            # Add multiple visual overlays with transitions
            video_clip = self._add_multiple_visual_overlays(video_clip, visual_clips, duration, video_type)
            
            # Apply cinematic video effects
            video_clip = self._apply_cinematic_video_effects(video_clip, video_type)
            
            # Add cinematic text overlays (if available)
            video_clip = self._add_cinematic_text_overlays(video_clip, voiceover, video_type)
            
            # Export the final video
            output_filename = f"cinematic_{video_type}_{int(time.time())}.mp4"
            output_path = os.path.join(self._get_output_directory(video_type), output_filename)
            
            # Use high quality settings
            video_clip.write_videofile(
                output_path,
                fps=fps,
                codec='libx264',
                audio_codec='aac',
                bitrate='8000k',
                audio_bitrate='192k',
                threads=4,
                preset='medium'
            )
            
            self.logger.info(f"✅ Created cinematic {video_type} video: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creating real video: {e}")
            return None
    
    def _create_multiple_cinematic_visuals(self, visual: Dict, duration: int, size: tuple, video_type: str) -> List[mp.VideoClip]:
        """Create multiple cinematic visual clips for variety"""
        try:
            visual_clips = []
            
            # Create multiple visual variations
            for i in range(5):  # Create 5 different visual clips
                try:
                    # Load the base visual
                    visual_path = visual.get('image_file', '')
                    if os.path.exists(visual_path):
                        # Create visual clip with different effects
                        visual_clip = mp.ImageClip(visual_path, duration=duration/5)
                        visual_clip = visual_clip.resize(size)
                        
                        # Apply different cinematic effects to each clip
                        if i == 0:
                            visual_clip = self._apply_ken_burns_effect(visual_clip, 'zoom_in')
                        elif i == 1:
                            visual_clip = self._apply_ken_burns_effect(visual_clip, 'pan_left')
                        elif i == 2:
                            visual_clip = self._apply_ken_burns_effect(visual_clip, 'zoom_out')
                        elif i == 3:
                            visual_clip = self._apply_ken_burns_effect(visual_clip, 'pan_right')
                        else:
                            visual_clip = self._apply_ken_burns_effect(visual_clip, 'zoom_center')
                        
                        # Add cinematic color grading
                        visual_clip = self._apply_cinematic_color_grading(visual_clip, i)
                        
                        visual_clips.append(visual_clip)
                    else:
                        # Create fallback visual
                        fallback_clip = self._create_cinematic_fallback_visual(size, duration/5, i)
                        visual_clips.append(fallback_clip)
                        
                except Exception as e:
                    self.logger.error(f"Error creating visual clip {i}: {e}")
                    # Create fallback visual
                    fallback_clip = self._create_cinematic_fallback_visual(size, duration/5, i)
                    visual_clips.append(fallback_clip)
            
            return visual_clips
            
        except Exception as e:
            self.logger.error(f"Error creating multiple visuals: {e}")
            return []
    
    def _apply_ken_burns_effect(self, clip: mp.VideoClip, effect_type: str) -> mp.VideoClip:
        """Apply Ken Burns effect to video clip"""
        try:
            def ken_burns_transform(get_frame, t):
                frame = get_frame(t)
                h, w = frame.shape[:2]
                
                # Calculate zoom and pan based on effect type
                if effect_type == 'zoom_in':
                    zoom_factor = 1.0 + (t / clip.duration) * 0.3
                    pan_x, pan_y = 0, 0
                elif effect_type == 'zoom_out':
                    zoom_factor = 1.3 - (t / clip.duration) * 0.3
                    pan_x, pan_y = 0, 0
                elif effect_type == 'pan_left':
                    zoom_factor = 1.1
                    pan_x = (t / clip.duration) * 0.2
                    pan_y = 0
                elif effect_type == 'pan_right':
                    zoom_factor = 1.1
                    pan_x = -(t / clip.duration) * 0.2
                    pan_y = 0
                else:  # zoom_center
                    zoom_factor = 1.0 + (t / clip.duration) * 0.2
                    pan_x, pan_y = 0, 0
                
                # Apply transformation
                new_h, new_w = int(h * zoom_factor), int(w * zoom_factor)
                
                # Resize frame
                import numpy as np
                from PIL import Image
                pil_img = Image.fromarray(frame)
                resized_pil = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                resized = np.array(resized_pil)
                
                # Calculate crop area
                start_y = max(0, (new_h - h) // 2 + int(pan_y * h))
                start_x = max(0, (new_w - w) // 2 + int(pan_x * w))
                end_y = min(new_h, start_y + h)
                end_x = min(new_w, start_x + w)
                
                # Crop to original size
                cropped = resized[start_y:end_y, start_x:end_x]
                
                return cropped
            
            return clip.fl(ken_burns_transform)
            
        except Exception as e:
            self.logger.error(f"Error applying Ken Burns effect: {e}")
            return clip
    
    def _apply_cinematic_color_grading(self, clip: mp.VideoClip, variation: int) -> mp.VideoClip:
        """Apply cinematic color grading to video clip"""
        try:
            # Different color grading for each variation
            color_presets = [
                {'contrast': 1.2, 'brightness': 1.1, 'saturation': 1.3},  # Warm
                {'contrast': 1.3, 'brightness': 0.9, 'saturation': 0.8},  # Cool
                {'contrast': 1.1, 'brightness': 1.2, 'saturation': 1.1},  # Bright
                {'contrast': 1.4, 'brightness': 0.8, 'saturation': 1.2},  # Dramatic
                {'contrast': 1.0, 'brightness': 1.0, 'saturation': 1.0}   # Natural
            ]
            
            preset = color_presets[variation % len(color_presets)]
            
            def color_transform(get_frame, t):
                frame = get_frame(t)
                
                # Apply color adjustments
                frame = frame * preset['contrast']
                frame = frame + (preset['brightness'] - 1.0) * 50
                frame = np.clip(frame, 0, 255)
                
                return frame.astype(np.uint8)
            
            return clip.fl(color_transform)
            
        except Exception as e:
            self.logger.error(f"Error applying color grading: {e}")
            return clip
    
    def _create_cinematic_fallback_visual(self, size: tuple, duration: float, variation: int) -> mp.VideoClip:
        """Create a cinematic fallback visual"""
        try:
            import numpy as np
            
            # Create different patterns for each variation
            w, h = size
            
            def create_frame(t):
                frame = np.zeros((h, w, 3), dtype=np.uint8)
                
                # Create different cinematic patterns
                if variation == 0:
                    # Gradient pattern
                    for y in range(h):
                        for x in range(w):
                            frame[y, x] = [int(255 * x/w), int(255 * y/h), int(255 * (x+y)/(w+h))]
                elif variation == 1:
                    # Radial pattern
                    center_x, center_y = w//2, h//2
                    for y in range(h):
                        for x in range(w):
                            dist = np.sqrt((x-center_x)**2 + (y-center_y)**2)
                            intensity = int(255 * (1 - dist/max(center_x, center_y)))
                            frame[y, x] = [intensity, intensity//2, intensity//3]
                elif variation == 2:
                    # Wave pattern
                    for y in range(h):
                        for x in range(w):
                            wave = np.sin(x/50 + t) * np.cos(y/50 + t)
                            intensity = int(128 + 127 * wave)
                            frame[y, x] = [intensity, intensity//2, intensity//3]
                elif variation == 3:
                    # Stripes pattern
                    for y in range(h):
                        for x in range(w):
                            stripe = int(255 * ((x + int(t*50)) % 100 < 50))
                            frame[y, x] = [stripe, stripe//2, stripe//3]
                else:
                    # Random cinematic pattern
                    for y in range(h):
                        for x in range(w):
                            noise = np.random.randint(0, 100)
                            frame[y, x] = [noise, noise//2, noise//3]
                
                return frame
            
            return mp.VideoClip(create_frame, duration=duration)
            
        except Exception as e:
            self.logger.error(f"Error creating fallback visual: {e}")
            # Create simple color clip as last resort
            return mp.ColorClip(size, color=(100, 100, 100), duration=duration)
    
    def _add_multiple_visual_overlays(self, video_clip: mp.VideoClip, visual_clips: List[mp.VideoClip], duration: int, video_type: str) -> mp.VideoClip:
        """Add multiple visual overlays with smooth transitions"""
        try:
            if not visual_clips:
                return video_clip
            
            # Create transition clips
            transition_duration = 2.0  # 2 seconds for transitions
            clips_with_transitions = []
            
            for i, visual_clip in enumerate(visual_clips):
                # Add fade in/out effects
                visual_clip = visual_clip.fadein(transition_duration).fadeout(transition_duration)
                
                # Position the visual clip
                if video_type == "short":
                    # For shorts, center the visual
                    visual_clip = visual_clip.set_position('center')
                else:
                    # For long videos, use picture-in-picture style
                    visual_clip = visual_clip.set_position(('right', 'bottom')).resize(width=400)
                
                clips_with_transitions.append(visual_clip)
            
            # Composite all clips with the main video
            all_clips = [video_clip] + clips_with_transitions
            return mp.CompositeVideoClip(all_clips)
            
        except Exception as e:
            self.logger.error(f"Error adding multiple visual overlays: {e}")
            return video_clip
    
    def _create_cinematic_visual_clip(self, visual_path: str, duration: int, width: int, height: int) -> mp.VideoClip:
        """Create a cinematic visual clip with motion effects"""
        try:
            if visual_path.lower().endswith(('.mp4', '.avi', '.mov')):
                # Video file - apply cinematic effects
                video_clip = mp.VideoFileClip(visual_path)
                video_clip = video_clip.resize((width, height))
                
                # Apply cinematic motion effects
                video_clip = self._apply_cinematic_motion_effects(video_clip, duration)
                
            else:
                # Image file - create cinematic motion
                image_clip = mp.ImageClip(visual_path, duration=duration)
                image_clip = image_clip.resize((width, height))
                
                # Apply cinematic motion effects to image
                video_clip = self._apply_cinematic_motion_effects(image_clip, duration)
            
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error creating cinematic visual clip: {e}")
            # Fallback to dynamic background
            return self._create_cinematic_background(width, height, duration, 'general')
    
    def _apply_cinematic_motion_effects(self, clip: mp.VideoClip, duration: int) -> mp.VideoClip:
        """Apply cinematic motion effects to video clip"""
        try:
            # Apply Ken Burns effect (slow zoom/pan)
            def ken_burns_effect(get_frame, t):
                frame = get_frame(t)
                # Calculate zoom factor over time
                zoom_factor = 1.0 + (t / duration) * 0.1  # 10% zoom over duration
                
                # Apply zoom effect
                h, w = frame.shape[:2]
                new_h, new_w = int(h * zoom_factor), int(w * zoom_factor)
                
                # Resize frame using numpy instead of moviepy
                import numpy as np
                from PIL import Image
                
                # Convert to PIL Image for resizing
                pil_img = Image.fromarray(frame)
                resized_pil = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                # Convert back to numpy array
                resized = np.array(resized_pil)
                
                # Crop to original size
                start_y = (new_h - h) // 2
                start_x = (new_w - w) // 2
                cropped = resized[start_y:start_y+h, start_x:start_x+w]
                
                return cropped
            
            # Apply the effect
            clip = clip.fl(ken_burns_effect)
            
            # Add subtle motion blur
            clip = clip.fx(mp.vfx.colorx, 1.1)  # Slight color enhancement
            
            return clip
            
        except Exception as e:
            self.logger.error(f"Error applying cinematic motion effects: {e}")
            return clip
    
    def _create_cinematic_background(self, width: int, height: int, duration: int, channel_type: str) -> mp.VideoClip:
        """Create a cinematic dynamic background"""
        def make_cinematic_frame(t):
            import numpy as np
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Channel-specific cinematic color schemes
            if channel_type == "cklegends":
                # Epic golden/red cinematic theme
                for y in range(height):
                    for x in range(width):
                        # Dynamic golden gradient with motion
                        r = int(180 + 40 * np.sin(x/300 + t/3) + 20 * np.sin(y/200 + t/2))
                        g = int(120 + 30 * np.sin(x/400 + t/4) + 15 * np.sin(y/300 + t/3))
                        b = int(60 + 20 * np.sin(x/500 + t/5) + 10 * np.sin(y/400 + t/4))
                        frame[y, x] = [r, g, b]
                        
            elif channel_type == "ckdrive":
                # Cool blue/silver automotive cinematic theme
                for y in range(height):
                    for x in range(width):
                        # Dynamic blue gradient with motion
                        r = int(40 + 20 * np.sin(x/250 + t/2))
                        g = int(80 + 40 * np.sin(y/300 + t/3))
                        b = int(200 + 50 * np.sin((x+y)/400 + t/4))
                        frame[y, x] = [r, g, b]
                        
            elif channel_type == "ckcombat":
                # Dark red/black combat cinematic theme
                for y in range(height):
                    for x in range(width):
                        # Dynamic dark theme with motion
                        r = int(100 + 50 * np.sin(x/200 + t/2))
                        g = int(20 + 10 * np.sin(y/200 + t/3))
                        b = int(20 + 10 * np.sin((x+y)/400 + t/4))
                        frame[y, x] = [r, g, b]
                        
            elif channel_type == "ckironwill":
                # Warm motivational cinematic theme
                for y in range(height):
                    for x in range(width):
                        # Dynamic warm gradient with motion
                        r = int(150 + 30 * np.sin(x/300 + t/2))
                        g = int(100 + 20 * np.sin(y/300 + t/3))
                        b = int(50 + 15 * np.sin((x+y)/400 + t/4))
                        frame[y, x] = [r, g, b]
                        
            elif channel_type == "ckfinancecore":
                # Professional sophisticated cinematic theme
                for y in range(height):
                    for x in range(width):
                        # Dynamic professional gradient with motion
                        r = int(80 + 30 * np.sin(x/300 + t/2))
                        g = int(120 + 40 * np.sin(y/300 + t/3))
                        b = int(160 + 50 * np.sin((x+y)/400 + t/4))
                        frame[y, x] = [r, g, b]
                        
            else:
                # Default cinematic gradient
                for y in range(height):
                    intensity = int(100 + 50 * (y / height) + 20 * np.sin(t/2))
                    frame[y, :] = [intensity//3, intensity//3, intensity]
            
            return frame
        
        return mp.VideoClip(make_cinematic_frame, duration=duration)
    
    def _add_cinematic_voiceover(self, video_clip: mp.VideoClip, voiceover_audio_path: str, duration: int) -> mp.VideoClip:
        """Add voiceover with cinematic audio processing"""
        try:
            voiceover_audio = mp.AudioFileClip(voiceover_audio_path)
            
            # Loop audio if shorter than video
            if voiceover_audio.duration < duration:
                loops_needed = int(duration / voiceover_audio.duration) + 1
                voiceover_audio = mp.concatenate_audioclips([voiceover_audio] * loops_needed)
            
            # Trim to video duration
            voiceover_audio = voiceover_audio.subclip(0, duration)
            
            # Apply cinematic audio processing
            voiceover_audio = voiceover_audio.volumex(1.2)  # Slightly louder
            
            # Add subtle fade in/out to individual clips before concatenating
            if hasattr(voiceover_audio, 'fadein'):
                voiceover_audio = voiceover_audio.fadein(0.5).fadeout(0.5)
            
            video_clip = video_clip.set_audio(voiceover_audio)
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error adding cinematic voiceover: {e}")
            return video_clip
    
    def _add_cinematic_music(self, video_clip: mp.VideoClip, music_audio_path: str, duration: int, has_voiceover: bool) -> mp.VideoClip:
        """Add background music with cinematic mixing"""
        try:
            music_audio = mp.AudioFileClip(music_audio_path)
            
            # Loop music if shorter than video
            if music_audio.duration < duration:
                loops_needed = int(duration / music_audio.duration) + 1
                music_audio = mp.concatenate_audioclips([music_audio] * loops_needed)
            
            # Trim to video duration
            music_audio = music_audio.subclip(0, duration)
            
            # Apply cinematic audio processing
            music_audio = music_audio.volumex(0.4)  # Lower volume for background
            
            # Add subtle fade in/out to individual clips before mixing
            if hasattr(music_audio, 'fadein'):
                music_audio = music_audio.fadein(1.0).fadeout(1.0)
            
            if has_voiceover:
                # Mix with existing voiceover
                existing_audio = video_clip.audio
                mixed_audio = mp.CompositeAudioClip([
                    existing_audio.volumex(1.0),
                    music_audio.volumex(0.3)  # Even lower for background
                ])
                video_clip = video_clip.set_audio(mixed_audio)
            else:
                # Set as main audio
                video_clip = video_clip.set_audio(music_audio)
            
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error adding cinematic music: {e}")
            return video_clip
    
    def _add_cinematic_text_overlays(self, video_clip: mp.VideoClip, voiceover: Dict, video_type: str) -> mp.VideoClip:
        """Add cinematic text overlays with professional effects"""
        try:
            if video_clip is None:
                self.logger.error("Video clip is None, cannot add text overlays")
                return None
            
            # Skip text overlays for now to avoid ImageMagick issues
            # Just return the video clip with cinematic effects
            self.logger.info("Skipping text overlays to avoid ImageMagick issues")
            
            # Apply cinematic video effects instead
            video_clip = self._apply_cinematic_video_effects(video_clip, video_type)
            
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error adding cinematic text overlays: {e}")
            return video_clip
    
    def _apply_cinematic_video_effects(self, video_clip: mp.VideoClip, video_type: str) -> mp.VideoClip:
        """Apply cinematic video effects and enhancements"""
        try:
            # Apply cinematic motion effects
            video_clip = self._apply_cinematic_motion_effects(video_clip, video_clip.duration)
            
            # Apply color correction and grading
            video_clip = video_clip.fx(mp.vfx.colorx, 1.1)  # Slight color enhancement
            
            # Apply subtle blur for cinematic look
            video_clip = video_clip.fx(mp.vfx.colorx, 1.05)  # Alternative to blur
            
            # Add film grain effect
            video_clip = self._add_film_grain(video_clip)
            
            # Add vignette effect
            video_clip = self._add_vignette(video_clip)
            
            # Adjust speed for cinematic feel
            if video_type == "short":
                video_clip = video_clip.speedx(1.1)  # Slightly faster for shorts
            else:
                video_clip = video_clip.speedx(0.95)  # Slightly slower for long videos
            
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error applying cinematic video effects: {e}")
            return video_clip
    
    def _apply_25th_frame_effect_func(self, video_clip: mp.VideoFileClip) -> mp.VideoFileClip:
        """Apply 25th frame subliminal messaging technique"""
        try:
            # Create a subliminal frame (very brief flash)
            subliminal_frame = mp.ColorClip(size=(1920, 1080), color=(255, 255, 255), duration=0.04)
            
            # Insert subliminal frame at specific intervals
            frames_to_insert = []
            interval = 25  # Every 25th frame
            
            for i in range(0, int(video_clip.duration * video_clip.fps), interval):
                time_pos = i / video_clip.fps
                if time_pos < video_clip.duration:
                    frames_to_insert.append((time_pos, subliminal_frame))
            
            # Apply subliminal frames
            for time_pos, frame in frames_to_insert:
                video_clip = video_clip.set_start(time_pos).crossfadein(0.02)
            
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error applying 25th frame effect: {e}")
            return video_clip
    
    def _apply_psychological_effects(self, video_clip: mp.VideoFileClip, voiceover: Dict) -> mp.VideoFileClip:
        """Apply psychological manipulation effects"""
        try:
            # Analyze voiceover content for manipulation keywords
            content = voiceover.get('text_content', '').lower()
            
            if any(keyword in content for keyword in ['shocking', 'secret', 'exclusive']):
                # Apply dramatic effects
                video_clip = video_clip.fx(mp.vfx.colorx, 1.2)  # Increase saturation
                video_clip = video_clip.fx(mp.vfx.lum_contrast, lum=1.1, contrast=1.2)
            
            elif any(keyword in content for keyword in ['urgent', 'limited', 'now']):
                # Apply urgency effects
                video_clip = video_clip.fx(mp.vfx.speedx, 1.05)  # Slight speed increase
                video_clip = video_clip.fx(mp.vfx.colorx, 1.1)  # Increase color intensity
            
            elif any(keyword in content for keyword in ['authority', 'expert', 'professional']):
                # Apply authority effects
                video_clip = video_clip.fx(mp.vfx.lum_contrast, lum=0.9, contrast=1.3)
            
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error applying psychological effects: {e}")
            return video_clip
    
    def _apply_transitions(self, video_clip: mp.VideoFileClip) -> mp.VideoFileClip:
        """Apply smooth transitions"""
        try:
            # Add fade in/out
            video_clip = video_clip.fadein(1.0).fadeout(1.0)
            
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error applying transitions: {e}")
            return video_clip
    
    def _apply_color_grading(self, video_clip: mp.VideoFileClip) -> mp.VideoFileClip:
        """Apply color grading for cinematic look"""
        try:
            # Apply cinematic color grading
            video_clip = video_clip.fx(mp.vfx.lum_contrast, lum=1.0, contrast=1.1)
            video_clip = video_clip.fx(mp.vfx.colorx, 1.05)
            
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error applying color grading: {e}")
            return video_clip
    
    def _add_subtitles(self, video_clip: mp.VideoFileClip, voiceover: Dict) -> mp.VideoFileClip:
        """Add multi-language subtitles"""
        if not self.config.get('subtitles', {}).get('enabled', True):
            return video_clip
        
        try:
            # Get text content
            text_content = voiceover.get('text_content', '')
            if not text_content:
                return video_clip
            
            # Create subtitles for different languages
            languages = self.config.get('subtitles', {}).get('languages', ['en'])
            
            subtitle_clips = []
            
            for lang in languages:
                if lang == 'en':
                    subtitle_text = text_content
                elif TRANSLATOR_AVAILABLE:
                    try:
                        translator = GoogleTranslator(source='en', target=lang)
                        subtitle_text = translator.translate(text_content)
                    except Exception as e:
                        self.logger.warning(f"Translation failed for {lang}: {e}")
                        subtitle_text = text_content
                else:
                    subtitle_text = text_content
                
                # Create text clip
                if MOVIEPY_AVAILABLE:
                    text_clip = mp.TextClip(
                        subtitle_text,
                        fontsize=self.config.get('subtitles', {}).get('font_size', 24),
                        color=self.config.get('subtitles', {}).get('font_color', 'white'),
                        bg_color=self.config.get('subtitles', {}).get('background_color', 'black')
                    ).set_duration(video_clip.duration)
                    
                    # Position text
                    position = self.config.get('subtitles', {}).get('position', 'bottom')
                    if position == 'bottom':
                        text_clip = text_clip.set_position(('center', 'bottom'))
                    elif position == 'top':
                        text_clip = text_clip.set_position(('center', 'top'))
                    else:
                        text_clip = text_clip.set_position('center')
                    
                    subtitle_clips.append(text_clip)
            
            # Composite video with subtitles
            if subtitle_clips:
                video_clip = mp.CompositeVideoClip([video_clip] + subtitle_clips)
            
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error adding subtitles: {e}")
            return video_clip
