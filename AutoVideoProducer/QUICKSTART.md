# AutoVideoProducer - Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Prerequisites
```bash
# Install Python 3.8+ from https://python.org
# Install Ollama from https://ollama.ai/
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
# Windows
run.bat

# Linux/Mac
chmod +x run.sh
./run.sh

# Or directly with Python
python src/main.py
```

## 📋 What You'll See

1. **GUI Window**: Dark-themed interface with real-time logs
2. **Status Bar**: Shows current application state
3. **Log Display**: Live updates of all operations
4. **Control Buttons**: Start/Stop production and clear logs

## ⚙️ Configuration

Edit `config/config.json` to customize:
- Channel names and topics
- Daily video output targets
- Supported languages

## 🔧 Testing Your Setup

Run the verification script:
```bash
python test_setup.py
```

## 📁 Project Structure

```
AutoVideoProducer/
├── src/main.py           # Main application
├── config/config.json    # Channel settings
├── logs/                 # Application logs
├── assets/               # Generated content
├── models/               # AI models
├── requirements.txt      # Dependencies
└── README.md            # Full documentation
```

## 🎯 Next Steps

1. **Customize Channels**: Edit `config/config.json`
2. **Add Dependencies**: Install additional packages as needed
3. **Extend Functionality**: Modify `src/main.py`
4. **Build Executable**: Use PyInstaller for standalone app

## 🆘 Troubleshooting

- **GUI not showing**: Check tkinter installation
- **Ollama errors**: Ensure Ollama is running
- **Import errors**: Run `pip install -r requirements.txt`
- **Permission issues**: Run as administrator if needed

## 📞 Support

- Check logs in `logs/` directory
- Review GUI log display for real-time info
- Run `test_setup.py` for diagnostics

---

**Ready to create automated video content! 🎬**
