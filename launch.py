"""
Professional Launcher for Resume/CV AI Application with Vector Database
Comprehensive setup and launch script with dependency management.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import argparse

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
    print("=" * 80)
    print("🤖 Resume/CV AI Assistant with Vector Database")
    print("   Professional Setup and Launch Script")
    print("=" * 80)
    print(f"{Color.ENDC}")

def print_status(message: str, status: str = "info"):
    """Print status message with color coding"""
    colors = {
        "info": Color.BLUE,
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
    
    color = colors.get(status, Color.BLUE)
    icon = icons.get(status, "ℹ️")
    
    print(f"{color}{icon} {message}{Color.ENDC}")

def check_python_version() -> bool:
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_status("Python 3.8+ is required", "error")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print_status(f"Python version {version.major}.{version.minor}.{version.micro} is compatible", "success")
    return True

def check_system_requirements() -> Dict[str, bool]:
    """Check system requirements"""
    requirements = {
        "python": check_python_version(),
        "pip": shutil.which("pip") is not None,
        "git": shutil.which("git") is not None,
        "disk_space": check_disk_space(),
        "internet": check_internet_connection()
    }
    
    return requirements

def check_disk_space() -> bool:
    """Check available disk space"""
    try:
        import shutil
        free_space = shutil.disk_usage('.').free
        required_space = 2 * 1024 * 1024 * 1024  # 2GB
        return free_space > required_space
    except:
        return True  # Assume sufficient space if check fails

def check_internet_connection() -> bool:
    """Check internet connection"""
    try:
        import urllib.request
        urllib.request.urlopen('https://www.google.com', timeout=5)
        return True
    except:
        return False

def create_virtual_environment(env_path: Path) -> bool:
    """Create virtual environment"""
    try:
        print_status("Creating virtual environment...", "info")
        
        # Create virtual environment
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
    """Install Python dependencies"""
    try:
        print_status("Installing dependencies...", "info")
        
        python_exe = get_venv_python(env_path)
        pip_exe = get_venv_pip(env_path)
        
        # Upgrade pip first
        subprocess.run([
            str(python_exe), "-m", "pip", "install", "--upgrade", "pip"
        ], check=True, capture_output=True)
        
        # Install requirements
        if Path(requirements_file).exists():
            subprocess.run([
                str(pip_exe), "install", "-r", requirements_file
            ], check=True, capture_output=True)
        else:
            print_status(f"Requirements file {requirements_file} not found", "warning")
            return install_core_dependencies(env_path)
        
        print_status("Dependencies installed successfully", "success")
        return True
        
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to install dependencies: {e}", "error")
        return False

def install_core_dependencies(env_path: Path) -> bool:
    """Install core dependencies manually"""
    try:
        print_status("Installing core dependencies...", "info")
        
        pip_exe = get_venv_pip(env_path)
        
        core_packages = [
            "streamlit>=1.29.0",
            "chromadb>=0.4.0",
            "sentence-transformers>=2.2.2",
            "google-generativeai>=0.3.2",
            "openai>=1.3.0",
            "pandas>=2.1.0",
            "numpy>=1.24.0",
            "plotly>=5.17.0",
            "PyPDF2>=3.0.1",
            "python-docx>=1.1.0"
        ]
        
        for package in core_packages:
            subprocess.run([
                str(pip_exe), "install", package
            ], check=True, capture_output=True)
        
        print_status("Core dependencies installed successfully", "success")
        return True
        
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to install core dependencies: {e}", "error")
        return False

def setup_nltk_data(env_path: Path) -> bool:
    """Setup NLTK data"""
    try:
        print_status("Setting up NLTK data...", "info")
        
        python_exe = get_venv_python(env_path)
        
        # Download NLTK data
        nltk_script = """
import nltk
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    print("NLTK data downloaded successfully")
except Exception as e:
    print(f"Error downloading NLTK data: {e}")
    exit(1)
