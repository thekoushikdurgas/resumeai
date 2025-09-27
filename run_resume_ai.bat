@echo off
REM =====================================================
REM Resume AI Application Launcher
REM =====================================================
REM This batch file runs the Resume AI application
REM with proper virtual environment activation
REM =====================================================

echo.
echo =====================================================
echo 🤖 Resume AI Application Launcher
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

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found!
    echo Please ensure you're in the correct directory.
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed
echo 🔍 Checking dependencies...
python -c "import streamlit, chromadb, sentence_transformers" 2>nul
if errorlevel 1 (
    echo ⚠️ Some dependencies may be missing. Installing...
    pip install -r requirements.txt
)

REM Create necessary directories
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp
if not exist "uploads" mkdir uploads
if not exist "data\vectordb" mkdir data\vectordb

REM Set environment variables
set PYTHONPATH=%CD%
set STREAMLIT_SERVER_PORT=8501
set STREAMLIT_SERVER_HEADLESS=true

echo.
echo 🚀 Starting Resume AI Application...
echo 📱 The application will open in your default web browser
echo 🌐 URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

REM Run the application
python -m streamlit run main.py --server.port 8501 --server.headless true

REM Deactivate virtual environment
call resume_ai_env\Scripts\deactivate.bat

echo.
echo 👋 Resume AI Application stopped.
pause
