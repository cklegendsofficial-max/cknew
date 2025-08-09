#!/usr/bin/env python3
"""
Test script for AutoVideoProducer setup verification
"""

import sys
import os
import json
import subprocess
from pathlib import Path

def test_python_version():
    """Test Python version"""
    print("✓ Python version check...")
    if sys.version_info >= (3, 8):
        print(f"  Python {sys.version_info.major}.{sys.version_info.minor} ✓")
        return True
    else:
        print(f"  Python {sys.version_info.major}.{sys.version_info.minor} ✗ (3.8+ required)")
        return False

def test_imports():
    """Test required imports"""
    print("✓ Testing imports...")
    required_modules = [
        'tkinter',
        'json',
        'logging',
        'threading',
        'subprocess',
        'requests',
        'datetime'
    ]
    
    optional_modules = [
        'ollama',
        'moviepy',
        'torch',
        'pydub',
        'PIL',
        'gtts',
        'music21',
        'ast'
    ]
    
    all_good = True
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  {module} ✓")
        except ImportError:
            print(f"  {module} ✗")
            all_good = False
    
    print("  Optional modules:")
    for module in optional_modules:
        try:
            __import__(module)
            print(f"    {module} ✓")
        except ImportError:
            print(f"    {module} ✗ (install with: pip install {module})")
    
    return all_good

def test_directory_structure():
    """Test directory structure"""
    print("✓ Testing directory structure...")
    
    base_dir = Path(__file__).parent
    required_dirs = ['src', 'models', 'assets', 'logs', 'config']
    
    all_good = True
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"  {dir_name}/ ✓")
        else:
            print(f"  {dir_name}/ ✗")
            all_good = False
    
    return all_good

def test_config_file():
    """Test configuration file"""
    print("✓ Testing configuration file...")
    
    config_path = Path(__file__).parent / 'config' / 'config.json'
    
    if not config_path.exists():
        print("  config.json ✗ (not found)")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_keys = ['channels', 'daily_output', 'languages']
        all_good = True
        
        for key in required_keys:
            if key in config:
                print(f"  {key} ✓")
            else:
                print(f"  {key} ✗")
                all_good = False
        
        if 'channels' in config:
            print(f"    Found {len(config['channels'])} channels")
        
        return all_good
        
    except json.JSONDecodeError as e:
        print(f"  config.json ✗ (invalid JSON: {e})")
        return False
    except Exception as e:
        print(f"  config.json ✗ (error: {e})")
        return False

def test_ollama():
    """Test Ollama installation"""
    print("✓ Testing Ollama...")
    
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"  Ollama {result.stdout.strip()} ✓")
            return True
        else:
            print("  Ollama ✗ (not found or not working)")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  Ollama ✗ (not installed)")
        print("    Install from: https://ollama.ai/")
        return False
    except Exception as e:
        print(f"  Ollama ✗ (error: {e})")
        return False

def test_main_script():
    """Test main script syntax"""
    print("✓ Testing main script...")
    
    main_path = Path(__file__).parent / 'src' / 'main.py'
    
    if not main_path.exists():
        print("  main.py ✗ (not found)")
        return False
    
    try:
        with open(main_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic syntax check
        compile(content, str(main_path), 'exec')
        print("  main.py ✓ (syntax OK)")
        return True
        
    except SyntaxError as e:
        print(f"  main.py ✗ (syntax error: {e})")
        return False
    except Exception as e:
        print(f"  main.py ✗ (error: {e})")
        return False

def main():
    """Run all tests"""
    print("AutoVideoProducer Setup Verification")
    print("=" * 40)
    
    tests = [
        test_python_version,
        test_imports,
        test_directory_structure,
        test_config_file,
        test_ollama,
        test_main_script
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  Test failed with exception: {e}")
            results.append(False)
        print()
    
    print("=" * 40)
    print("Summary:")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("✓ All tests passed! AutoVideoProducer is ready to use.")
        print("\nTo start the application:")
        print("  python src/main.py")
    else:
        print(f"✗ {total - passed} test(s) failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  1. Install Python 3.8+: https://python.org")
        print("  2. Install dependencies: pip install -r requirements.txt")
        print("  3. Install Ollama: https://ollama.ai/")
        print("  4. Check file permissions and directory structure")

if __name__ == "__main__":
    main()
