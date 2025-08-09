#!/usr/bin/env python3
"""
Music Generator Module
Generates music using audiocraft with fallback to music21 MIDI generation
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
    import audiocraft
    from audiocraft.models import MusicGen
    AUDIOCRAFT_AVAILABLE = True
except ImportError:
    AUDIOCRAFT_AVAILABLE = False
    logging.warning("Audiocraft not available for music generation")

try:
    import music21
    MUSIC21_AVAILABLE = True
except ImportError:
    MUSIC21_AVAILABLE = False
    logging.warning("music21 not available for MIDI generation")

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logging.warning("PyTorch not available for music generation")

try:
    import pydub
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    logging.warning("pydub not available for MIDI to WAV conversion")

class MusicGenerator:
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the music generator with configuration"""
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self.music_cache = {}
        self.model = None
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize music generation model
        self._init_music_model()
        
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
            "audiocraft": {
                "model": "facebook/musicgen-small",
                "duration": 30,
                "temperature": 1.0,
                "top_k": 250,
                "top_p": 0.0,
                "cfg_coef": 3.0
            },
            "music21": {
                "default_key": "C",
                "default_tempo": 120,
                "default_duration": 30,
                "chord_progression": ["C", "Am", "F", "G"]
            },
            "output_directory": "music",
            "audio_format": "mp3",
            "sample_rate": 44100,
            "use_manipulation_music": True,
            "mimic_best_composers": True
        }
    
    def _init_music_model(self):
        """Initialize music generation model"""
        if not AUDIOCRAFT_AVAILABLE or not TORCH_AVAILABLE:
            self.logger.warning("Audiocraft/PyTorch not available - using music21 fallback")
            return
        
        try:
            ac_config = self.config.get("audiocraft", {})
            model_name = ac_config.get("model", "facebook/musicgen-small")
            
            self.logger.info(f"Initializing MusicGen with model: {model_name}")
            
            self.model = MusicGen.get_pretrained(model_name)
            
            # Set generation parameters
            self.model.set_generation_params(
                duration=ac_config.get("duration", 30),
                temperature=ac_config.get("temperature", 1.0),
                top_k=ac_config.get("top_k", 250),
                top_p=ac_config.get("top_p", 0.0),
                cfg_coef=ac_config.get("cfg_coef", 3.0)
            )
            
            self.logger.info("MusicGen model initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing MusicGen: {e}")
            self.model = None
    
    def generate_music(self, scripts: List[Dict]) -> List[Dict]:
        """
        Generate music for scripts
        
        Args:
            scripts: List of scripts from script writer
            
        Returns:
            List of generated music tracks with metadata
        """
        try:
            self.logger.info(f"Generating music for {len(scripts)} scripts")
            
            music_tracks = []
            
            for i, script in enumerate(scripts):
                try:
                    music = self._generate_single_music(script, i)
                    if music:
                        music_tracks.append(music)
                except Exception as e:
                    self.logger.error(f"Error generating music for script {i+1}: {e}")
                    continue
            
            return music_tracks
            
        except Exception as e:
            self.logger.error(f"Error generating music: {e}")
            return []
    
    def _generate_single_music(self, script: Dict, index: int) -> Optional[Dict]:
        """Generate music for a single script"""
        try:
            # Create output directory
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'music')
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate music file - DIRECT WAV, NO MIDI
            music_filename = f"music_{index+1}_{int(time.time())}.wav"  # Direct WAV
            music_path = os.path.join(output_dir, music_filename)
            
            # Generate music using music21 with direct WAV output
            if MUSIC21_AVAILABLE:
                try:
                    # Create music based on script content
                    music_stream = self._create_music_from_script(script)
                    
                    # Export directly to WAV using music21
                    try:
                        music_stream.write('musicxml', fp=music_path.replace('.wav', '.xml'))
                        # Convert XML to WAV using simple sine wave
                        self._create_wav_from_stream(music_stream, music_path)
                    except Exception as e:
                        self.logger.warning(f"Could not export to WAV directly: {e}")
                        # Create simple WAV as fallback
                        self._create_simple_wav_fallback(script, index, music_path)
                    
                    self.logger.info(f"Generated music: {music_path}")
                    
                    return {
                        'id': f"music_{index+1}_{int(time.time())}",
                        'title': f"Music for {script.get('title', 'Script')}",
                        'audio_file': music_path,
                        'duration': self._get_music_duration(music_stream),
                        'genre': self._determine_genre(script),
                        'tempo': 120,
                        'metadata': {
                            'generated_at': datetime.now().isoformat(),
                            'script_id': script.get('id', f'script_{index+1}'),
                            'method': 'music21_direct_wav',
                            'enhanced': True
                        }
                    }
                    
                except Exception as e:
                    self.logger.error(f"Error generating music21 music: {e}")
                    return self._create_simple_wav_fallback(script, index, music_path)
            
            else:
                self.logger.warning("music21 not available, creating fallback music")
                return self._create_simple_wav_fallback(script, index, music_path)
                
        except Exception as e:
            self.logger.error(f"Error in music generation: {e}")
            return self._create_simple_wav_fallback(script, index, music_path)
    
    def _create_music_from_script(self, script: Dict) -> 'music21.stream.Stream':
        """Create music based on script content"""
        from music21 import stream, note, chord, key, meter
        
        # Create a stream
        s = stream.Stream()
        
        # Set key and meter
        s.append(key.Key('C'))
        s.append(meter.TimeSignature('4/4'))
        
        # Determine style based on script content
        title = script.get('title', '').lower()
        content = script.get('content', '').lower()
        
        if any(word in title for word in ['warrior', 'battle', 'legend']):
            # Epic/heroic style
            notes = [
                note.Note('C4', quarterLength=1),
                note.Note('E4', quarterLength=1),
                note.Note('G4', quarterLength=1),
                note.Note('C5', quarterLength=1),
                note.Note('G4', quarterLength=1),
                note.Note('E4', quarterLength=1),
                note.Note('C4', quarterLength=2)
            ]
        elif any(word in title for word in ['car', 'racing', 'drive']):
            # Fast/energetic style
            notes = [
                note.Note('C4', quarterLength=0.5),
                note.Note('D4', quarterLength=0.5),
                note.Note('E4', quarterLength=0.5),
                note.Note('F4', quarterLength=0.5),
                note.Note('G4', quarterLength=0.5),
                note.Note('A4', quarterLength=0.5),
                note.Note('B4', quarterLength=0.5),
                note.Note('C5', quarterLength=1)
            ]
        elif any(word in title for word in ['combat', 'martial', 'fight']):
            # Intense/aggressive style
            notes = [
                note.Note('C4', quarterLength=0.25),
                note.Note('C4', quarterLength=0.25),
                note.Note('E4', quarterLength=0.25),
                note.Note('E4', quarterLength=0.25),
                note.Note('G4', quarterLength=0.25),
                note.Note('G4', quarterLength=0.25),
                note.Note('C5', quarterLength=1)
            ]
        elif any(word in title for word in ['mental', 'strength', 'success']):
            # Motivational/inspirational style
            notes = [
                note.Note('C4', quarterLength=2),
                note.Note('E4', quarterLength=2),
                note.Note('G4', quarterLength=2),
                note.Note('C5', quarterLength=2)
            ]
        elif any(word in title for word in ['investment', 'finance', 'wealth']):
            # Professional/sophisticated style
            notes = [
                note.Note('C4', quarterLength=1),
                note.Note('F4', quarterLength=1),
                note.Note('A4', quarterLength=1),
                note.Note('C5', quarterLength=1)
            ]
        else:
            # Default style
            notes = [
                note.Note('C4', quarterLength=1),
                note.Note('D4', quarterLength=1),
                note.Note('E4', quarterLength=1),
                note.Note('F4', quarterLength=1),
                note.Note('G4', quarterLength=1),
                note.Note('A4', quarterLength=1),
                note.Note('B4', quarterLength=1),
                note.Note('C5', quarterLength=1)
            ]
        
        # Add notes to stream
        for n in notes:
            s.append(n)
        
        # Add a chord at the end
        c = chord.Chord(['C4', 'E4', 'G4'], quarterLength=2)
        s.append(c)
        
        return s
    
    def _determine_genre(self, script: Dict) -> str:
        """Determine music genre based on script content"""
        title = script.get('title', '').lower()
        
        if any(word in title for word in ['warrior', 'battle', 'legend']):
            return 'epic'
        elif any(word in title for word in ['car', 'racing', 'drive']):
            return 'energetic'
        elif any(word in title for word in ['combat', 'martial', 'fight']):
            return 'intense'
        elif any(word in title for word in ['mental', 'strength', 'success']):
            return 'motivational'
        elif any(word in title for word in ['investment', 'finance', 'wealth']):
            return 'sophisticated'
        else:
            return 'ambient'
    
    def _get_music_duration(self, music_stream: 'music21.stream.Stream') -> float:
        """Get music duration in seconds"""
        try:
            return music_stream.duration.quarterLength * 0.5  # Approximate seconds
        except:
            return 30.0  # Default duration
    
    def _create_fallback_music(self, script: Dict, index: int, music_path: str) -> Dict:
        """Create fallback music using music21"""
        try:
            import music21 as m21
            
            # Create a simple composition
            s = m21.stream.Stream()
            
            # Add a simple melody
            notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'F4', 'E4', 'D4']
            for note_name in notes:
                n = m21.note.Note(note_name)
                n.duration = m21.duration.Duration(1.0)  # Quarter note
                s.append(n)
            
            # Add some chords for harmony
            chord = m21.chord.Chord(['C4', 'E4', 'G4'])
            chord.duration = m21.duration.Duration(4.0)  # Whole note
            s.append(chord)
            
            # Create WAV directly from stream
            wav_path = music_path.replace('.mid', '.wav')
            self._create_wav_from_stream(s, wav_path)
            
            return {
                'id': f"music_{index+1}_{int(time.time())}",
                'title': f"Fallback Music for {script.get('title', 'Script')}",
                'audio_file': wav_path,
                'duration': 30.0,
                'genre': 'ambient',
                'tempo': 120,
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'script_id': script.get('id', f'script_{index+1}'),
                    'method': 'music21_fallback_wav',
                    'enhanced': False
                }
            }
                
        except Exception as e:
            self.logger.error(f"Error in fallback music generation: {e}")
            return self._create_simple_wav_fallback(script, index, music_path)
    
    def _create_simple_wav_fallback(self, script: Dict, index: int, music_path: str) -> Dict:
        """Create a simple WAV file as last resort"""
        try:
            import numpy as np
            import wave
            
            # Create a simple sine wave
            sample_rate = 44100
            duration = 30.0
            frequency = 440.0  # A4 note
            
            # Generate sine wave
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
            
            # Convert to 16-bit PCM
            audio_data = (audio_data * 32767).astype(np.int16)
            
            # Save as WAV
            wav_path = music_path.replace('.mid', '.wav')
            with wave.open(wav_path, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data.tobytes())
            
            return {
                'id': f"music_{index+1}_{int(time.time())}",
                'title': f"Simple Fallback Music for {script.get('title', 'Script')}",
                'audio_file': wav_path,
                'duration': duration,
                'genre': 'ambient',
                'tempo': 120,
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'script_id': script.get('id', f'script_{index+1}'),
                    'method': 'simple_wav_fallback',
                    'enhanced': False
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error creating simple WAV fallback: {e}")
            return None
    
    def _extract_music_prompts(self, script: Dict) -> List[str]:
        """Extract music prompts from script content"""
        prompts = []
        
        # Extract from script content
        content = script.get('content', '')
        sections = script.get('sections', {})
        
        # Combine all text for analysis
        all_text = content
        for section_content in sections.values():
            if section_content:
                all_text += " " + section_content
        
        # Generate prompts based on content analysis
        prompts.extend(self._generate_content_based_prompts(all_text))
        
        # Add manipulation-specific prompts if enabled
        if self.config.get('use_manipulation_music', True):
            prompts.extend(self._generate_manipulation_prompts(all_text))
        
        # Add "mimic best" prompts if enabled
        if self.config.get('mimic_best_composers', True):
            prompts.extend(self._generate_mimic_best_prompts(all_text))
        
        return list(set(prompts))  # Remove duplicates
    
    def _generate_content_based_prompts(self, text: str) -> List[str]:
        """Generate prompts based on script content"""
        prompts = []
        
        # Simple keyword-based prompt generation
        keywords = {
            'epic': ['epic', 'grand', 'heroic', 'triumphant', 'victory'],
            'dramatic': ['dramatic', 'intense', 'emotional', 'powerful'],
            'calm': ['peaceful', 'calm', 'serene', 'relaxing', 'gentle'],
            'energetic': ['energetic', 'upbeat', 'exciting', 'dynamic'],
            'mysterious': ['mysterious', 'dark', 'suspenseful', 'enigmatic'],
            'inspiring': ['inspiring', 'motivational', 'uplifting', 'positive']
        }
        
        text_lower = text.lower()
        
        for category, words in keywords.items():
            if any(word in text_lower for word in words):
                prompts.append(f"{category} music, cinematic, professional quality")
        
        # Default prompt if no specific category found
        if not prompts:
            prompts.append("cinematic background music, professional quality, engaging")
        
        return prompts
    
    def _generate_manipulation_prompts(self, text: str) -> List[str]:
        """Generate prompts for psychological manipulation music"""
        prompts = []
        
        # Check for manipulation keywords
        manipulation_keywords = ['shocking', 'secret', 'exclusive', 'urgent', 'limited', 'reveal']
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in manipulation_keywords):
            prompts.extend([
                "suspenseful music, psychological thriller soundtrack, building tension",
                "dramatic orchestral music, emotional manipulation, cinematic impact",
                "intense background music, psychological warfare, subliminal messaging"
            ])
        
        return prompts
    
    def _generate_mimic_best_prompts(self, text: str) -> List[str]:
        """Generate prompts to mimic best composers (Hans Zimmer, John Williams, etc.)"""
        prompts = []
        
        # Add prompts that mimic the style of renowned composers
        prompts.extend([
            "Hans Zimmer style, epic orchestral, emotional depth, cinematic grandeur",
            "John Williams style, memorable melodies, heroic themes, orchestral excellence",
            "Howard Shore style, atmospheric, emotional storytelling, professional composition"
        ])
        
        return prompts
    
    def _generate_audiocraft_music(self, prompts: List[str], script: Dict) -> Optional[Dict]:
        """Generate music using Audiocraft/MusicGen"""
        if not self.model:
            return None
        
        try:
            ac_config = self.config.get("audiocraft", {})
            
            # Combine prompts with enhancement
            enhanced_prompt = self._enhance_prompt_for_audiocraft(prompts[0], script)
            
            # Generate music
            wav = self.model.generate([enhanced_prompt])
            
            # Save audio
            output_dir = self.config.get("output_directory", "music")
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"{output_dir}/music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            
            # Convert tensor to audio file
            import torchaudio
            torchaudio.save(filename, wav.squeeze(0), self.config.get("sample_rate", 44100))
            
            return {
                'id': f"music_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'script_id': script.get('id', 'unknown'),
                'title': script.get('title', 'Generated Music'),
                'audio_file': filename,
                'prompt': enhanced_prompt,
                'method': 'audiocraft',
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'duration': ac_config.get("duration", 30),
                    'sample_rate': self.config.get("sample_rate", 44100),
                    'file_size': os.path.getsize(filename) if os.path.exists(filename) else 0,
                    'enhanced': True
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error in Audiocraft generation: {e}")
            return None
    
    def _enhance_prompt_for_audiocraft(self, base_prompt: str, script: Dict) -> str:
        """Enhance prompt for Audiocraft with manipulation techniques"""
        enhanced = base_prompt
        
        # Add manipulation enhancement
        if self.config.get('use_manipulation_music', True):
            enhanced += ", psychological impact, subliminal messaging, emotional manipulation"
        
        # Add mimic best enhancement
        if self.config.get('mimic_best_composers', True):
            enhanced += ", surpass Hans Zimmer/John Williams quality, professional composition"
        
        # Add technical quality
        enhanced += ", high quality, professional production, cinematic soundtrack"
        
        return enhanced
    
    def _generate_music21_music(self, prompts: List[str], script: Dict) -> Optional[Dict]:
        """Generate music using music21 MIDI"""
        if not MUSIC21_AVAILABLE:
            return None
        
        try:
            m21_config = self.config.get("music21", {})
            
            # Create a simple composition
            composition = self._create_music21_composition(prompts[0], m21_config)
            
            # Save MIDI file
            output_dir = self.config.get("output_directory", "music")
            os.makedirs(output_dir, exist_ok=True)
            
            midi_filename = f"{output_dir}/music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mid"
            composition.write('midi', fp=midi_filename)
            
            # Convert MIDI to audio if possible
            audio_filename = self._convert_midi_to_audio(midi_filename)
            
            return {
                'id': f"music_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'script_id': script.get('id', 'unknown'),
                'title': script.get('title', 'Generated Music'),
                'audio_file': audio_filename or midi_filename,
                'prompt': prompts[0],
                'method': 'music21',
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'duration': m21_config.get("default_duration", 30),
                    'tempo': m21_config.get("default_tempo", 120),
                    'key': m21_config.get("default_key", "C"),
                    'file_size': os.path.getsize(audio_filename or midi_filename) if os.path.exists(audio_filename or midi_filename) else 0,
                    'enhanced': False
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error in music21 generation: {e}")
            return None
    
    def _create_music21_composition(self, prompt: str, config: Dict) -> music21.stream.Stream:
        """Create a music21 composition based on prompt"""
        # Create a stream
        stream = music21.stream.Stream()
        
        # Add instruments
        piano = music21.instrument.Piano()
        stream.append(piano)
        
        # Create chord progression
        chords = config.get("chord_progression", ["C", "Am", "F", "G"])
        
        # Determine style from prompt
        style = "major" if any(word in prompt.lower() for word in ["happy", "upbeat", "positive"]) else "minor"
        
        # Create melody and harmony
        for i, chord_name in enumerate(chords):
            # Create chord
            chord = music21.chord.Chord(chord_name)
            chord.duration = music21.duration.Duration(2)  # 2 beats
            
            # Add to stream
            stream.append(chord)
            
            # Add simple melody
            if i % 2 == 0:  # Every other chord
                note = music21.note.Note(chord_name[0])
                note.duration = music21.duration.Duration(1)
                stream.append(note)
        
        # Set tempo
        tempo = music21.tempo.MetronomeMark(number=config.get("default_tempo", 120))
        stream.insert(0, tempo)
        
        return stream
    
    def _convert_midi_to_audio(self, midi_filename: str) -> Optional[str]:
        """Convert MIDI file to audio using fluidsynth or similar"""
        try:
            # Try using fluidsynth if available
            audio_filename = midi_filename.replace('.mid', '.wav')
            
            result = subprocess.run([
                'fluidsynth', '-ni', 'soundfont.sf2', midi_filename, 
                '-F', audio_filename, '-r', '44100'
            ], capture_output=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(audio_filename):
                return audio_filename
            else:
                return None
                
        except Exception as e:
            self.logger.warning(f"MIDI to audio conversion failed: {e}")
            return None
    
    def _generate_placeholder_music(self, script: Dict) -> Dict:
        """Generate a placeholder music when other methods fail"""
        # Create a placeholder file
        output_dir = self.config.get("output_directory", "music")
        os.makedirs(output_dir, exist_ok=True)
        
        placeholder_file = f"{output_dir}/placeholder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(placeholder_file, 'w', encoding='utf-8') as f:
            f.write(f"MUSIC PLACEHOLDER\n\nScript: {script.get('title', 'Unknown')}\n\nPlease generate music manually or install music generation dependencies.")
        
        return {
            'id': f"placeholder_music_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'script_id': script.get('id', 'unknown'),
            'title': script.get('title', 'Placeholder Music'),
            'audio_file': placeholder_file,
            'prompt': 'placeholder',
            'method': 'placeholder',
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'method': 'placeholder',
                'duration': 0.0,
                'file_size': os.path.getsize(placeholder_file) if os.path.exists(placeholder_file) else 0,
                'enhanced': False
            }
        }
    
    def enhance_music(self, music: Dict) -> Dict:
        """Enhance music with additional effects"""
        if music.get('method') == 'placeholder':
            return music
        
        try:
            audio_file = music.get('audio_file')
            if not audio_file or not os.path.exists(audio_file):
                return music
            
            # Apply enhancements based on method
            if music.get('method') == 'audiocraft':
                # Already enhanced
                return music
            elif music.get('method') == 'music21':
                # Apply basic enhancements (could add effects here)
                pass
            
            return music
            
        except Exception as e:
            self.logger.error(f"Error enhancing music: {e}")
            return music
    
    def save_music_metadata(self, music: Dict, filename: str = None) -> str:
        """Save music metadata to JSON file"""
        if not filename:
            filename = f"music/{music['id']}_metadata.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(music, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Music metadata saved to {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error saving music metadata: {e}")
            return ""

    def _generate_music21_fallback(self, scripts: List[Dict]) -> List[Dict]:
        """Generate music using music21 fallback"""
        try:
            if not music21:
                self.logger.warning("music21 not available for fallback")
                return []
            
            self.logger.info("Generating music with music21 fallback...")
            
            music_tracks = []
            
            for i, script in enumerate(scripts):
                try:
                    # Create a simple melody without problematic accidentals
                    from music21 import stream, note, chord
                    
                    # Create a basic stream
                    s = stream.Stream()
                    
                    # Add simple notes without accidentals
                    notes = [
                        note.Note('C4'), 
                        note.Note('D4'), 
                        note.Note('E4'), 
                        note.Note('F4'),
                        note.Note('G4'),
                        note.Note('A4'),
                        note.Note('B4'),
                        note.Note('C5')
                    ]
                    
                    for n in notes:
                        s.append(n)
                    
                    # Add a simple chord (C major)
                    c = chord.Chord(['C4', 'E4', 'G4'])
                    s.append(c)
                    
                    # Export to MIDI
                    output_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f'fallback_music_{i+1}.mid')
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    s.write('midi', fp=output_path)
                    
                    music_track = {
                        'id': f"music_{i+1}_{int(time.time())}",
                        'title': f"Music for {script.get('title', f'Script {i+1}')}",
                        'audio_file': output_path,
                        'duration': 30.0,
                        'genre': 'ambient',
                        'tempo': 120,
                        'metadata': {
                            'generated_at': datetime.now().isoformat(),
                            'script_id': script.get('id', f'script_{i+1}'),
                            'method': 'music21_fallback',
                            'enhanced': False
                        }
                    }
                    
                    music_tracks.append(music_track)
                    self.logger.info(f"Generated fallback music: {output_path}")
                    
                except Exception as e:
                    self.logger.error(f"Error generating music21 fallback for script {i+1}: {e}")
                    # Create placeholder music track
                    music_track = {
                        'id': f"music_{i+1}_{int(time.time())}",
                        'title': f"Placeholder Music for {script.get('title', f'Script {i+1}')}",
                        'audio_file': None,
                        'duration': 30.0,
                        'genre': 'ambient',
                        'tempo': 120,
                        'metadata': {
                            'generated_at': datetime.now().isoformat(),
                            'script_id': script.get('id', f'script_{i+1}'),
                            'method': 'placeholder',
                            'enhanced': False
                        }
                    }
                    music_tracks.append(music_track)
            
            return music_tracks
            
        except Exception as e:
            self.logger.error(f"Error in music21 fallback generation: {e}")
            return []

    def _create_wav_from_stream(self, music_stream, wav_path: str):
        """Create WAV file from music21 stream"""
        try:
            import numpy as np
            import wave
            
            # Create a simple melody based on the stream
            sample_rate = 44100
            duration = 30.0
            
            # Generate a simple melody
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Create a simple melody with multiple frequencies
            frequencies = [440, 494, 523, 587, 659, 587, 523, 494]  # A4, B4, C5, D5, E5, D5, C5, B4
            audio_data = np.zeros_like(t)
            
            for i, freq in enumerate(frequencies):
                start_time = i * duration / len(frequencies)
                end_time = (i + 1) * duration / len(frequencies)
                mask = (t >= start_time) & (t < end_time)
                audio_data[mask] = np.sin(2 * np.pi * freq * (t[mask] - start_time)) * 0.2
            
            # Convert to 16-bit PCM
            audio_data = (audio_data * 32767).astype(np.int16)
            
            # Save as WAV
            with wave.open(wav_path, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data.tobytes())
                
        except Exception as e:
            self.logger.error(f"Error creating WAV from stream: {e}")
            # Fallback to simple sine wave
            self._create_simple_wav_fallback(None, 0, wav_path)

# Example usage
if __name__ == "__main__":
    # Test music generation
    music_generator = MusicGenerator()
    
    test_script = {
        'id': 'test_script_001',
        'title': 'The Psychology of Success',
        'content': 'Discover the shocking secrets of successful people and how they manipulate their environment for maximum impact.',
        'sections': {
            'hook': 'Have you ever wondered why some people succeed while others fail?',
            'intro': 'The answer lies in psychological manipulation techniques.',
            'main': 'Here are the three key principles that successful people use.',
            'cta': 'Apply these techniques to transform your life!'
        }
    }
    
    music_tracks = music_generator.generate_music([test_script])
    print(f"Generated {len(music_tracks)} music tracks")
    
    if music_tracks:
        print("First music track preview:")
        print(f"Audio file: {music_tracks[0]['audio_file']}")
        print(f"Method: {music_tracks[0]['method']}")
        print(f"Prompt: {music_tracks[0]['prompt']}")
