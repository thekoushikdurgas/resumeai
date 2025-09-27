@echo off
REM =====================================================
REM Resume AI Application Setup Script
REM =====================================================
REM This batch file sets up the Resume AI application
REM including virtual environment, dependencies, and configuration
REM =====================================================

echo.
echo =====================================================
echo 🛠️ Resume AI Application Setup
echo =====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Display Python version
echo ✅ Python found:
python --version

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not available!
    echo Please ensure pip is installed with Python.
    echo.
    pause
    exit /b 1
)

echo ✅ pip found:
pip --version
echo.

REM Remove existing virtual environment if it exists
if exist "resume_ai_env" (
    echo 🗑️ Removing existing virtual environment...
    rmdir /s /q "resume_ai_env"
)

REM Create virtual environment
echo 🔄 Creating virtual environment...
python -m venv resume_ai_env
if errorlevel 1 (
    echo ❌ Failed to create virtual environment!
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call resume_ai_env\Scripts\activate.bat

REM Upgrade pip
echo 🔄 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 🔄 Installing dependencies...
if exist "requirements.txt" (
    echo 📦 Installing from requirements.txt...
    pip install -r requirements.txt
) else (
    echo ⚠️ requirements.txt not found, installing core dependencies...
    pip install streamlit>=1.29.0
    pip install chromadb>=0.4.0
    pip install sentence-transformers>=2.2.2
    pip install google-generativeai>=0.3.2
    pip install openai>=1.3.0
    pip install pandas>=2.1.0
    pip install numpy>=1.24.0
    pip install plotly>=5.17.0
    pip install PyPDF2>=3.0.1
    pip install python-docx>=1.1.0
    pip install nltk>=3.8.1
    pip install spacy>=3.7.0
    pip install scikit-learn>=1.3.2
    pip install transformers>=4.35.0
    pip install torch>=2.1.0
)

REM Create necessary directories
echo 🔄 Creating project directories...
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp
if not exist "uploads" mkdir uploads
if not exist "data" mkdir data
if not exist "data\vectordb" mkdir data\vectordb
if not exist "data\templates" mkdir data\templates
if not exist "data\samples" mkdir data\samples
if not exist "data\exports" mkdir data\exports
if not exist "cache" mkdir cache

REM Create .streamlit directory and config
echo 🔄 Creating Streamlit configuration...
if not exist ".streamlit" mkdir .streamlit

REM Create secrets.toml
echo 📝 Creating secrets configuration...
(
echo # Resume AI Application Secrets
echo # Add your API keys here
echo.
echo # Google Gemini API Key
echo GEMINI_API_KEY = "your_gemini_api_key_here"
echo.
echo # OpenAI API Key ^(optional^)
echo OPENAI_API_KEY = "your_openai_api_key_here"
echo.
echo # Anthropic Claude API Key ^(optional^)
echo ANTHROPIC_API_KEY = "your_anthropic_api_key_here"
echo.
echo # Other configuration
echo VECTOR_DB_PATH = "./data/vectordb"
echo LOG_LEVEL = "INFO"
) > .streamlit\secrets.toml

REM Create config.toml
echo 📝 Creating Streamlit config...
(
echo [global]
echo developmentMode = false
echo.
echo [server]
echo headless = true
echo port = 8501
echo enableCORS = false
echo enableXsrfProtection = false
echo.
echo [browser]
echo gatherUsageStats = false
echo.
echo [theme]
echo primaryColor = "#1f77b4"
echo backgroundColor = "#ffffff"
echo secondaryBackgroundColor = "#f0f2f6"
echo textColor = "#262730"
) > .streamlit\config.toml

REM Download NLTK data
echo 🔄 Setting up NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')" 2>nul

REM Download spaCy model
echo 🔄 Setting up spaCy English model...
python -m spacy download en_core_web_sm 2>nul

REM Validate installation
echo 🔍 Validating installation...
python -c "import streamlit, chromadb, sentence_transformers, pandas, numpy; print('✅ All core packages imported successfully')" 2>nul
if errorlevel 1 (
    echo ⚠️ Some packages may not be installed correctly
    echo You may need to install them manually
)

REM Deactivate virtual environment
call resume_ai_env\Scripts\deactivate.bat

echo.
echo =====================================================
echo ✅ Setup completed successfully!
echo =====================================================
echo.
echo Next steps:
echo 1. Add your API keys to .streamlit\secrets.toml
echo 2. Run run_resume_ai.bat to start the application
echo 3. Or run demo_resume_ai.bat to see a demo
echo.
echo 📝 Important: Edit .streamlit\secrets.toml to add your API keys
echo.
pause
