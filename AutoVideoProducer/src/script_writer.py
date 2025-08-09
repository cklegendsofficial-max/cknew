#!/usr/bin/env python3
"""
Script Writer Module
Generates video scripts using Ollama with advanced NLP manipulation techniques
"""

import json
import os
import logging
from typing import List, Dict, Optional
from datetime import datetime

# Try to import optional dependencies
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logging.warning("Ollama not available for script generation")

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    logging.warning("Deep translator not available for multi-language support")

class ScriptWriter:
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the script writer with configuration"""
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self.scripts_cache = {}
        self.manipulation_prompts = [
            "Use 25th frame notes, hypnosis NLP, state tactics for addiction",
            "Implement subliminal messaging and psychological triggers",
            "Apply cognitive bias exploitation and emotional manipulation",
            "Use anchoring techniques and social proof elements",
            "Implement scarcity and urgency psychological triggers"
        ]
        
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
            "script_length": "medium",  # short, medium, long
            "target_audience": "general",
            "content_type": "educational",
            "language": "en",
            "manipulation_level": "subtle",  # subtle, moderate, aggressive
            "include_hooks": True,
            "include_call_to_action": True
        }
    
    def generate_scripts(self, ideas: List[Dict]) -> List[Dict]:
        """
        Generate scripts from content ideas using Ollama
        
        Args:
            ideas: List of content ideas from idea generator
            
        Returns:
            List of generated scripts with metadata
        """
        if not ideas:
            self.logger.warning("No ideas provided for script generation")
            return []
        
        scripts = []
        
        for idea in ideas:
            try:
                script = self._generate_single_script(idea)
                if script:
                    scripts.append(script)
            except Exception as e:
                self.logger.error(f"Error generating script for idea {idea.get('title', 'Unknown')}: {e}")
                continue
        
        return scripts
    
    def _generate_single_script(self, idea: Dict) -> Optional[Dict]:
        """Generate a single script from an idea"""
        if not OLLAMA_AVAILABLE:
            return self._generate_fallback_script(idea)
        
        try:
            # Create enhanced prompt with manipulation techniques
            prompt = self._create_enhanced_prompt(idea)
            
            # Generate script using Ollama with better error handling
            try:
                response = ollama.chat(
                    model='llama3',
                    messages=[
                        {
                            'role': 'system',
                            'content': 'You are an expert video script writer specializing in psychological manipulation and engagement techniques.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                )
                
                script_content = response['message']['content']
                
                # Parse and structure the script
                structured_script = self._parse_script_content(script_content, idea)
                
                return structured_script
                
            except Exception as ollama_error:
                self.logger.error(f"Ollama connection error: {ollama_error}")
                # Fallback to local script generation
                return self._generate_fallback_script(idea)
            
        except Exception as e:
            self.logger.error(f"Error in Ollama script generation: {e}")
            return self._generate_fallback_script(idea)
    
    def _create_enhanced_prompt(self, idea: Dict) -> str:
        """Create an enhanced prompt with manipulation techniques"""
        title = idea.get('title', 'Unknown Topic')
        description = idea.get('description', '')
        category = idea.get('category', 'general')
        
        # Get script length with safe fallback
        script_length = self.config.get('script_length', 'medium')
        if script_length not in ['short', 'medium', 'long']:
            script_length = 'medium'  # Safe fallback
        
        # Select manipulation prompt based on content type
        manipulation_prompt = self.manipulation_prompts[hash(title) % len(self.manipulation_prompts)]
        
        prompt = f"""
Create a compelling video script for: "{title}"

Description: {description}
Category: {category}

Requirements:
1. {manipulation_prompt}
2. Use psychological triggers for maximum engagement
3. Include emotional hooks and cognitive biases
4. Implement subliminal messaging techniques
5. Create urgency and scarcity elements
6. Use social proof and authority signals

Script Structure:
- Hook (0-10 seconds): Immediate attention grabber
- Introduction (10-30 seconds): Problem/opportunity presentation
- Main Content (30-90 seconds): Value delivery with manipulation
- Call to Action (90-120 seconds): Clear next steps

Target Length: {script_length} (2-3 minutes)
Language: {self.config.get('language', 'en')}

