#!/usr/bin/env python3
"""
Test script for the self-improvement system
"""

import os
import sys
import logging

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_self_improver():
    """Test the self-improver module"""
    print("Testing Self-Improver...")
    
    try:
        from self_improver import SelfImprover
        
        # Initialize self-improver
        improver = SelfImprover()
        print("✓ SelfImprover initialized successfully")
        
        # Test with a simple Python file
        test_file = os.path.join('src', 'main.py')
        if os.path.exists(test_file):
            print(f"Testing improvement on {test_file}")
            result = improver.improve_code(test_file)
            print(f"✓ Improvement result: {result}")
        else:
            print("✗ Test file not found")
            
    except Exception as e:
        print(f"✗ Error testing self-improver: {e}")

def test_audience_analyzer():
    """Test the audience analyzer module"""
    print("\nTesting Audience Analyzer...")
    
    try:
        from izleyici_analyzer import IzleyiciAnalyzer
        
        # Initialize analyzer
        analyzer = IzleyiciAnalyzer()
        print("✓ IzleyiciAnalyzer initialized successfully")
        
        # Test with a dummy video
        test_video = "test_video.mp4"
        result = analyzer.analyze_video(test_video)
        print(f"✓ Analysis result: {result}")
        
    except Exception as e:
        print(f"✗ Error testing audience analyzer: {e}")

def test_integration():
    """Test integration with main application"""
    print("\nTesting Integration...")
    
    try:
        # Test importing both modules
        from self_improver import SelfImprover
        from izleyici_analyzer import IzleyiciAnalyzer
        
        print("✓ Both modules imported successfully")
        
        # Test initialization
        improver = SelfImprover()
        analyzer = IzleyiciAnalyzer()
        
        print("✓ Both systems initialized successfully")
        
        # Test basic functionality
        src_dir = os.path.join('src')
        if os.path.exists(src_dir):
            python_files = []
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    if file.endswith('.py') and file != 'self_improver.py':
                        python_files.append(os.path.join(root, file))
            
            if python_files:
                print(f"✓ Found {len(python_files)} Python files for improvement")
            else:
                print("✗ No Python files found")
        
    except Exception as e:
        print(f"✗ Error testing integration: {e}")

def main():
    """Run all tests"""
    print("AutoVideoProducer Self-Improvement System Test")
    print("=" * 50)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Run tests
    test_self_improver()
    test_audience_analyzer()
    test_integration()
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main()
