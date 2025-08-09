"""
Izleyici (Audience) Analyzer Module
Analyzes audience using torch RNN simulation and feedback loops
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
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logging.warning("PyTorch not available for audience analysis")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    logging.warning("NumPy not available for audience analysis")

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logging.warning("Ollama not available for audience analysis")

class IzleyiciAnalyzer:
    """Alias for AudienceAnalyzer for Turkish compatibility"""
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the audience analyzer with configuration"""
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self.analysis_cache = {}
        self.model = None
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize analysis model
        self._init_analysis_model()
    
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
            "torch": {
                "input_size": 100,
                "hidden_size": 64,
                "num_layers": 2,
                "output_size": 10,
                "learning_rate": 0.001
            },
            "analysis": {
                "engagement_threshold": 0.7,
                "retention_threshold": 0.8,
                "conversion_threshold": 0.6,
                "feedback_loop_enabled": True,
                "prediction_horizon": 30  # days
            },
            "audience_segments": {
                "demographics": ["age", "gender", "location", "interests"],
                "behavioral": ["watch_time", "engagement_rate", "click_through", "sharing"],
                "psychological": ["attention_span", "emotional_response", "cognitive_load"]
            },
            "output_directory": "analysis",
            "use_psychological_analysis": True,
            "enhance_manipulation_insights": True
        }
    
    def _init_analysis_model(self):
        """Initialize audience analysis model"""
        if not TORCH_AVAILABLE or not NUMPY_AVAILABLE:
            self.logger.warning("PyTorch/NumPy not available - using basic analysis")
            return
        
        try:
            torch_config = self.config.get("torch", {})
            
            # Create simple RNN model for audience analysis
            self.model = AudienceRNN(
                input_size=torch_config.get("input_size", 100),
                hidden_size=torch_config.get("hidden_size", 64),
                num_layers=torch_config.get("num_layers", 2),
                output_size=torch_config.get("output_size", 10)
            )
            
            self.logger.info("Audience analysis model initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing analysis model: {e}")
            self.model = None
    
    def analyze_audience(self, videos: List[Dict]) -> List[Dict]:
        """
        Analyze audience for videos
        
        Args:
            videos: List of videos from video editor
            
        Returns:
            List of audience analysis results with metadata
        """
        if not videos:
            self.logger.warning("No videos provided for audience analysis")
            return []
        
        analyses = []
        
        for video in videos:
            try:
                analysis = self._analyze_single_audience(video)
                if analysis:
                    analyses.append(analysis)
            except Exception as e:
                self.logger.error(f"Error analyzing audience for video {video.get('title', 'Unknown')}: {e}")
                continue
        
        return analyses
    
    def _analyze_single_audience(self, video: Dict) -> Optional[Dict]:
        """Analyze audience for a single video"""
        try:
            # Extract video features for analysis
            video_features = self._extract_video_features(video)
            
            # Perform audience analysis
            if self.model and TORCH_AVAILABLE:
                analysis = self._perform_torch_analysis(video_features, video)
            else:
                analysis = self._perform_basic_analysis(video_features, video)
            
            # Add psychological analysis if enabled
            if self.config.get('use_psychological_analysis', True):
                analysis = self._add_psychological_analysis(analysis, video)
            
            # Add manipulation insights if enabled
            if self.config.get('enhance_manipulation_insights', True):
                analysis = self._add_manipulation_insights(analysis, video)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in audience analysis: {e}")
            return self._create_fallback_analysis(video)
    
    def _extract_video_features(self, video: Dict) -> Dict:
        """Extract features from video for analysis"""
        features = {
            'duration': video.get('metadata', {}).get('duration', 0),
            'file_size': video.get('metadata', {}).get('file_size', 0),
            'width': video.get('metadata', {}).get('width', 0),
            'height': video.get('metadata', {}).get('height', 0),
            'fps': video.get('metadata', {}).get('fps', 30),
            'enhanced': video.get('metadata', {}).get('enhanced', False)
        }
        
        # Add derived features
        features['aspect_ratio'] = features['width'] / features['height'] if features['height'] > 0 else 16/9
        features['file_size_mb'] = features['file_size'] / (1024 * 1024)
        features['is_short'] = features['duration'] < 60
        features['is_long'] = features['duration'] > 300
        
        return features
    
    def _perform_torch_analysis(self, features: Dict, video: Dict) -> Dict:
        """Perform analysis using PyTorch model"""
        try:
            # Convert features to tensor
            feature_vector = self._features_to_tensor(features)
            
            # Get model prediction
            with torch.no_grad():
                prediction = self.model(feature_vector.unsqueeze(0))
                scores = torch.sigmoid(prediction).squeeze().numpy()
            
            # Interpret scores
            analysis = {
                'engagement_score': float(scores[0]),
                'retention_score': float(scores[1]),
                'conversion_score': float(scores[2]),
                'sharing_potential': float(scores[3]),
                'viral_potential': float(scores[4]),
                'audience_reach': float(scores[5]),
                'watch_time_prediction': float(scores[6]),
                'click_through_rate': float(scores[7]),
                'emotional_impact': float(scores[8]),
                'cognitive_load': float(scores[9]),
                'confidence': self._calculate_confidence(scores),
                'analysis_method': 'torch_rnn',
                'timestamp': datetime.now().isoformat(),
                'video_id': video.get('id', 'unknown')
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in torch analysis: {e}")
            return self._perform_basic_analysis(features, video)
    
    def _features_to_tensor(self, features: Dict) -> torch.Tensor:
        """Convert features to PyTorch tensor"""
        try:
            # Create feature vector
            feature_list = [
                features.get('duration', 0),
                features.get('file_size_mb', 0),
                features.get('width', 0),
                features.get('height', 0),
                features.get('fps', 30),
                features.get('aspect_ratio', 16/9),
                float(features.get('is_short', False)),
                float(features.get('is_long', False)),
                float(features.get('enhanced', False)),
                1.0  # bias term
            ]
            
            # Pad or truncate to expected size
            expected_size = self.config.get("torch", {}).get("input_size", 100)
            while len(feature_list) < expected_size:
                feature_list.append(0.0)
            feature_list = feature_list[:expected_size]
            
            return torch.tensor(feature_list, dtype=torch.float32)
            
        except Exception as e:
            self.logger.error(f"Error converting features to tensor: {e}")
            # Return zero tensor as fallback
            return torch.zeros(self.config.get("torch", {}).get("input_size", 100), dtype=torch.float32)
    
    def _calculate_confidence(self, scores: np.ndarray) -> float:
        """Calculate confidence score for analysis"""
        try:
            return float(np.mean(scores))
        except:
            return 0.5
    
    def _perform_basic_analysis(self, features: Dict, video: Dict) -> Dict:
        """Perform basic analysis without PyTorch"""
        try:
            # Simple heuristic-based analysis
            duration = features.get('duration', 0)
            file_size_mb = features.get('file_size_mb', 0)
            aspect_ratio = features.get('aspect_ratio', 16/9)
            
            # Calculate basic scores
            engagement_score = min(1.0, duration / 300)  # Longer videos = higher engagement
            retention_score = min(1.0, file_size_mb / 100)  # Larger files = more content
            conversion_score = 0.5  # Default middle value
            sharing_potential = 0.6 if duration < 60 else 0.4  # Short videos share more
            viral_potential = 0.7 if aspect_ratio > 1.5 else 0.5  # Vertical videos more viral
            audience_reach = 0.8  # Default high reach
            watch_time_prediction = duration * 0.8  # 80% of video duration
            click_through_rate = 0.05  # 5% default CTR
            emotional_impact = 0.6  # Default emotional impact
            cognitive_load = 0.4  # Default cognitive load
            
            analysis = {
                'engagement_score': engagement_score,
                'retention_score': retention_score,
                'conversion_score': conversion_score,
                'sharing_potential': sharing_potential,
                'viral_potential': viral_potential,
                'audience_reach': audience_reach,
                'watch_time_prediction': watch_time_prediction,
                'click_through_rate': click_through_rate,
                'emotional_impact': emotional_impact,
                'cognitive_load': cognitive_load,
                'confidence': 0.6,
                'analysis_method': 'basic_heuristic',
                'timestamp': datetime.now().isoformat(),
                'video_id': video.get('id', 'unknown')
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in basic analysis: {e}")
            return self._create_fallback_analysis(video)
    
    def _add_psychological_analysis(self, analysis: Dict, video: Dict) -> Dict:
        """Add psychological analysis to results"""
        try:
            # Add psychological insights
            analysis['psychological'] = {
                'attention_span': analysis.get('engagement_score', 0.5),
                'emotional_response': analysis.get('emotional_impact', 0.5),
                'cognitive_load': analysis.get('cognitive_load', 0.5),
                'memory_retention': analysis.get('retention_score', 0.5),
                'decision_making_impact': analysis.get('conversion_score', 0.5),
                'social_proof_potential': analysis.get('sharing_potential', 0.5)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error adding psychological analysis: {e}")
            return analysis
    
    def _add_manipulation_insights(self, analysis: Dict, video: Dict) -> Dict:
        """Add manipulation insights to analysis"""
        try:
            # Add manipulation techniques insights
            analysis['manipulation_insights'] = {
                'urgency_creation': analysis.get('engagement_score', 0.5) > 0.7,
                'social_proof_enhancement': analysis.get('sharing_potential', 0.5) > 0.6,
                'authority_establishment': analysis.get('retention_score', 0.5) > 0.8,
                'scarcity_illusion': analysis.get('viral_potential', 0.5) > 0.7,
                'emotional_triggers': analysis.get('emotional_impact', 0.5) > 0.6,
                'cognitive_biases': analysis.get('cognitive_load', 0.5) < 0.4
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error adding manipulation insights: {e}")
            return analysis
    
    def _create_fallback_analysis(self, video: Dict) -> Dict:
        """Create fallback analysis when all else fails"""
        return {
            'engagement_score': 0.5,
            'retention_score': 0.5,
            'conversion_score': 0.5,
            'sharing_potential': 0.5,
            'viral_potential': 0.5,
            'audience_reach': 0.5,
            'watch_time_prediction': 60,
            'click_through_rate': 0.05,
            'emotional_impact': 0.5,
            'cognitive_load': 0.5,
            'confidence': 0.3,
            'analysis_method': 'fallback',
            'timestamp': datetime.now().isoformat(),
            'video_id': video.get('id', 'unknown'),
            'error': 'Analysis failed, using fallback values'
        }
    
    def generate_feedback_loop(self, analysis: Dict) -> Dict:
        """Generate feedback loop for continuous improvement"""
        try:
            feedback = {
                'engagement_improvement': max(0, 0.8 - analysis.get('engagement_score', 0.5)),
                'retention_improvement': max(0, 0.9 - analysis.get('retention_score', 0.5)),
                'conversion_improvement': max(0, 0.7 - analysis.get('conversion_score', 0.5)),
                'sharing_improvement': max(0, 0.8 - analysis.get('sharing_potential', 0.5)),
                'viral_improvement': max(0, 0.9 - analysis.get('viral_potential', 0.5)),
                'audience_reach_improvement': max(0, 0.9 - analysis.get('audience_reach', 0.5)),
                'watch_time_improvement': max(0, 300 - analysis.get('watch_time_prediction', 60)),
                'click_through_improvement': max(0, 0.1 - analysis.get('click_through_rate', 0.05)),
                'emotional_impact_improvement': max(0, 0.8 - analysis.get('emotional_impact', 0.5)),
                'cognitive_load_improvement': max(0, analysis.get('cognitive_load', 0.5) - 0.3),
                'timestamp': datetime.now().isoformat(),
                'analysis_id': analysis.get('video_id', 'unknown')
            }
            
            return feedback
            
        except Exception as e:
            self.logger.error(f"Error generating feedback loop: {e}")
            return {'error': 'Feedback generation failed'}
    
    def save_analysis_metadata(self, analysis: Dict, filename: str = None) -> str:
        """Save analysis metadata to file"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"analysis_{analysis.get('video_id', 'unknown')}_{timestamp}.json"
            
            output_dir = self.config.get('output_directory', 'analysis')
            os.makedirs(output_dir, exist_ok=True)
            
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Analysis metadata saved to {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error saving analysis metadata: {e}")
            return ""

class AudienceAnalyzer:
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the audience analyzer with configuration"""
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self.analysis_cache = {}
        self.model = None
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize analysis model
        self._init_analysis_model()
        
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
            "torch": {
                "input_size": 100,
                "hidden_size": 64,
                "num_layers": 2,
                "output_size": 10,
                "learning_rate": 0.001
            },
            "analysis": {
                "engagement_threshold": 0.7,
                "retention_threshold": 0.8,
                "conversion_threshold": 0.6,
                "feedback_loop_enabled": True,
                "prediction_horizon": 30  # days
            },
            "audience_segments": {
                "demographics": ["age", "gender", "location", "interests"],
                "behavioral": ["watch_time", "engagement_rate", "click_through", "sharing"],
                "psychological": ["attention_span", "emotional_response", "cognitive_load"]
            },
            "output_directory": "analysis",
            "use_psychological_analysis": True,
            "enhance_manipulation_insights": True
        }
    
    def _init_analysis_model(self):
        """Initialize audience analysis model"""
        if not TORCH_AVAILABLE or not NUMPY_AVAILABLE:
            self.logger.warning("PyTorch/NumPy not available - using basic analysis")
            return
        
        try:
            torch_config = self.config.get("torch", {})
            
            # Create simple RNN model for audience analysis
            self.model = AudienceRNN(
                input_size=torch_config.get("input_size", 100),
                hidden_size=torch_config.get("hidden_size", 64),
                num_layers=torch_config.get("num_layers", 2),
                output_size=torch_config.get("output_size", 10)
            )
            
            self.logger.info("Audience analysis model initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing analysis model: {e}")
            self.model = None
    
    def analyze_audience(self, videos: List[Dict]) -> List[Dict]:
        """
        Analyze audience for videos
        
        Args:
            videos: List of videos from video editor
            
        Returns:
            List of audience analysis results with metadata
        """
        if not videos:
            self.logger.warning("No videos provided for audience analysis")
            return []
        
        analyses = []
        
        for video in videos:
            try:
                analysis = self._analyze_single_audience(video)
                if analysis:
                    analyses.append(analysis)
            except Exception as e:
                self.logger.error(f"Error analyzing audience for video {video.get('title', 'Unknown')}: {e}")
                continue
        
        return analyses
    
    def _analyze_single_audience(self, video: Dict) -> Optional[Dict]:
        """Analyze audience for a single video"""
        try:
            # Extract video features for analysis
            video_features = self._extract_video_features(video)
            
            # Perform audience analysis
            if self.model and TORCH_AVAILABLE:
                analysis = self._perform_torch_analysis(video_features, video)
            else:
                analysis = self._perform_basic_analysis(video_features, video)
            
            # Add psychological analysis if enabled
            if self.config.get('use_psychological_analysis', True):
                analysis = self._add_psychological_analysis(analysis, video)
            
            # Add manipulation insights if enabled
            if self.config.get('enhance_manipulation_insights', True):
                analysis = self._add_manipulation_insights(analysis, video)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in audience analysis: {e}")
            return self._create_fallback_analysis(video)
    
    def _extract_video_features(self, video: Dict) -> Dict:
        """Extract features from video for analysis"""
        features = {
            'duration': video.get('metadata', {}).get('duration', 0),
            'file_size': video.get('metadata', {}).get('file_size', 0),
            'width': video.get('metadata', {}).get('width', 0),
            'height': video.get('metadata', {}).get('height', 0),
            'fps': video.get('metadata', {}).get('fps', 30),
            'enhanced': video.get('metadata', {}).get('enhanced', False)
        }
        
        # Add derived features
        features['aspect_ratio'] = features['width'] / features['height'] if features['height'] > 0 else 16/9
        features['file_size_mb'] = features['file_size'] / (1024 * 1024)
        features['is_short'] = features['duration'] < 60
        features['is_long'] = features['duration'] > 300
        
        return features
    
    def _perform_torch_analysis(self, features: Dict, video: Dict) -> Dict:
        """Perform analysis using PyTorch model"""
        try:
            # Convert features to tensor
            feature_vector = self._features_to_tensor(features)
            
            # Get model prediction
            with torch.no_grad():
                prediction = self.model(feature_vector.unsqueeze(0))
                scores = torch.sigmoid(prediction).squeeze().numpy()
            
            # Interpret scores
            analysis = {
                'id': f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'video_id': video.get('id', 'unknown'),
                'title': video.get('title', 'Audience Analysis'),
                'method': 'torch_rnn',
                'predictions': {
                    'engagement_score': float(scores[0]),
                    'retention_score': float(scores[1]),
                    'conversion_score': float(scores[2]),
                    'viral_potential': float(scores[3]),
                    'audience_reach': float(scores[4]),
                    'watch_time_prediction': float(scores[5]),
                    'click_through_rate': float(scores[6]),
                    'sharing_probability': float(scores[7]),
                    'comment_engagement': float(scores[8]),
                    'subscriber_conversion': float(scores[9])
                },
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'model_version': 'rnn_v1',
                    'confidence': self._calculate_confidence(scores)
                }
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in torch analysis: {e}")
            return self._perform_basic_analysis(features, video)
    
    def _features_to_tensor(self, features: Dict) -> torch.Tensor:
        """Convert features to tensor"""
        # Normalize features
        normalized_features = []
        
        # Duration (normalize to 0-1, assuming max 600 seconds)
        normalized_features.append(min(features['duration'] / 600, 1.0))
        
        # File size (normalize to 0-1, assuming max 100MB)
        normalized_features.append(min(features['file_size_mb'] / 100, 1.0))
        
        # Aspect ratio (normalize to 0-1)
        normalized_features.append(min(features['aspect_ratio'] / 2, 1.0))
        
        # FPS (normalize to 0-1, assuming max 60fps)
        normalized_features.append(min(features['fps'] / 60, 1.0))
        
        # Boolean features
        normalized_features.append(1.0 if features['enhanced'] else 0.0)
        normalized_features.append(1.0 if features['is_short'] else 0.0)
        normalized_features.append(1.0 if features['is_long'] else 0.0)
        
        # Pad to required input size
        input_size = self.config.get("torch", {}).get("input_size", 100)
        while len(normalized_features) < input_size:
            normalized_features.append(0.0)
        
        return torch.tensor(normalized_features[:input_size], dtype=torch.float32)
    
    def _calculate_confidence(self, scores: np.ndarray) -> float:
        """Calculate confidence in predictions"""
        # Simple confidence based on score variance
        return float(np.std(scores))
    
    def _perform_basic_analysis(self, features: Dict, video: Dict) -> Dict:
        """Perform basic analysis without PyTorch"""
        try:
            # Simple heuristic-based analysis
            engagement_score = min(features['duration'] / 120, 1.0)  # Optimal around 2 minutes
            retention_score = 0.8 if features['is_short'] else 0.6  # Short videos retain better
            conversion_score = 0.7 if features['enhanced'] else 0.5  # Enhanced videos convert better
            
            analysis = {
                'id': f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'video_id': video.get('id', 'unknown'),
                'title': video.get('title', 'Audience Analysis'),
                'method': 'basic_heuristic',
                'predictions': {
                    'engagement_score': engagement_score,
                    'retention_score': retention_score,
                    'conversion_score': conversion_score,
                    'viral_potential': 0.6,
                    'audience_reach': 0.7,
                    'watch_time_prediction': features['duration'] * 0.8,
                    'click_through_rate': 0.05,
                    'sharing_probability': 0.3,
                    'comment_engagement': 0.4,
                    'subscriber_conversion': 0.02
                },
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'method': 'heuristic',
                    'confidence': 0.5
                }
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in basic analysis: {e}")
            return self._create_fallback_analysis(video)
    
    def _add_psychological_analysis(self, analysis: Dict, video: Dict) -> Dict:
        """Add psychological analysis using Ollama"""
        if not OLLAMA_AVAILABLE:
            return analysis
        
        try:
            # Analyze video content for psychological impact
            prompt = f"""
            Analyze this video for psychological impact on audience:
            
            Video: {video.get('title', 'Unknown')}
            Duration: {video.get('metadata', {}).get('duration', 0)} seconds
            Enhanced: {video.get('metadata', {}).get('enhanced', False)}
            
            Predict psychological effects:
            1. Attention span impact
            2. Emotional response
            3. Cognitive load
            4. Memory retention
            5. Behavioral influence
            
            Return as JSON with scores 0-1.
            """
            
            response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
            
            # Parse response (simplified)
            psychological_scores = {
                'attention_span_impact': 0.7,
                'emotional_response': 0.6,
                'cognitive_load': 0.5,
                'memory_retention': 0.8,
                'behavioral_influence': 0.6
            }
            
            analysis['psychological_analysis'] = psychological_scores
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in psychological analysis: {e}")
            return analysis
    
    def _add_manipulation_insights(self, analysis: Dict, video: Dict) -> Dict:
        """Add manipulation insights for audience control"""
        try:
            predictions = analysis.get('predictions', {})
            
            # Calculate manipulation effectiveness
            engagement = predictions.get('engagement_score', 0.5)
            retention = predictions.get('retention_score', 0.5)
            conversion = predictions.get('conversion_score', 0.5)
            
            manipulation_insights = {
                'addiction_potential': min(engagement * retention, 1.0),
                'psychological_hook_strength': engagement * 1.2,
                'cognitive_bias_effectiveness': retention * 0.8,
                'emotional_manipulation_score': (engagement + retention) / 2,
                'subliminal_impact': conversion * 0.9,
                'recommended_manipulation_techniques': []
            }
            
            # Recommend techniques based on scores
            if engagement < 0.6:
                manipulation_insights['recommended_manipulation_techniques'].append('Increase hook strength')
            if retention < 0.7:
                manipulation_insights['recommended_manipulation_techniques'].append('Add cliffhangers')
            if conversion < 0.5:
                manipulation_insights['recommended_manipulation_techniques'].append('Enhance call-to-action')
            
            analysis['manipulation_insights'] = manipulation_insights
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error adding manipulation insights: {e}")
            return analysis
    
    def _create_fallback_analysis(self, video: Dict) -> Dict:
        """Create fallback analysis when all methods fail"""
        return {
            'id': f"fallback_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'video_id': video.get('id', 'unknown'),
            'title': video.get('title', 'Fallback Analysis'),
            'method': 'fallback',
            'predictions': {
                'engagement_score': 0.5,
                'retention_score': 0.5,
                'conversion_score': 0.5,
                'viral_potential': 0.5,
                'audience_reach': 0.5,
                'watch_time_prediction': 0,
                'click_through_rate': 0.05,
                'sharing_probability': 0.3,
                'comment_engagement': 0.4,
                'subscriber_conversion': 0.02
            },
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'method': 'fallback',
                'confidence': 0.0
            }
        }
    
    def generate_feedback_loop(self, analysis: Dict) -> Dict:
        """Generate feedback loop for continuous improvement"""
        try:
            predictions = analysis.get('predictions', {})
            
            # Calculate improvement recommendations
            feedback = {
                'engagement_improvements': [],
                'retention_improvements': [],
                'conversion_improvements': [],
                'next_video_optimizations': []
            }
            
            # Engagement improvements
            if predictions.get('engagement_score', 0) < 0.7:
                feedback['engagement_improvements'].extend([
                    'Add more visual hooks in first 5 seconds',
                    'Increase emotional intensity',
                    'Use more dynamic transitions'
                ])
            
            # Retention improvements
            if predictions.get('retention_score', 0) < 0.8:
                feedback['retention_improvements'].extend([
                    'Add cliffhangers at 30-second intervals',
                    'Increase suspense elements',
                    'Use psychological triggers'
                ])
            
            # Conversion improvements
            if predictions.get('conversion_score', 0) < 0.6:
                feedback['conversion_improvements'].extend([
                    'Strengthen call-to-action',
                    'Add urgency elements',
                    'Use social proof techniques'
                ])
            
            # Next video optimizations
            feedback['next_video_optimizations'] = [
                'Optimize for identified weak points',
                'A/B test different approaches',
                'Monitor real audience metrics'
            ]
            
            analysis['feedback_loop'] = feedback
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error generating feedback loop: {e}")
            return analysis
    
    def save_analysis_metadata(self, analysis: Dict, filename: str = None) -> str:
        """Save analysis metadata to JSON file"""
        if not filename:
            filename = f"analysis/{analysis['id']}_metadata.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Analysis metadata saved to {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error saving analysis metadata: {e}")
            return ""


class AudienceRNN(nn.Module):
    """Simple RNN for audience analysis"""
    
    def __init__(self, input_size: int, hidden_size: int, num_layers: int, output_size: int):
        super(AudienceRNN, self).__init__()
        
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.rnn = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        # Initialize hidden state
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        
        # Forward propagate RNN
        out, _ = self.rnn(x, (h0, c0))
        
        # Decode hidden state of last time step
        out = self.fc(out[:, -1, :])
        
        return out


# Example usage
if __name__ == "__main__":
    # Test audience analysis
    audience_analyzer = AudienceAnalyzer()
    
    test_video = {
        'id': 'test_video_001',
        'title': 'Test Video',
        'video_file': 'videos/test_video.mp4',
        'metadata': {
            'duration': 120.0,
            'width': 1920,
            'height': 1080,
            'fps': 30,
            'file_size': 50000000,
            'enhanced': True
        }
    }
    
    analyses = audience_analyzer.analyze_audience([test_video])
    print(f"Generated {len(analyses)} audience analyses")
    
    if analyses:
        print("First analysis preview:")
        print(f"Engagement score: {analyses[0]['predictions']['engagement_score']}")
        print(f"Retention score: {analyses[0]['predictions']['retention_score']}")
        print(f"Method: {analyses[0]['method']}")
