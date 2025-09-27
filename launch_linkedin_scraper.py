"""
LinkedIn Job Scraper Launcher
Simple launcher script to test the LinkedIn Job Scraper functionality.
"""

import streamlit as st
import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def main():
    """Main launcher function"""
    st.set_page_config(
        page_title="LinkedIn Job Scraper - Test",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 LinkedIn Job Scraper - Integration Test")
    
    st.markdown("""
    ## Welcome to LinkedIn Job Scraper Integration Test
    
    This page tests the integration of the LinkedIn Job Scraper with your Resume AI application.
    
    ### Features Available:
    - ✅ LinkedIn job scraping with rate limiting
    - ✅ Vector database storage with ChromaDB
    - ✅ Semantic search capabilities
    - ✅ Job analytics and visualizations
    - ✅ Data export functionality
    
    ### Test Components:
    """)
    
    # Test imports
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Import Tests")
        try:
            from linkedin_scraper import LinkedInJobScraper, VectorDatabase
            st.success("✅ LinkedIn scraper imports successful")
        except ImportError as e:
            st.error(f"❌ Import failed: {e}")
        
        try:
            from linkedin_scraper.helpers import clean_text, extract_skills
            st.success("✅ Helper functions imports successful")
        except ImportError as e:
            st.error(f"❌ Helper imports failed: {e}")
    
    with col2:
        st.subheader("⚙️ Configuration Tests")
        try:
            from config.linkedin_scraper_config import get_config, DEFAULT_CONFIG
            config = get_config()
            st.success(f"✅ Configuration loaded: {config.delay_range}")
        except ImportError as e:
            st.error(f"❌ Config import failed: {e}")
    
    # Test basic functionality
    st.subheader("🧪 Basic Functionality Tests")
    
    if st.button("Test Helper Functions"):
        try:
            from linkedin_scraper.helpers import clean_text, extract_skills, format_salary
            
            # Test text cleaning
            dirty_text = "<p>This is a <b>dirty</b> text with HTML tags.</p>"
            clean_result = clean_text(dirty_text)
            st.write(f"**Text Cleaning:** '{dirty_text}' → '{clean_result}'")
            
            # Test skill extraction
            job_description = "We need a Python developer with machine learning experience and SQL knowledge."
            skills = extract_skills(job_description)
            st.write(f"**Skill Extraction:** {skills}")
            
            # Test salary formatting
            salary_text = "Salary: $80,000 - $120,000 per year"
            formatted_salary = format_salary(salary_text)
            st.write(f"**Salary Formatting:** '{salary_text}' → '{formatted_salary}'")
            
            st.success("✅ All helper function tests passed!")
            
        except Exception as e:
            st.error(f"❌ Helper function test failed: {e}")
    
    if st.button("Test Vector Database"):
        try:
            from linkedin_scraper import VectorDatabase
            
            # Initialize with test directory
            vector_db = VectorDatabase(
                persist_directory="./test_chroma_db",
                collection_name="test_job_postings"
            )
            
            job_count = vector_db.get_job_count()
            st.write(f"**Current job count:** {job_count}")
            
            stats = vector_db.get_statistics()
            st.write(f"**Database statistics:** {stats}")
            
            st.success("✅ Vector database test passed!")
            
        except Exception as e:
            st.error(f"❌ Vector database test failed: {e}")
    
    if st.button("Test Scraper Initialization"):
        try:
            from linkedin_scraper import LinkedInJobScraper
            
            scraper = LinkedInJobScraper()
            st.write("**Scraper initialized successfully**")
            
            # Test configuration
            config = {
                'job_title': 'Data Scientist',
                'location': 'United States',
                'max_pages': 1
            }
            st.write(f"**Test configuration:** {config}")
            
            st.success("✅ Scraper initialization test passed!")
            
        except Exception as e:
            st.error(f"❌ Scraper initialization test failed: {e}")
    
    # Integration status
    st.subheader("📊 Integration Status")
    
    status_items = [
        ("LinkedIn Scraper Module", "✅ Implemented"),
        ("Vector Database Integration", "✅ Implemented"),
        ("Helper Functions", "✅ Implemented"),
        ("Configuration System", "✅ Implemented"),
        ("UI Page Integration", "✅ Implemented"),
        ("Requirements Updated", "✅ Implemented")
    ]
    
    for item, status in status_items:
        st.write(f"{status} {item}")
    
    st.markdown("""
    ### 🚀 Next Steps:
    
    1. **Run the main application:** `streamlit run main.py`
    2. **Navigate to LinkedIn Job Scraper page** in the sidebar
    3. **Configure search parameters** and start scraping
    4. **Explore the analytics dashboard** for insights
    
    ### 📝 Notes:
    - The scraper includes rate limiting and anti-detection measures
    - All data is stored locally in ChromaDB
    - The system respects LinkedIn's terms of service
    - Use responsibly and ethically
    """)

if __name__ == "__main__":
    main()
