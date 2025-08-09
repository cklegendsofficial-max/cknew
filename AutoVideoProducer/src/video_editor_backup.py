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
        if not voiceovers:
            self.logger.warning("No voiceovers provided for video editing")
            return []
        
        edited_videos = []
        
        for i, voiceover in enumerate(voiceovers):
            try:
                visual = visuals[i] if i < len(visuals) else None
                music_track = music[i] if i < len(music) else None
                
                edited_video = self._edit_single_video(voiceover, visual, music_track)
                if edited_video:
                    edited_videos.append(edited_video)
                    
            except Exception as e:
                self.logger.error(f"Error editing video {i}: {e}")
                # Create placeholder video
                edited_videos.append(self._create_placeholder_video(voiceover, visual, music_track))
        
        return edited_videos
    
    def edit_video(self, voiceover: Dict, visual: Optional[Dict] = None, music: Optional[Dict] = None) -> Optional[Dict]:
        """
        Edit a single video from voiceover, visual, and music
        
        Args:
            voiceover: Voiceover data
            visual: Visual data (optional)
            music: Music data (optional)
            
        Returns:
            Edited video data or None if failed
        """
        try:
            return self._edit_single_video(voiceover, visual, music)
        except Exception as e:
            self.logger.error(f"Error editing video: {e}")
            return self._create_placeholder_video(voiceover, visual, music)
        """
        if not voiceovers:
            self.logger.warning("No voiceovers provided for video editing")
            return []
        
        videos = []
        
        for i, voiceover in enumerate(voiceovers):
            try:
                # Get corresponding visual and music
                visual = visuals[i] if i < len(visuals) else None
                music_track = music[i] if i < len(music) else None
                
                video = self._edit_single_video(voiceover, visual, music_track)
                if video:
                    videos.append(video)
            except Exception as e:
                self.logger.error(f"Error editing video for voiceover {voiceover.get('title', 'Unknown')}: {e}")
                continue
        
        return videos
    
    def _edit_single_video(self, voiceover: Dict, visual: Optional[Dict], music: Optional[Dict]) -> Optional[Dict]:
        """Edit a single video from voiceover, visual, and music"""
        if not MOVIEPY_AVAILABLE:
            return self._create_placeholder_video(voiceover, visual, music)
        
        try:
            # Create video composition
            video_clip = self._create_video_composition(voiceover, visual, music)
            
            if not video_clip:
                return self._create_placeholder_video(voiceover, visual, music)
            
            # Apply effects
            video_clip = self._apply_video_effects(video_clip, voiceover)
            
            # Add subtitles
            video_clip = self._add_subtitles(video_clip, voiceover)
            
            # Export video
            output_file = self._export_video(video_clip, voiceover)
            
            if not output_file:
                return self._create_placeholder_video(voiceover, visual, music)
            
            return {
                'id': f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'voiceover_id': voiceover.get('id', 'unknown'),
                'visual_id': visual.get('id', 'unknown') if visual else None,
                'music_id': music.get('id', 'unknown') if music else None,
                'title': voiceover.get('title', 'Generated Video'),
                'video_file': output_file,
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'duration': video_clip.duration if video_clip else 0,
                    'width': video_clip.w if video_clip else 0,
                    'height': video_clip.h if video_clip else 0,
                    'fps': video_clip.fps if video_clip else 30,
                    'file_size': os.path.getsize(output_file) if os.path.exists(output_file) else 0,
                    'enhanced': True
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error in video editing: {e}")
            return self._create_placeholder_video(voiceover, visual, music)
    
    def _create_video_composition(self, voiceover: Dict, visual: Optional[Dict], music: Optional[Dict]) -> Optional[mp.VideoFileClip]:
        """Create video composition from voiceover, visual, and music"""
        try:
            # Load voiceover audio
            voiceover_file = voiceover.get('audio_file')
            if not voiceover_file or not os.path.exists(voiceover_file):
                self.logger.warning("Voiceover file not found")
                return None
            
            audio_clip = mp.AudioFileClip(voiceover_file)
            
            # Create video from visual or placeholder
            if visual and os.path.exists(visual.get('image_file', '')):
                visual_file = visual['image_file']
                video_clip = mp.ImageClip(visual_file, duration=audio_clip.duration)
            else:
                # Create placeholder video
                video_clip = self._create_placeholder_video_clip(audio_clip.duration)
            
            # Set audio
            video_clip = video_clip.set_audio(audio_clip)
            
            # Add background music if available
            if music and os.path.exists(music.get('audio_file', '')):
                music_file = music['audio_file']
                music_clip = mp.AudioFileClip(music_file)
                
                # Loop music if shorter than video
                if music_clip.duration < video_clip.duration:
                    loops_needed = int(video_clip.duration / music_clip.duration) + 1
                    music_clip = mp.concatenate_audioclips([music_clip] * loops_needed)
                
                # Trim music to video duration
                music_clip = music_clip.subclip(0, video_clip.duration)
                
                # Mix audio (voiceover + background music)
                mixed_audio = mp.CompositeAudioClip([
                    audio_clip.volumex(1.0),
                    music_clip.volumex(0.3)  # Lower volume for background
                ])
                
                video_clip = video_clip.set_audio(mixed_audio)
            
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error creating video composition: {e}")
            return None
    
    def _create_placeholder_video_clip(self, duration: float) -> mp.VideoFileClip:
        """Create a placeholder video clip"""
        if not PIL_AVAILABLE:
            # Create a simple colored video
            return mp.ColorClip(size=(1920, 1080), color=(100, 100, 100), duration=duration)
        
        # Create a more sophisticated placeholder
        try:
            # Create image with text
            img = Image.new('RGB', (1920, 1080), color='darkblue')
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            text = "Video Content"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (1920 - text_width) // 2
            y = (1080 - text_height) // 2
            
            draw.text((x, y), text, fill='white', font=font)
            
            # Save temporary image
            temp_img_path = f"temp_placeholder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            img.save(temp_img_path)
            
            # Create video clip
            video_clip = mp.ImageClip(temp_img_path, duration=duration)
            
            # Clean up temp file
            if os.path.exists(temp_img_path):
                os.remove(temp_img_path)
            
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error creating placeholder video clip: {e}")
            return mp.ColorClip(size=(1920, 1080), color=(100, 100, 100), duration=duration)
    
    def _apply_video_effects(self, video_clip: mp.VideoFileClip, voiceover: Dict) -> mp.VideoFileClip:
        """Apply video effects including psychological manipulation"""
        try:
            # Apply 25th frame technique if enabled
            if self.config.get('effects', {}).get('use_25th_frame', True):
                video_clip = self._apply_25th_frame_effect_func(video_clip)
            
            # Apply psychological effects if enabled
            if self.config.get('effects', {}).get('use_psychological_effects', True):
                video_clip = self._apply_psychological_effects(video_clip, voiceover)
            
            # Apply transitions if enabled
            if self.config.get('effects', {}).get('use_transitions', True):
                video_clip = self._apply_transitions(video_clip)
            
            # Apply color grading if enabled
            if self.config.get('effects', {}).get('use_color_grading', True):
                video_clip = self._apply_color_grading(video_clip)
            
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error applying video effects: {e}")
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
                    except:
                        subtitle_text = text_content
                else:
                    subtitle_text = text_content
                
                # Create subtitle clip
                subtitle_clip = self._create_subtitle_clip(subtitle_text, video_clip.duration, lang)
                if subtitle_clip:
                    subtitle_clips.append(subtitle_clip)
            
            # Composite video with subtitles
            if subtitle_clips:
                video_clip = mp.CompositeVideoClip([video_clip] + subtitle_clips)
            
            return video_clip
            
        except Exception as e:
            self.logger.error(f"Error adding subtitles: {e}")
            return video_clip
    
    def _create_subtitle_clip(self, text: str, duration: float, language: str) -> Optional[mp.TextClip]:
        """Create a subtitle text clip"""
        try:
            subtitle_config = self.config.get('subtitles', {})
            
            # Create text clip
            txt_clip = mp.TextClip(
                text,
                fontsize=subtitle_config.get('font_size', 24),
                color=subtitle_config.get('font_color', 'white'),
                bg_color=subtitle_config.get('background_color', 'black'),
                font='Arial'
            )
            
            # Position subtitle
            position = subtitle_config.get('position', 'bottom')
            if position == 'bottom':
                txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(duration)
            else:
                txt_clip = txt_clip.set_position('center').set_duration(duration)
            
            return txt_clip
            
        except Exception as e:
            self.logger.error(f"Error creating subtitle clip: {e}")
            return None
    
    def _export_video(self, video_clip: mp.VideoFileClip, voiceover: Dict) -> Optional[str]:
        """Export video to file"""
        try:
            output_dir = self.config.get("output_directory", "videos")
            os.makedirs(output_dir, exist_ok=True)
            
            video_config = self.config.get("video", {})
            
            filename = f"{output_dir}/video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{video_config.get('format', 'mp4')}"
            
            # Export video
            video_clip.write_videofile(
                filename,
                fps=video_config.get('fps', 30),
                codec=video_config.get('codec', 'libx264'),
                audio_codec='aac'
            )
            
            return filename
            
        except Exception as e:
            self.logger.error(f"Error exporting video: {e}")
            return None
    
    def _create_placeholder_video(self, voiceover: Dict, visual: Optional[Dict], music: Optional[Dict]) -> Dict:
        """Create a placeholder video when MoviePy is not available"""
        # Create a placeholder file
        output_dir = self.config.get("output_directory", "videos")
        os.makedirs(output_dir, exist_ok=True)
        
        placeholder_file = f"{output_dir}/placeholder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(placeholder_file, 'w', encoding='utf-8') as f:
            f.write(f"VIDEO PLACEHOLDER\n\nVoiceover: {voiceover.get('title', 'Unknown')}\n")
            if visual:
                f.write(f"Visual: {visual.get('title', 'Unknown')}\n")
            if music:
                f.write(f"Music: {music.get('title', 'Unknown')}\n")
            f.write("\nPlease generate video manually or install video editing dependencies.")
        
        return {
            'id': f"placeholder_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'voiceover_id': voiceover.get('id', 'unknown'),
            'visual_id': visual.get('id', 'unknown') if visual else None,
            'music_id': music.get('id', 'unknown') if music else None,
            'title': voiceover.get('title', 'Placeholder Video'),
            'video_file': placeholder_file,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'method': 'placeholder',
                'duration': 0.0,
                'file_size': os.path.getsize(placeholder_file) if os.path.exists(placeholder_file) else 0,
                'enhanced': False
            }
        }
    
    def save_video_metadata(self, video: Dict, filename: str = None) -> str:
        """Save video metadata to JSON file"""
        if not filename:
            filename = f"videos/{video['id']}_metadata.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(video, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Video metadata saved to {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error saving video metadata: {e}")
            return ""

# Example usage
if __name__ == "__main__":
    # Test video editing
    video_editor = VideoEditor()
    
    test_voiceover = {
        'id': 'test_voiceover_001',
        'title': 'Test Voiceover',
        'audio_file': 'voiceovers/test_voiceover.wav',
        'text_content': 'This is a test voiceover for video editing.',
        'metadata': {
            'duration': 30.0
        }
    }
    
    test_visual = {
        'id': 'test_visual_001',
        'title': 'Test Visual',
        'image_file': 'visuals/test_visual.png',
        'metadata': {
            'width': 1920,
            'height': 1080
        }
    }
    
    test_music = {
        'id': 'test_music_001',
        'title': 'Test Music',
        'audio_file': 'music/test_music.wav',
        'metadata': {
            'duration': 30.0
        }
    }
    
    videos = video_editor.edit_videos([test_voiceover], [test_visual], [test_music])
    print(f"Generated {len(videos)} videos")
    
    if videos:
        print("First video preview:")
        print(f"Video file: {videos[0]['video_file']}")
        print(f"Duration: {videos[0]['metadata']['duration']} seconds")
