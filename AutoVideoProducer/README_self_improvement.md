# AutoVideoProducer Self-Improvement System

## Overview

The AutoVideoProducer now includes an advanced self-improvement system that allows the program to analyze and rewrite its own code for continuous optimization. This system combines AST (Abstract Syntax Tree) analysis, Ollama AI suggestions, and audience feedback to create a self-evolving video production platform.

## Features

### 1. Self-Improver (`self_improver.py`)

**Core Functionality:**
- **AST Analysis**: Uses Python's `ast` module to parse and analyze code structure
- **Complexity Metrics**: Analyzes function length, nested loops, hardcoded values
- **Ollama Integration**: Uses AI to suggest improvements for efficiency and best practices
- **Java Support**: Optional Java code improvement using `javalang` parser
- **Backup System**: Automatically creates backups before making changes
- **Daily Scheduling**: Runs automatic improvements daily at 2 AM

**Key Classes:**
- `CodeAnalyzer`: Analyzes Python code using AST
- `ComplexityAnalyzer`: Calculates code complexity metrics
- `OllamaImprover`: Gets AI suggestions for code improvements
- `JavaImprover`: Handles Java code improvement (optional)
- `SelfImprover`: Main orchestrator for the improvement process

**Usage:**
```python
from self_improver import SelfImprover

# Initialize
improver = SelfImprover()

# Improve a specific file
improver.improve_code("src/main.py")

# Run daily improvement cycle
improver.run_daily_improvement()

# Schedule automatic improvements
improver.schedule_daily_improvement()
```

### 2. Audience Analyzer (`izleyici_analyzer.py`)

**Core Functionality:**
- **PyTorch RNN Model**: Simulates audience behavior using LSTM neural network
- **Video Feature Extraction**: Analyzes visual, audio, and content features
- **Engagement Prediction**: Predicts engagement, retention, and satisfaction scores
- **Feedback Generation**: Provides actionable recommendations for content improvement
- **Synthetic Training Data**: Generates realistic training data for the model

**Key Classes:**
- `AudienceRNN`: LSTM neural network for audience prediction
- `VideoFeatureExtractor`: Extracts comprehensive video features
- `AudienceDataset`: Dataset for training the audience model
- `IzleyiciAnalyzer`: Main audience analysis orchestrator

**Usage:**
```python
from izleyici_analyzer import IzleyiciAnalyzer

# Initialize analyzer
analyzer = IzleyiciAnalyzer()

# Analyze a video
result = analyzer.analyze_video("video.mp4")

# Get feedback
print(f"Engagement: {result['metrics']['engagement']:.2f}")
print(f"Retention: {result['metrics']['retention']:.2f}")
print(f"Satisfaction: {result['metrics']['satisfaction']:.2f}")
```

## Integration with Main Application

### GUI Integration
- **Self-Improve Button**: Manual trigger for self-improvement
- **Real-time Logging**: Shows improvement progress in GUI
- **Audience Analysis**: Integrated into production pipeline
- **Feedback Loop**: Audience feedback feeds back to AI for next iterations

### Production Pipeline Integration
1. **Step 10**: Audience response analysis
2. **Post-Production**: Automatic self-improvement cycle
3. **Feedback Loop**: Audience insights inform next content generation

## Installation

### Dependencies
```bash
pip install javalang  # For Java support (optional)
pip install opencv-python  # For video analysis
pip install librosa  # For audio analysis
```

### Requirements Update
The `requirements.txt` has been updated to include:
- `javalang>=0.13.0` for Java code parsing
- Existing PyTorch and other ML libraries

## Configuration

### Self-Improvement Settings
- **Daily Schedule**: Runs at 2 AM by default
- **Files per Day**: Improves 2-3 random files per cycle
- **Backup Retention**: Creates timestamped backups
- **Model Selection**: Uses "llama3" by default for Ollama

### Audience Analysis Settings
- **Model Training**: 50 epochs by default
- **Feature Extraction**: 10 frame samples for video analysis
- **Prediction Thresholds**: Configurable engagement/retention thresholds

## Testing

Run the test script to verify functionality:
```bash
python test_self_improvement.py
```

This will test:
- Self-improver initialization
- Audience analyzer setup
- Integration with main application
- Basic functionality verification

## Safety Features

### Backup System
- Automatic file backups before modifications
- Timestamped backup files
- Rollback capability if needed

### Error Handling
- Graceful failure handling
- Detailed error logging
- Fallback to original code if improvement fails

### Validation
- AST validation before applying changes
- Syntax checking after modifications
- Model prediction confidence scoring

## Advanced Features

### Java Integration
- Subprocess-based Java improvement
- `javalang` parser for Java code analysis
- Cross-language improvement capabilities

### Local Control (pyautogui)
- Automatic folder opening
- GUI automation capabilities
- System integration features

### Continuous Learning
- Improvement history tracking
- Performance metrics over time
- Adaptive improvement strategies

## Monitoring and Logging

### Improvement History
- JSON-based improvement tracking
- Metrics before/after comparison
- Suggestion effectiveness analysis

### GUI Logging
- Real-time improvement status
- Audience analysis results
- Error reporting and debugging

## Future Enhancements

### Planned Features
- **Multi-language Support**: C++, JavaScript, Go
- **Advanced AST Manipulation**: Direct code transformation
- **Performance Profiling**: Runtime performance analysis
- **Collaborative Learning**: Cross-instance improvement sharing
- **Custom Models**: Trainable improvement models

### Research Areas
- **Code Quality Metrics**: Advanced complexity analysis
- **Semantic Understanding**: Deep code comprehension
- **Optimization Strategies**: Performance-focused improvements
- **Security Analysis**: Vulnerability detection and fixing

## Troubleshooting

### Common Issues
1. **Ollama Not Found**: Install Ollama and download llama3 model
2. **Java Support Disabled**: Install `javalang` package
3. **Model Training Fails**: Check PyTorch installation and GPU availability
4. **Video Analysis Errors**: Install OpenCV and librosa

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

### Development Guidelines
- Follow existing code structure
- Add comprehensive error handling
- Include unit tests for new features
- Update documentation for changes

### Testing New Features
- Use the test script as a template
- Verify integration with main application
- Test error conditions and edge cases

## License

This self-improvement system is part of the AutoVideoProducer project and follows the same licensing terms.
