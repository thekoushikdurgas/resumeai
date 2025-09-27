#!/usr/bin/env python3
"""
Resume/CV AI - Professional Project Launcher
Complete launcher script with setup, validation, and execution
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path
import json
from typing import Dict, List, Optional
import platform
import shutil
import tempfile

# Project Information
PROJECT_NAME = "Resume/CV AI"
PROJECT_VERSION = "1.0.0"
PYTHON_MIN_VERSION = (3, 8)
PROJECT_ROOT = Path(__file__).parent

class Color:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Print application header"""
    print(f"{Color.HEADER}{Color.BOLD}")
    print("=" * 60)
    print(f"  {PROJECT_NAME} v{PROJECT_VERSION}")
    print("  Professional AI-Powered Resume Assistant")
    print("=" * 60)
    print(f"{Color.ENDC}")

def print_status(message: str, status: str = "info"):
    """Print status message with color coding"""
    colors = {
        "info": Color.CYAN,
        "success": Color.GREEN, 
        "warning": Color.WARNING,
        "error": Color.FAIL
    }
    
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️", 
        "error": "❌"
    }
    
    color = colors.get(status, Color.CYAN)
    icon = icons.get(status, "•")
    
    print(f"{color}{icon} {message}{Color.ENDC}")

def check_python_version() -> bool:
    """Check Python version compatibility"""
    current_version = sys.version_info[:2]
    
    if current_version >= PYTHON_MIN_VERSION:
        print_status(f"Python {current_version[0]}.{current_version[1]} - Compatible", "success")
        return True
    else:
        print_status(f"Python {current_version[0]}.{current_version[1]} - Requires {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}+", "error")
        return False

def check_system_requirements() -> Dict[str, bool]:
    """Check system requirements and dependencies"""
    print_status("Checking system requirements...", "info")
    
    requirements = {
        "python_version": check_python_version(),
        "pip_available": shutil.which("pip") is not None,
        "git_available": shutil.which("git") is not None,
        "sufficient_disk_space": check_disk_space(),
        "internet_connection": check_internet_connection()
    }
    
    # Check pip
    if requirements["pip_available"]:
        print_status("pip package manager - Available", "success")
    else:
        print_status("pip package manager - Not found", "error")
    
    # Check git (optional)
    if requirements["git_available"]:
        print_status("Git version control - Available", "success")
    else:
        print_status("Git version control - Not found (optional)", "warning")
    
    # Check disk space
    if requirements["sufficient_disk_space"]:
        print_status("Disk space - Sufficient", "success")
    else:
        print_status("Disk space - Low (may cause issues)", "warning")
    
    # Check internet connection
    if requirements["internet_connection"]:
        print_status("Internet connection - Available", "success")
    else:
        print_status("Internet connection - Limited (required for AI features)", "warning")
    
    return requirements

def check_disk_space() -> bool:
    """Check available disk space"""
    try:
        stats = shutil.disk_usage(PROJECT_ROOT)
        free_gb = stats.free / (1024**3)
        return free_gb > 1.0  # Require at least 1GB free
    except:
        return True  # Assume sufficient if can't check

def check_internet_connection() -> bool:
    """Check internet connectivity"""
    try:
        import urllib.request
        urllib.request.urlopen('https://www.google.com', timeout=5)
        return True
    except:
        return False

def create_virtual_environment(env_path: Path) -> bool:
    """Create Python virtual environment"""
    try:
        print_status(f"Creating virtual environment at {env_path}...", "info")
        
        subprocess.run([
            sys.executable, "-m", "venv", str(env_path)
        ], check=True, capture_output=True)
        
        print_status("Virtual environment created successfully", "success")
        return True
    
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to create virtual environment: {e}", "error")
        return False

def get_venv_python(env_path: Path) -> Path:
    """Get Python executable path in virtual environment"""
    if platform.system() == "Windows":
        return env_path / "Scripts" / "python.exe"
    else:
        return env_path / "bin" / "python"

def get_venv_pip(env_path: Path) -> Path:
    """Get pip executable path in virtual environment"""
    if platform.system() == "Windows":
        return env_path / "Scripts" / "pip.exe"
    else:
        return env_path / "bin" / "pip"

