# Resume/CV AI - Setup and Installation Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (optional, for cloning)

### Installation Steps

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd resumeai
   
   # Or download and extract the files
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv resume_ai_env
   
   # Activate virtual environment
   # On Windows:
   resume_ai_env\Scripts\activate
   
   # On macOS/Linux:
   source resume_ai_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download required NLTK data**
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

5. **Install spaCy English model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

6. **Set up environment variables**
   Create a `.streamlit/secrets.toml` file in your project directory:
   ```toml
   # .streamlit/secrets.toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```

7. **Run the application**
   ```bash
   streamlit run resume_ai_app.py
   ```

## 🔧 Configuration

### API Keys Setup
The application supports multiple AI providers:

#### Google Gemini API
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your secrets.toml file

#### OpenAI API (Optional)
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add it to your secrets.toml file

### Environment Variables
```bash
# Optional environment variables
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=localhost
```

## 📁 Project Structure
```
resumeai/
├── resume_ai_app.py          # Main application file
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── .streamlit/
│   └── secrets.toml         # API keys and secrets
├── data/                    # Data storage (auto-created)
├── templates/               # Resume templates (auto-created)
└── exports/                 # Generated reports (auto-created)
```

## 🔍 Features Overview

### 📄 Resume Analysis
- **Multi-format support**: PDF, DOCX, TXT
- **Smart parsing**: Extracts personal info, skills, experience, education
- **Section analysis**: Identifies and categorizes resume sections
- **Contact validation**: Checks for email, phone, LinkedIn profiles

### 🎯 Job Matching
- **Compatibility scoring**: Matches resume against job descriptions
- **Skill gap analysis**: Identifies missing skills and requirements
- **ATS optimization**: Checks Applicant Tracking System compatibility
- **Keyword matching**: Analyzes keyword alignment with job posts

### ✨ AI Enhancement
- **Content improvement**: Suggests better phrasing and structure
- **Achievement quantification**: Helps add metrics and numbers
- **Industry optimization**: Tailors content for specific industries
- **Grammar and style**: Improves language and professional tone

### 📊 ATS Checker
- **Format validation**: Ensures ATS-friendly formatting
- **Keyword analysis**: Checks for relevant keywords
- **Scoring system**: Provides ATS compatibility score
- **Improvement suggestions**: Specific recommendations for better ATS performance

### 🔧 Resume Builder
- **Guided creation**: Step-by-step resume building
- **AI assistance**: Smart suggestions for each section
- **Multiple formats**: Export to DOCX, PDF
- **Template integration**: Professional resume templates

### 📋 Templates
- **Industry-specific**: Templates for different professions
- **ATS-optimized**: All templates are ATS-friendly
- **Customizable**: Color schemes, fonts, layouts
- **Modern designs**: Professional and contemporary styles

### 📈 Career Insights
- **Progress tracking**: Monitor resume improvements over time
- **Analytics dashboard**: Visual insights into job applications
- **Skill development**: Track skill gap closure
- **Performance metrics**: ATS scores, interview rates

### 🎨 Customization
- **Visual styling**: Colors, fonts, layouts
- **Content organization**: Section ordering and visibility
- **Enhancement options**: Various content improvements
- **Export options**: Multiple format support

## 🛠️ Troubleshooting

### Common Issues

#### Import Errors
```bash
# If you get import errors, try:
pip install --upgrade -r requirements.txt

# For spaCy model issues:
python -m spacy download en_core_web_sm
```

#### Memory Issues
```bash
# For large documents or limited memory:
export STREAMLIT_SERVER_MEMORY_LIMIT=2048
```

#### API Connection Issues
- Check your internet connection
- Verify API keys are correctly set in secrets.toml
- Ensure API keys have proper permissions

### Performance Optimization

#### For better performance:
1. Use Python 3.9+ for better compatibility
2. Install packages in a virtual environment
3. Close unnecessary browser tabs when running
4. Use smaller PDF files when possible

## 🔐 Security Considerations

### API Key Security
- Never commit secrets.toml to version control
- Use environment variables in production
- Rotate API keys regularly
- Monitor API usage and costs

### Data Privacy
- Resume data is processed locally
- No data is stored permanently by default
- User can clear session data anytime
- Consider data encryption for sensitive information

## 🚀 Advanced Usage

### Custom AI Models
You can extend the application to use other AI models:
```python
# Add to AIHandler class
def setup_custom_model(self):
    # Your custom model setup here
    pass
```

### Additional Document Formats
To support more formats, extend the DocumentProcessor class:
```python
@staticmethod
def extract_text_from_rtf(rtf_file):
    # RTF processing logic here
    pass
```

### Database Integration
For persistent data storage, you can integrate with databases:
```python
# Example with SQLite
import sqlite3

def setup_database():
    conn = sqlite3.connect('resume_data.db')
    # Create tables, etc.
    return conn
```

## 📱 Mobile and Cloud Deployment

### Streamlit Cloud
1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Add secrets in Streamlit Cloud dashboard
4. Deploy automatically

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "resume_ai_app.py"]
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Install development dependencies:
   ```bash
   pip install pytest black flake8
   ```
4. Run tests: `pytest`
5. Format code: `black .`
6. Submit pull request

### Feature Requests
- Open GitHub issues for feature requests
- Describe the use case and expected behavior
- Include examples or mockups if applicable

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help
1. Check this README first
2. Look at the troubleshooting section
3. Search existing GitHub issues
4. Create a new issue with:
   - Python version
   - Operating system
   - Full error message
   - Steps to reproduce

### Community
- GitHub Discussions for general questions
- Stack Overflow with `streamlit` and `resumeai` tags
- Discord community for real-time help

## 🔄 Updates and Maintenance

### Keeping Updated
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update spaCy model
python -m spacy download en_core_web_sm --upgrade
```

### Version History
- v1.0.0: Initial release with core features
- v1.1.0: Added job matching and ATS checking
- v1.2.0: Enhanced AI capabilities and templates
- v1.3.0: Career insights and customization features

---

## 🎉 You're All Set!

Your Resume/CV AI Assistant is now ready to use. Open your browser to the displayed URL (usually http://localhost:8501) and start analyzing and improving your resume with AI-powered insights!

For the best experience:
1. Start with the Resume Analysis tab
2. Upload a well-formatted resume
3. Explore different features systematically
4. Save your progress and generated reports
5. Iterate and improve based on AI suggestions