# Resume/CV AI - Docker Configuration
# Multi-stage Docker build for production-ready Resume AI application

# =============================================================================
# Stage 1: Base Image with Python and System Dependencies
# =============================================================================
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Essential build tools
    build-essential \
    gcc \
    g++ \
    make \
    # System libraries
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    # OCR dependencies
    tesseract-ocr \
    tesseract-ocr-eng \
    # PDF processing dependencies
    poppler-utils \
    # Image processing dependencies
    libmagic1 \
    # Network utilities
    curl \
    wget \
    # Git for version control
    git \
    # Clean up
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# =============================================================================
# Stage 2: Python Dependencies
# =============================================================================
FROM base as python-deps

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# Stage 3: Application Build
# =============================================================================
FROM python-deps as app

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create necessary directories
RUN mkdir -p /app/logs \
    /app/cache \
    /app/temp \
    /app/uploads \
    /app/downloads \
    /app/chroma_db \
    /app/faiss_index \
    && chown -R appuser:appuser /app

# Copy application code
COPY . .

# Set proper permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

# =============================================================================
# Stage 4: Production Image (Optional - for smaller production image)
# =============================================================================
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    libffi-dev \
    libssl-dev \
    libmagic1 \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python dependencies from python-deps stage
COPY --from=python-deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-deps /usr/local/bin /usr/local/bin

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create necessary directories
RUN mkdir -p /app/logs \
    /app/cache \
    /app/temp \
    /app/uploads \
    /app/downloads \
    /app/chroma_db \
    /app/faiss_index \
    && chown -R appuser:appuser /app

# Copy application code
COPY . .

# Set proper permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

# =============================================================================
# Development Image (Optional)
# =============================================================================
FROM app as development

# Install development dependencies
RUN pip install --no-cache-dir \
    pytest \
    pytest-cov \
    black \
    flake8 \
    mypy \
    ipython \
    jupyter

# Override command for development
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=true"]

# =============================================================================
# Build Instructions
# =============================================================================
# 
# Build production image:
# docker build -t resumeai:latest .
#
# Build development image:
# docker build --target development -t resumeai:dev .
#
# Run production container:
# docker run -p 8501:8501 -e OPENAI_API_KEY=your_key resumeai:latest
#
# Run development container:
# docker run -p 8501:8501 -v $(pwd):/app resumeai:dev
#
# Run with docker-compose:
# docker-compose up -d
#
# =============================================================================
# Environment Variables
# =============================================================================
# 
# Required:
# - OPENAI_API_KEY: Your OpenAI API key
# - GOOGLE_API_KEY: Your Google API key (optional)
# - ANTHROPIC_API_KEY: Your Anthropic API key (optional)
#
# Optional:
# - DATABASE_URL: Database connection string
# - REDIS_URL: Redis connection string
# - LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR)
# - APP_ENVIRONMENT: Environment (development, staging, production)
#
# =============================================================================
# Volume Mounts
# =============================================================================
# 
# For persistent data:
# - /app/logs: Application logs
# - /app/cache: Cache files
# - /app/chroma_db: Vector database
# - /app/faiss_index: FAISS index
# - /app/uploads: User uploads
# - /app/downloads: Generated files
#
# =============================================================================
# Security Notes
# =============================================================================
# 
# 1. This Dockerfile uses a non-root user for security
# 2. System dependencies are minimized
# 3. Health checks are included
# 4. Proper file permissions are set
# 5. Multi-stage build reduces image size
# 6. No sensitive data is included in the image
#
# =============================================================================
# Performance Optimizations
# =============================================================================
# 
# 1. Multi-stage build reduces final image size
# 2. Python dependencies are cached in separate layer
# 3. System dependencies are installed efficiently
# 4. Unnecessary files are cleaned up
# 5. Health checks ensure container is running properly
#
# =============================================================================
