#!/usr/bin/env python3
"""
Voiceover Generator Module
Generates voiceovers using gTTS with tone mimic capabilities and fallback options
"""

import os
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime
import subprocess
import tempfile
import time

# Try to import optional dependencies
try:
    import gtts
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    logging.warning("gTTS not available for voiceover generation")

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    logging.warning("pyttsx3 not available for voiceover generation")

try:
    import pydub
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    logging.warning("pydub not available for audio processing")

class VoiceoverSettings:
    """Settings for voiceover generation"""
    def __init__(self):
        self.default_language = "en"
        self.default_tone = "friendly"
        self.audio_format = "mp3"
        self.sample_rate = 22050
        self.bitrate = "64k"
        self.output_directory = "voiceovers"
        self.use_manipulation_tone = True
        self.enhance_psychological_impact = True

class VoiceoverGenerator:
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the voiceover generator with configuration"""
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self.voice_cache = {}
        self.tone_presets = {
            'excited': {'rate': 1.2, 'pitch': 1.1, 'volume': 1.2},
            'calm': {'rate': 0.9, 'pitch': 0.95, 'volume': 0.9},
            'authoritative': {'rate': 1.0, 'pitch': 1.05, 'volume': 1.1},
            'friendly': {'rate': 1.1, 'pitch': 1.0, 'volume': 1.0},
            'dramatic': {'rate': 0.95, 'pitch': 1.15, 'volume': 1.3},
            'manipulative': {'rate': 1.05, 'pitch': 1.08, 'volume': 1.15}  # For psychological manipulation
        }
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize audio processing
        self._init_audio_processing()
        
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
            "default_language": "en",
            "default_tone": "friendly",
            "audio_format": "mp3",
            "sample_rate": 22050,
            "bitrate": "64k",
            "output_directory": "voiceovers",
            "use_manipulation_tone": True,
            "enhance_psychological_impact": True
        }
    
    def _init_audio_processing(self):
        """Initialize audio processing capabilities"""
        self.can_process_audio = PYDUB_AVAILABLE
        if not self.can_process_audio:
            self.logger.warning("Audio processing not available - voiceovers will be basic")
    
    def generate_voiceovers(self, scripts: List[Dict]) -> List[Dict]:
        """Generate voiceovers for scripts using gTTS"""
        if not scripts:
            self.logger.warning("No scripts provided for voiceover generation")
            return []
        
        voiceovers = []
        
        for i, script in enumerate(scripts):
            try:
                voiceover = self._generate_single_voiceover(script, i)
                if voiceover:
                    voiceovers.append(voiceover)
            except Exception as e:
                self.logger.error(f"Error generating voiceover for script {i}: {e}")
                continue
        
        return voiceovers
    
    def _generate_single_voiceover(self, script: Dict, index: int) -> Optional[Dict]:
        """Generate a single voiceover from script"""
        try:
            # Get script content
            content = script.get('content', '')
            title = script.get('title', f'Script {index+1}')
            
            # If content is empty or fallback, create better content
            if not content or 'fallback' in content.lower():
                content = self._create_enhanced_script_content(title, script)
            
            # Create output directory
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'voiceovers')
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate voiceover file
            voiceover_filename = f"voiceover_{index+1}_{int(time.time())}.mp3"
            voiceover_path = os.path.join(output_dir, voiceover_filename)
            
            # Generate voiceover using gTTS
            if GTTS_AVAILABLE:
                try:
                    # Create gTTS object with enhanced settings
                    tts = gtts.gTTS(
                        text=content,
                        lang='en',
                        slow=False,
                        lang_check=True
                    )
                    
                    # Save the voiceover
                    tts.save(voiceover_path)
                    
                    # Verify file was created
                    if os.path.exists(voiceover_path) and os.path.getsize(voiceover_path) > 0:
                        self.logger.info(f"Generated voiceover: {voiceover_path}")
                        
                        return {
                            'id': f"voiceover_{index+1}_{int(time.time())}",
                            'title': title,
                            'audio_file': voiceover_path,
                            'content': content,
                            'duration': self._estimate_audio_duration(content),
                            'language': 'en',
                            'metadata': {
                                'generated_at': datetime.now().isoformat(),
                                'script_id': script.get('id', f'script_{index+1}'),
                                'method': 'gtts',
                                'enhanced': True
                            }
                        }
                    else:
                        raise Exception("Voiceover file was not created properly")
                        
                except Exception as e:
                    self.logger.error(f"Error generating gTTS voiceover: {e}")
                    return self._create_fallback_voiceover(script, index, voiceover_path)
            
            else:
                self.logger.warning("gTTS not available, creating fallback voiceover")
                return self._create_fallback_voiceover(script, index, voiceover_path)
                
        except Exception as e:
            self.logger.error(f"Error in voiceover generation: {e}")
            return None
    
    def _create_enhanced_script_content(self, title: str, script: Dict) -> str:
        """Create enhanced script content when original is fallback"""
        try:
            # Create engaging content based on title
            enhanced_content = f"""
Welcome to our channel! Today we're exploring {title}.

This is a fascinating topic that will change your perspective completely. 
What you're about to learn will surprise you and make you think differently.

The key insights we'll cover today are absolutely crucial for understanding this subject.
You won't want to miss what comes next.

Stay tuned as we dive deep into the most important aspects of {title}.
This information could be life-changing for you.

