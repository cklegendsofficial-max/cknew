# AutoVideoProducer - CK Empire

An automated video production system with AI integration for creating content across multiple channels.

## Features

- **Multi-Channel Support**: Automated content generation for 5 different channels
- **AI Integration**: Uses Ollama with Llama3 for content generation
- **Multi-Language Support**: Generates subtitles in 6 languages (EN, FR, DE, ES, JP, KR)
- **Real-time GUI**: Tkinter-based interface with live logging
- **Error-Proof Design**: Comprehensive error handling and logging
- **Modular Architecture**: Clean separation of concerns
- **System Monitoring**: RAM/CPU monitoring with automatic production pausing
- **File Watching**: Automatic restart on file changes
- **Demo Mode**: Quick test video generation
- **Dependency Management**: Automatic installation of missing packages
- **Self-Improvement**: AI-powered code enhancement
- **Psychological Manipulation**: Advanced NLP techniques for audience engagement

## Project Structure

```
AutoVideoProducer/
├── src/                    # Core application scripts
│   └── main.py            # Main application entry point
├── models/                 # Ollama models and local AI weights
├── assets/                 # Generated images, audio, videos
├── logs/                   # Application logs and tracking
├── config/                 # Configuration files
│   └── config.json        # Channel and settings configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** installed and running
   - Download from: https://ollama.ai/
   - Install and start the Ollama service

### Setup

1. **Clone or download the project**:
   ```bash
   cd AutoVideoProducer
   ```

2. **Run setup.py first for dependencies**:
   ```bash
   python src/setup.py
   ```
   This will automatically install all required packages and set up Ollama.

3. **Install Python dependencies** (if setup.py fails):
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Ollama models** (will be done automatically on first run):
   ```bash
   ollama pull llama3
   ```

## Configuration

The application uses `config/config.json` for settings:

```json
{
    "channels": [
        {"name": "CKLegends", "topic": "History"},
        {"name": "CKFinanceCore", "topic": "Finance"},
        {"name": "CKDrive", "topic": "Automobiles"},
        {"name": "CKCombat", "topic": "Combat Sports"},
        {"name": "CKIronWill", "topic": "Motivation"}
    ],
    "daily_output": {"long": 1, "shorts": 3},
    "languages": ["en", "fr", "de", "es", "jp", "kr"]
}
```

## Usage

### Running the Application

1. **Start the application**:
   ```bash
   python src/main.py
   ```

2. **GUI Interface**:
   - The application will open a Tkinter GUI window
   - Real-time logs are displayed in the text area
   - Use "Start Production" to begin video generation
   - Use "Stop" to halt the process
   - Use "Clear Logs" to clear the log display

### Production Process

The application follows this workflow:

1. **Configuration Loading**: Loads channel and language settings
2. **Ollama Setup**: Ensures Llama3 model is available
3. **Content Generation**: Creates video scripts and ideas
4. **Audio Processing**: Generates narration and background music
5. **Video Processing**: Combines audio with visual elements
6. **Subtitle Generation**: Creates multi-language subtitles
7. **Final Rendering**: Produces completed videos
8. **Channel Upload**: Prepares content for distribution

## Building Executable

To create a standalone executable:

```bash
python build_exe.py
```

This will create `dist/AutoVideoProducer.exe` with all dependencies included.

## Advanced Features

### System Monitoring
- **RAM/CPU Monitoring**: Automatically pauses production when system resources are high
- **File Watching**: Restarts production when source files are modified
- **Crash Recovery**: Automatic restart on application crashes

### Demo Mode
- **Quick Testing**: Generate a short test video to verify system functionality
- **No Dependencies**: Works even with limited AI models available

### Self-Improvement
- **Code Analysis**: Automatically analyzes and improves Python code
- **Performance Optimization**: Identifies and fixes performance bottlenecks
- **Error Prevention**: Reduces bugs and improves reliability

## Channels

The system supports 5 specialized channels:

- **CKLegends**: Historical content and stories
- **CKFinanceCore**: Financial education and market analysis
- **CKDrive**: Automotive reviews and car culture
- **CKCombat**: Combat sports and martial arts
- **CKIronWill**: Motivational and self-improvement content

## Daily Output

- **Long Videos**: 1 per day (10-15 minutes)
- **Short Videos**: 3 per day (1-3 minutes each)

## Multi-Language Support

Subtitles are generated in 6 languages:
- English (EN)
- French (FR)
- German (DE)
- Spanish (ES)
- Japanese (JP)
- Korean (KR)

## Error Handling

The application includes comprehensive error handling:

- **Try-catch blocks** around all critical operations
- **Logging** to both file and GUI
- **Graceful degradation** when services are unavailable
- **User-friendly error messages**

## Logging

Logs are stored in the `logs/` directory with timestamps:
- Application logs: `autovideoproducer_YYYYMMDD_HHMMSS.log`
- Production logs: Separate files for each production cycle
- Error logs: Detailed error tracking and debugging information

## Building Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed src/main.py
```

The executable will be created in the `dist/` directory.

## Troubleshooting

### Common Issues

1. **Ollama not found**:
   - Ensure Ollama is installed and running
   - Check if `ollama --version` works in terminal

2. **Missing dependencies**:
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

3. **GUI not displaying**:
   - Ensure tkinter is available (usually comes with Python)
   - Check display settings on headless systems

4. **Permission errors**:
   - Run as administrator if needed
   - Check file permissions in project directories

### Getting Help

- Check the logs in the `logs/` directory
- Review the GUI log display for real-time information
- Ensure all prerequisites are installed correctly

## Development

### Adding New Features

1. **New Channels**: Add to `config/config.json`
2. **New Languages**: Update the languages array
3. **New AI Models**: Modify the Ollama setup in `main.py`
4. **GUI Enhancements**: Extend the Tkinter interface

### Code Structure

- **Main Class**: `AutoVideoProducer` handles the application lifecycle
- **GUI Methods**: All GUI-related functionality is in separate methods
- **Worker Threads**: Production processes run in background threads
- **Error Handling**: Comprehensive try-catch blocks throughout

## License

This project is part of the CK Empire content production system.

## Support

For issues and questions:
1. Check the logs for detailed error information
2. Ensure all dependencies are properly installed
3. Verify Ollama is running and accessible
4. Review the configuration file for correct settings
