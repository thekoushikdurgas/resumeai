# LinkedIn Job Scraper - Installation & Usage Guide

## Overview

The LinkedIn Job Scraper is a powerful tool integrated into the Resume AI application that allows you to scrape job postings from LinkedIn, store them in a vector database, and perform advanced analytics and semantic search.

## Features

- 🔍 **Ethical Job Scraping**: Rate-limited requests with anti-detection measures
- 💾 **Vector Database Storage**: ChromaDB for semantic search capabilities
- 📊 **Analytics Dashboard**: Interactive visualizations and market insights
- 🎯 **Smart Search**: Natural language queries and similarity matching
- 📈 **Market Analysis**: Skills demand, salary trends, and company insights

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Internet connection

### Quick Installation

#### Windows
```bash
# Run the batch file
install_linkedin_scraper.bat
```

#### Linux/Mac
```bash
# Make the script executable and run
chmod +x install_linkedin_scraper.sh
./install_linkedin_scraper.sh
```

#### Manual Installation
```bash
# Install Python packages
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Verify installation
python test_linkedin_integration.py
```

### Dependencies

The LinkedIn scraper requires the following key packages:

```
# Core scraping
beautifulsoup4>=4.12.0
fake-useragent>=1.4.0
selenium>=4.15.0
lxml>=4.9.0

# Vector database
chromadb
sentence-transformers

# Data processing
pandas>=2.1.0
numpy
plotly>=5.17.0
nltk>=3.8.1

# HTTP clients
requests>=2.31.0
urllib3>=1.26.0
```

## Usage

### Starting the Application

1. **Launch the main application:**
   ```bash
   streamlit run main.py
   ```

2. **Navigate to LinkedIn Job Scraper:**
   - Open the sidebar
   - Click on "🔍 LinkedIn Job Scraper"

### Basic Job Scraping

1. **Configure search parameters:**
   - Job Title: e.g., "Data Scientist"
   - Location: e.g., "United States"
   - Experience Level: Select from dropdown
   - Job Type: Full-time, Part-time, etc.
   - Max Pages: Number of pages to scrape (1-10)

2. **Start scraping:**
   - Click "🚀 Start Job Scraping"
   - Wait for the process to complete
   - View results in the dashboard

### Advanced Features

#### Semantic Search
- Use natural language queries
- Example: "Find Python developer jobs with machine learning experience"
- Results ranked by semantic similarity

#### Similarity Matching
- Select a job from the database
- Find similar job recommendations
- View similarity scores

#### Analytics Dashboard
- **Job Market Analytics**: Trends and insights
- **Skills Demand**: Most requested technologies
- **Salary Analysis**: Compensation by role/location
- **Company Intelligence**: Hiring patterns

#### Data Export
- Export job data to CSV
- Download analytics reports
- Share insights with others

## Configuration

### Scraper Settings

Edit `config/linkedin_scraper_config.py`:

```python
SCRAPER_CONFIG = {
    'delay_range': (2, 5),          # Delay between requests (seconds)
    'max_retries': 3,               # Retry attempts
    'max_pages_per_search': 10,     # Maximum pages to scrape
    'respect_robots_txt': True,     # Follow robots.txt
    'user_agent_rotation': True,    # Rotate user agents
}
```

### Environment Variables

Create a `.env` file:

```bash
# Scraper settings
SCRAPER_MIN_DELAY=2
SCRAPER_MAX_DELAY=5
SCRAPER_MAX_RETRIES=3
SCRAPER_MAX_PAGES=10

# Database settings
CHROMA_PERSIST_DIR=./data/linkedin_chroma_db
CHROMA_COLLECTION_NAME=linkedin_job_postings
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Cache settings
CACHE_TTL=3600
MAX_DISPLAY_JOBS=50
```

## API Reference

### LinkedInJobScraper

```python
from linkedin_scraper import LinkedInJobScraper

# Initialize scraper
scraper = LinkedInJobScraper()

# Scrape jobs
config = {
    'job_title': 'Data Scientist',
    'location': 'United States',
    'max_pages': 5
}
jobs = scraper.scrape_jobs(config)
```

### VectorDatabase

```python
from linkedin_scraper import VectorDatabase

# Initialize database
db = VectorDatabase()

# Store jobs
db.store_jobs(jobs)

# Semantic search
results = db.semantic_search("python machine learning", top_k=10)

# Find similar jobs
similar = db.find_similar_jobs(job_id, top_k=5)
```

### Helper Functions

```python
from linkedin_scraper.helpers import (
    clean_text, extract_skills, format_salary,
    extract_experience_level, generate_job_summary
)

# Clean text
clean_text("<p>Dirty HTML text</p>")

# Extract skills
skills = extract_skills("Python developer with ML experience")

# Format salary
formatted = format_salary("$80,000 - $120,000 per year")
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Reinstall packages
   pip install -r requirements.txt --force-reinstall
   ```

2. **ChromaDB Issues**
   ```bash
   # Clear database
   rm -rf ./data/linkedin_chroma_db
   ```

3. **Scraping Failures**
   - Check internet connection
   - Increase delay between requests
   - Update user agent strings

4. **Memory Issues**
   - Reduce max_pages setting
   - Process jobs in smaller batches
   - Clear browser cache

### Performance Optimization

1. **Faster Scraping**
   - Reduce delay_range in config
   - Use parallel processing (carefully)
   - Optimize page selection

2. **Better Search**
   - Optimize ChromaDB settings
   - Use caching effectively
   - Reduce search result count

3. **Memory Management**
   - Process jobs in batches
   - Clear unused variables
   - Monitor memory usage

## Legal and Ethical Considerations

### Important Notes

- ⚠️ **Educational Use Only**: This tool is for educational and personal use
- ⚠️ **Respect Terms of Service**: Follow LinkedIn's terms of service
- ⚠️ **Rate Limiting**: Built-in delays to avoid overloading servers
- ⚠️ **Public Data Only**: Only scrape publicly available information
- ⚠️ **Data Privacy**: Comply with GDPR, CCPA, and other regulations

### Best Practices

1. **Ethical Scraping**
   - Use appropriate delays between requests
   - Respect robots.txt files
   - Don't overload target servers
   - Attribute data sources properly

2. **Data Handling**
   - Store data securely
   - Respect user privacy
   - Follow data retention policies
   - Implement proper access controls

3. **Legal Compliance**
   - Check local laws and regulations
   - Obtain necessary permissions
   - Respect intellectual property rights
   - Follow platform terms of service

## Support

### Getting Help

1. **Check Documentation**: Review this README and code comments
2. **Run Tests**: Use `python test_linkedin_integration.py`
3. **Check Logs**: Review error messages and logs
4. **Community Support**: Create an issue for bugs or feature requests

### Contributing

1. **Fork Repository**: Create your own fork
2. **Create Branch**: Make changes in a feature branch
3. **Add Tests**: Include tests for new features
4. **Submit PR**: Create pull request with clear description

## Changelog

### Version 1.0.0
- Initial release
- LinkedIn job scraping functionality
- Vector database integration
- Analytics dashboard
- Semantic search capabilities

## License

This project is provided as-is for educational purposes. Users are responsible for ensuring their use complies with all applicable laws and terms of service.

## Disclaimer

This project is not affiliated with LinkedIn and is provided for educational purposes only. Users are responsible for ensuring their use complies with all applicable laws and terms of service.
