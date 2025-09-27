@echo off
REM =====================================================
REM Resume AI Application Quick Start
REM =====================================================
REM This batch file provides a quick start menu
REM for the Resume AI application
REM =====================================================

:menu
cls
echo.
echo =====================================================
echo 🤖 Resume AI Application - Quick Start Menu
echo =====================================================
echo.
echo Choose an option:
echo.
echo 1. 🚀 Run Application (if already set up)
echo 2. 🛠️ Setup Application (first time)
echo 3. 🎬 Run Demo
echo 4. 🔧 Development Mode
echo 5. 🧹 Cleanup
echo 6. ❌ Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto run_app
if "%choice%"=="2" goto setup_app
if "%choice%"=="3" goto run_demo
if "%choice%"=="4" goto dev_mode
if "%choice%"=="5" goto cleanup
if "%choice%"=="6" goto exit
goto invalid_choice

:run_app
echo.
echo 🚀 Starting Resume AI Application...
call run_resume_ai.bat
goto menu

:setup_app
echo.
echo 🛠️ Setting up Resume AI Application...
call setup_resume_ai.bat
goto menu

:run_demo
echo.
echo 🎬 Running Resume AI Demo...
call demo_resume_ai.bat
goto menu

:dev_mode
echo.
echo 🔧 Starting Development Mode...
call dev_resume_ai.bat
goto menu

:cleanup
echo.
echo 🧹 Starting Cleanup...
call cleanup_resume_ai.bat
goto menu

:invalid_choice
echo.
echo ❌ Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:exit
echo.
echo 👋 Goodbye!
timeout /t 1 >nul
exit /b 0
