"""
Integrator Module
Integrates daily content with threading for continuous production
"""

import os
import json
import logging
import threading
import time
from typing import List, Dict, Optional
from datetime import datetime
import subprocess
import tempfile

# Try to import optional dependencies
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
    logging.warning("Schedule not available for daily integration")

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logging.warning("Ollama not available for integration")

class DailyIntegrator:
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the daily integrator with configuration"""
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self.integration_cache = {}
        self.is_running = False
        self.thread = None
        
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
            "daily": {
                "production_time": "00:00",
                "max_videos_per_day": 5,
                "min_video_duration": 60,
                "max_video_duration": 600,
                "quality_threshold": 0.7
            },
            "threading": {
                "max_workers": 4,
                "timeout": 3600,
                "retry_attempts": 3,
                "retry_delay": 300
            },
            "integration": {
                "combine_videos": True,
                "create_playlist": True,
                "generate_metadata": True,
                "optimize_for_platform": True
            },
            "output_directory": "integrated",
            "use_continuous_production": True,
            "enhance_psychological_impact": True
        }
    
    def integrate_content(self, videos: List[Dict], analysis: List[Dict]) -> Dict:
        """
        Integrate content from videos and analysis
        
        Args:
            videos: List of videos from video editor
            analysis: List of analysis from audience analyzer
            
        Returns:
            Integration result with metadata
        """
        if not videos:
            self.logger.warning("No videos provided for integration")
            return self._create_fallback_integration()
        
        try:
            # Start integration process
            self.logger.info(f"Starting content integration for {len(videos)} videos")
            
            # Create integration result
            integration = {
                'id': f"integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'videos': videos,
                'analysis': analysis,
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'total_videos': len(videos),
                    'total_duration': sum(v.get('metadata', {}).get('duration', 0) for v in videos),
                    'average_quality': self._calculate_average_quality(videos, analysis)
                }
            }
            
            # Perform integration tasks
            integration = self._perform_integration_tasks(integration)
            
            # Add psychological enhancement if enabled
            if self.config.get('enhance_psychological_impact', True):
                integration = self._add_psychological_enhancement(integration)
            
            # Save integration result
            self._save_integration_result(integration)
            
            self.logger.info("Content integration completed successfully")
            return integration
            
        except Exception as e:
            self.logger.error(f"Error in content integration: {e}")
            return self._create_fallback_integration()
    
    def _perform_integration_tasks(self, integration: Dict) -> Dict:
        """Perform various integration tasks"""
        try:
            # Combine videos if enabled
            if self.config.get('integration', {}).get('combine_videos', True):
                integration = self._combine_videos(integration)
            
            # Create playlist if enabled
            if self.config.get('integration', {}).get('create_playlist', True):
                integration = self._create_playlist(integration)
            
            # Generate metadata if enabled
            if self.config.get('integration', {}).get('generate_metadata', True):
                integration = self._generate_metadata(integration)
            
            # Optimize for platform if enabled
            if self.config.get('integration', {}).get('optimize_for_platform', True):
                integration = self._optimize_for_platform(integration)
            
            return integration
            
        except Exception as e:
            self.logger.error(f"Error performing integration tasks: {e}")
            return integration
    
    def _combine_videos(self, integration: Dict) -> Dict:
        """Combine multiple videos into a single production"""
        try:
            videos = integration.get('videos', [])
            if len(videos) <= 1:
                return integration
            
            # Create combined video info
            combined_info = {
                'id': f"combined_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'title': f"Daily Production - {datetime.now().strftime('%Y-%m-%d')}",
                'description': f"Combined daily content with {len(videos)} videos",
                'total_duration': sum(v.get('metadata', {}).get('duration', 0) for v in videos),
                'video_count': len(videos),
                'combined_file': f"integrated/combined_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            }
            
            integration['combined_video'] = combined_info
            
            return integration
            
        except Exception as e:
            self.logger.error(f"Error combining videos: {e}")
            return integration
    
    def _create_playlist(self, integration: Dict) -> Dict:
        """Create playlist from videos"""
        try:
            videos = integration.get('videos', [])
            
            playlist = {
                'id': f"playlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'title': f"Daily Playlist - {datetime.now().strftime('%Y-%m-%d')}",
                'description': f"Daily content playlist with {len(videos)} videos",
                'videos': [v.get('id', 'unknown') for v in videos],
                'playlist_file': f"integrated/playlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            }
            
            # Save playlist file
            os.makedirs(os.path.dirname(playlist['playlist_file']), exist_ok=True)
            with open(playlist['playlist_file'], 'w', encoding='utf-8') as f:
                json.dump(playlist, f, indent=2, ensure_ascii=False)
            
            integration['playlist'] = playlist
            
            return integration
            
        except Exception as e:
            self.logger.error(f"Error creating playlist: {e}")
            return integration
    
    def _generate_metadata(self, integration: Dict) -> Dict:
        """Generate comprehensive metadata for integrated content"""
        try:
            videos = integration.get('videos', [])
            analysis = integration.get('analysis', [])
            
            metadata = {
                'id': f"metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'production_date': datetime.now().isoformat(),
                'total_videos': len(videos),
                'total_duration': sum(v.get('metadata', {}).get('duration', 0) for v in videos),
                'average_engagement': self._calculate_average_engagement(analysis),
                'quality_metrics': self._calculate_quality_metrics(videos, analysis),
                'content_summary': self._generate_content_summary(videos),
                'optimization_recommendations': self._generate_optimization_recommendations(analysis)
            }
            
            # Save metadata file
            metadata_file = f"integrated/metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            integration['metadata_file'] = metadata_file
            integration['detailed_metadata'] = metadata
            
            return integration
            
        except Exception as e:
            self.logger.error(f"Error generating metadata: {e}")
            return integration
    
    def _optimize_for_platform(self, integration: Dict) -> Dict:
        """Optimize content for different platforms"""
        try:
            platforms = ['youtube', 'tiktok', 'instagram', 'facebook']
            optimizations = {}
            
            for platform in platforms:
                platform_optimization = {
                    'platform': platform,
                    'recommended_format': self._get_platform_format(platform),
                    'optimal_duration': self._get_platform_duration(platform),
                    'content_adaptations': self._get_platform_adaptations(platform),
                    'upload_ready': self._check_platform_requirements(platform, integration)
                }
                optimizations[platform] = platform_optimization
            
            integration['platform_optimizations'] = optimizations
            
            return integration
            
        except Exception as e:
            self.logger.error(f"Error optimizing for platform: {e}")
            return integration
    
    def _get_platform_format(self, platform: str) -> str:
        """Get recommended format for platform"""
        formats = {
            'youtube': 'MP4, 1920x1080, H.264',
            'tiktok': 'MP4, 1080x1920, H.264',
            'instagram': 'MP4, 1080x1080, H.264',
            'facebook': 'MP4, 1920x1080, H.264'
        }
        return formats.get(platform, 'MP4, 1920x1080, H.264')
    
    def _get_platform_duration(self, platform: str) -> int:
        """Get optimal duration for platform"""
        durations = {
            'youtube': 600,  # 10 minutes
            'tiktok': 60,    # 1 minute
            'instagram': 60,  # 1 minute
            'facebook': 300   # 5 minutes
        }
        return durations.get(platform, 300)
    
    def _get_platform_adaptations(self, platform: str) -> List[str]:
        """Get content adaptations for platform"""
        adaptations = {
            'youtube': ['Add end cards', 'Include description', 'Use tags'],
            'tiktok': ['Vertical format', 'Add trending sounds', 'Use hashtags'],
            'instagram': ['Square format', 'Add stories', 'Use IGTV'],
            'facebook': ['Add captions', 'Include call-to-action', 'Use groups']
        }
        return adaptations.get(platform, [])
    
    def _check_platform_requirements(self, platform: str, integration: Dict) -> bool:
        """Check if content meets platform requirements"""
        try:
            videos = integration.get('videos', [])
            if not videos:
                return False
            
            # Check basic requirements
            total_duration = sum(v.get('metadata', {}).get('duration', 0) for v in videos)
            optimal_duration = self._get_platform_duration(platform)
            
            # Simple check: duration within reasonable range
            return 0.5 * optimal_duration <= total_duration <= 2 * optimal_duration
            
        except Exception as e:
            self.logger.error(f"Error checking platform requirements: {e}")
            return False
    
    def _add_psychological_enhancement(self, integration: Dict) -> Dict:
        """Add psychological enhancement to integration"""
        try:
            if not OLLAMA_AVAILABLE:
                return integration
            
            # Analyze integration for psychological impact
            prompt = f"""
            Analyze this daily content integration for psychological impact:
            
            Videos: {len(integration.get('videos', []))} videos
            Total Duration: {integration.get('metadata', {}).get('total_duration', 0)} seconds
            Average Quality: {integration.get('metadata', {}).get('average_quality', 0)}
            
            Suggest psychological enhancements:
            1. Content sequencing for maximum impact
            2. Emotional manipulation techniques
            3. Viewer retention strategies
            4. Call-to-action optimization
            
            Return as JSON with recommendations.
            """
            
            response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
            
            # Parse response (simplified)
            psychological_enhancement = {
                'content_sequencing': 'Optimize for emotional progression',
                'emotional_manipulation': 'Use cliffhangers and suspense',
                'retention_strategies': 'Implement psychological hooks',
                'cta_optimization': 'Place calls-to-action at peak moments'
            }
            
            integration['psychological_enhancement'] = psychological_enhancement
            
            return integration
            
        except Exception as e:
            self.logger.error(f"Error adding psychological enhancement: {e}")
            return integration
    
    def _calculate_average_quality(self, videos: List[Dict], analysis: List[Dict]) -> float:
        """Calculate average quality score"""
        try:
            if not analysis:
                return 0.5
            
            quality_scores = []
            for a in analysis:
                predictions = a.get('predictions', {})
                engagement = predictions.get('engagement_score', 0.5)
                retention = predictions.get('retention_score', 0.5)
                conversion = predictions.get('conversion_score', 0.5)
                
                quality_score = (engagement + retention + conversion) / 3
                quality_scores.append(quality_score)
            
            return sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
            
        except Exception as e:
            self.logger.error(f"Error calculating average quality: {e}")
            return 0.5
    
    def _calculate_average_engagement(self, analysis: List[Dict]) -> float:
        """Calculate average engagement score"""
        try:
            if not analysis:
                return 0.5
            
            engagement_scores = []
            for a in analysis:
                predictions = a.get('predictions', {})
                engagement = predictions.get('engagement_score', 0.5)
                engagement_scores.append(engagement)
            
            return sum(engagement_scores) / len(engagement_scores) if engagement_scores else 0.5
            
        except Exception as e:
            self.logger.error(f"Error calculating average engagement: {e}")
            return 0.5
    
    def _calculate_quality_metrics(self, videos: List[Dict], analysis: List[Dict]) -> Dict:
        """Calculate comprehensive quality metrics"""
        try:
            metrics = {
                'total_videos': len(videos),
                'total_duration': sum(v.get('metadata', {}).get('duration', 0) for v in videos),
                'average_engagement': self._calculate_average_engagement(analysis),
                'quality_distribution': {
                    'high_quality': len([a for a in analysis if a.get('predictions', {}).get('engagement_score', 0) > 0.8]),
                    'medium_quality': len([a for a in analysis if 0.5 <= a.get('predictions', {}).get('engagement_score', 0) <= 0.8]),
                    'low_quality': len([a for a in analysis if a.get('predictions', {}).get('engagement_score', 0) < 0.5])
                }
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating quality metrics: {e}")
            return {'total_videos': len(videos), 'total_duration': 0, 'average_engagement': 0.5}
    
    def _generate_content_summary(self, videos: List[Dict]) -> str:
        """Generate content summary"""
        try:
            if not videos:
                return "No videos available for summary"
            
            titles = [v.get('title', 'Unknown') for v in videos]
            total_duration = sum(v.get('metadata', {}).get('duration', 0) for v in videos)
            
            summary = f"Daily production with {len(videos)} videos totaling {total_duration:.1f} seconds. "
            summary += f"Content includes: {', '.join(titles[:3])}"
            if len(titles) > 3:
                summary += f" and {len(titles) - 3} more videos"
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating content summary: {e}")
            return "Content summary unavailable"
    
    def _generate_optimization_recommendations(self, analysis: List[Dict]) -> List[str]:
        """Generate optimization recommendations"""
        try:
            recommendations = []
            
            if not analysis:
                recommendations.append("No analysis data available for recommendations")
                return recommendations
            
            # Analyze engagement scores
            engagement_scores = [a.get('predictions', {}).get('engagement_score', 0.5) for a in analysis]
            avg_engagement = sum(engagement_scores) / len(engagement_scores)
            
            if avg_engagement < 0.6:
                recommendations.append("Increase engagement through better hooks and visual variety")
            
            # Analyze retention scores
            retention_scores = [a.get('predictions', {}).get('retention_score', 0.5) for a in analysis]
            avg_retention = sum(retention_scores) / len(retention_scores)
            
            if avg_retention < 0.7:
                recommendations.append("Improve retention with better pacing and cliffhangers")
            
            # Analyze conversion scores
            conversion_scores = [a.get('predictions', {}).get('conversion_score', 0.5) for a in analysis]
            avg_conversion = sum(conversion_scores) / len(conversion_scores)
            
            if avg_conversion < 0.5:
                recommendations.append("Enhance conversion through stronger calls-to-action")
            
            if not recommendations:
                recommendations.append("Content quality is good, maintain current standards")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating optimization recommendations: {e}")
            return ["Unable to generate recommendations"]
    
    def _save_integration_result(self, integration: Dict):
        """Save integration result to file"""
        try:
            output_dir = self.config.get("output_directory", "integrated")
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"{output_dir}/integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(integration, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Integration result saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving integration result: {e}")
    
    def _create_fallback_integration(self) -> Dict:
        """Create fallback integration when process fails"""
        return {
            'id': f"fallback_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'videos': [],
            'analysis': [],
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'method': 'fallback',
                'total_videos': 0,
                'total_duration': 0,
                'average_quality': 0.0
            },
            'error': 'Integration process failed'
        }
    
    def start_continuous_production(self):
        """Start continuous production loop"""
        if self.is_running:
            self.logger.warning("Continuous production already running")
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._continuous_production_loop)
        self.thread.daemon = True
        self.thread.start()
        
        self.logger.info("Continuous production started")
    
    def stop_continuous_production(self):
        """Stop continuous production loop"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=10)
        
        self.logger.info("Continuous production stopped")
    
    def _continuous_production_loop(self):
        """Continuous production loop"""
        try:
            while self.is_running:
                # Check if it's time for daily production
                current_time = datetime.now().strftime("%H:%M")
                production_time = self.config.get("daily", {}).get("production_time", "00:00")
                
                if current_time == production_time:
                    self.logger.info("Starting daily production")
                    # Trigger daily production (this would call the main production pipeline)
                    # For now, just log the event
                    self.logger.info("Daily production triggered")
                
                # Sleep for 1 minute before next check
                time.sleep(60)
                
        except Exception as e:
            self.logger.error(f"Error in continuous production loop: {e}")
            self.is_running = False

# Example usage
if __name__ == "__main__":
    # Test content integration
    integrator = DailyIntegrator()
    
    test_videos = [
        {
            'id': 'video_001',
            'title': 'Test Video 1',
            'video_file': 'videos/test1.mp4',
            'metadata': {'duration': 120.0}
        },
        {
            'id': 'video_002',
            'title': 'Test Video 2',
            'video_file': 'videos/test2.mp4',
            'metadata': {'duration': 180.0}
        }
    ]
    
    test_analysis = [
        {
            'id': 'analysis_001',
            'predictions': {
                'engagement_score': 0.8,
                'retention_score': 0.7,
                'conversion_score': 0.6
            }
        },
        {
            'id': 'analysis_002',
            'predictions': {
                'engagement_score': 0.7,
                'retention_score': 0.8,
                'conversion_score': 0.5
            }
        }
    ]
    
    integration = integrator.integrate_content(test_videos, test_analysis)
    print("Integration completed:")
    print(f"Total videos: {integration['metadata']['total_videos']}")
    print(f"Total duration: {integration['metadata']['total_duration']} seconds")
    print(f"Average quality: {integration['metadata']['average_quality']}")

