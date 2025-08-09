#!/bin/bash

echo "AutoVideoProducer - CK Empire"
echo "================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "src/main.py" ]; then
    echo "ERROR: main.py not found"
    echo "Please run this script from the AutoVideoProducer directory"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "WARNING: Some dependencies may not be installed"
    echo "Run: pip3 install -r requirements.txt"
    echo
fi

# Run the application
echo "Starting AutoVideoProducer..."
echo
python3 src/main.py

# If we get here, the application has closed
echo
echo "AutoVideoProducer has closed."
