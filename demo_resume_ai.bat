@echo off
REM =====================================================
REM Resume AI Application Demo Script
REM =====================================================
REM This batch file runs the demo script to showcase
REM the Resume AI application features
REM =====================================================

echo.
echo =====================================================
echo 🎬 Resume AI Application Demo
echo =====================================================
echo.

REM Check if virtual environment exists
if not exist "resume_ai_env\Scripts\python.exe" (
    echo ❌ Virtual environment not found!
    echo Please run setup_resume_ai.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call resume_ai_env\Scripts\activate.bat

REM Check if demo.py exists
if not exist "demo.py" (
    echo ❌ demo.py not found!
    echo Please ensure you're in the correct directory.
    echo.
    pause
    exit /b 1
)

REM Create necessary directories for demo
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp
if not exist "data\vectordb" mkdir data\vectordb

REM Set environment variables
set PYTHONPATH=%CD%

echo.
echo 🎬 Starting Resume AI Demo...
echo This demo will showcase the key features of the application.
echo Note: Some features may require API keys to work fully.
echo.

REM Run the demo
python demo.py

REM Deactivate virtual environment
call resume_ai_env\Scripts\deactivate.bat

echo.
echo 👋 Demo completed!
echo.
echo To run the full application:
echo 1. Add your API keys to .streamlit\secrets.toml
echo 2. Run run_resume_ai.bat
echo.
pause