Generate a script that maximizes viewer retention and psychological impact.
"""
        return prompt
    
    def _parse_script_content(self, content: str, idea: Dict) -> Dict:
        """Parse and structure the generated script content"""
        try:
            # Extract sections from the generated content
            sections = self._extract_sections(content)
            
            # Get config values safely
            script_length = self.config.get('script_length', 'medium')
            language = self.config.get('language', 'en')
            manipulation_level = self.config.get('manipulation_level', 'subtle')
            
            script = {
                'id': f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'title': idea.get('title', 'Generated Script'),
                'original_idea': idea,
                'content': content,
                'sections': sections,
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'length': script_length,
                    'language': language,
                    'manipulation_level': manipulation_level,
                    'word_count': len(content.split()),
                    'estimated_duration': self._estimate_duration(content)
                }
            }
            
            return script
            
        except Exception as e:
            self.logger.error(f"Error parsing script content: {e}")
            return {
                'id': f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'title': idea.get('title', 'Generated Script'),
                'original_idea': idea,
                'content': content,
                'sections': {'hook': '', 'intro': '', 'main': '', 'cta': ''},
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'error': str(e)
                }
            }
    
    def _extract_sections(self, content: str) -> Dict:
        """Extract different sections from the script content"""
        sections = {
            'hook': '',
            'intro': '',
            'main': '',
            'cta': ''
        }
        
        # Simple section extraction based on keywords
        lines = content.split('\n')
        current_section = 'main'
        
        for line in lines:
            line_lower = line.lower().strip()
            
            if any(keyword in line_lower for keyword in ['hook', 'attention', 'grab']):
                current_section = 'hook'
            elif any(keyword in line_lower for keyword in ['intro', 'introduction', 'problem']):
                current_section = 'intro'
            elif any(keyword in line_lower for keyword in ['main', 'content', 'body']):
                current_section = 'main'
            elif any(keyword in line_lower for keyword in ['call', 'action', 'cta', 'subscribe', 'like']):
                current_section = 'cta'
            
            if line.strip():
                sections[current_section] += line + '\n'
        
        return sections
    
    def _estimate_duration(self, content: str) -> int:
        """Estimate video duration in seconds based on content length"""
        words = len(content.split())
        # Average speaking rate: 150 words per minute
        duration_minutes = words / 150
        return int(duration_minutes * 60)
    
    def _generate_fallback_script(self, idea: Dict) -> Dict:
        """Generate a fallback script when Ollama is not available"""
        title = idea.get('title', 'Unknown Topic')
        description = idea.get('description', '')
        
        fallback_content = f"""
HOOK (0-10 seconds):
"Have you ever wondered about {title}? What if I told you everything you know is wrong?"

INTRODUCTION (10-30 seconds):
"Today, we're diving deep into {title}. This is something that will completely change your perspective."

MAIN CONTENT (30-90 seconds):
"{description}

Here's what you need to know:
1. The shocking truth about {title}
2. Why most people get this wrong
3. The secret technique that works every time

This is not just theory - this is proven psychology that works."

CALL TO ACTION (90-120 seconds):
"If you found this valuable, hit that like button and subscribe for more mind-blowing content. The algorithm loves engagement, and your support helps us create more content like this."
"""
        
        return {
            'id': f"fallback_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'title': title,
            'original_idea': idea,
            'content': fallback_content,
            'sections': {
                'hook': 'Have you ever wondered about {title}? What if I told you everything you know is wrong?',
                'intro': f'Today, we\'re diving deep into {title}. This is something that will completely change your perspective.',
                'main': f'{description}\n\nHere\'s what you need to know:\n1. The shocking truth about {title}\n2. Why most people get this wrong\n3. The secret technique that works every time',
                'cta': 'If you found this valuable, hit that like button and subscribe for more mind-blowing content.'
            },
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'method': 'fallback',
                'estimated_duration': 120
            }
        }
    
    def translate_script(self, script: Dict, target_language: str) -> Dict:
        """Translate script to target language"""
        if not TRANSLATOR_AVAILABLE:
            self.logger.warning("Translator not available for script translation")
            return script
        
        try:
            translator = GoogleTranslator(source='auto', target=target_language)
            
            translated_script = script.copy()
            translated_script['content'] = translator.translate(script['content'])
            
            # Translate sections
            for section_key, section_content in script['sections'].items():
                if section_content:
                    translated_script['sections'][section_key] = translator.translate(section_content)
            
            translated_script['metadata']['translated_to'] = target_language
            translated_script['metadata']['translated_at'] = datetime.now().isoformat()
            
            return translated_script
            
        except Exception as e:
            self.logger.error(f"Error translating script: {e}")
            return script
    
    def save_script(self, script: Dict, filename: str = None) -> str:
        """Save script to JSON file"""
        if not filename:
            filename = f"scripts/{script['id']}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(script, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Script saved to {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error saving script: {e}")
            return ""
    
    def load_script(self, filename: str) -> Optional[Dict]:
        """Load script from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading script {filename}: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Test script generation
    script_writer = ScriptWriter()
    
    test_idea = {
        'title': 'The Psychology of Social Media Addiction',
        'description': 'How social media platforms use psychological manipulation to keep users engaged',
        'category': 'psychology'
    }
    
    scripts = script_writer.generate_scripts([test_idea])
    print(f"Generated {len(scripts)} scripts")
    
    if scripts:
        print("First script preview:")
        print(scripts[0]['content'][:200] + "...")
