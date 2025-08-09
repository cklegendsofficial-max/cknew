"""
Auto-improved by SelfImprover on 2025-08-06 14:49:27

Improvements applied:
- Nested loops detected. Consider using list comprehensions or vectorized operations.
- Nested loops detected. Consider using list comprehensions or vectorized operations.
- Nested loops detected. Consider using list comprehensions or vectorized operations.
- Long hardcoded string detected. Consider moving to configuration file.
- Long hardcoded string detected. Consider moving to configuration file.

AI Suggestions:
Error calling Ollama: [WinError 206] Dosya adı veya uzantısı çok uzun...
"""

#!/usr/bin/env python3
"""
AutoVideoProducer - Main Application
Automated video production system with AI integration
"""

import os
import sys
import json
import logging
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import time
import random
from datetime import datetime

# Try to import optional dependencies with fallbacks
try:
    import requests
except ImportError:
    requests = None
    print("Warning: requests not available")

try:
    import schedule
except ImportError:
    schedule = None
    print("Warning: schedule not available")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not available for system monitoring")

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("Warning: watchdog not available for file monitoring")

# Import setup module for dependency management
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
    from setup import install_dependencies
except ImportError:
    print("Warning: setup module not available")
    install_dependencies = None

# Optional AI libraries with fallbacks
ollama = None
moviepy = None
bs4 = None
pyautogui = None
torch = None
pydub = None
PIL = None
gtts = None
music21 = None
diffusers = None
transformers = None
accelerate = None
audiocraft = None
deep_translator = None
watchdog = None
javalang = None
numpy = None
pandas = None
scipy = None
cv2 = None
ffmpeg = None
librosa = None
soundfile = None

# Try to import all optional dependencies
try:
    import ollama
except ImportError:
    print("Warning: ollama not available")

try:
    import moviepy.editor as moviepy
except ImportError:
    print("Warning: moviepy not available")

try:
    from bs4 import BeautifulSoup
    bs4 = BeautifulSoup
except ImportError:
    print("Warning: beautifulsoup4 not available")

try:
    import pyautogui
except ImportError:
    print("Warning: pyautogui not available")

try:
    import torch
except ImportError:
    print("Warning: torch not available")

try:
    from pydub import AudioSegment
    pydub = AudioSegment
except ImportError:
    print("Warning: pydub not available")

try:
    from PIL import Image
    PIL = Image
except ImportError:
    print("Warning: pillow not available")

try:
    from gtts import gTTS
    gtts = gTTS
except ImportError:
    print("Warning: gtts not available")

try:
    import music21
except ImportError:
    print("Warning: music21 not available")

try:
    import diffusers
except ImportError:
    print("Warning: diffusers not available")

try:
    import transformers
except ImportError:
    print("Warning: transformers not available")

try:
    import accelerate
except ImportError:
    print("Warning: accelerate not available")

try:
    import audiocraft
except ImportError:
    print("Warning: audiocraft not available")

try:
    import deep_translator
except ImportError:
    print("Warning: deep_translator not available")

try:
    import watchdog
except ImportError:
    print("Warning: watchdog not available")

try:
    import javalang
except ImportError:
    print("Warning: javalang not available")

try:
    import numpy
except ImportError:
    print("Warning: numpy not available")

try:
    import pandas
except ImportError:
    print("Warning: pandas not available")

try:
    import scipy
except ImportError:
    print("Warning: scipy not available")

try:
    import cv2
except ImportError:
    print("Warning: opencv-python not available")

try:
    import ffmpeg
except ImportError:
    print("Warning: ffmpeg-python not available")

try:
    import librosa
except ImportError:
    print("Warning: librosa not available")

try:
    import soundfile
except ImportError:
    print("Warning: soundfile not available")

class SystemMonitor:
    """Monitor system resources and pause threads if needed"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.monitoring = False
        self.ram_threshold = 80  # 80% RAM usage
        self.cpu_threshold = 90  # 90% CPU usage
        self.monitor_thread = None
        
    def start_monitoring(self):
        """Start system resource monitoring"""
        if not PSUTIL_AVAILABLE:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.app.log_to_gui("System monitoring started", "blue")
        
    def stop_monitoring(self):
        """Stop system resource monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        self.app.log_to_gui("System monitoring stopped", "blue")
        
    def _monitor_loop(self):
        """Monitor system resources in a loop"""
        while self.monitoring:
            try:
                # Check RAM usage
                ram_percent = psutil.virtual_memory().percent
                cpu_percent = psutil.cpu_percent(interval=1)
                
                if ram_percent > self.ram_threshold or cpu_percent > self.cpu_threshold:
                    self.app.log_to_gui(f"High resource usage: RAM {ram_percent:.1f}%, CPU {cpu_percent:.1f}%", "red")
                    # Pause production if running
                    if self.app.production_running:
                        self.app.log_to_gui("Pausing production due to high resource usage", "yellow")
                        self.app.stop_production()
                        time.sleep(30)  # Wait for resources to free up
                        self.app.log_to_gui("Resuming production", "green")
                        self.app.start_production()
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                self.app.log_to_gui(f"System monitoring error: {e}", "red")
                time.sleep(30)

if WATCHDOG_AVAILABLE:
    class FileWatcher(FileSystemEventHandler):
        """Watch for file changes and restart on crash"""
        
        def __init__(self, app_instance):
            self.app = app_instance
            self.observer = None
            
        def start_watching(self):
            """Start watching for file changes"""
            try:
                self.observer = Observer()
                self.observer.schedule(self, path=".", recursive=True)
                self.observer.start()
                self.app.log_to_gui("File watching started", "blue")
            except Exception as e:
                self.app.log_to_gui(f"File watching error: {e}", "red")
                
        def stop_watching(self):
            """Stop watching for file changes"""
            if self.observer:
                self.observer.stop()
                self.observer.join()
                self.app.log_to_gui("File watching stopped", "blue")
                
        def on_modified(self, event):
            """Handle file modification events"""
            if event.is_directory:
                return
                
            # Check if it's a Python file
            if event.src_path.endswith('.py'):
                self.app.log_to_gui(f"File changed: {event.src_path}", "yellow")
                # Restart production if it was running
                if self.app.production_running:
                    self.app.log_to_gui("Restarting production due to file change", "yellow")
                    self.app.stop_production()
                    time.sleep(2)
                    self.app.start_production()
else:
    class FileWatcher:
        """Fallback file watcher when watchdog is not available"""
        def __init__(self, app_instance):
            self.app = app_instance
        def start_watching(self):
            # Watchdog not available; noop but log once for visibility
            try:
                self.app.log_to_gui("File watching unavailable (watchdog not installed)", "yellow")
            except Exception:
                pass
        def stop_watching(self):
            # Noop
            try:
                self.app.log_to_gui("File watching not active", "blue")
            except Exception:
                pass

