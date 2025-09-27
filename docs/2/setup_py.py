# Complete Project Setup and Installation Guide
# setup.py - Professional setup script for Resume/CV AI

from setuptools import setup, find_packages
from pathlib import Path
import os

# Read README for long description
README_PATH = Path(__file__).parent / "README.md"
if README_PATH.exists():
    with open(README_PATH, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "Resume/CV AI - Comprehensive AI-powered resume analysis and optimization tool"

# Read requirements
def read_requirements(filename):
    """Read requirements from file"""
    req_path = Path(__file__).parent / filename
    if req_path.exists():
        with open(req_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

# Core requirements (essential for basic functionality)
core_requirements = [
    "streamlit>=1.29.0",
    "pandas>=2.1.0", 
    "numpy>=1.24.0",
    "plotly>=5.17.0",
    "PyPDF2>=3.0.1",
    "python-docx>=1.1.0",
    "google-generativeai>=0.3.2",
    "openai>=1.3.0",
    "nltk>=3.8.1",
    "scikit-learn>=1.3.2",
    "requests>=2.31.0",
    "python-dateutil>=2.8.2",
    "pydantic>=2.4.0",
    "python-dotenv>=1.0.0"
]

# Optional requirements for extended functionality
extras_require = {
    "full": read_requirements("requirements.txt"),
    "dev": read_requirements("requirements-dev.txt") if Path("requirements-dev.txt").exists() else [
        "pytest>=7.4.0",
        "black>=23.9.0",
        "flake8>=6.1.0",
        "mypy>=1.6.0",
        "pre-commit>=3.4.0"
    ],
    "test": [
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
        "pytest-cov>=4.1.0",
        "pytest-mock>=3.11.0"
    ],
    "ocr": [
        "pytesseract>=0.3.10",
        "pdf2image>=1.16.3",
        "Pillow>=10.1.0"
    ],
    "advanced_ai": [
        "anthropic>=0.7.0",
        "sentence-transformers>=2.2.2",
        "transformers>=4.35.0",
        "torch>=2.1.0"
    ],
    "database": [
        "sqlalchemy>=2.0.0",
        "alembic>=1.12.0",
        "psycopg2-binary>=2.9.0"
    ],
    "cloud": [
        "boto3>=1.29.0",
        "google-cloud-storage>=2.10.0",
        "azure-storage-blob>=12.19.0"
    ],
    "monitoring": [
        "loguru>=0.7.2",
        "sentry-sdk>=1.38.0",
        "psutil>=5.9.0"
    ],
    "docs": [
        "mkdocs>=1.5.0",
        "mkdocs-material>=9.4.0",
        "sphinx>=7.2.0"
    ]
}

# Get version from version file or environment
def get_version():
    """Get version from version.py or environment variable"""
    version_path = Path(__file__).parent / "app" / "version.py"
    if version_path.exists():
        exec(open(version_path).read())
        return locals()["__version__"]
    return os.getenv("APP_VERSION", "1.0.0")

setup(
    name="resume-cv-ai",
    version=get_version(),
    author="Resume AI Team",
    author_email="contact@resumeai.com",
    description="AI-powered resume analysis, optimization, and career advancement tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thekoushikdurgas/resumeai",
    project_urls={
        "Bug Reports": "https://github.com/thekoushikdurgas/resumeai/issues",
        "Source": "https://github.com/thekoushikdurgas/resumeai",
        "Documentation": "https://resumeai.readthedocs.io/",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs", "docs.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Text Processing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Environment :: Web Environment",
        "Framework :: Streamlit",
    ],
    python_requires=">=3.8",
    install_requires=core_requirements,
    extras_require=extras_require,
    include_package_data=True,
    package_data={
        "app": [
            "ui/styles/*.css",
            "ui/assets/**/*",
        ],
        "data": [
            "templates/*.json",
            "skills/*.json",
            "samples/**/*",
        ],
        "config": [
            "*.py",
            "environments/*.py",
        ],
    },
    entry_points={
        "console_scripts": [
            "resumeai=app.main:main",
            "resumeai-setup=scripts.setup:main",
            "resumeai-demo=scripts.demo:main",
        ],
    },
    keywords=[
        "resume", "cv", "artificial intelligence", "job search", 
        "career", "ats", "recruitment", "streamlit", "nlp",
        "document processing", "text analysis", "job matching"
    ],
    zip_safe=False,
    platforms=["any"],
    license="MIT",
)