def install_dependencies(env_path: Path, requirements_file: str = "requirements.txt") -> bool:
    """Install project dependencies"""
    try:
        req_path = PROJECT_ROOT / requirements_file
        
        if not req_path.exists():
            print_status(f"Requirements file not found: {requirements_file}", "warning")
            return install_core_dependencies(env_path)
        
        print_status(f"Installing dependencies from {requirements_file}...", "info")
        
        pip_path = get_venv_pip(env_path)
        
        # Upgrade pip first
        subprocess.run([
            str(pip_path), "install", "--upgrade", "pip"
        ], check=True, capture_output=True)
        
        # Install requirements
        subprocess.run([
            str(pip_path), "install", "-r", str(req_path)
        ], check=True)
        
        print_status("Dependencies installed successfully", "success")
        return True
    
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to install dependencies: {e}", "error")
        return False

def install_core_dependencies(env_path: Path) -> bool:
    """Install core dependencies when requirements.txt is not available"""
    core_packages = [
        "streamlit>=1.29.0",
        "pandas>=2.1.0",
        "plotly>=5.17.0", 
        "PyPDF2>=3.0.1",
        "python-docx>=1.1.0",
        "google-generativeai>=0.3.2",
        "nltk>=3.8.1",
        "requests>=2.31.0"
    ]
    
    try:
        print_status("Installing core dependencies...", "info")
        
        pip_path = get_venv_pip(env_path)
        
        for package in core_packages:
            subprocess.run([
                str(pip_path), "install", package
            ], check=True, capture_output=True)
        
        print_status("Core dependencies installed", "success")
        return True
    
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to install core dependencies: {e}", "error")
        return False

def setup_nltk_data(env_path: Path) -> bool:
    """Download required NLTK data"""
    try:
        print_status("Setting up NLTK data...", "info")
        
        python_path = get_venv_python(env_path)
        
        # Download NLTK data
        nltk_script = """
import nltk
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    print('NLTK data downloaded successfully')
except Exception as e:
    print(f'NLTK setup warning: {e}')
"""
        
        result = subprocess.run([
            str(python_path), "-c", nltk_script
        ], capture_output=True, text=True)
        
        if "successfully" in result.stdout:
            print_status("NLTK data setup complete", "success")
        else:
            print_status("NLTK data setup completed with warnings", "warning")
        
        return True
    
    except Exception as e:
        print_status(f"NLTK setup failed: {e}", "warning")
        return False

def setup_spacy_model(env_path: Path) -> bool:
    """Download spaCy English model"""
    try:
        print_status("Setting up spaCy model...", "info")
        
        python_path = get_venv_python(env_path)
        
        # Install spaCy first
        pip_path = get_venv_pip(env_path)
        subprocess.run([
            str(pip_path), "install", "spacy>=3.7.0"
        ], check=True, capture_output=True)
        
        # Download English model
        subprocess.run([
            str(python_path), "-m", "spacy", "download", "en_core_web_sm"
        ], check=True, capture_output=True)
        
        print_status("spaCy model installed", "success")
        return True
    
    except subprocess.CalledProcessError:
        print_status("spaCy model installation failed (optional)", "warning")
        return False

def create_secrets_file() -> bool:
    """Create secrets configuration file"""
    secrets_dir = PROJECT_ROOT / ".streamlit"
    secrets_file = secrets_dir / "secrets.toml"
    
    try:
        secrets_dir.mkdir(exist_ok=True)
        
        if not secrets_file.exists():
            print_status("Creating secrets configuration file...", "info")
            
            secrets_content = """# Streamlit Secrets Configuration
# Add your API keys here for AI services

# Google Gemini API Key (Primary)
GEMINI_API_KEY = "your_gemini_api_key_here"

# OpenAI API Key (Optional)
OPENAI_API_KEY = "your_openai_api_key_here"

# Anthropic Claude API Key (Optional)
ANTHROPIC_API_KEY = "your_anthropic_api_key_here"

# Application Configuration
# DEBUG = true
# ENVIRONMENT = "development"

# Email Configuration (Optional)
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_USERNAME = "your_email@gmail.com" 
# SMTP_PASSWORD = "your_app_password"

# Database Configuration (Optional)
# DATABASE_URL = "sqlite:///resume_ai.db"

# External Services (Optional)
# SENTRY_DSN = "your_sentry_dsn"
# ANALYTICS_KEY = "your_analytics_key"
"""
            
            with open(secrets_file, "w") as f:
                f.write(secrets_content)
            
            print_status(f"Secrets file created: {secrets_file}", "success")
            print_status("⚠️  Please add your API keys to the secrets file", "warning")
        else:
            print_status("Secrets file already exists", "info")
        
        return True
    
    except Exception as e:
        print_status(f"Failed to create secrets file: {e}", "error")
        return False

