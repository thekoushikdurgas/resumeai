@echo off
echo ========================================
echo LinkedIn Job Scraper Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found. Starting installation...
echo.

REM Run the installation script
python install_linkedin_scraper.py

if errorlevel 1 (
    echo.
    echo Installation failed! Please check the error messages above.
    pause
    exit /b 1
) else (
    echo.
    echo Installation completed successfully!
    echo.
    echo To start the application, run: streamlit run main.py
    echo.
    pause
)
