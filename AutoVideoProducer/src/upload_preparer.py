"""
Upload Preparer Module
Prepares uploads using shutil copy and PyAutoGUI to open folders
"""

import os
import json
import logging
import shutil
from typing import List, Dict, Optional
from datetime import datetime
import subprocess
import tempfile

# Try to import optional dependencies
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logging.warning("PyAutoGUI not available for folder operations")

try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
    logging.warning("Schedule not available for upload scheduling")

class UploadPreparer:
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the upload preparer with configuration"""
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self.upload_cache = {}
        
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
            "upload": {
                "auto_open_folders": True,
                "create_backup": True,
                "organize_by_date": True,
                "add_metadata": True,
                "compress_large_files": True,
                "max_file_size_mb": 100
            },
            "platforms": {
                "youtube": {
                    "upload_folder": "uploads/youtube",
                    "file_formats": ["mp4", "mov"],
                    "max_duration": 43200,  # 12 hours
                    "max_file_size_mb": 128000
                },
                "tiktok": {
                    "upload_folder": "uploads/tiktok",
                    "file_formats": ["mp4"],
                    "max_duration": 600,  # 10 minutes
                    "max_file_size_mb": 287
                },
                "instagram": {
                    "upload_folder": "uploads/instagram",
                    "file_formats": ["mp4"],
                    "max_duration": 60,  # 1 minute
                    "max_file_size_mb": 100
                },
                "facebook": {
                    "upload_folder": "uploads/facebook",
                    "file_formats": ["mp4"],
                    "max_duration": 240,  # 4 minutes
                    "max_file_size_mb": 4096
                }
            },
            "output_directory": "uploads",
            "use_auto_organization": True,
            "enhance_upload_metadata": True
        }
    
    def prepare_uploads(self, videos: List[Dict]) -> List[Dict]:
        """
        Prepare videos for upload to different platforms
        
        Args:
            videos: List of videos from video editor
            
        Returns:
            List of prepared uploads with metadata
        """
        if not videos:
            self.logger.warning("No videos provided for upload preparation")
            return []
        
        uploads = []
        
        for video in videos:
            try:
                upload = self._prepare_single_upload(video)
                if upload:
                    uploads.append(upload)
            except Exception as e:
                self.logger.error(f"Error preparing upload for video {video.get('title', 'Unknown')}: {e}")
                continue
        
        return uploads
    
    def _prepare_single_upload(self, video: Dict) -> Optional[Dict]:
        """Prepare a single video for upload"""
        try:
            # Get video file path
            video_file = video.get('video_file')
            if not video_file or not os.path.exists(video_file):
                self.logger.warning(f"Video file not found: {video_file}")
                return None
            
            # Prepare uploads for different platforms
            platform_uploads = {}
            
            for platform, config in self.config.get("platforms", {}).items():
                platform_upload = self._prepare_platform_upload(video, platform, config)
                if platform_upload:
                    platform_uploads[platform] = platform_upload
            
            if not platform_uploads:
                self.logger.warning("No platform uploads prepared")
                return None
            
            # Create upload result
            upload = {
                'id': f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'video_id': video.get('id', 'unknown'),
                'title': video.get('title', 'Prepared Upload'),
                'original_file': video_file,
                'platform_uploads': platform_uploads,
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'total_platforms': len(platform_uploads),
                    'original_size': os.path.getsize(video_file) if os.path.exists(video_file) else 0,
                    'prepared': True
                }
            }
            
            # Add upload metadata if enabled
            if self.config.get('upload', {}).get('add_metadata', True):
                upload = self._add_upload_metadata(upload, video)
            
            # Auto-open folders if enabled
            if self.config.get('upload', {}).get('auto_open_folders', True):
                self._open_upload_folders(platform_uploads)
            
            return upload
            
        except Exception as e:
            self.logger.error(f"Error in upload preparation: {e}")
            return None
    
    def _prepare_platform_upload(self, video: Dict, platform: str, config: Dict) -> Optional[Dict]:
        """Prepare upload for specific platform"""
        try:
            video_file = video.get('video_file')
            if not video_file or not os.path.exists(video_file):
                return None
            
            # Check platform requirements
            if not self._check_platform_requirements(video, platform, config):
                self.logger.warning(f"Video does not meet {platform} requirements")
                return None
            
            # Create platform upload folder
            upload_folder = config.get('upload_folder', f"uploads/{platform}")
            os.makedirs(upload_folder, exist_ok=True)
            
            # Generate platform-specific filename
            filename = self._generate_platform_filename(video, platform)
            upload_path = os.path.join(upload_folder, filename)
            
            # Copy file to upload location
            shutil.copy2(video_file, upload_path)
            
            # Create backup if enabled
            if self.config.get('upload', {}).get('create_backup', True):
                backup_path = self._create_backup(upload_path, platform)
            else:
                backup_path = None
            
            # Add platform-specific metadata
            platform_metadata = self._generate_platform_metadata(video, platform, config)
            
            return {
                'platform': platform,
                'upload_path': upload_path,
                'backup_path': backup_path,
                'filename': filename,
                'file_size': os.path.getsize(upload_path) if os.path.exists(upload_path) else 0,
                'metadata': platform_metadata,
                'ready_for_upload': True
            }
            
        except Exception as e:
            self.logger.error(f"Error preparing {platform} upload: {e}")
            return None
    
    def _check_platform_requirements(self, video: Dict, platform: str, config: Dict) -> bool:
        """Check if video meets platform requirements"""
        try:
            video_file = video.get('video_file')
            if not video_file or not os.path.exists(video_file):
                return False
            
            # Check file format
            file_extension = os.path.splitext(video_file)[1].lower().lstrip('.')
            allowed_formats = config.get('file_formats', ['mp4'])
            if file_extension not in allowed_formats:
                self.logger.warning(f"File format {file_extension} not allowed for {platform}")
                return False
            
            # Check file size
            file_size_mb = os.path.getsize(video_file) / (1024 * 1024)
            max_size_mb = config.get('max_file_size_mb', 100)
            if file_size_mb > max_size_mb:
                self.logger.warning(f"File size {file_size_mb:.1f}MB exceeds {platform} limit of {max_size_mb}MB")
                return False
            
            # Check duration
            duration = video.get('metadata', {}).get('duration', 0)
            max_duration = config.get('max_duration', 600)
            if duration > max_duration:
                self.logger.warning(f"Duration {duration}s exceeds {platform} limit of {max_duration}s")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking platform requirements: {e}")
            return False
    
    def _generate_platform_filename(self, video: Dict, platform: str) -> str:
        """Generate platform-specific filename"""
        try:
            # Get base filename
            original_file = video.get('video_file', '')
            base_name = os.path.splitext(os.path.basename(original_file))[0]
            
            # Add platform and timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{base_name}_{platform}_{timestamp}.mp4"
            
            return filename
            
        except Exception as e:
            self.logger.error(f"Error generating platform filename: {e}")
            return f"upload_{platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    
    def _create_backup(self, upload_path: str, platform: str) -> Optional[str]:
        """Create backup of upload file"""
        try:
            backup_dir = f"backups/{platform}"
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_filename = f"backup_{os.path.basename(upload_path)}"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            shutil.copy2(upload_path, backup_path)
            
            return backup_path
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            return None
    
    def _generate_platform_metadata(self, video: Dict, platform: str, config: Dict) -> Dict:
        """Generate platform-specific metadata"""
        try:
            metadata = {
                'platform': platform,
                'upload_date': datetime.now().isoformat(),
                'original_video_id': video.get('id', 'unknown'),
                'title': video.get('title', 'Unknown'),
                'duration': video.get('metadata', {}).get('duration', 0),
                'file_size_mb': os.path.getsize(video.get('video_file', '')) / (1024 * 1024) if os.path.exists(video.get('video_file', '')) else 0,
                'platform_requirements': {
                    'max_duration': config.get('max_duration', 600),
                    'max_file_size_mb': config.get('max_file_size_mb', 100),
                    'allowed_formats': config.get('file_formats', ['mp4'])
                }
            }
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error generating platform metadata: {e}")
            return {'platform': platform, 'error': str(e)}
    
    def _add_upload_metadata(self, upload: Dict, video: Dict) -> Dict:
        """Add comprehensive upload metadata"""
        try:
            # Create upload metadata file
            metadata_file = f"uploads/upload_metadata_{upload['id']}.json"
            os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
            
            upload_metadata = {
                'upload_id': upload['id'],
                'video_id': video.get('id', 'unknown'),
                'title': video.get('title', 'Unknown'),
                'upload_date': datetime.now().isoformat(),
                'platforms': list(upload['platform_uploads'].keys()),
                'total_files': len(upload['platform_uploads']),
                'total_size_mb': sum(u.get('file_size', 0) for u in upload['platform_uploads'].values()) / (1024 * 1024),
                'status': 'prepared',
                'notes': self._generate_upload_notes(upload, video)
            }
            
            # Save metadata file
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(upload_metadata, f, indent=2, ensure_ascii=False)
            
            upload['metadata_file'] = metadata_file
            upload['upload_metadata'] = upload_metadata
            
            return upload
            
        except Exception as e:
            self.logger.error(f"Error adding upload metadata: {e}")
            return upload
    
    def _generate_upload_notes(self, upload: Dict, video: Dict) -> List[str]:
        """Generate upload notes and recommendations"""
        try:
            notes = []
            
            # Check file sizes
            for platform, platform_upload in upload['platform_uploads'].items():
                file_size_mb = platform_upload.get('file_size', 0) / (1024 * 1024)
                if file_size_mb > 50:
                    notes.append(f"{platform}: Large file size ({file_size_mb:.1f}MB), consider compression")
            
            # Check duration
            duration = video.get('metadata', {}).get('duration', 0)
            if duration > 300:  # 5 minutes
                notes.append("Long video duration, consider breaking into shorter segments")
            elif duration < 30:
                notes.append("Short video duration, ensure content is engaging")
            
            # Platform-specific recommendations
            platforms = list(upload['platform_uploads'].keys())
            if 'youtube' in platforms:
                notes.append("YouTube: Add end cards and description")
            if 'tiktok' in platforms:
                notes.append("TikTok: Use trending hashtags and sounds")
            if 'instagram' in platforms:
                notes.append("Instagram: Add stories and IGTV version")
            if 'facebook' in platforms:
                notes.append("Facebook: Include captions and call-to-action")
            
            if not notes:
                notes.append("All uploads prepared successfully")
            
            return notes
            
        except Exception as e:
            self.logger.error(f"Error generating upload notes: {e}")
            return ["Unable to generate upload notes"]
    
    def _open_upload_folders(self, platform_uploads: Dict):
        """Open upload folders using PyAutoGUI"""
        if not PYAUTOGUI_AVAILABLE:
            self.logger.warning("PyAutoGUI not available for opening folders")
            return
        
        try:
            for platform, upload_info in platform_uploads.items():
                upload_path = upload_info.get('upload_path')
                if upload_path and os.path.exists(upload_path):
                    folder_path = os.path.dirname(os.path.abspath(upload_path))
                    
                    # Open folder using system command
                    if os.name == 'nt':  # Windows
                        os.startfile(folder_path)
                    elif os.name == 'posix':  # macOS/Linux
                        subprocess.run(['open', folder_path] if os.name == 'darwin' else ['xdg-open', folder_path])
                    
                    self.logger.info(f"Opened upload folder for {platform}: {folder_path}")
                    
        except Exception as e:
            self.logger.error(f"Error opening upload folders: {e}")
    
    def organize_uploads_by_date(self):
        """Organize uploads by date if enabled"""
        if not self.config.get('upload', {}).get('organize_by_date', True):
            return
        
        try:
            upload_dir = self.config.get("output_directory", "uploads")
            if not os.path.exists(upload_dir):
                return
            
            # Create date-based organization
            today = datetime.now().strftime('%Y-%m-%d')
            organized_dir = os.path.join(upload_dir, today)
            os.makedirs(organized_dir, exist_ok=True)
            
            # Move files to organized directory
            for root, dirs, files in os.walk(upload_dir):
                for file in files:
                    if file.endswith(('.mp4', '.mov', '.avi')):
                        file_path = os.path.join(root, file)
                        if os.path.dirname(file_path) != organized_dir:
                            new_path = os.path.join(organized_dir, file)
                            if not os.path.exists(new_path):
                                shutil.move(file_path, new_path)
            
            self.logger.info(f"Organized uploads by date: {organized_dir}")
            
        except Exception as e:
            self.logger.error(f"Error organizing uploads by date: {e}")
    
    def compress_large_files(self):
        """Compress large files if enabled"""
        if not self.config.get('upload', {}).get('compress_large_files', True):
            return
        
        try:
            max_size_mb = self.config.get('upload', {}).get('max_file_size_mb', 100)
            upload_dir = self.config.get("output_directory", "uploads")
            
            if not os.path.exists(upload_dir):
                return
            
            # Find large files
            for root, dirs, files in os.walk(upload_dir):
                for file in files:
                    if file.endswith(('.mp4', '.mov', '.avi')):
                        file_path = os.path.join(root, file)
                        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                        
                        if file_size_mb > max_size_mb:
                            self.logger.info(f"Large file detected: {file} ({file_size_mb:.1f}MB)")
                            # Note: Actual compression would require ffmpeg or similar
                            # For now, just log the large files
                            
        except Exception as e:
            self.logger.error(f"Error compressing large files: {e}")
    
    def create_upload_summary(self, uploads: List[Dict]) -> Dict:
        """Create summary of all uploads"""
        try:
            summary = {
                'id': f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'total_uploads': len(uploads),
                'total_videos': len(set(u.get('video_id', '') for u in uploads)),
                'platforms_used': list(set(platform for u in uploads for platform in u.get('platform_uploads', {}).keys())),
                'total_size_mb': sum(
                    sum(p.get('file_size', 0) for p in u.get('platform_uploads', {}).values()) 
                    for u in uploads
                ) / (1024 * 1024),
                'generated_at': datetime.now().isoformat(),
                'status': 'completed'
            }
            
            # Save summary
            summary_file = f"uploads/upload_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs(os.path.dirname(summary_file), exist_ok=True)
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            summary['summary_file'] = summary_file
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error creating upload summary: {e}")
            return {'error': str(e)}

# Example usage
if __name__ == "__main__":
    # Test upload preparation
    upload_preparer = UploadPreparer()
    
    test_video = {
        'id': 'test_video_001',
        'title': 'Test Video for Upload',
        'video_file': 'videos/test_video.mp4',
        'metadata': {
            'duration': 120.0,
            'width': 1920,
            'height': 1080,
            'fps': 30
        }
    }
    
    uploads = upload_preparer.prepare_uploads([test_video])
    print(f"Prepared {len(uploads)} uploads")
    
    if uploads:
        print("First upload preview:")
        print(f"Video ID: {uploads[0]['video_id']}")
        print(f"Platforms: {list(uploads[0]['platform_uploads'].keys())}")
        print(f"Total platforms: {uploads[0]['metadata']['total_platforms']}")

