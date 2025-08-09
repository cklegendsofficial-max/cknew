@echo off
echo AutoVideoProducer - CK Empire
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "src\main.py" (
    echo ERROR: main.py not found
    echo Please run this script from the AutoVideoProducer directory
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Some dependencies may not be installed
    echo Run: pip install -r requirements.txt
    echo.
)

REM Run the application
echo Starting AutoVideoProducer...
echo.
python src\main.py

REM If we get here, the application has closed
echo.
echo AutoVideoProducer has closed.
pause
