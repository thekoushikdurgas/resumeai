# 🤖 Resume/CV AI - Comprehensive Streamlit Application

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive, production-ready AI-powered resume analysis and optimization platform built with Streamlit, featuring advanced vector database integration, multi-provider AI support, and enterprise-level architecture.

## 🌟 Key Features

### 📄 **Resume Analysis & Processing**
- **Multi-format Support**: PDF, DOCX, TXT, RTF with OCR fallback
- **AI-Powered Parsing**: Advanced content extraction and structure analysis
- **Contact Information**: Automatic extraction of name, email, phone, location
- **Skills Identification**: Categorized technical and soft skills detection
- **Experience Analysis**: Work history parsing with achievement quantification
- **Education Tracking**: Academic background and certification extraction

### 🎯 **Job Matching & Compatibility**
- **Semantic Matching**: Vector-based job-resume compatibility scoring
- **Skills Gap Analysis**: Identify missing skills and recommendations
- **Experience Alignment**: Match work experience with job requirements
- **Keyword Optimization**: ATS-friendly keyword density analysis
- **Industry-Specific**: Tailored analysis for different sectors

### ✨ **AI Enhancement & Optimization**
- **Content Improvement**: AI-powered writing suggestions and enhancements
- **ATS Optimization**: Applicant Tracking System compatibility checking
- **Achievement Quantification**: Help quantify and improve accomplishments
- **Grammar & Language**: Professional tone and language optimization
- **Industry Tailoring**: Customize content for specific industries

### 🔧 **Resume Builder & Templates**
- **AI-Assisted Creation**: Step-by-step resume building with AI guidance
- **Professional Templates**: 10+ industry-specific resume templates
- **Real-time Preview**: Live preview of resume changes
- **Multiple Export Formats**: PDF, DOCX, JSON export options
- **Customization**: Color schemes, fonts, and layout options

### 📊 **Analytics & Insights**
- **Career Insights**: Market trends and career path recommendations
- **Progress Tracking**: Application status and improvement metrics
- **Skills Development**: Learning recommendations and skill gaps
- **Salary Insights**: Market salary data and benchmarking
- **Performance Analytics**: Usage statistics and optimization metrics

### 🗄️ **Vector Database Integration**
- **Semantic Search**: Find similar resumes and job descriptions
- **Embedding Generation**: Advanced text embeddings for similarity
- **Knowledge Base**: Persistent storage of resume and job data
- **Similarity Matching**: Find related content and opportunities
- **Scalable Storage**: Handle large datasets efficiently

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional)
- API Keys for AI providers (OpenAI, Google Gemini, Anthropic Claude)

### 1. Clone Repository
```bash
git clone https://github.com/thekoushikdurgas/resumeai.git
cd resumeai
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 3. Install Dependencies
```bash
# Using pip
pip install -r requirements.txt

# Or using virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run Application
```bash
# Development mode
streamlit run main.py

# Production mode
streamlit run main.py --server.headless=true --server.port=8501
```

### 5. Access Application
Open your browser and navigate to: `http://localhost:8501`

## 🐳 Docker Deployment

### Quick Start with Docker
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f resumeai-app

# Stop services
docker-compose down
```

### Production Deployment
```bash
# Build production image
docker build -t resumeai:latest .

# Run with environment variables
docker run -d \
  -p 8501:8501 \
  -e OPENAI_API_KEY=your_key \
  -e GOOGLE_API_KEY=your_key \
  -e ANTHROPIC_API_KEY=your_key \
  resumeai:latest
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
# AI API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./resume_ai.db
REDIS_URL=redis://localhost:6379/0

# Application Settings
APP_ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG_LOGGING=true

