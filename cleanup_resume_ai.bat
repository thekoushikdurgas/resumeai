@echo off
REM =====================================================
REM Resume AI Application Cleanup Script
REM =====================================================
REM This batch file cleans up temporary files and
REM optionally removes the entire installation
REM =====================================================

echo.
echo =====================================================
echo 🧹 Resume AI Application Cleanup
echo =====================================================
echo.

echo Choose cleanup option:
echo 1. Clean temporary files only (recommended)
echo 2. Full cleanup (removes virtual environment and all data)
echo 3. Cancel
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" goto clean_temp
if "%choice%"=="2" goto full_cleanup
if "%choice%"=="3" goto cancel
goto invalid_choice

:clean_temp
echo.
echo 🧹 Cleaning temporary files...
echo.

REM Clean temporary directories
if exist "temp" (
    echo Removing temp directory...
    rmdir /s /q "temp"
    echo ✅ temp directory removed
)

if exist "logs" (
    echo Removing log files...
    del /q "logs\*" 2>nul
    echo ✅ Log files cleaned
)

if exist "cache" (
    echo Removing cache directory...
    rmdir /s /q "cache"
    echo ✅ Cache directory removed
)

if exist "uploads" (
    echo Removing uploaded files...
    del /q "uploads\*" 2>nul
    echo ✅ Uploaded files cleaned
)

if exist "__pycache__" (
    echo Removing Python cache...
    rmdir /s /q "__pycache__"
    echo ✅ Python cache removed
)

REM Clean Python cache in subdirectories
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
for /r . %%f in (*.pyc) do @if exist "%%f" del "%%f"

echo.
echo ✅ Temporary files cleanup completed!
goto end

:full_cleanup
echo.
echo ⚠️ WARNING: This will remove the virtual environment and all data!
echo This action cannot be undone.
echo.
set /p confirm="Are you sure you want to continue? (yes/no): "
if /i not "%confirm%"=="yes" goto cancel

echo.
echo 🧹 Performing full cleanup...

REM Remove virtual environment
if exist "resume_ai_env" (
    echo Removing virtual environment...
    rmdir /s /q "resume_ai_env"
    echo ✅ Virtual environment removed
)

REM Remove data directories
if exist "data" (
    echo Removing data directory...
    rmdir /s /q "data"
    echo ✅ Data directory removed
)

REM Remove configuration
if exist ".streamlit" (
    echo Removing Streamlit configuration...
    rmdir /s /q ".streamlit"
    echo ✅ Streamlit configuration removed
)

REM Clean temporary files
call :clean_temp

echo.
echo ✅ Full cleanup completed!
echo You can run setup_resume_ai.bat to reinstall the application.
goto end

:cancel
echo.
echo ❌ Cleanup cancelled.
goto end

:invalid_choice
echo.
echo ❌ Invalid choice. Please run the script again.
goto end

:end
echo.
pause