def create_streamlit_config() -> bool:
    """Create Streamlit configuration file"""
    config_dir = PROJECT_ROOT / ".streamlit"
    config_file = config_dir / "config.toml"
    
    try:
        config_dir.mkdir(exist_ok=True)
        
        if not config_file.exists():
            print_status("Creating Streamlit configuration...", "info")
            
            config_content = """[global]
developmentMode = false

[server]
port = 8501
address = "localhost"
maxUploadSize = 10
enableCORS = false
enableXsrfProtection = true

[browser]
serverAddress = "localhost"
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[logger]
level = "info"
messageFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
"""
            
            with open(config_file, "w") as f:
                f.write(config_content)
            
            print_status("Streamlit configuration created", "success")
        else:
            print_status("Streamlit configuration already exists", "info")
        
        return True
    
    except Exception as e:
        print_status(f"Failed to create Streamlit config: {e}", "error")
        return False

def create_project_directories() -> bool:
    """Create necessary project directories"""
    directories = [
        "data/templates",
        "data/samples", 
        "data/exports",
        "logs",
        "cache",
        "temp",
        "uploads",
        "backups"
    ]
    
    try:
        print_status("Creating project directories...", "info")
        
        for directory in directories:
            dir_path = PROJECT_ROOT / directory
            dir_path.mkdir(parents=True, exist_ok=True)
        
        print_status("Project directories created", "success")
        return True
    
    except Exception as e:
        print_status(f"Failed to create directories: {e}", "error")
        return False

def validate_installation(env_path: Path) -> bool:
    """Validate the installation by running basic tests"""
    try:
        print_status("Validating installation...", "info")
        
        python_path = get_venv_python(env_path)
        
        # Test basic imports
        test_script = """
import streamlit
import pandas
import plotly
import requests
print("Core packages imported successfully")

# Test file creation
from pathlib import Path
test_file = Path("test_installation.tmp")
test_file.write_text("Installation test")
test_file.unlink()
print("File operations working")

print("Installation validation passed")
"""
        
        result = subprocess.run([
            str(python_path), "-c", test_script
        ], capture_output=True, text=True, cwd=PROJECT_ROOT)
        
        if result.returncode == 0:
            print_status("Installation validation passed", "success")
            return True
        else:
            print_status(f"Installation validation failed: {result.stderr}", "error")
            return False
    
    except Exception as e:
        print_status(f"Installation validation error: {e}", "error")
        return False

def run_application(env_path: Path, mode: str = "app", port: int = 8501, dev_mode: bool = False) -> None:
    """Run the Streamlit application"""
    try:
        python_path = get_venv_python(env_path)
        
        # Determine which file to run
        if mode == "demo":
            app_file = PROJECT_ROOT / "demo.py"
            if not app_file.exists():
                print_status("Demo file not found, running main application", "warning")
                app_file = PROJECT_ROOT / "app" / "main.py"
        else:
            app_file = PROJECT_ROOT / "app" / "main.py"
            
            # Fallback to single file version
            if not app_file.exists():
                app_file = PROJECT_ROOT / "resume_ai_app.py"
        
        if not app_file.exists():
            print_status("Application file not found", "error")
            return
        
        print_status(f"Starting {PROJECT_NAME}...", "info")
        print_status(f"Mode: {mode.upper()}", "info")
        print_status(f"Port: {port}", "info")
        print_status(f"Application will open at: http://localhost:{port}", "info")
        
        # Streamlit command
        cmd = [
            str(python_path), "-m", "streamlit", "run", str(app_file),
            "--server.port", str(port),
            "--server.address", "localhost"
        ]
        
        if not dev_mode:
            cmd.extend(["--logger.level", "warning"])
        
        # Set environment variables
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT)
        
        # Run the application
        subprocess.run(cmd, env=env, cwd=PROJECT_ROOT)
    
    except KeyboardInterrupt:
        print_status("\nApplication stopped by user", "info")
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to start application: {e}", "error")
    except Exception as e:
        print_status(f"Unexpected error: {e}", "error")