"""
        
        subprocess.run([
            str(python_exe), "-c", nltk_script
        ], check=True, capture_output=True)
        
        print_status("NLTK data setup completed", "success")
        return True
        
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to setup NLTK data: {e}", "warning")
        return False

def setup_spacy_model(env_path: Path) -> bool:
    """Setup spaCy English model"""
    try:
        print_status("Setting up spaCy English model...", "info")
        
        python_exe = get_venv_python(env_path)
        
        # Download spaCy model
        subprocess.run([
            str(python_exe), "-m", "spacy", "download", "en_core_web_sm"
        ], check=True, capture_output=True)
        
        print_status("spaCy model setup completed", "success")
        return True
        
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to setup spaCy model: {e}", "warning")
        return False

def create_secrets_file() -> bool:
    """Create secrets.toml file for API keys"""
    try:
        print_status("Creating secrets configuration file...", "info")
        
        # Create .streamlit directory
        streamlit_dir = Path(".streamlit")
        streamlit_dir.mkdir(exist_ok=True)
        
        # Create secrets.toml
        secrets_file = streamlit_dir / "secrets.toml"
        
        if not secrets_file.exists():
            secrets_content = """# Resume AI Application Secrets
# Add your API keys here

# Google Gemini API Key
GEMINI_API_KEY = "your_gemini_api_key_here"

# OpenAI API Key (optional)
OPENAI_API_KEY = "your_openai_api_key_here"

# Anthropic Claude API Key (optional)
ANTHROPIC_API_KEY = "your_anthropic_api_key_here"

# Other configuration
VECTOR_DB_PATH = "./data/vectordb"
LOG_LEVEL = "INFO"
"""
            
            with open(secrets_file, 'w') as f:
                f.write(secrets_content)
            
            print_status("Secrets file created at .streamlit/secrets.toml", "success")
            print_status("Please add your API keys to the secrets file", "warning")
        else:
            print_status("Secrets file already exists", "info")
        
        return True
        
    except Exception as e:
        print_status(f"Failed to create secrets file: {e}", "error")
        return False

def create_streamlit_config() -> bool:
    """Create Streamlit configuration file"""
    try:
        print_status("Creating Streamlit configuration...", "info")
        
        # Create .streamlit directory
        streamlit_dir = Path(".streamlit")
        streamlit_dir.mkdir(exist_ok=True)
        
        # Create config.toml
        config_file = streamlit_dir / "config.toml"
        
        config_content = """[global]
developmentMode = false

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
"""
        
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        print_status("Streamlit configuration created", "success")
        return True
        
    except Exception as e:
        print_status(f"Failed to create Streamlit config: {e}", "error")
        return False

def create_project_directories() -> bool:
    """Create necessary project directories"""
    try:
        print_status("Creating project directories...", "info")
        
        directories = [
            "data",
            "data/vectordb",
            "data/templates",
            "data/samples",
            "data/exports",
            "logs",
            "temp",
            "cache",
            "uploads"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        print_status("Project directories created", "success")
        return True
        
    except Exception as e:
        print_status(f"Failed to create directories: {e}", "error")
        return False

def validate_installation(env_path: Path) -> bool:
    """Validate the installation"""
    try:
        print_status("Validating installation...", "info")
        
        python_exe = get_venv_python(env_path)
        
        # Test imports
        test_script = """
try:
    import streamlit
    import chromadb
    import sentence_transformers
    import google.generativeai
    import pandas
    import numpy
    print("All core packages imported successfully")
except ImportError as e:
    print(f"Import error: {e}")
    exit(1)
