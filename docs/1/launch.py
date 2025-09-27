#!/usr/bin/env python3
"""
Resume/CV AI - Launch Script
Easy launcher for the Resume AI application with setup checks and options
"""

import subprocess
import sys
import os
from pathlib import Path
import argparse

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit', 'pandas', 'plotly', 'PyPDF2', 
        'python-docx', 'nltk', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def setup_nltk_data():
    """Download required NLTK data"""
    try:
        import nltk
        print("📦 Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data ready")
    except Exception as e:
        print(f"⚠️  NLTK setup warning: {e}")

def setup_spacy_model():
    """Download spaCy English model if not present"""
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            print("✅ spaCy model ready")
        except OSError:
            print("📦 Downloading spaCy English model...")
            subprocess.run([
                sys.executable, "-m", "spacy", "download", "en_core_web_sm"
            ], check=True)
            print("✅ spaCy model installed")
    except Exception as e:
        print(f"⚠️  spaCy setup warning: {e}")

def check_secrets():
    """Check if secrets file exists"""
    secrets_path = Path(".streamlit/secrets.toml")
    
    if not secrets_path.exists():
        print("⚠️  No secrets.toml file found")
        print("Creating sample secrets file...")
        
        secrets_path.parent.mkdir(exist_ok=True)
        
        sample_secrets = '''# Streamlit Secrets Configuration
# Add your API keys here

# Google Gemini API Key
GEMINI_API_KEY = "your_gemini_api_key_here"

# OpenAI API Key (Optional)
OPENAI_API_KEY = "your_openai_api_key_here"

# Other optional configurations
# ANTHROPIC_API_KEY = "your_anthropic_api_key_here"
'''
        
        with open(secrets_path, 'w') as f:
            f.write(sample_secrets)
        
        print(f"✅ Created {secrets_path}")
        print("📝 Please add your API keys to the secrets file")
    else:
        print("✅ Secrets file exists")

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'exports', 'templates', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created")

def run_application(mode='app', port=8501, debug=False):
    """Run the Streamlit application"""
    
    if mode == 'demo':
        app_file = 'demo.py'
        print(f"🚀 Starting Resume AI Demo on port {port}")
    else:
        app_file = 'resume_ai_app.py'
        print(f"🚀 Starting Resume AI Application on port {port}")
    
    # Check if file exists
    if not Path(app_file).exists():
        print(f"❌ Error: {app_file} not found")
        sys.exit(1)
    
    # Streamlit command
    cmd = [
        'streamlit', 'run', app_file,
        '--server.port', str(port),
        '--server.address', 'localhost'
    ]
    
    if not debug:
        cmd.extend(['--logger.level', 'warning'])
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description="Resume AI Application Launcher")
    
    parser.add_argument(
        '--mode', 
        choices=['app', 'demo'], 
        default='app',
        help='Run mode: app (full application) or demo (demonstration)'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=8501,
        help='Port to run the application on (default: 8501)'
    )
    
    parser.add_argument(
        '--setup', 
        action='store_true',
        help='Run setup and dependency installation'
    )
    
    parser.add_argument(
        '--install', 
        action='store_true',
        help='Install dependencies only'
    )
    
    parser.add_argument(
        '--debug', 
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--check', 
        action='store_true',
        help='Check system requirements only'
    )
    
    args = parser.parse_args()
    
    print("🤖 Resume/CV AI Application Launcher")
    print("=" * 40)
    
    # Check Python version first
    check_python_version()
    
    if args.install:
        install_dependencies()
        return
    
    if args.setup:
        print("\n🔧 Running setup...")
        install_dependencies()
        setup_nltk_data()
        setup_spacy_model()
        check_secrets()
        create_directories()
        print("\n✅ Setup completed!")
        return
    
    if args.check:
        print("\n🔍 Checking system requirements...")
        check_dependencies()
        check_secrets()
        print("\n✅ System check completed!")
        return
    
    # Standard startup checks
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first:")
        print("python launch.py --install")
        sys.exit(1)
    
    print("\n🔧 Setting up environment...")
    setup_nltk_data()
    setup_spacy_model()
    check_secrets()
    create_directories()
    
    print("\n" + "=" * 40)
    
    # Run the application
    run_application(mode=args.mode, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()