def full_setup(venv_path: Path, requirements_file: str = "requirements.txt") -> bool:
    """Perform complete setup process"""
    print_status("Starting complete setup process...", "info")
    
    steps = [
        ("System Requirements", lambda: check_system_requirements()["python_version"] and check_system_requirements()["pip_available"]),
        ("Virtual Environment", lambda: create_virtual_environment(venv_path)),
        ("Dependencies", lambda: install_dependencies(venv_path, requirements_file)),
        ("NLTK Data", lambda: setup_nltk_data(venv_path)),
        ("spaCy Model", lambda: setup_spacy_model(venv_path)),
        ("Configuration", lambda: create_secrets_file() and create_streamlit_config()),
        ("Directories", lambda: create_project_directories()),
        ("Validation", lambda: validate_installation(venv_path))
    ]
    
    for step_name, step_func in steps:
        print_status(f"\n--- {step_name} ---", "info")
        
        if not step_func():
            print_status(f"Setup failed at step: {step_name}", "error")
            return False
    
    print_status("\n🎉 Setup completed successfully!", "success")
    print_status("Next steps:", "info")
    print_status("1. Add your AI API keys to .streamlit/secrets.toml", "info")
    print_status("2. Run: python launch.py --run", "info")
    
    return True

def cleanup_installation(venv_path: Path) -> None:
    """Clean up installation files"""
    try:
        print_status("Cleaning up installation...", "info")
        
        if venv_path.exists():
            shutil.rmtree(venv_path)
            print_status("Virtual environment removed", "success")
        
        # Clean up temporary files
        temp_files = [
            PROJECT_ROOT / "test_installation.tmp",
            PROJECT_ROOT / "*.pyc",
            PROJECT_ROOT / "__pycache__"
        ]
        
        for temp_file in temp_files:
            if temp_file.exists():
                if temp_file.is_file():
                    temp_file.unlink()
                elif temp_file.is_dir():
                    shutil.rmtree(temp_file)
        
        print_status("Cleanup completed", "success")
    
    except Exception as e:
        print_status(f"Cleanup failed: {e}", "error")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description=f"{PROJECT_NAME} - Professional Setup and Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch.py --setup                    # Complete setup
  python launch.py --run                      # Run application  
  python launch.py --demo                     # Run demo mode
  python launch.py --run --port 8080          # Custom port
  python launch.py --check                    # Check requirements only
  python launch.py --cleanup                  # Remove installation
        """
    )
    
    parser.add_argument("--setup", action="store_true", help="Complete setup process")
    parser.add_argument("--run", action="store_true", help="Run the application")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode")
    parser.add_argument("--check", action="store_true", help="Check system requirements")
    parser.add_argument("--cleanup", action="store_true", help="Clean up installation")
    parser.add_argument("--port", type=int, default=8501, help="Port to run on (default: 8501)")
    parser.add_argument("--dev", action="store_true", help="Development mode")
    parser.add_argument("--venv", default="venv", help="Virtual environment path")
    parser.add_argument("--requirements", default="requirements.txt", help="Requirements file")
    
    args = parser.parse_args()
    
    # Print header
    print_header()
    
    # Set virtual environment path
    venv_path = PROJECT_ROOT / args.venv
    
    try:
        if args.check:
            requirements = check_system_requirements()
            if all(requirements.values()):
                print_status("All requirements satisfied", "success")
                sys.exit(0)
            else:
                print_status("Some requirements not met", "warning")
                sys.exit(1)
        
        elif args.cleanup:
            cleanup_installation(venv_path)
            sys.exit(0)
        
        elif args.setup:
            success = full_setup(venv_path, args.requirements)
            sys.exit(0 if success else 1)
        
        elif args.run or args.demo:
            if not venv_path.exists():
                print_status("Virtual environment not found. Running setup first...", "warning")
                if not full_setup(venv_path, args.requirements):
                    sys.exit(1)
            
            mode = "demo" if args.demo else "app"
            run_application(venv_path, mode, args.port, args.dev)
        
        else:
            # Default behavior - check if setup is needed
            if not venv_path.exists():
                print_status("First time setup required", "info")
                response = input(f"{Color.CYAN}Would you like to run setup now? (y/N): {Color.ENDC}")
                
                if response.lower().startswith('y'):
                    if full_setup(venv_path, args.requirements):
                        run_application(venv_path, "app", args.port, args.dev)
                else:
                    print_status("Setup cancelled. Run 'python launch.py --setup' when ready.", "info")
            else:
                run_application(venv_path, "app", args.port, args.dev)
    
    except KeyboardInterrupt:
        print_status("\nOperation cancelled by user", "info")
        sys.exit(1)
    except Exception as e:
        print_status(f"Unexpected error: {e}", "error")
        sys.exit(1)

if __name__ == "__main__":
    main()