"""
        
        result = subprocess.run([
            str(python_exe), "-c", test_script
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print_status("Installation validation successful", "success")
            return True
        else:
            print_status(f"Installation validation failed: {result.stderr}", "error")
            return False
        
    except Exception as e:
        print_status(f"Installation validation error: {e}", "error")
        return False

def run_application(env_path: Path, mode: str = "app", port: int = 8501, dev_mode: bool = False) -> None:
    """Run the application"""
    try:
        print_status(f"Starting application in {mode} mode...", "info")
        
        python_exe = get_venv_python(env_path)
        
        if mode == "app":
            # Run main application
            subprocess.run([
                str(python_exe), "-m", "streamlit", "run", "main.py",
                "--server.port", str(port),
                "--server.headless", "true" if not dev_mode else "false"
            ])
        elif mode == "demo":
            # Run demo mode
            print_status("Demo mode not implemented yet", "warning")
        else:
            print_status(f"Unknown mode: {mode}", "error")
    
    except KeyboardInterrupt:
        print_status("Application stopped by user", "info")
    except Exception as e:
        print_status(f"Failed to run application: {e}", "error")

def full_setup(venv_path: Path, requirements_file: str = "requirements.txt") -> bool:
    """Perform full setup"""
    print_status("Starting full setup...", "info")
    
    # Check requirements
    requirements = check_system_requirements()
    if not all(requirements.values()):
        print_status("System requirements not met", "error")
        return False
    
    # Create virtual environment
    if not create_virtual_environment(venv_path):
        return False
    
    # Install dependencies
    if not install_dependencies(venv_path, requirements_file):
        return False
    
    # Setup NLTK data
    setup_nltk_data(venv_path)
    
    # Setup spaCy model
    setup_spacy_model(venv_path)
    
    # Create configuration files
    create_secrets_file()
    create_streamlit_config()
    
    # Create directories
    create_project_directories()
    
    # Validate installation
    if not validate_installation(venv_path):
        return False
    
    print_status("Full setup completed successfully!", "success")
    return True

def cleanup_installation(venv_path: Path) -> None:
    """Cleanup installation"""
    try:
        print_status("Cleaning up installation...", "info")
        
        if venv_path.exists():
            import shutil
            shutil.rmtree(venv_path)
            print_status("Virtual environment removed", "success")
        
        # Remove other generated files
        cleanup_files = [
            ".streamlit",
            "logs",
            "data",
            "temp",
            "cache"
        ]
        
        for file_path in cleanup_files:
            if Path(file_path).exists():
                import shutil
                shutil.rmtree(file_path)
        
        print_status("Cleanup completed", "success")
        
    except Exception as e:
        print_status(f"Cleanup failed: {e}", "error")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Resume AI Application Launcher")
    parser.add_argument("--setup", action="store_true", help="Perform full setup")
    parser.add_argument("--run", action="store_true", help="Run the application")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode")
    parser.add_argument("--check", action="store_true", help="Check requirements")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup installation")
    parser.add_argument("--port", type=int, default=8501, help="Port to run on")
    parser.add_argument("--dev", action="store_true", help="Run in development mode")
    
    args = parser.parse_args()
    
    print_header()
    
    # Default virtual environment path
    venv_path = Path("resume_ai_env")
    
    if args.check:
        requirements = check_system_requirements()
        print_status("System requirements check completed", "success")
        return
    
    if args.cleanup:
        cleanup_installation(venv_path)
        return
    
    if args.setup:
        if full_setup(venv_path):
            print_status("Setup completed! Run with --run to start the application", "success")
        else:
            print_status("Setup failed!", "error")
            return
    
    if args.run or args.demo:
        if not venv_path.exists():
            print_status("Virtual environment not found. Run --setup first", "error")
            return
        
        mode = "demo" if args.demo else "app"
        run_application(venv_path, mode, args.port, args.dev)
    
    if not any([args.setup, args.run, args.demo, args.check, args.cleanup]):
        # No arguments provided, show help
        print_status("No action specified. Use --help for available options", "warning")
        print("\nQuick start:")
        print("  python launch.py --setup    # Full setup")
        print("  python launch.py --run      # Run application")
        print("  python launch.py --check    # Check requirements")

if __name__ == "__main__":
    main()