# Feature Flags
ENABLE_AI_ANALYSIS=true
ENABLE_VECTOR_SEARCH=true
ENABLE_PDF_EXPORT=true
```

### AI Provider Setup

#### OpenAI
1. Get API key from [OpenAI Platform](https://platform.openai.com)
2. Set `OPENAI_API_KEY` in your `.env` file
3. Choose model: `gpt-4`, `gpt-3.5-turbo`, etc.

#### Google Gemini
1. Get API key from [Google AI Studio](https://makersuite.google.com)
2. Set `GOOGLE_API_KEY` in your `.env` file
3. Choose model: `gemini-pro`, `gemini-pro-vision`

#### Anthropic Claude
1. Get API key from [Anthropic Console](https://console.anthropic.com)
2. Set `ANTHROPIC_API_KEY` in your `.env` file
3. Choose model: `claude-3-sonnet-20240229`

## 🏗️ Architecture

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   FastAPI API   │    │   AI Services   │
│                 │    │                 │    │                 │
│ • Analysis Tab  │◄──►│ • REST Endpoints│◄──►│ • OpenAI        │
│ • Job Matching  │    │ • Authentication│    │ • Google Gemini │
│ • Enhancement   │    │ • Rate Limiting │    │ • Anthropic     │
│ • Templates     │    │ • Validation    │    │ • Embeddings    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Vector Database│    │   File Storage  │    │   Monitoring    │
│                 │    │                 │    │                 │
│ • ChromaDB      │    │ • Local Storage │    │ • Prometheus    │
│ • FAISS Index   │    │ • AWS S3        │    │ • Grafana       │
│ • Embeddings    │    │ • Azure Blob    │    │ • Logging       │
│ • Similarity    │    │ • Google Cloud  │    │ • Analytics     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack
- **Frontend**: Streamlit, HTML/CSS, JavaScript
- **Backend**: Python, FastAPI, SQLAlchemy
- **AI/ML**: OpenAI, Google Gemini, Anthropic Claude, SentenceTransformers
- **Vector DB**: ChromaDB, FAISS
- **Database**: PostgreSQL, SQLite, Redis
- **Document Processing**: PyPDF2, python-docx, Tesseract OCR
- **Deployment**: Docker, Docker Compose, Nginx
- **Monitoring**: Prometheus, Grafana, ELK Stack

## 📁 Project Structure

```
resumeai/
├── 📄 main.py                    # Main Streamlit application
├── 📄 requirements.txt           # Python dependencies
├── 📄 Dockerfile                 # Docker configuration
├── 📄 docker-compose.yml         # Multi-service setup
├── 📄 Makefile                   # Build automation
├── 📄 .env.example               # Environment template
├── 📄 .gitignore                 # Git ignore rules
│
├── 📁 core/                      # Core business logic
│   ├── ai_handler.py             # AI model integrations
│   ├── document_processor.py     # Document processing
│   ├── resume_analyzer.py        # Resume analysis
│   ├── job_matcher.py            # Job matching
│   ├── ats_checker.py            # ATS compatibility
│   ├── resume_builder.py         # Resume creation
│   └── vector_db.py              # Vector database
│
├── 📁 ui/                        # User interface
│   ├── 📁 tabs/                  # Feature tabs
│   ├── 📁 components/            # Reusable components
│   ├── 📁 pages/                 # Full-page components
│   └── 📁 styles/                # Styling and themes
│
├── 📁 models/                    # Data models
│   ├── resume_model.py           # Resume data structures
│   ├── job_model.py              # Job description models
│   └── analysis_model.py         # Analysis result models
│
├── 📁 services/                  # External services
│   ├── ai_service.py             # AI service abstraction
│   ├── storage_service.py        # File storage
│   └── email_service.py          # Email notifications
│
├── 📁 utils/                     # Utility functions
│   ├── text_processing.py        # Text utilities
│   ├── file_handler.py           # File operations
│   └── logger.py                 # Logging configuration
│
├── 📁 data/                      # Data and templates
│   ├── 📁 templates/             # Resume templates
│   ├── 📁 skills/                # Skills databases
│   └── 📁 samples/               # Sample data
│
└── 📁 tests/                     # Test suites
    ├── 📁 unit/                  # Unit tests
    ├── 📁 integration/           # Integration tests
    └── 📁 performance/           # Performance tests