Remember to like, subscribe, and share this video with others who might benefit.
Thank you for watching, and we'll see you in the next video!
"""
            return enhanced_content
            
        except Exception as e:
            self.logger.error(f"Error creating enhanced content: {e}")
            return f"Welcome to our channel! Today we're exploring {title}. This is an amazing topic that will change your perspective. Stay tuned for more content!"
    
    def _create_fallback_voiceover(self, script: Dict, index: int, voiceover_path: str) -> Dict:
        """Create a fallback voiceover when gTTS fails"""
        try:
            title = script.get('title', f'Script {index+1}')
            
            # Create simple text content
            fallback_content = f"Welcome to our channel! Today we're exploring {title}. This is an amazing topic that will change your perspective. Stay tuned for more content!"
            
            # Try to create a simple audio file
            try:
                import numpy as np
                import wave
                
                # Create a simple beep sound
                sample_rate = 44100
                duration = 10.0  # 10 seconds
                frequency = 440.0  # A4 note
                
                # Generate sine wave
                t = np.linspace(0, duration, int(sample_rate * duration), False)
                audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
                
                # Convert to 16-bit PCM
                audio_data = (audio_data * 32767).astype(np.int16)
                
                # Save as WAV first, then convert to MP3 if possible
                wav_path = voiceover_path.replace('.mp3', '.wav')
                with wave.open(wav_path, 'w') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(audio_data.tobytes())
                
                # Try to convert WAV to MP3
                try:
                    from pydub import AudioSegment
                    audio = AudioSegment.from_wav(wav_path)
                    audio.export(voiceover_path, format="mp3")
                    os.remove(wav_path)  # Clean up WAV file
                except:
                    # If MP3 conversion fails, use WAV file
                    voiceover_path = wav_path
                
                return {
                    'id': f"voiceover_{index+1}_{int(time.time())}",
                    'title': title,
                    'audio_file': voiceover_path,
                    'content': fallback_content,
                    'duration': duration,
                    'language': 'en',
                    'metadata': {
                        'generated_at': datetime.now().isoformat(),
                        'script_id': script.get('id', f'script_{index+1}'),
                        'method': 'fallback_audio',
                        'enhanced': False
                    }
                }
                
            except Exception as e:
                self.logger.error(f"Error creating fallback audio: {e}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error creating fallback voiceover: {e}")
            return None
    
    def _get_audio_duration(self, audio_path: str) -> float:
        """Get audio file duration"""
        try:
            if PYDUB_AVAILABLE:
                from pydub import AudioSegment
                audio = AudioSegment.from_file(audio_path)
                return len(audio) / 1000.0  # Convert to seconds
            else:
                return 10.0  # Default duration
        except Exception as e:
            self.logger.error(f"Error getting audio duration: {e}")
            return 10.0
    
    def _generate_fallback_voiceover(self, script: Dict) -> Dict:
        """Generate a fallback voiceover when TTS is not available"""
        text_content = self._extract_voiceover_text(script)
        
        # Create a placeholder file
        output_dir = self.config.get('output_directory', 'voiceovers')
        os.makedirs(output_dir, exist_ok=True)
        
        placeholder_file = f"{output_dir}/placeholder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(placeholder_file, 'w', encoding='utf-8') as f:
            f.write(f"VOICEOVER PLACEHOLDER\n\nText Content:\n{text_content}\n\nPlease generate voiceover manually or install TTS dependencies.")
        
        return {
            'id': f"fallback_voiceover_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'script_id': script.get('id', 'unknown'),
            'title': script.get('title', 'Fallback Voiceover'),
            'audio_file': placeholder_file,
            'text_content': text_content,
            'tone': 'friendly',
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'method': 'fallback',
                'duration': 0.0,
                'file_size': os.path.getsize(placeholder_file) if os.path.exists(placeholder_file) else 0,
                'enhanced': False
            }
        }
    
    def create_multi_language_voiceover(self, script: Dict, languages: List[str]) -> Dict[str, str]:
        """Create voiceover in multiple languages"""
        if not GTTS_AVAILABLE:
            self.logger.warning("gTTS not available for multi-language voiceover")
            return {}
        
        voiceovers = {}
        text_content = self._extract_voiceover_text(script)
        
        for language in languages:
            try:
                audio_file = self._generate_audio(text_content, 'friendly', language)
                if audio_file:
                    voiceovers[language] = audio_file
            except Exception as e:
                self.logger.error(f"Error generating voiceover for language {language}: {e}")
                continue
        
        return voiceovers
    
    def save_voiceover_metadata(self, voiceover: Dict, filename: str = None) -> str:
        """Save voiceover metadata to JSON file"""
        if not filename:
            filename = f"voiceovers/{voiceover['id']}_metadata.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(voiceover, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Voiceover metadata saved to {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error saving voiceover metadata: {e}")
            return ""

# Example usage
if __name__ == "__main__":
    # Test voiceover generation
    voiceover_generator = VoiceoverGenerator()
    
    test_script = {
        'id': 'test_script_001',
        'title': 'Test Script',
        'content': 'This is a test script for voiceover generation. It contains exciting content that will engage viewers.',
        'sections': {
            'hook': 'Have you ever wondered about the secrets of success?',
            'intro': 'Today we reveal the shocking truth.',
            'main': 'Here are the three key principles that will change your life.',
            'cta': 'Subscribe now for more exclusive content!'
        },
        'metadata': {
            'language': 'en'
        }
    }
    
    voiceovers = voiceover_generator.generate_voiceovers([test_script])
    print(f"Generated {len(voiceovers)} voiceovers")
    
    if voiceovers:
        print("First voiceover preview:")
        print(f"Audio file: {voiceovers[0]['audio_file']}")
        print(f"Duration: {voiceovers[0]['metadata']['duration']} seconds")