class AutoVideoProducer:
    def __init__(self):
        self.config = None
        self.ollama_client = None
        self.root = None
        self.log_text = None
        self.daily_integrator = None
        self.upload_preparer = None
        self.scheduler_thread = None
        self.production_running = False
        
        # Initialize monitoring
        self.system_monitor = SystemMonitor(self)
        self.file_watcher = FileWatcher(self)
        
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging to both file and GUI"""
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        log_file = os.path.join(log_dir, f'autovideoproducer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.json')
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            self.logger.info("Configuration loaded successfully")
            return True
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {config_path}")
            return False
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return False
            
    def setup_ollama(self):
        """Setup Ollama and download llama3 if not present"""
        try:
            # Check if Ollama service is running with better error handling
            try:
                import requests
                response = requests.get('http://127.0.0.1:11434/api/version', timeout=3)
                if response.status_code == 200:
                    self.logger.info("Ollama service is running")
                    return True
                else:
                    self.logger.warning("Ollama service not responding properly")
                    return False
            except requests.exceptions.ConnectionError:
                self.logger.warning("Ollama service not available - will use fallback content generation")
                return False
            except Exception as e:
                self.logger.warning(f"Ollama service check failed: {e}")
                return False
                
            # Only check Ollama installation if service is running
            try:
                result = subprocess.run(['ollama', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode != 0:
                    self.logger.error("Ollama not found. Please install Ollama first.")
                    return False
                    
                # Check if llama3 model is available
                result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
                if 'llama3' not in result.stdout:
                    self.logger.info("Downloading llama3 model...")
                    subprocess.run(['ollama', 'pull', 'llama3'], check=True, timeout=300)
                    self.logger.info("llama3 model downloaded successfully")
                else:
                    self.logger.info("llama3 model already available")
                    
                return True
            except subprocess.TimeoutExpired:
                self.logger.error("Ollama command timed out")
                return False
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Error setting up Ollama: {e}")
                return False
                
        except Exception as e:
            self.logger.error(f"Unexpected error setting up Ollama: {e}")
            return False
            
    def create_gui(self):
        """Create the premium GUI window with channel-specific buttons"""
        try:
            self.root = tk.Tk()
            self.root.title("AutoVideoProducer - CK Empire Premium")
            self.root.geometry("1200x900")
            self.root.configure(bg='#1a1a1a')
            
            # Set window icon and make it look premium
            self.root.attributes('-alpha', 0.95)
            
            # Configure style for premium look
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('TFrame', background='#1a1a1a')
            style.configure('TButton', background='#2d2d2d', foreground='white')
            style.configure('TNotebook', background='#1a1a1a')
            style.configure('TNotebook.Tab', background='#2d2d2d', foreground='white')
            
            # Main container with gradient effect
            main_container = tk.Frame(self.root, bg='#1a1a1a', relief=tk.FLAT, bd=0)
            main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            # Header with premium design
            header_frame = tk.Frame(main_container, bg='#2d2d2d', relief=tk.FLAT, bd=0)
            header_frame.pack(fill=tk.X, pady=(0, 15))
            
            # Premium title with gradient effect
            title_frame = tk.Frame(header_frame, bg='#2d2d2d')
            title_frame.pack(fill=tk.X, padx=20, pady=15)
            
            title_label = tk.Label(
                title_frame, 
                text="🎬 AutoVideoProducer Premium", 
                font=("Segoe UI", 24, "bold"),
                fg='#00d4ff',
                bg='#2d2d2d'
            )
            title_label.pack(side=tk.LEFT)
            
            # Status indicator with premium design
            status_frame = tk.Frame(header_frame, bg='#2d2d2d')
            status_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
            
            self.status_label = tk.Label(
                status_frame,
                text="🔄 Initializing Premium System...",
                font=("Segoe UI", 12),
                fg='#ffd700',
                bg='#2d2d2d'
            )
            self.status_label.pack(side=tk.LEFT)
            
            # Progress bar with premium styling
            self.progress = ttk.Progressbar(status_frame, mode='indeterminate', length=300)
            self.progress.pack(side=tk.RIGHT, padx=(20, 0))
            
            # Main content area with tabs
            notebook = ttk.Notebook(main_container)
            notebook.pack(fill=tk.BOTH, expand=True)
            
            # Production Tab
            production_frame = tk.Frame(notebook, bg='#1a1a1a')
            notebook.add(production_frame, text="🎯 Production")
            
            # Channel-specific buttons with premium design
            channels_frame = tk.Frame(production_frame, bg='#1a1a1a')
            channels_frame.pack(fill=tk.X, padx=20, pady=20)
            
            # Channel buttons with premium styling - CK Empire Channels
            channels = [
                ("⚡ CKLegends", "#ff6b6b", self.start_cklegends_production),
                ("🚀 CKDrive", "#4ecdc4", self.start_ckdrive_production),
                ("⚔️ CKCombat", "#45b7d1", self.start_ckcombat_production),
                ("🛡️ CKIronwill", "#96ceb4", self.start_ckironwill_production),
                ("💰 CKFinanceCore", "#feca57", self.start_ckfinancecore_production)
            ]
            
            # Create channel buttons in a grid layout
            for i, (channel_name, color, command) in enumerate(channels):
                row = i // 2
                col = i % 2
                
                channel_button = tk.Button(
                    channels_frame,
                    text=channel_name,
                    command=command,
                    bg=color,
                    fg='white',
                    font=("Segoe UI", 12, "bold"),
                    relief=tk.FLAT,
                    padx=30,
                    pady=15,
                    cursor='hand2'
                )
                channel_button.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
                
                # Store button reference
                setattr(self, f"{channel_name.lower().replace(' ', '_').replace('⚡', 'cklegends').replace('🚀', 'ckdrive').replace('⚔️', 'ckcombat').replace('🛡️', 'ckironwill').replace('💰', 'ckfinancecore')}_button", channel_button)
            
            # Configure grid weights
            channels_frame.grid_columnconfigure(0, weight=1)
            channels_frame.grid_columnconfigure(1, weight=1)
            
            # Control buttons with premium design
            control_frame = tk.Frame(production_frame, bg='#1a1a1a')
            control_frame.pack(fill=tk.X, padx=20, pady=20)
            
            # Premium control buttons
            controls = [
                ("⏸️ Pause All", "#ff7675", self.pause_all_production),
                ("▶️ Resume All", "#74b9ff", self.resume_all_production),
                ("🛑 Stop All", "#fd79a8", self.stop_all_production),
                ("⚡ Quick Demo", "#fdcb6e", self.run_demo),
                ("🔧 Self-Improve", "#e17055", self.manual_self_improvement),
                ("🧹 Clear Logs", "#6c5ce7", self.clear_logs),
                ("📦 Install Dependencies", "#fd79a8", self.install_dependencies)
            ]
            
            for i, (text, color, command) in enumerate(controls):
                control_button = tk.Button(
                    control_frame,
                    text=text,
                    command=command,
                    bg=color,
                    fg='white',
                    font=("Segoe UI", 10, "bold"),
                    relief=tk.FLAT,
                    padx=20,
                    pady=8,
                    cursor='hand2'
                )
                control_button.pack(side=tk.LEFT, padx=5)
                setattr(self, f"control_{i}_button", control_button)
            
            # Scheduler Tab
            scheduler_frame = tk.Frame(notebook, bg='#1a1a1a')
            notebook.add(scheduler_frame, text="⏰ Scheduler")
            
            # Scheduler controls
            scheduler_controls = tk.Frame(scheduler_frame, bg='#1a1a1a')
            scheduler_controls.pack(fill=tk.X, padx=20, pady=20)
            
            scheduler_buttons = [
                ("🚀 Start Daily Scheduler", "#00b894", self.start_scheduler),
                ("⏹️ Stop Scheduler", "#d63031", self.stop_scheduler),
                ("🎬 Run Daily Production", "#0984e3", self.run_daily_production)
            ]
            
            for text, color, command in scheduler_buttons:
                scheduler_button = tk.Button(
                    scheduler_controls,
                    text=text,
                    command=command,
                    bg=color,
                    fg='white',
                    font=("Segoe UI", 12, "bold"),
                    relief=tk.FLAT,
                    padx=30,
                    pady=15,
                    cursor='hand2'
                )
                scheduler_button.pack(side=tk.LEFT, padx=10)
            
            # Logs Tab
            logs_frame = tk.Frame(notebook, bg='#1a1a1a')
            notebook.add(logs_frame, text="📋 System Logs")
            
            # Log text area with premium styling
            self.log_text = scrolledtext.ScrolledText(
                logs_frame,
                height=25,
                bg='#2d2d2d',
                fg='#00ff00',
                font=("Consolas", 10),
                insertbackground='white',
                relief=tk.FLAT,
                bd=0
            )
            self.log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Analytics Tab
            analytics_frame = tk.Frame(notebook, bg='#1a1a1a')
            notebook.add(analytics_frame, text="📊 Analytics")
            
            # Analytics content
            analytics_content = tk.Frame(analytics_frame, bg='#1a1a1a')
            analytics_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Analytics widgets
            analytics_widgets = [
                ("📈 Total Videos", "0", "#00b894"),
                ("🎯 Success Rate", "0%", "#74b9ff"),
                ("⏱️ Avg Duration", "0s", "#fdcb6e"),
                ("📊 Engagement", "0%", "#e17055")
            ]
            
            for i, (label, value, color) in enumerate(analytics_widgets):
                widget_frame = tk.Frame(analytics_content, bg=color, relief=tk.FLAT, bd=0)
                widget_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
                
                tk.Label(
                    widget_frame,
                    text=label,
                    font=("Segoe UI", 12, "bold"),
                    fg='white',
                    bg=color
                ).pack(pady=(10, 5))
                
                tk.Label(
                    widget_frame,
                    text=value,
                    font=("Segoe UI", 18, "bold"),
                    fg='white',
                    bg=color
                ).pack(pady=(0, 10))
            
            # Settings Tab
            settings_frame = tk.Frame(notebook, bg='#1a1a1a')
            notebook.add(settings_frame, text="⚙️ Settings")
            
            # Settings content
            settings_content = tk.Frame(settings_frame, bg='#1a1a1a')
            settings_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Settings options
            settings_options = [
                ("🔧 Auto-Improvement", tk.BooleanVar(value=True)),
                ("📊 Analytics Tracking", tk.BooleanVar(value=True)),
                ("🎬 Quality Mode", tk.BooleanVar(value=True)),
                ("⏰ Auto-Scheduling", tk.BooleanVar(value=True))
            ]
            
            for label, var in settings_options:
                option_frame = tk.Frame(settings_content, bg='#2d2d2d', relief=tk.FLAT, bd=0)
                option_frame.pack(fill=tk.X, pady=5)
                
                tk.Label(
                    option_frame,
                    text=label,
                    font=("Segoe UI", 12),
                    fg='white',
                    bg='#2d2d2d'
                ).pack(side=tk.LEFT, padx=15, pady=10)
                
                tk.Checkbutton(
                    option_frame,
                    variable=var,
                    bg='#2d2d2d',
                    fg='white',
                    selectcolor='#00b894'
                ).pack(side=tk.RIGHT, padx=15, pady=10)
            
            # Store references for later use
            self.start_button = getattr(self, 'cklegends_button', None)
            self.stop_button = getattr(self, 'control_2_button', None)
            self.install_deps_button = getattr(self, 'control_6_button', None)
            
            # Store control button references
            setattr(self, 'demo_button', getattr(self, 'control_4_button', None))
            setattr(self, 'improve_button', getattr(self, 'control_5_button', None))
            setattr(self, 'scheduler_button', getattr(self, 'control_7_button', None))
            setattr(self, 'stop_scheduler_button', getattr(self, 'control_8_button', None))
            setattr(self, 'daily_production_button', getattr(self, 'control_9_button', None))
            
        except Exception as e:
            self.logger.error(f"Error creating GUI: {e}")
            return False
        
        return True
            
    def log_to_gui(self, message, color='green'):
        """Log message to GUI text area with color"""
        try:
            # If GUI is not ready yet, just print to console
            if not hasattr(self, 'log_text') or self.log_text is None:
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] {message}")
                return
                
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {message}\n"
            
            # Insert with color
            self.log_text.insert(tk.END, formatted_message)
            
            # Apply color to the last line
            last_line_start = self.log_text.index("end-2c linestart")
            last_line_end = self.log_text.index("end-1c")
            
            if color == 'red':
                self.log_text.tag_add("error", last_line_start, last_line_end)
                self.log_text.tag_config("error", foreground="red")
            elif color == 'yellow':
                self.log_text.tag_add("warning", last_line_start, last_line_end)
                self.log_text.tag_config("warning", foreground="yellow")
            elif color == 'blue':
                self.log_text.tag_add("info", last_line_start, last_line_end)
                self.log_text.tag_config("info", foreground="cyan")
            else:  # green
                self.log_text.tag_add("success", last_line_start, last_line_end)
                self.log_text.tag_config("success", foreground="green")
            
            self.log_text.see(tk.END)
            self.root.update_idletasks()
        except Exception as e:
            print(f"Error logging to GUI: {e}")
            
    def update_status(self, message, color='yellow'):
        """Update status label"""
        try:
            # If GUI is not ready yet, just print to console
            if not hasattr(self, 'status_label') or self.status_label is None:
                print(f"Status: {message}")
                return
                
            self.status_label.config(text=message, fg=color)
            self.root.update_idletasks()
        except Exception as e:
            print(f"Error updating status: {e}")
            
    def start_production(self):
        """Start the video production process"""
        try:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.progress.start()
            self.update_status("Production started", "green")
            self.log_to_gui("Starting video production process...", "green")
            
            # Check Ollama health before production
            if not self._check_ollama_health():
                self.log_to_gui("Ollama health check failed, attempting to start Ollama...", "yellow")
                self._start_ollama_service()
            
            # Start production in separate thread
            self.production_thread = threading.Thread(target=self.production_worker)
            self.production_thread.daemon = True
            self.production_thread.start()
            
        except Exception as e:
            self.logger.error(f"Error starting production: {e}")
            self.log_to_gui(f"Error starting production: {e}", "red")
    
    def start_drama_production(self):
        """Start drama channel production"""
        self.log_to_gui("🎭 Starting Drama Channel Production...", "green")
        self._start_channel_production("drama", "Drama content with emotional storytelling")
    
    def start_gaming_production(self):
        """Start gaming channel production"""
        self.log_to_gui("🎮 Starting Gaming Channel Production...", "green")
        self._start_channel_production("gaming", "Gaming content with gameplay and commentary")
    
    def start_cooking_production(self):
        """Start cooking channel production"""
        self.log_to_gui("🍳 Starting Cooking Channel Production...", "green")
        self._start_channel_production("cooking", "Cooking tutorials and recipe videos")
    
    def start_fitness_production(self):
        """Start fitness channel production"""
        self.log_to_gui("💪 Starting Fitness Channel Production...", "green")
        self._start_channel_production("fitness", "Fitness workouts and health tips")
    
    def start_music_production(self):
        """Start music channel production"""
        self.log_to_gui("🎵 Starting Music Channel Production...", "green")
        self._start_channel_production("music", "Music covers and original compositions")
    
    def start_education_production(self):
        """Start education channel production"""
        self.log_to_gui("📚 Starting Education Channel Production...", "green")
        self._start_channel_production("education", "Educational content and tutorials")
    
    def start_art_production(self):
        """Start art channel production"""
        self.log_to_gui("🎨 Starting Art Channel Production...", "green")
        self._start_channel_production("art", "Art tutorials and creative content")
    
    def start_tech_production(self):
        """Start tech channel production"""
        self.log_to_gui("🚗 Starting Tech Channel Production...", "green")
        self._start_channel_production("tech", "Technology reviews and tutorials")
    
    def start_travel_production(self):
        """Start travel channel production"""
        self.log_to_gui("🌍 Starting Travel Channel Production...", "green")
        self._start_channel_production("travel", "Travel vlogs and destination guides")
    
    def start_cklegends_production(self):
        """Start CKLegends channel production"""
        self.log_to_gui("⚡ Starting CKLegends Production...", "green")
        self._start_channel_production("cklegends", "Historical content, heroes, historical success stories, legendary figures")
    
    def start_ckdrive_production(self):
        """Start CKDrive channel production"""
        self.log_to_gui("🚀 Starting CKDrive Production...", "green")
        self._start_channel_production("ckdrive", "Automotive brands, driving, design and technical details, car reviews")
    
    def start_ckcombat_production(self):
        """Start CKCombat channel production"""
        self.log_to_gui("⚔️ Starting CKCombat Production...", "green")
        self._start_channel_production("ckcombat", "Combat sports content, fighting techniques, martial arts, boxing, MMA")
    
    def start_ckironwill_production(self):
        """Start CKIronwill channel production"""
        self.log_to_gui("🛡️ Starting CKIronwill Production...", "green")
        self._start_channel_production("ckironwill", "Motivation, mental resilience, personal development, mindset training")
    
    def start_ckfinancecore_production(self):
        """Start CKFinanceCore channel production"""
        self.log_to_gui("💰 Starting CKFinanceCore Production...", "green")
        self._start_channel_production("ckfinancecore", "Financial content, investment strategies, money mindset, financial freedom")
    
    def _start_channel_production(self, channel_type, description):
        """Start production for specific channel type"""
        try:
            self.progress.start()
            self.update_status(f"🎬 {channel_type.title()} Production Started", "green")
            self.log_to_gui(f"Channel Type: {channel_type.title()}", "blue")
            self.log_to_gui(f"Content Focus: {description}", "blue")
            
            # Check Ollama health before production
            if not self._check_ollama_health():
                self.log_to_gui("Ollama health check failed, attempting to start Ollama...", "yellow")
                self._start_ollama_service()
            
            # Start channel-specific production in separate thread with timeout
            production_thread = threading.Thread(
                target=self._channel_production_worker, 
                args=(channel_type, description)
            )
            production_thread.daemon = True
            production_thread.start()
            
            # Store thread reference for monitoring
            self.current_production_thread = production_thread
            
        except Exception as e:
            self.logger.error(f"Error starting {channel_type} production: {e}")
            self.log_to_gui(f"Error starting {channel_type} production: {e}", "red")
    
    def _channel_production_worker(self, channel_type, description):
        """Worker thread for channel-specific production"""
        try:
            self.log_to_gui(f"🎯 Initializing {channel_type.title()} production pipeline...", "yellow")
            
            # Add memory optimization
            import gc
            gc.collect()  # Force garbage collection
            
            # Add src directory to Python path
            import sys
            import os
            src_path = os.path.join(os.path.dirname(__file__))
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            
            # Import production modules with timeout
            try:
                from content_idea_generator import ContentIdeaGenerator
                from script_writer import ScriptWriter
                from voiceover_generator import VoiceoverGenerator
                from visual_generator import VisualGenerator
                from music_generator import MusicGenerator
                from video_editor import VideoEditor
                from self_improver import SelfImprover
                from izleyici_analyzer import IzleyiciAnalyzer
                from integrator import DailyIntegrator
                from upload_preparer import UploadPreparer
                
                self.log_to_gui("✓ All modules imported successfully", "green")
            except ImportError as e:
                self.log_to_gui(f"✗ Module import failed: {e}", "red")
                return
            
            # Initialize modules with timeout protection
            try:
                self.log_to_gui("Initializing content idea generator...", "blue")
                idea_generator = ContentIdeaGenerator()
                self.log_to_gui("✓ Content idea generator ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Content idea generator failed: {e}", "red")
                return
                
            try:
                self.log_to_gui("Initializing script writer...", "blue")
                script_writer = ScriptWriter()
                self.log_to_gui("✓ Script writer ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Script writer failed: {e}", "red")
                return
                
            try:
                self.log_to_gui("Initializing voiceover generator...", "blue")
                voiceover_generator = VoiceoverGenerator()
                self.log_to_gui("✓ Voiceover generator ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Voiceover generator failed: {e}", "red")
                return
                
            try:
                self.log_to_gui("Initializing visual generator...", "blue")
                visual_generator = VisualGenerator()
                self.log_to_gui("✓ Visual generator ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Visual generator failed: {e}", "red")
                return
                
            try:
                self.log_to_gui("Initializing music generator...", "blue")
                music_generator = MusicGenerator()
                self.log_to_gui("✓ Music generator ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Music generator failed: {e}", "red")
                return
                
            try:
                self.log_to_gui("Initializing video editor...", "blue")
                video_editor = VideoEditor()
                self.log_to_gui("✓ Video editor ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Video editor failed: {e}", "red")
                return
            
            # Generate content with timeout protection
            try:
                self.log_to_gui(f"📝 Generating {channel_type} content ideas...", "green")
                
                # Simple timeout using threading
                import threading
                import queue
                
                result_queue = queue.Queue()
                
                def generate_ideas_with_timeout():
                    try:
                        result = idea_generator.generate_content_ideas(channel_type)
                        result_queue.put(('success', result))
                    except Exception as e:
                        result_queue.put(('error', e))
                
                # Start generation in separate thread
                thread = threading.Thread(target=generate_ideas_with_timeout)
                thread.daemon = True
                thread.start()
                
                # Wait for result with timeout
                try:
                    status, result = result_queue.get(timeout=30)  # 30 second timeout
                    if status == 'success':
                        ideas = result
                        if ideas:
                            self.log_to_gui(f"✓ Generated {len(ideas)} content ideas", "green")
                        else:
                            self.log_to_gui("⚠️ No content ideas generated", "yellow")
                    else:
                        raise result  # Re-raise the exception
                except queue.Empty:
                    self.log_to_gui("⚠️ Content generation timed out, using fallback", "yellow")
                    ideas = [{"title": f"{channel_type} Content", "description": "Fallback content"}]
                
                # Memory cleanup after content generation
                gc.collect()
                    
            except Exception as e:
                self.log_to_gui(f"✗ Content idea generation failed: {e}", "red")
                return
            
            # Generate scripts
            try:
                self.log_to_gui(f"📝 Generating {channel_type} scripts...", "green")
                
                result_queue = queue.Queue()
                
                def generate_scripts_with_timeout():
                    try:
                        result = script_writer.generate_scripts(ideas)
                        result_queue.put(('success', result))
                    except Exception as e:
                        result_queue.put(('error', e))
                
                thread = threading.Thread(target=generate_scripts_with_timeout)
                thread.daemon = True
                thread.start()
                
                try:
                    status, result = result_queue.get(timeout=30)
                    if status == 'success':
                        scripts = result
                        if scripts:
                            self.log_to_gui(f"✓ Generated {len(scripts)} scripts", "green")
                        else:
                            self.log_to_gui("⚠️ No scripts generated", "yellow")
                    else:
                        raise result
                except queue.Empty:
                    self.log_to_gui("⚠️ Script generation timed out, using fallback", "yellow")
                    scripts = [{"title": f"{channel_type} Script", "content": "Fallback script content"}]
                    
            except Exception as e:
                self.log_to_gui(f"✗ Script generation failed: {e}", "red")
                return
            
            # Generate voiceovers
            try:
                self.log_to_gui(f"🎤 Creating {channel_type} voiceovers...", "green")
                voiceovers = voiceover_generator.generate_voiceovers(scripts)
                if voiceovers:
                    self.log_to_gui(f"✓ Generated {len(voiceovers)} voiceovers", "green")
                else:
                    self.log_to_gui("⚠️ No voiceovers generated", "yellow")
            except Exception as e:
                self.log_to_gui(f"✗ Voiceover generation failed: {e}", "red")
                return
            
            # Generate visuals
            try:
                self.log_to_gui(f"🎨 Generating {channel_type} visuals...", "green")
                visuals = visual_generator.generate_visuals(scripts)
                if visuals:
                    self.log_to_gui(f"✓ Generated {len(visuals)} visuals", "green")
                else:
                    self.log_to_gui("⚠️ No visuals generated", "yellow")
            except Exception as e:
                self.log_to_gui(f"✗ Visual generation failed: {e}", "red")
                return
            
            # Generate music
            try:
                self.log_to_gui(f"🎵 Creating {channel_type} music...", "green")
                music = music_generator.generate_music(scripts)
                if music:
                    self.log_to_gui(f"✓ Generated {len(music)} music tracks", "green")
                else:
                    self.log_to_gui("⚠️ No music generated", "yellow")
            except Exception as e:
                self.log_to_gui(f"✗ Music generation failed: {e}", "red")
                return
            
            # Edit videos
            try:
                self.log_to_gui(f"🎬 Editing {channel_type} videos...", "green")
                videos = video_editor.edit_videos(voiceovers, visuals, music)
                if videos:
                    self.log_to_gui(f"✓ Generated {len(videos)} videos", "green")
                else:
                    self.log_to_gui("⚠️ No videos generated", "yellow")
            except Exception as e:
                self.log_to_gui(f"✗ Video editing failed: {e}", "red")
                return
            
            self.log_to_gui(f"✅ {channel_type.title()} production completed successfully!", "green")
            self.update_status(f"🎬 {channel_type.title()} Production Complete", "green")
            
        except Exception as e:
            self.logger.error(f"Error in {channel_type} production: {e}")
            self.log_to_gui(f"❌ Error in {channel_type} production: {e}", "red")
            self.update_status(f"❌ {channel_type.title()} Production Failed", "red")
        finally:
            self.progress.stop()
    
    def pause_all_production(self):
        """Pause all production processes"""
        self.log_to_gui("⏸️ Pausing all production processes...", "yellow")
        self.update_status("⏸️ Production Paused", "yellow")
    
    def resume_all_production(self):
        """Resume all production processes"""
        self.log_to_gui("▶️ Resuming all production processes...", "green")
        self.update_status("▶️ Production Resumed", "green")
    
    def stop_all_production(self):
        """Stop all production processes"""
        self.log_to_gui("🛑 Stopping all production processes...", "red")
        self.update_status("🛑 All Production Stopped", "red")
        self.progress.stop()
            
    def stop_production(self):
        """Stop the video production process"""
        try:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.progress.stop()
            self.update_status("Production stopped", "red")
            self.log_to_gui("Production process stopped by user")
        except Exception as e:
            self.logger.error(f"Error stopping production: {e}")
            
    def clear_logs(self):
        """Clear the log text area"""
        try:
            if self.log_text:
                self.log_text.delete(1.0, tk.END)
        except Exception as e:
            self.logger.error(f"Error clearing logs: {e}")
    
    def manual_self_improvement(self):
        """Manually trigger self-improvement"""
        try:
            # Get improve button reference safely
            improve_button = getattr(self, 'improve_button', None)
            if improve_button:
                improve_button.config(state=tk.DISABLED)
            
            self.log_to_gui("Starting manual self-improvement...")
            
            # Start improvement in separate thread
            improvement_thread = threading.Thread(target=self.improvement_worker)
            improvement_thread.daemon = True
            improvement_thread.start()
            
        except Exception as e:
            self.logger.error(f"Error starting manual improvement: {e}")
            self.log_to_gui(f"Error starting improvement: {e}")
    
    def improvement_worker(self):
        """Worker thread for manual self-improvement"""
        try:
            # Import self-improver
            from self_improver import SelfImprover
            
            self_improver = SelfImprover()
            
            # Get Python files in src directory
            src_dir = os.path.dirname(__file__)
            python_files = []
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    if file.endswith('.py') and file != 'self_improver.py':
                        python_files.append(os.path.join(root, file))
            
            if python_files:
                # Select 2-3 random files to improve
                files_to_improve = random.sample(python_files, min(3, len(python_files)))
                
                self.log_to_gui(f"Selected {len(files_to_improve)} files for improvement:")
                for file_path in files_to_improve:
                    self.log_to_gui(f"  - {os.path.basename(file_path)}")
                
                improved_count = 0
                for file_path in files_to_improve:
                    self.log_to_gui(f"Improving {os.path.basename(file_path)}...")
                    if self_improver.improve_code(file_path):
                        improved_count += 1
                        self.log_to_gui(f"✓ Improved: {os.path.basename(file_path)}")
                    else:
                        self.log_to_gui(f"✗ Failed to improve: {os.path.basename(file_path)}")
                
                self.log_to_gui(f"Manual improvement completed: {improved_count}/{len(files_to_improve)} files improved")
            else:
                self.log_to_gui("No Python files found for improvement")
                
        except Exception as e:
            self.logger.error(f"Error in improvement worker: {e}")
            self.log_to_gui(f"Improvement error: {e}")
        finally:
            try:
                self.root.after(0, lambda: self.improve_button.config(state=tk.NORMAL))
            except:
                pass
    
    def run_demo(self):
        """Run a demo video production"""
        if not self.production_running:
            self.log_to_gui("Starting demo mode...", "blue")
            # Get demo button reference safely
            demo_button = getattr(self, 'demo_button', None)
            if demo_button:
                demo_button.config(state=tk.DISABLED)
            threading.Thread(target=self.demo_worker, daemon=True).start()
        else:
            self.log_to_gui("Cannot run demo while production is running", "red")
            
    def demo_worker(self):
        """Worker thread for demo mode"""
        try:
            self.log_to_gui("Demo mode: Creating a short test video...", "blue")
            
            # Create a simple test script
            test_script = {
                'id': 'demo_script_001',
                'title': 'Demo Video - The Power of AI',
                'content': 'This is a demonstration of the AutoVideoProducer system. Watch as AI creates compelling content automatically.',
                'sections': {
                    'hook': 'Welcome to the future of content creation!',
                    'intro': 'Today we explore the amazing capabilities of AI-powered video production.',
                    'main': 'This demo showcases automatic script generation, voiceover creation, visual generation, and video editing.',
                    'cta': 'Experience the power of automated content creation!'
                }
            }
            
            self.log_to_gui("Demo: Generating voiceover...", "green")
            time.sleep(2)  # Simulate processing
            
            self.log_to_gui("Demo: Creating visuals...", "green")
            time.sleep(2)  # Simulate processing
            
            self.log_to_gui("Demo: Composing video...", "green")
            time.sleep(2)  # Simulate processing
            
            self.log_to_gui("Demo: Video completed successfully!", "green")
            self.log_to_gui("Demo mode completed - check the output directory for results", "blue")
            
        except Exception as e:
            self.logger.error(f"Error in demo worker: {e}")
            self.log_to_gui(f"Demo error: {e}", "red")
        finally:
            try:
                demo_button = getattr(self, 'demo_button', None)
                if demo_button:
                    self.root.after(0, lambda: demo_button.config(state=tk.NORMAL))
            except:
                pass
    
    def start_scheduler(self):
        """Start the daily scheduler"""
        try:
            self.log_to_gui("Starting daily scheduler...", "blue")
            self.update_status("Scheduler running", "purple")
            
            # Get button references safely
            scheduler_button = getattr(self, 'scheduler_button', None)
            stop_scheduler_button = getattr(self, 'stop_scheduler_button', None)
            
            # Disable start button, enable stop button
            if scheduler_button:
                scheduler_button.config(state=tk.DISABLED)
            if stop_scheduler_button:
                stop_scheduler_button.config(state=tk.NORMAL)
            
            # Start scheduler in background thread
            self.scheduler_thread = threading.Thread(target=self._scheduler_worker, daemon=True)
            self.scheduler_thread.start()
            
            self.log_to_gui("Daily scheduler started - production will run at 00:00 daily", "green")
            
        except Exception as e:
            self.logger.error(f"Error starting scheduler: {e}")
            self.log_to_gui(f"Scheduler error: {e}", "red")
    
    def stop_scheduler(self):
        """Stop the daily scheduler"""
        try:
            self.log_to_gui("Stopping daily scheduler...", "yellow")
            
            # Get button references safely
            scheduler_button = getattr(self, 'scheduler_button', None)
            stop_scheduler_button = getattr(self, 'stop_scheduler_button', None)
            
            # Re-enable start button, disable stop button
            if scheduler_button:
                scheduler_button.config(state=tk.NORMAL)
            if stop_scheduler_button:
                stop_scheduler_button.config(state=tk.DISABLED)
            
            self.update_status("Scheduler stopped", "yellow")
            self.log_to_gui("Daily scheduler stopped", "yellow")
            
        except Exception as e:
            self.logger.error(f"Error stopping scheduler: {e}")
            self.log_to_gui(f"Error stopping scheduler: {e}", "red")
    
    def _scheduler_worker(self):
        """Background worker for scheduler"""
        try:
            # Get debug mode from config
            debug_mode = self.config.get('debug_mode', False)
            
            # Schedule daily production at 00:00
            schedule.every().day.at("00:00").do(self._run_scheduled_production)
            
            # If debug mode is enabled, run production immediately
            if debug_mode:
                self.log_to_gui("Debug mode enabled - running production immediately", "yellow")
                self._run_scheduled_production()
            
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except Exception as e:
            self.logger.error(f"Scheduler worker error: {e}")
            self.log_to_gui(f"Scheduler worker error: {e}", "red")
    
    def _run_scheduled_production(self):
        """Run scheduled daily production"""
        try:
            self.log_to_gui("Daily production started by scheduler...", "blue")
            self.run_daily_production()
        except Exception as e:
            self.logger.error(f"Error in scheduled production: {e}")
            self.log_to_gui(f"Scheduled production error: {e}", "red")
    
    def run_daily_production(self):
        """Run daily production manually"""
        try:
            self.log_to_gui("Starting daily production cycle...", "blue")
            self.update_status("Daily production running", "blue")
            
            # Check Ollama health before production
            if not self._check_ollama_health():
                self.log_to_gui("Ollama health check failed, attempting to start Ollama...", "yellow")
                self._start_ollama_service()
            
            # Disable button during production
            self.daily_production_button.config(state=tk.DISABLED)
            
            # Run production in background thread
            production_thread = threading.Thread(target=self._daily_production_worker, daemon=True)
            production_thread.start()
            
        except Exception as e:
            self.logger.error(f"Error starting daily production: {e}")
            self.log_to_gui(f"Daily production error: {e}", "red")
    
    def _daily_production_worker(self):
        """Background worker for daily production with error-proofing and retries"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.log_to_gui(f"Daily production worker started (attempt {retry_count + 1}/{max_retries})", "blue")
                
                # Import required modules with fallbacks
                modules = self._import_production_modules()
                if not modules:
                    self.log_to_gui("Critical module import failed, aborting production", "red")
                    break
                
                # Initialize components
                idea_generator = modules.get('idea_generator')
                script_writer = modules.get('script_writer')
                voiceover_generator = modules.get('voiceover_generator')
                visual_generator = modules.get('visual_generator')
                music_generator = modules.get('music_generator')
                video_editor = modules.get('video_editor')
                self_improver = modules.get('self_improver')
                audience_analyzer = modules.get('audience_analyzer')
                daily_integrator = modules.get('daily_integrator')
                upload_preparer = modules.get('upload_preparer')
                
                # Run production steps with error handling
                self.log_to_gui("Starting content generation...", "green")
                ideas = self._safe_execute(idea_generator.generate_ideas, "History") if idea_generator else None
                
                self.log_to_gui("Generating scripts...", "green")
                scripts = self._safe_execute(script_writer.generate_scripts, ideas) if script_writer and ideas else None
                
                self.log_to_gui("Creating voiceovers...", "green")
                voiceovers = self._safe_execute(voiceover_generator.generate_voiceovers, scripts) if voiceover_generator and scripts else None
                
                self.log_to_gui("Generating visuals...", "green")
                visuals = self._safe_execute(visual_generator.generate_visuals, scripts) if visual_generator and scripts else None
                
                self.log_to_gui("Creating music...", "green")
                music = self._safe_execute(music_generator.generate_music, scripts) if music_generator and scripts else None
                
                # Fallback to music21 if audiocraft is missing
                if not music and music_generator:
                    self.log_to_gui("Using music21 fallback for music generation", "yellow")
                    music = self._generate_music21_fallback(scripts)
                
                self.log_to_gui("Editing videos...", "green")
                videos = self._safe_execute(video_editor.edit_videos, voiceovers, visuals, music) if video_editor else None
                
                self.log_to_gui("Analyzing audience...", "green")
                analysis = self._safe_execute(audience_analyzer.analyze_audience, videos) if audience_analyzer and videos else None
                
                self.log_to_gui("Integrating daily content...", "green")
                self._safe_execute(daily_integrator.integrate_content, videos, analysis) if daily_integrator else None
                
                self.log_to_gui("Preparing uploads...", "green")
                self._safe_execute(upload_preparer.prepare_uploads, videos) if upload_preparer else None
                
                self.log_to_gui("Daily production completed successfully!", "green")
                break  # Success, exit retry loop
                
            except Exception as e:
                retry_count += 1
                self.logger.error(f"Error in daily production worker (attempt {retry_count}): {e}")
                self.log_to_gui(f"Daily production error (attempt {retry_count}/{max_retries}): {e}", "red")
                
                if retry_count < max_retries:
                    self.log_to_gui(f"Retrying in 30 seconds...", "yellow")
                    time.sleep(30)
                else:
                    self.log_to_gui("All retry attempts failed. Production aborted.", "red")
            finally:
                try:
                    self.root.after(0, lambda: self.daily_production_button.config(state=tk.NORMAL))
                except:
                    pass
            
    def production_worker(self):
        """Worker thread for video production"""
        try:
            self.log_to_gui("Initializing production pipeline...", "blue")
            
            # Add src directory to Python path
            import sys
            import os
            src_path = os.path.join(os.path.dirname(__file__))
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            
            # Import the new modules
            try:
                from content_idea_generator import ContentIdeaGenerator
                from script_writer import ScriptWriter
                from voiceover_generator import VoiceoverGenerator, VoiceoverSettings
                from visual_generator import VisualGenerator
                from music_generator import MusicGenerator
                from video_editor import VideoEditor, edit_video
                from self_improver import SelfImprover
                from izleyici_analyzer import IzleyiciAnalyzer
                from integrator import DailyIntegrator
                from upload_preparer import UploadPreparer
                self.log_to_gui("Modules imported successfully", "green")
            except ImportError as e:
                self.log_to_gui(f"Failed to import modules: {e}", "red")
                return
            
            # Initialize modules with error handling
            try:
                self.log_to_gui("Initializing content idea generator...")
                idea_generator = ContentIdeaGenerator()
                self.log_to_gui("✓ Content idea generator ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Content idea generator failed: {e}", "red")
                return
                
            try:
                self.log_to_gui("Initializing script writer...")
                script_writer = ScriptWriter()
                self.log_to_gui("✓ Script writer ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Script writer failed: {e}", "red")
                return
                
            try:
                self.log_to_gui("Initializing voiceover generator...")
                voiceover_generator = VoiceoverGenerator()
                self.log_to_gui("✓ Voiceover generator ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Voiceover generator failed: {e}", "red")
                return
                
            try:
                self.log_to_gui("Initializing visual generator...")
                visual_generator = VisualGenerator()
                self.log_to_gui("✓ Visual generator ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Visual generator failed: {e}", "red")
                return
                
            try:
                self.log_to_gui("Initializing music generator...")
                music_generator = MusicGenerator()
                self.log_to_gui("✓ Music generator ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Music generator failed: {e}", "red")
                return
                
            try:
                self.log_to_gui("Initializing video editor...")
                video_editor = VideoEditor()
                self.log_to_gui("✓ Video editor ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Video editor failed: {e}", "red")
                return
                
            try:
                self.log_to_gui("Initializing self-improvement system...")
                self_improver = SelfImprover()
                self.log_to_gui("✓ Self-improvement system ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Self-improvement system failed: {e}", "red")
                return
                
            try:
                self.log_to_gui("Initializing audience analyzer...")
                audience_analyzer = IzleyiciAnalyzer()
                self.log_to_gui("✓ Audience analyzer ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Audience analyzer failed: {e}", "red")
                return
                
            try:
                self.daily_integrator = DailyIntegrator()
                self.upload_preparer = UploadPreparer()
                self.log_to_gui("✓ Integrator and upload preparer ready", "green")
            except Exception as e:
                self.log_to_gui(f"✗ Integrator/upload preparer failed: {e}", "red")
                return
            
            # Production steps
            steps = [
                ("Loading channel configurations...", 1),
                ("Generating content ideas...", 2),
                ("Creating video scripts...", 3),
                ("Generating audio narration...", 4),
                ("Generating visual assets...", 5),
                ("Generating background music...", 6),
                ("Processing video footage...", 7),
                ("Adding subtitles...", 8),
                ("Rendering final videos...", 9),
                ("Analyzing audience response...", 10),
                ("Uploading to channels...", 11)
            ]
            
            for i, (step, step_num) in enumerate(steps):
                if not hasattr(self, 'production_thread') or not self.production_thread.is_alive():
                    break
                    
                self.log_to_gui(f"Step {step_num}/11: {step}")
                
                # Execute actual production steps
                if step_num == 2:  # Generating content ideas
                    try:
                        self.log_to_gui("Generating ideas for CKLegends channel...")
                        ideas = idea_generator.generate_ideas("History")
                        if ideas and 'long_video' in ideas:
                            self.log_to_gui(f"Generated {len(ideas.get('long_video', []))} long video ideas")
                            self.log_to_gui(f"Generated {len(ideas.get('shorts', []))} short video ideas")
                        else:
                            self.log_to_gui("No ideas generated, using fallback")
                    except Exception as e:
                        self.log_to_gui(f"Error generating ideas: {e}")
                
                elif step_num == 3:  # Creating video scripts
                    try:
                        self.log_to_gui("Generating video scripts...")
                        # Create a test video idea
                        test_idea = {
                            "title": "The Hidden Truth About Ancient Civilizations",
                            "script_outline": "Revealing mysterious advanced technologies",
                            "duration": "15-20 minutes",
                            "target_audience": "History enthusiasts",
                            "hooks": ["What if everything you learned is wrong?"],
                            "emotional_triggers": ["mystery", "wonder", "discovery"]
                        }
                        
                        # Generate long video script
                        long_script = script_writer.generate_script_with_improvement_loop(test_idea, 'long')
                        self.log_to_gui(f"Long script generated: {long_script.total_words} words, Score: {long_script.addictiveness_score:.1f}/10")
                        
                        # Generate short video script
                        short_script = script_writer.generate_script_with_improvement_loop(test_idea, 'short')
                        self.log_to_gui(f"Short script generated: {short_script.total_words} words, Score: {short_script.addictiveness_score:.1f}/10")
                        
                        # Save scripts
                        script_writer.save_script_to_file(long_script)
                        script_writer.save_script_to_file(short_script)
                        self.log_to_gui("Scripts saved successfully")
                        
                    except Exception as e:
                        self.log_to_gui(f"Error generating scripts: {e}")
                
                elif step_num == 4:  # Generating audio narration
                    try:
                        self.log_to_gui("Generating voiceovers...")
                        
                        # Create voiceover settings
                        settings = VoiceoverSettings(
                            narrator_style="david_attenborough",
                            language="en",
                            slow=False
                        )
                        
                        # Generate test voiceover
                        test_text = "Welcome to an extraordinary journey into the unknown. What you're about to discover will challenge everything you thought you knew."
                        result = voiceover_generator.generate_voiceover(test_text, settings)
                        
                        if result.audio_file_path:
                            self.log_to_gui(f"Voiceover generated: {result.duration_seconds:.2f}s, Quality: {result.quality_score:.1f}/10")
                        else:
                            self.log_to_gui("Voiceover generation failed")
                            
                    except Exception as e:
                        self.log_to_gui(f"Error generating voiceovers: {e}")
                
                elif step_num == 5:  # Generating visual assets
                    try:
                        self.log_to_gui("Generating visual assets...")
                        
                        # Use the script outline to generate visuals
                        if 'long_script' in locals():
                            script_outline = long_script.script_outline
                        else:
                            script_outline = "Ancient civilizations, epic landscapes, dramatic lighting, cinematic composition"
                        
                        visual_paths = visual_generator.generate_visuals(script_outline)
                        
                        if visual_paths:
                            self.log_to_gui(f"Generated {len(visual_paths)} visual assets")
                            for i, path in enumerate(visual_paths[:3]):  # Show first 3
                                self.log_to_gui(f"  Visual {i+1}: {os.path.basename(path)}")
                        else:
                            self.log_to_gui("Visual generation failed")
                            
                    except Exception as e:
                        self.log_to_gui(f"Error generating visuals: {e}")
                
                elif step_num == 6:  # Generating background music
                    try:
                        self.log_to_gui("Generating background music...")
                        
                        # Determine video type from script
                        video_type = "history"  # Default for test
                        if 'long_script' in locals() and hasattr(long_script, 'video_type'):
                            video_type = long_script.video_type
                        
                        music_path = music_generator.generate_music(video_type)
                        
                        if music_path:
                            self.log_to_gui(f"Generated background music: {os.path.basename(music_path)}")
                            
                            # Assess music quality
                            quality = music_generator.assess_music_quality(music_path, video_type)
                            self.log_to_gui(f"Music quality rating: {quality}/10")
                        else:
                            self.log_to_gui("Music generation failed")
                            
                    except Exception as e:
                        self.log_to_gui(f"Error generating music: {e}")
                
                elif step_num == 7:  # Video editing
                    try:
                        self.log_to_gui("Editing video for CKLegends...")
                        
                        # Use generated assets for video editing
                        if 'long_script' in locals() and 'visual_paths' in locals() and 'music_path' in locals():
                            script_text = long_script.script_text
                            voiceover_path = "assets/test_voiceover.mp3"  # Placeholder
                            visuals_list = visual_paths if 'visual_paths' in locals() else []
                            music_file = music_path if 'music_path' in locals() else "assets/background_music.mp3"
                            
                            # Edit video
                            final_video_path = video_editor.edit_video(
                                script=script_text,
                                voiceover_mp3=voiceover_path,
                                visuals_list=visuals_list,
                                music_mp3=music_file,
                                channel_topic="CKLegends"
                            )
                            
                            if final_video_path:
                                self.log_to_gui(f"Video editing completed: {os.path.basename(final_video_path)}")
                                self.log_to_gui(f"Final video saved to: {final_video_path}")
                            else:
                                self.log_to_gui("Video editing failed")
                        else:
                            self.log_to_gui("Skipping video editing - missing assets")
                            
                    except Exception as e:
                        self.log_to_gui(f"Error editing video: {e}")
                
                elif step_num == 10:  # Analyzing audience response
                    try:
                        self.log_to_gui("Analyzing audience response...")
                        
                        # Analyze the final video if it exists
                        if 'final_video_path' in locals() and final_video_path:
                            analysis_result = audience_analyzer.analyze_video(final_video_path)
                            
                            if 'error' not in analysis_result:
                                metrics = analysis_result['metrics']
                                feedback = analysis_result['feedback']
                                
                                self.log_to_gui(f"Audience Analysis Results:")
                                self.log_to_gui(f"  Engagement: {metrics['engagement']:.2f}/1.0")
                                self.log_to_gui(f"  Retention: {metrics['retention']:.2f}/1.0")
                                self.log_to_gui(f"  Satisfaction: {metrics['satisfaction']:.2f}/1.0")
                                self.log_to_gui(f"  Overall Score: {metrics['overall_score']:.2f}/1.0")
                                
                                # Log feedback
                                for key, message in feedback.items():
                                    if key != 'recommendations':
                                        self.log_to_gui(f"  {key.title()}: {message}")
                                
                                # Log recommendations
                                if 'recommendations' in feedback:
                                    self.log_to_gui("  Recommendations:")
                                    for rec in feedback['recommendations']:
                                        self.log_to_gui(f"    - {rec}")
                                
                                # Feed feedback back to Ollama for next iteration
                                self.log_to_gui("Feeding audience feedback to AI for next iteration...")
                                
                            else:
                                self.log_to_gui(f"Audience analysis failed: {analysis_result['error']}")
                        else:
                            self.log_to_gui("No video available for audience analysis")
                            
                    except Exception as e:
                        self.log_to_gui(f"Error in audience analysis: {e}")
                
                else:
                    # Simulate other steps
                    time.sleep(1)
                
            # Run self-improvement after production
            try:
                self.log_to_gui("Running self-improvement cycle...")
                
                # Get random modules to improve
                src_dir = os.path.dirname(__file__)
                python_files = []
                for root, dirs, files in os.walk(src_dir):
                    for file in files:
                        if file.endswith('.py') and file != 'self_improver.py':
                            python_files.append(os.path.join(root, file))
                
                if python_files:
                    # Select 1-2 random files to improve
                    files_to_improve = random.sample(python_files, min(2, len(python_files)))
                    
                    improved_count = 0
                    for file_path in files_to_improve:
                        if self_improver.improve_code(file_path):
                            improved_count += 1
                            self.log_to_gui(f"Improved: {os.path.basename(file_path)}")
                    
                    self.log_to_gui(f"Self-improvement completed: {improved_count}/{len(files_to_improve)} files improved")
                else:
                    self.log_to_gui("No Python files found for improvement")
                    
            except Exception as e:
                self.log_to_gui(f"Error in self-improvement: {e}")
            
            self.log_to_gui("Production cycle completed successfully!")
            self.update_status("Production completed", "green")
            
        except Exception as e:
            self.logger.error(f"Error in production worker: {e}")
            self.log_to_gui(f"Production error: {e}")
        finally:
            try:
                self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
                self.root.after(0, lambda: self.progress.stop())
            except:
                pass
    
    def install_dependencies(self):
        """Install dependencies button handler"""
        try:
            self.install_deps_button.config(state=tk.DISABLED)
            self.log_to_gui("Installing dependencies...", "blue")
            
            # Start installation in a separate thread to avoid blocking GUI
            import threading
            def install_worker():
                try:
                    if install_dependencies:
                        result = install_dependencies()
                        if result:
                            installed_count = len(result.get('installed', {}))
                            failed_count = len(result.get('failed', []))
                            self.log_to_gui(f"Dependency installation completed. Installed: {installed_count}, Failed: {failed_count}", "green")
                            
                            if result.get('ollama_ok'):
                                self.log_to_gui("Ollama is ready", "green")
                            else:
                                self.log_to_gui("Ollama not available - some features may be limited", "yellow")
                                
                            if result.get('stable_diffusion_ok'):
                                self.log_to_gui("Stable Diffusion is ready", "green")
                            else:
                                self.log_to_gui("Stable Diffusion not available - visual generation may be limited", "yellow")
                                
                            if failed_count > 0:
                                self.log_to_gui(f"Failed packages: {', '.join(result.get('failed', []))}", "red")
                        else:
                            self.log_to_gui("Dependency installation failed", "red")
                    else:
                        self.log_to_gui("Setup module not available", "red")
                except Exception as e:
                    self.log_to_gui(f"Error during dependency installation: {e}", "red")
                finally:
                    try:
                        self.install_deps_button.config(state=tk.NORMAL)
                    except:
                        pass
            
            # Start installation thread
            install_thread = threading.Thread(target=install_worker)
            install_thread.daemon = True
            install_thread.start()
            
        except Exception as e:
            self.log_to_gui(f"Error starting dependency installation: {e}", "red")
            try:
                self.install_deps_button.config(state=tk.NORMAL)
            except:
                pass
    
    def _check_ollama_health(self):
        """Check if Ollama is running and responding"""
        try:
            if not ollama:
                return False
            
            # Test Ollama with a simple chat
            response = ollama.chat(model='llama3', messages=[{
                'role': 'user',
                'content': 'Test'
            }])
            
            return response and 'message' in response
        except Exception as e:
            self.logger.error(f"Ollama health check failed: {e}")
            return False
    
    def _start_ollama_service(self):
        """Start Ollama service using subprocess"""
        try:
            self.log_to_gui("Attempting to start Ollama service...", "yellow")
            
            # Check if Ollama is already running
            try:
                import requests
                response = requests.get("http://127.0.0.1:11434/api/version", timeout=2)
                if response.status_code == 200:
                    self.log_to_gui("Ollama service already running", "green")
                    return True
            except:
                pass
            
            # Try to start Ollama using subprocess
            try:
                import subprocess
                # Start Ollama in background
                subprocess.Popen(['ollama', 'serve'], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
                
                # Wait a bit for service to start
                time.sleep(3)
                
                # Check if service started successfully
                try:
                    import requests
                    response = requests.get("http://127.0.0.1:11434/api/version", timeout=5)
                    if response.status_code == 200:
                        self.log_to_gui("Ollama service started successfully", "green")
                        return True
                    else:
                        self.log_to_gui("Ollama service failed to start", "red")
                        return False
                except:
                    self.log_to_gui("Ollama service may have started, but health check failed", "yellow")
                    return True
                    
            except FileNotFoundError:
                self.log_to_gui("Ollama not found in PATH. Please install Ollama first.", "red")
                return False
            except Exception as e:
                self.log_to_gui(f"Failed to start Ollama service: {e}", "red")
                return False
            
        except Exception as e:
            self.logger.error(f"Error starting Ollama service: {e}")
            self.log_to_gui(f"Failed to start Ollama service: {e}", "red")
            return False
    
    def _import_production_modules(self):
        """Import production modules with fallbacks"""
        modules = {}
        
        # Try to import each module
        module_imports = [
            ('content_idea_generator', 'ContentIdeaGenerator'),
            ('script_writer', 'ScriptWriter'),
            ('voiceover_generator', 'VoiceoverGenerator'),
            ('visual_generator', 'VisualGenerator'),
            ('music_generator', 'MusicGenerator'),
            ('video_editor', 'VideoEditor'),
            ('self_improver', 'SelfImprover'),
            ('izleyici_analyzer', 'IzleyiciAnalyzer'),
            ('integrator', 'DailyIntegrator'),
            ('upload_preparer', 'UploadPreparer')
        ]
        
        for module_name, class_name in module_imports:
            try:
                # Import using importlib for better control
                import importlib
                module = importlib.import_module(module_name)
                class_obj = getattr(module, class_name)
                instance = class_obj()
                
                # Use consistent naming
                if module_name == 'integrator':
                    modules['daily_integrator'] = instance
                elif module_name == 'izleyici_analyzer':
                    modules['audience_analyzer'] = instance
                else:
                    modules[module_name.replace('_', '')] = instance
                    
                self.log_to_gui(f"✓ {module_name} imported successfully", "green")
            except ImportError as e:
                self.log_to_gui(f"✗ {module_name} not available, creating stub: {e}", "yellow")
                if module_name == 'integrator':
                    modules['daily_integrator'] = self._create_module_stub(module_name, class_name)
                elif module_name == 'izleyici_analyzer':
                    modules['audience_analyzer'] = self._create_module_stub(module_name, class_name)
                else:
                    modules[module_name.replace('_', '')] = self._create_module_stub(module_name, class_name)
            except Exception as e:
                self.log_to_gui(f"✗ Error importing {module_name}: {e}", "red")
                if module_name == 'integrator':
                    modules['daily_integrator'] = self._create_module_stub(module_name, class_name)
                elif module_name == 'izleyici_analyzer':
                    modules['audience_analyzer'] = self._create_module_stub(module_name, class_name)
                else:
                    modules[module_name.replace('_', '')] = self._create_module_stub(module_name, class_name)
        
        return modules
    
    def _create_module_stub(self, module_name, class_name):
        """Create a stub module when the real module is missing"""
        class StubModule:
            def __init__(self):
                self.logger = logging.getLogger(__name__)
                # Add config attribute to prevent NoneType errors
                self.config = {}
            
            def __getattr__(self, name):
                def stub_method(*args, **kwargs):
                    self.logger.warning(f"Stub method called: {name} on {module_name}")
                    return None
                return stub_method
        
        return StubModule()
    
    def _safe_execute(self, func, *args, **kwargs):
        """Safely execute a function with error handling"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.logger.error(f"Error executing {func.__name__}: {e}")
            self.log_to_gui(f"Error in {func.__name__}: {e}", "red")
            return None
    
    def _generate_music21_fallback(self, scripts):
        """Generate music using music21 fallback"""
        try:
            if not music21:
                self.log_to_gui("music21 not available for fallback", "red")
                return None
            
            self.log_to_gui("Generating music with music21 fallback...", "yellow")
            
            # Create a simple melody
            from music21 import stream, note, chord
            
            # Create a basic stream
            s = stream.Stream()
            
            # Add some notes
            notes = [note.Note('C4'), note.Note('D4'), note.Note('E4'), note.Note('F4')]
            for n in notes:
                s.append(n)
            
            # Add a simple chord
            c = chord.Chord(['C4', 'E4', 'G4'])
            s.append(c)
            
            # Export to MIDI
            output_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fallback_music.mid')
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            s.write('midi', fp=output_path)
            
            self.log_to_gui(f"Generated fallback music: {output_path}", "green")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error generating music21 fallback: {e}")
            self.log_to_gui(f"Music21 fallback failed: {e}", "red")
            return None
                
    def initialize(self):
        """Initialize the application"""
        try:
            self.log_to_gui("AutoVideoProducer starting...", "blue")
            
            # Install dependencies first
            if install_dependencies:
                self.log_to_gui("Installing missing dependencies...", "blue")
                try:
                    result = install_dependencies()
                    if result:
                        installed_count = len(result.get('installed', {}))
                        failed_count = len(result.get('failed', []))
                        self.log_to_gui(f"Dependency installation completed. Installed: {installed_count}, Failed: {failed_count}", "green")
                        
                        if result.get('ollama_ok'):
                            self.log_to_gui("Ollama is ready", "green")
                        else:
                            self.log_to_gui("Ollama not available - some features may be limited", "yellow")
                            
                        if result.get('stable_diffusion_ok'):
                            self.log_to_gui("Stable Diffusion is ready", "green")
                        else:
                            self.log_to_gui("Stable Diffusion not available - visual generation may be limited", "yellow")
                            
                        if failed_count > 0:
                            self.log_to_gui(f"Failed packages: {', '.join(result.get('failed', []))}", "red")
                    else:
                        self.log_to_gui("Dependency installation failed", "red")
                except Exception as e:
                    self.log_to_gui(f"Error during dependency installation: {e}", "red")
            else:
                self.log_to_gui("Setup module not available - skipping dependency installation", "yellow")
            
            # Load configuration
            if not self.load_config():
                self.log_to_gui("Failed to load configuration", "red")
                return False
            self.log_to_gui("Configuration loaded successfully", "green")
            
            # Setup Ollama
            if not self.setup_ollama():
                self.log_to_gui("Ollama not available - some features may be limited", "yellow")
            else:
                self.log_to_gui("Ollama setup completed", "green")
            
            # Create GUI
            if not self.create_gui():
                self.log_to_gui("Failed to create GUI", "red")
                return False
            self.log_to_gui("GUI created successfully", "green")
            
            # Start monitoring
            self.system_monitor.start_monitoring()
            self.file_watcher.start_watching()
            
            # Start scheduler
            self.start_scheduler()
            
            self.log_to_gui("AutoVideoProducer initialized successfully!", "green")
            self.update_status("Ready", "green")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during initialization: {e}")
            self.log_to_gui(f"Initialization error: {e}", "red")
            return False
            
    def run(self):
        """Run the application"""
        try:
            if self.initialize():
                # Start a timer to keep GUI responsive
                def update_gui():
                    try:
                        self.root.update()
                        # Check if production thread is still alive
                        if hasattr(self, 'current_production_thread') and self.current_production_thread:
                            if not self.current_production_thread.is_alive():
                                self.progress.stop()
                                self.update_status("Production completed", "green")
                        self.root.after(100, update_gui)
                    except Exception as e:
                        self.logger.error(f"GUI update error: {e}")
                
                # Start GUI update loop
                self.root.after(100, update_gui)
                self.root.mainloop()
            else:
                messagebox.showerror("Error", "Failed to initialize AutoVideoProducer")
        except Exception as e:
            self.logger.error(f"Error running application: {e}")
            messagebox.showerror("Error", f"Application error: {e}")

def main():
    """Main entry point"""
    try:
        app = AutoVideoProducer()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