```

## 🧪 Testing

### Run Tests
```bash
# All tests
make test

# Unit tests only
make test-unit

# Integration tests
make test-integration

# With coverage
make test-coverage
```

### Test Structure
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Load and stress testing
- **UI Tests**: Streamlit interface testing

## 🔧 Development

### Development Setup
```bash
# Complete development setup
make dev-setup

# Install development dependencies
make install-dev

# Run in development mode
make run-dev
```

### Code Quality
```bash
# Run all quality checks
make quality

# Format code
make format

# Lint code
make lint

# Type checking
make type-check

# Security checks
make security-check
```

### Database Management
```bash
# Initialize database
make db-init

# Run migrations
make db-migrate

# Create backup
make db-backup

# Reset database (WARNING: Deletes all data)
make db-reset
```

## 📊 Monitoring & Analytics

### Application Monitoring
- **Health Checks**: Automated health monitoring
- **Performance Metrics**: Response times and throughput
- **Error Tracking**: Comprehensive error logging
- **Usage Analytics**: User behavior and feature usage

### Logging
- **Structured Logging**: JSON-formatted logs
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Log Rotation**: Automatic log file management
- **Centralized Logging**: ELK Stack integration

### Metrics Dashboard
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and alerting
- **Custom Dashboards**: Application-specific metrics
- **Real-time Monitoring**: Live performance data

## 🚀 Deployment

### Production Deployment
```bash
# Build production image
make docker-build

# Deploy to production
make prod-deploy

# Start monitoring
make monitor
```

### Environment-Specific Configurations
- **Development**: Hot reload, debug mode, verbose logging
- **Staging**: Production-like with test data
- **Production**: Optimized performance, security hardening

### Scaling Options
- **Horizontal Scaling**: Multiple container instances
- **Load Balancing**: Nginx reverse proxy
- **Database Scaling**: Read replicas, connection pooling
- **Caching**: Redis for session and data caching

## 🔒 Security

### Security Features
- **Authentication**: JWT-based user authentication
- **Authorization**: Role-based access control
- **Rate Limiting**: API abuse prevention
- **Input Validation**: Comprehensive data validation
- **Encryption**: Data encryption at rest and in transit
- **Security Headers**: CORS, CSP, and security headers

### Security Best Practices
- **API Key Management**: Secure storage and rotation
- **Dependency Scanning**: Regular security updates
- **Code Analysis**: Static security analysis
- **Penetration Testing**: Regular security assessments

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run quality checks
6. Submit a pull request

### Code Standards
- **Python**: PEP 8 compliance
- **Documentation**: Comprehensive docstrings
- **Testing**: Minimum 80% coverage
- **Type Hints**: Full type annotation
- **Security**: Security-first development

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Comprehensive guides and API docs
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Community**: Discord/Slack community (coming soon)

### Troubleshooting
- **Common Issues**: See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **FAQ**: Frequently Asked Questions
- **Debug Mode**: Enable debug logging for detailed information

## 🗺️ Roadmap

### Upcoming Features
- **Mobile App**: React Native mobile application
- **Advanced Analytics**: Machine learning insights
- **Team Collaboration**: Multi-user resume sharing
- **API Integration**: Third-party job board APIs
- **Advanced Templates**: More industry-specific templates
- **Real-time Collaboration**: Live editing capabilities

### Version History
- **v1.0.0**: Initial release with core features
- **v1.1.0**: Enhanced AI capabilities (planned)
- **v1.2.0**: Mobile application (planned)
- **v2.0.0**: Advanced analytics and ML features (planned)

## 🙏 Acknowledgments

- **OpenAI**: For GPT models and API
- **Google**: For Gemini AI models
- **Anthropic**: For Claude AI models
- **Streamlit**: For the amazing web framework
- **ChromaDB**: For vector database capabilities
- **Community**: For feedback and contributions

---

**Built with ❤️ by the Resume AI Team**

For more information, visit our [documentation](docs/) or [website](https://resumeai.com).