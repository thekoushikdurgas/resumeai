@echo off
REM =====================================================
REM Resume AI Application Development Mode
REM =====================================================
REM This batch file runs the Resume AI application
REM in development mode with hot reload and debugging
REM =====================================================

echo.
echo =====================================================
echo 🔧 Resume AI Development Mode
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

REM Create necessary directories
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp
if not exist "uploads" mkdir uploads
if not exist "data\vectordb" mkdir data\vectordb

REM Set environment variables for development
set PYTHONPATH=%CD%
set STREAMLIT_SERVER_PORT=8501
set STREAMLIT_SERVER_HEADLESS=false
set STREAMLIT_SERVER_RUN_ON_SAVE=true
set STREAMLIT_SERVER_FILE_WATCHER_TYPE=auto
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

echo.
echo 🔧 Starting Resume AI in Development Mode...
echo 📱 The application will open in your default web browser
echo 🌐 URL: http://localhost:8501
echo 🔄 Hot reload is enabled - changes will be reflected automatically
echo 🐛 Debug mode is enabled
echo.
echo Press Ctrl+C to stop the application
echo.

REM Run the application in development mode
python -m streamlit run main.py --server.port 8501 --server.headless false --server.runOnSave true --server.fileWatcherType auto

REM Deactivate virtual environment
call resume_ai_env\Scripts\deactivate.bat

echo.
echo 👋 Development session ended.
pause
