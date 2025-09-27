"""
LinkedIn Job Scraper Installation Script
Installs all required dependencies for the LinkedIn Job Scraper integration.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def install_python_packages():
    """Install Python packages from requirements.txt"""
    print("📦 Installing Python packages...")
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False
    
    # Install packages
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing packages from requirements.txt"
    )

def install_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    
    nltk_script = """
import nltk
try:
    nltk.data.find('tokenizers/punkt')
    print("punkt already downloaded")
except LookupError:
    nltk.download('punkt')
    print("punkt downloaded")

try:
    nltk.data.find('corpora/stopwords')
    print("stopwords already downloaded")
except LookupError:
    nltk.download('stopwords')
    print("stopwords downloaded")
"""
    
    try:
        result = subprocess.run([sys.executable, "-c", nltk_script], 
                              capture_output=True, text=True, check=True)
        print("✅ NLTK data downloaded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ NLTK data download failed: {e}")
        return False

def verify_installation():
    """Verify that all components are installed correctly"""
    print("🔍 Verifying installation...")
    
    verification_script = """
import sys
try:
    # Test core imports
    import streamlit
    import pandas
    import numpy
    import plotly
    import chromadb
    import sentence_transformers
    import beautifulsoup4
    import fake_useragent
    import selenium
    import lxml
    import nltk
    import requests
    print("✅ All core packages imported successfully")
    
    # Test LinkedIn scraper imports
    from linkedin_scraper import LinkedInJobScraper, VectorDatabase
    from linkedin_scraper.helpers import clean_text, extract_skills
    print("✅ LinkedIn scraper modules imported successfully")
    
    # Test configuration
    from config.linkedin_scraper_config import get_config
    config = get_config()
    print(f"✅ Configuration loaded: {config.delay_range}")
    
    print("🎉 All verification tests passed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Verification error: {e}")
    sys.exit(1)
"""
    
    try:
        result = subprocess.run([sys.executable, "-c", verification_script], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Verification failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating necessary directories...")
    
    directories = [
        "data/linkedin_chroma_db",
        "data/exports",
        "logs",
        "temp"
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        except Exception as e:
            print(f"❌ Failed to create directory {directory}: {e}")
            return False
    
    return True

def main():
    """Main installation function"""
    print("🚀 LinkedIn Job Scraper Installation")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Installation steps
    steps = [
        ("Creating directories", create_directories),
        ("Installing Python packages", install_python_packages),
        ("Downloading NLTK data", install_nltk_data),
        ("Verifying installation", verify_installation)
    ]
    
    success_count = 0
    total_steps = len(steps)
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        if step_func():
            success_count += 1
        else:
            print(f"❌ {step_name} failed!")
            break
    
    # Summary
    print("\n" + "="*50)
    print("📊 INSTALLATION SUMMARY")
    print("="*50)
    
    if success_count == total_steps:
        print("🎉 Installation completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run the main application: streamlit run main.py")
        print("2. Navigate to 'LinkedIn Job Scraper' in the sidebar")
        print("3. Configure your search parameters and start scraping")
        print("\n⚠️  Important notes:")
        print("- Use the scraper responsibly and ethically")
        print("- Respect LinkedIn's terms of service")
        print("- The scraper includes rate limiting to avoid overloading servers")
        return True
    else:
        print(f"⚠️  Installation completed with {total_steps - success_count} failures")
        print("Please check the error messages above and try again")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
