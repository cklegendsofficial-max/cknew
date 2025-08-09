#!/usr/bin/env python3
"""
Test Visual and Music Generator Integration
Verifies that both modules are properly integrated and working
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    try:
        from visual_generator import VisualGenerator
        print("✓ VisualGenerator imported successfully")
    except ImportError as e:
        print(f"✗ VisualGenerator import failed: {e}")
        return False
    
    try:
        from music_generator import MusicGenerator
        print("✓ MusicGenerator imported successfully")
    except ImportError as e:
        print(f"✗ MusicGenerator import failed: {e}")
        return False
    
    return True

def test_visual_generator():
    """Test visual generator functionality"""
    print("\nTesting Visual Generator...")
    
    try:
        from visual_generator import VisualGenerator
        
        # Initialize generator
        generator = VisualGenerator()
        print("✓ VisualGenerator initialized")
        
        # Test script parsing
        test_script = """
        Scene: Ancient Rome at sunset
        Visual: Epic battle scene with dramatic lighting
        Show: Modern city skyline at night
        """
        
        cues = generator.parse_script_for_visual_cues(test_script)
        print(f"✓ Found {len(cues)} visual cues")
        
        # Test configuration
        config = generator.config
        print(f"✓ Configuration loaded: {config['image_width']}x{config['image_height']}")
        
        # Test generation stats
        stats = generator.get_generation_stats()
        print(f"✓ Generation stats available: {stats['sd_available']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Visual generator test failed: {e}")
        return False

def test_music_generator():
    """Test music generator functionality"""
    print("\nTesting Music Generator...")
    
    try:
        from music_generator import MusicGenerator
        
        # Initialize generator
        generator = MusicGenerator()
        print("✓ MusicGenerator initialized")
        
        # Test style determination
        video_types = ["history", "motivation", "corporate", "nature"]
        for video_type in video_types:
            style = generator.determine_music_style(video_type)
            print(f"✓ {video_type} → {style} style")
        
        # Test configuration
        config = generator.config
        print(f"✓ Configuration loaded: {len(config['music_styles'])} music styles")
        
        # Test generation stats
        stats = generator.get_generation_stats()
        print(f"✓ Generation stats available: Music21={stats['music21_available']}, Audiocraft={stats['audiocraft_available']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Music generator test failed: {e}")
        return False

def test_integration():
    """Test integration with main application"""
    print("\nTesting Main Application Integration...")
    
    try:
        # Import main application modules
        from main import AutoVideoProducer
        
        # Test that the modules are available in main
        app = AutoVideoProducer()
        print("✓ AutoVideoProducer initialized")
        
        # Test configuration loading
        if app.load_config():
            print("✓ Configuration loaded in main app")
        else:
            print("⚠ Configuration loading failed (may be expected)")
        
        return True
        
    except Exception as e:
        print(f"✗ Main application integration test failed: {e}")
        return False

def test_dependencies():
    """Test that required dependencies are available"""
    print("\nTesting Dependencies...")
    
    dependencies = {
        'torch': 'PyTorch for AI models',
        'diffusers': 'Stable Diffusion',
        'transformers': 'Hugging Face transformers',
        'music21': 'Music theory and composition',
        'pydub': 'Audio processing',
        'pillow': 'Image processing',
        'requests': 'HTTP requests',
        'ollama': 'Ollama CLI (optional)'
    }
    
    all_available = True
    
    for dep, description in dependencies.items():
        try:
            if dep == 'ollama':
                # Check if ollama command is available
                import subprocess
                result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✓ {dep}: {description}")
                else:
                    print(f"⚠ {dep}: {description} (not available)")
            else:
                __import__(dep)
                print(f"✓ {dep}: {description}")
        except ImportError:
            print(f"✗ {dep}: {description} (not installed)")
            all_available = False
    
    return all_available

def main():
    """Run all tests"""
    print("=== Visual and Music Generator Integration Test ===\n")
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Module Imports", test_imports),
        ("Visual Generator", test_visual_generator),
        ("Music Generator", test_music_generator),
        ("Main Integration", test_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running {test_name} Test")
        print('='*50)
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name:20} {status}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Visual and Music generators are ready to use.")
    elif passed >= total * 0.8:
        print("⚠ Most tests passed. Some features may be limited.")
    else:
        print("❌ Many tests failed. Please check dependencies and installation.")
    
    # Recommendations
    print(f"\n{'='*50}")
    print("RECOMMENDATIONS")
    print('='*50)
    
    if not all(r[1] for r in results[:2]):  # Dependencies and imports
        print("• Install missing dependencies: pip install -r requirements.txt")
        print("• Check Python environment and virtual environment")
    
    if not results[2][1]:  # Visual generator
        print("• Visual generator needs Stable Diffusion setup")
        print("• Install: pip install diffusers transformers accelerate")
    
    if not results[3][1]:  # Music generator
        print("• Music generator needs music21 and audiocraft")
        print("• Install: pip install music21 audiocraft pydub")
    
    if not results[4][1]:  # Main integration
        print("• Main application integration needs configuration")
        print("• Check config/config.json file exists")
    
    print("\nFor detailed setup instructions, see:")
    print("• src/README_visual_generator.md")
    print("• src/README_music_generator.md")

if __name__ == "__main__":
    main()
