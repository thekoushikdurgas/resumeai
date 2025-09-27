# Resume/CV AI - Comprehensive Streamlit Application
# Advanced AI-powered resume management, analysis, and optimization tool

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import base64
import json
import re
import hashlib
import zipfile
from pathlib import Path
import tempfile
import os

# Third-party imports for AI and document processing
try:
    import PyPDF2
    import docx
    from docx import Document
    from docx.shared import Inches
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    from PIL import Image
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from collections import Counter
    import spacy
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    import requests
    import torch
except ImportError as e:
    st.error(f"Missing required package: {e}. Please install it using pip install {e.name}")

# Page configuration
st.set_page_config(
    page_title="Resume/CV AI Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }
    
    .success-text {
        color: #28a745;
        font-weight: 600;
    }
    
    .warning-text {
        color: #ffc107;
        font-weight: 600;
    }
    
    .error-text {
        color: #dc3545;
        font-weight: 600;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0 0;
        color: #262730;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize session state variables"""
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = {}
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'job_descriptions' not in st.session_state:
        st.session_state.job_descriptions = []
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {
            'ai_model': 'huggingface-dialoGPT',
            'analysis_depth': 'comprehensive',
            'output_format': 'detailed'
        }

# AI Configuration - Hugging Face Only
class AIHandler:
    def __init__(self):
        self.setup_ai_models()
    
    def setup_ai_models(self):
        """Setup Hugging Face AI models and configurations"""
        # Setup Hugging Face API key
        self.hf_api_key = st.secrets.get("HUGGINGFACE_API_KEY")
        
        # Set device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize Hugging Face text generation pipeline
        try:
            self.text_generation_pipeline = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",
                device=0 if self.device == "cuda" else -1
            )
        except Exception as e:
            st.warning(f"Could not load text generation model: {e}")
            self.text_generation_pipeline = None
        
        # Initialize sentence transformer for embeddings
        try:
            self.sentence_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        except Exception as e:
            st.warning(f"Could not load sentence transformer: {e}")
            self.sentence_model = None
        
        # Download required NLTK data
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
        except:
            pass
    
    def generate_ai_response(self, prompt, context=""):
        """Generate AI response using Hugging Face models"""
        if self.text_generation_pipeline:
            try:
                full_prompt = f"{context}\n\n{prompt}" if context else prompt
                
                # Configure generation parameters
                generation_kwargs = {
                    "max_new_tokens": 2000,
                    "temperature": 0.7,
                    "do_sample": True,
                    "pad_token_id": self.text_generation_pipeline.tokenizer.eos_token_id
                }
                
                # Generate response
                result = self.text_generation_pipeline(full_prompt, **generation_kwargs)
                
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '')
                elif isinstance(result, dict):
                    return result.get('generated_text', '')
                else:
                    return str(result)
            except Exception as e:
                return f"AI service unavailable: {str(e)}"
        else:
            return "AI service not configured. Please check your Hugging Face setup."

# Document Processing Classes
class DocumentProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(docx_file):
        """Extract text from DOCX file"""
        try:
            doc = Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_from_txt(txt_file):
        """Extract text from TXT file"""
        try:
            return txt_file.getvalue().decode('utf-8')
        except Exception as e:
            st.error(f"Error reading TXT: {str(e)}")
            return ""

class ResumeAnalyzer:
    def __init__(self, ai_handler):
        self.ai_handler = ai_handler
    
    def parse_resume_sections(self, text):
        """Parse resume into structured sections"""
        sections = {
            'personal_info': self.extract_personal_info(text),
            'education': self.extract_education(text),
            'experience': self.extract_experience(text),
            'skills': self.extract_skills(text),
            'projects': self.extract_projects(text),
            'certifications': self.extract_certifications(text)
        }
        return sections
    
    def extract_personal_info(self, text):
        """Extract personal information from resume text"""
        info = {}
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        info['email'] = emails[0] if emails else ""
        
        # Extract phone numbers
        phone_pattern = r'[\+]?[\d\s\-\(\)]{10,}'
        phones = re.findall(phone_pattern, text)
        info['phone'] = phones[0] if phones else ""
        
        # Extract LinkedIn profile
        linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
        linkedin = re.findall(linkedin_pattern, text.lower())
        info['linkedin'] = linkedin[0] if linkedin else ""
        
        # Extract name (simplified approach)
        lines = text.split('\n')[:5]  # Check first 5 lines
        for line in lines:
            if line.strip() and len(line.split()) >= 2 and not any(char.isdigit() for char in line):
                if '@' not in line and 'phone' not in line.lower():
                    info['name'] = line.strip()
                    break
        
        return info
    
    def extract_education(self, text):
        """Extract education information"""
        education_keywords = ['education', 'academic', 'university', 'college', 'degree', 'bachelor', 'master', 'phd']
        education_section = self.find_section(text, education_keywords)
        return education_section
    
    def extract_experience(self, text):
        """Extract work experience"""
        experience_keywords = ['experience', 'employment', 'work', 'career', 'professional']
        experience_section = self.find_section(text, experience_keywords)
        return experience_section
    
    def extract_skills(self, text):
        """Extract skills from resume"""
        skills_keywords = ['skills', 'technical', 'competencies', 'expertise']
        skills_section = self.find_section(text, skills_keywords)
        
        # Common technical skills
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node', 'express',
            'django', 'flask', 'spring', 'hibernate', 'mysql', 'postgresql', 'mongodb',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'jenkins', 'ci/cd',
            'html', 'css', 'sass', 'bootstrap', 'tailwind', 'figma', 'photoshop'
        ]
        
        found_skills = []
        text_lower = text.lower()
        for skill in tech_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return {'section': skills_section, 'parsed_skills': found_skills}
    
    def extract_projects(self, text):
        """Extract projects information"""
        project_keywords = ['projects', 'portfolio', 'work samples']
        return self.find_section(text, project_keywords)
    
    def extract_certifications(self, text):
        """Extract certifications"""
        cert_keywords = ['certifications', 'certificates', 'licenses', 'credentials']
        return self.find_section(text, cert_keywords)
    
    def find_section(self, text, keywords):
        """Find and extract section based on keywords"""
        lines = text.split('\n')
        section_start = -1
        
        for i, line in enumerate(lines):
            if any(keyword.lower() in line.lower() for keyword in keywords):
                section_start = i
                break
        
        if section_start == -1:
            return ""
        
        # Extract section content
        section_content = []
        for i in range(section_start, min(section_start + 10, len(lines))):
            line = lines[i].strip()
            if line:
                section_content.append(line)
        
        return '\n'.join(section_content)
    
    def calculate_ats_score(self, resume_text, job_description=""):
        """Calculate ATS compatibility score"""
        score = 100
        issues = []
        recommendations = []
        
        # Check basic formatting
        if len(resume_text) < 500:
            score -= 20
            issues.append("Resume too short")
            recommendations.append("Add more detailed descriptions of your experience")
        
        # Check for contact information
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
            score -= 15
            issues.append("Missing email address")
            recommendations.append("Include a professional email address")
        
        if not re.search(r'[\d\s\-\(\)]{10,}', resume_text):
            score -= 10
            issues.append("Missing phone number")
            recommendations.append("Add your phone number for contact")
        
        # Check for keywords if job description provided
        if job_description:
            job_words = set(word_tokenize(job_description.lower()))
            resume_words = set(word_tokenize(resume_text.lower()))
            
            # Remove stopwords
            try:
                stop_words = set(stopwords.words('english'))
                job_words = job_words - stop_words
                resume_words = resume_words - stop_words
            except:
                pass
            
            common_words = job_words.intersection(resume_words)
            keyword_match_ratio = len(common_words) / len(job_words) if job_words else 0
            
            if keyword_match_ratio < 0.3:
                score -= 25
                issues.append("Low keyword match with job description")
                recommendations.append("Include more relevant keywords from the job description")
        
        return max(0, score), issues, recommendations

class JobMatcher:
    def __init__(self, ai_handler):
        self.ai_handler = ai_handler
    
    def analyze_job_fit(self, resume_sections, job_description):
        """Analyze how well resume fits a job description"""
        analysis = {
            'overall_score': 0,
            'skill_match': self.calculate_skill_match(resume_sections, job_description),
            'experience_match': self.calculate_experience_match(resume_sections, job_description),
            'education_match': self.calculate_education_match(resume_sections, job_description),
            'missing_skills': [],
            'recommendations': []
        }
        
        # Calculate overall score
        analysis['overall_score'] = (
            analysis['skill_match'] * 0.4 +
            analysis['experience_match'] * 0.4 +
            analysis['education_match'] * 0.2
        )
        
        return analysis
    
    def calculate_skill_match(self, resume_sections, job_description):
        """Calculate skill match percentage"""
        resume_skills = resume_sections.get('skills', {}).get('parsed_skills', [])
        
        # Extract skills from job description
        job_skills = self.extract_skills_from_job_description(job_description)
        
        if not job_skills:
            return 50  # Default score if no skills found
        
        matched_skills = set(skill.lower() for skill in resume_skills) & set(skill.lower() for skill in job_skills)
        return (len(matched_skills) / len(job_skills)) * 100 if job_skills else 0
    
    def calculate_experience_match(self, resume_sections, job_description):
        """Calculate experience match percentage"""
        # Simplified experience matching based on keywords
        experience_text = resume_sections.get('experience', '').lower()
        job_desc_lower = job_description.lower()
        
        # Common experience keywords
        exp_keywords = ['years', 'experience', 'worked', 'developed', 'managed', 'led', 'created']
        
        matches = sum(1 for keyword in exp_keywords if keyword in experience_text and keyword in job_desc_lower)
        return min(matches * 15, 100)  # Max 100%
    
    def calculate_education_match(self, resume_sections, job_description):
        """Calculate education match percentage"""
        education_text = resume_sections.get('education', '').lower()
        job_desc_lower = job_description.lower()
        
        # Education keywords
        edu_keywords = ['degree', 'bachelor', 'master', 'phd', 'university', 'college']
        
        matches = sum(1 for keyword in edu_keywords if keyword in education_text and keyword in job_desc_lower)
        return min(matches * 20, 100)  # Max 100%
    
    def extract_skills_from_job_description(self, job_description):
        """Extract skills mentioned in job description"""
        # Common technical skills
        all_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node', 'express',
            'django', 'flask', 'spring', 'hibernate', 'mysql', 'postgresql', 'mongodb',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'jenkins', 'ci/cd',
            'html', 'css', 'sass', 'bootstrap', 'tailwind', 'figma', 'photoshop',
            'machine learning', 'data science', 'tensorflow', 'pytorch', 'pandas',
            'numpy', 'scikit-learn', 'tableau', 'power bi', 'excel', 'sql'
        ]
        
        found_skills = []
        job_desc_lower = job_description.lower()
        
        for skill in all_skills:
            if skill in job_desc_lower:
                found_skills.append(skill.title())
        
        return found_skills

# Main Application Class
class ResumeAIApp:
    def __init__(self):
        initialize_session_state()
        self.ai_handler = AIHandler()
        self.doc_processor = DocumentProcessor()
        self.resume_analyzer = ResumeAnalyzer(self.ai_handler)
        self.job_matcher = JobMatcher(self.ai_handler)
    
    def run(self):
        """Main application runner"""
        # Header
        st.markdown('<h1 class="main-header">🤖 Resume/CV AI Assistant</h1>', unsafe_allow_html=True)
        st.markdown("**Your comprehensive AI-powered resume companion for analysis, optimization, and career advancement**")
        
        # Sidebar
        self.render_sidebar()
        
        # Main content
        self.render_main_content()
    
    def render_sidebar(self):
        """Render sidebar with navigation and settings"""
        with st.sidebar:
            st.image("https://via.placeholder.com/300x150/667eea/white?text=Resume+AI", caption="Resume AI Assistant")
            
            st.markdown("### 🚀 Features")
            st.markdown("""
            - **📄 Resume Analysis** - Parse and analyze your resume
            - **🎯 Job Matching** - Match resume with job descriptions
            - **📊 ATS Scoring** - Check ATS compatibility
            - **✨ AI Enhancement** - Get AI-powered improvements
            - **📈 Career Insights** - Track your progress
            - **🔧 Resume Builder** - Create new resumes
            - **📋 Templates** - Professional resume templates
            - **🎨 Customization** - Personalize your resume
            """)
            
            st.markdown("### ⚙️ Settings")
            st.session_state.user_preferences['ai_model'] = st.selectbox(
                "AI Model",
                ["gemini-1.5-flash", "gpt-3.5-turbo", "claude-3"],
                index=0
            )
            
            st.session_state.user_preferences['analysis_depth'] = st.selectbox(
                "Analysis Depth",
                ["quick", "standard", "comprehensive"],
                index=2
            )
            
            st.markdown("### 📊 Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Resumes Analyzed", len(st.session_state.analysis_history))
            with col2:
                st.metric("Avg ATS Score", "85%" if st.session_state.analysis_history else "N/A")
    
    def render_main_content(self):
        """Render main content with tabs"""
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📄 Resume Analysis", "🎯 Job Matching", "✨ AI Enhancement", 
            "📊 ATS Checker", "🔧 Resume Builder", "📋 Templates", 
            "📈 Career Insights", "🎨 Customization"
        ])
        
        with tab1:
            self.render_resume_analysis_tab()
        
        with tab2:
            self.render_job_matching_tab()
        
        with tab3:
            self.render_ai_enhancement_tab()
        
        with tab4:
            self.render_ats_checker_tab()
        
        with tab5:
            self.render_resume_builder_tab()
        
        with tab6:
            self.render_templates_tab()
        
        with tab7:
            self.render_career_insights_tab()
        
        with tab8:
            self.render_customization_tab()
    
    def render_resume_analysis_tab(self):
        """Render resume analysis tab"""
        st.header("📄 Resume Analysis")
        st.write("Upload your resume to get comprehensive AI-powered analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Upload Resume",
                type=['pdf', 'docx', 'txt'],
                help="Supported formats: PDF, DOCX, TXT"
            )
            
            if uploaded_file:
                # Extract text based on file type
                if uploaded_file.type == "application/pdf":
                    text = self.doc_processor.extract_text_from_pdf(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = self.doc_processor.extract_text_from_docx(uploaded_file)
                else:
                    text = self.doc_processor.extract_text_from_txt(uploaded_file)
                
                if text:
                    st.success("✅ Resume uploaded successfully!")
                    
                    # Analyze resume
                    with st.spinner("🔍 Analyzing your resume..."):
                        sections = self.resume_analyzer.parse_resume_sections(text)
                        st.session_state.resume_data = {
                            'text': text,
                            'sections': sections,
                            'filename': uploaded_file.name,
                            'upload_date': datetime.now().isoformat()
                        }
                    
                    # Display analysis results
                    self.display_resume_analysis(sections)
        
        with col2:
            st.markdown("""
            ### 💡 Tips for Better Analysis
            
            **File Format:**
            - PDF files work best
            - Avoid scanned images
            - Use standard fonts
            
            **Content Structure:**
            - Clear section headings
            - Consistent formatting
            - Bullet points for experiences
            
            **Information Quality:**
            - Include contact details
            - Quantify achievements
            - Use action verbs
            """)
    
    def display_resume_analysis(self, sections):
        """Display resume analysis results"""
        st.subheader("📋 Analysis Results")
        
        # Personal Information
        if sections['personal_info']:
            with st.expander("👤 Personal Information", expanded=True):
                info = sections['personal_info']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Name:** {info.get('name', 'Not found')}")
                with col2:
                    st.write(f"**Email:** {info.get('email', 'Not found')}")
                with col3:
                    st.write(f"**Phone:** {info.get('phone', 'Not found')}")
                
                if info.get('linkedin'):
                    st.write(f"**LinkedIn:** {info['linkedin']}")
        
        # Skills
        if sections['skills']:
            with st.expander("🛠️ Skills Analysis", expanded=True):
                skills_data = sections['skills']
                if skills_data.get('parsed_skills'):
                    st.write("**Identified Technical Skills:**")
                    skills_df = pd.DataFrame({
                        'Skill': skills_data['parsed_skills'],
                        'Category': ['Technical'] * len(skills_data['parsed_skills'])
                    })
                    st.dataframe(skills_df, use_container_width=True)
                
                if skills_data.get('section'):
                    st.text_area("Skills Section", skills_data['section'], height=100)
        
        # Experience
        if sections['experience']:
            with st.expander("💼 Experience Summary"):
                st.text_area("Experience Section", sections['experience'], height=150)
        
        # Education
        if sections['education']:
            with st.expander("🎓 Education Background"):
                st.text_area("Education Section", sections['education'], height=100)
        
        # Quick Actions
        st.subheader("🎯 Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Check ATS Score", type="primary"):
                st.switch_page("ATS Checker")  # This would switch to ATS tab
        
        with col2:
            if st.button("✨ Get AI Suggestions"):
                st.switch_page("AI Enhancement")  # This would switch to Enhancement tab
        
        with col3:
            if st.button("🎯 Match with Job"):
                st.switch_page("Job Matching")  # This would switch to Job Matching tab
        
        with col4:
            if st.button("📄 Generate Report"):
                self.generate_analysis_report(sections)
    
    def render_job_matching_tab(self):
        """Render job matching tab"""
        st.header("🎯 Job Matching Analysis")
        st.write("Compare your resume against specific job descriptions")
        
        # Check if resume is uploaded
        if 'resume_data' not in st.session_state or not st.session_state.resume_data:
            st.warning("⚠️ Please upload a resume in the Resume Analysis tab first.")
            return
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Job description input
            st.subheader("📋 Job Description")
            job_description = st.text_area(
                "Paste the job description here",
                height=300,
                placeholder="Paste the complete job description including requirements, responsibilities, and qualifications..."
            )
            
            if job_description and st.button("🔍 Analyze Job Match", type="primary"):
                with st.spinner("🎯 Analyzing job match..."):
                    # Perform job matching analysis
                    resume_sections = st.session_state.resume_data['sections']
                    match_analysis = self.job_matcher.analyze_job_fit(resume_sections, job_description)
                    
                    # Display results
                    self.display_job_match_results(match_analysis, job_description)
        
        with col2:
            st.markdown("""
            ### 🎯 Job Matching Features
            
            **What we analyze:**
            - Skill alignment
            - Experience relevance
            - Education requirements
            - Keyword matching
            
            **Get insights on:**
            - Overall compatibility score
            - Missing skills
            - Improvement suggestions
            - ATS optimization
            
            **Pro Tips:**
            - Use complete job descriptions
            - Include requirements section
            - Check multiple positions
            """)
    
    def display_job_match_results(self, match_analysis, job_description):
        """Display job matching results"""
        st.subheader("📊 Job Match Results")
        
        # Overall Score
        overall_score = match_analysis['overall_score']
        
        # Score color coding
        if overall_score >= 80:
            score_color = "success"
            score_text = "Excellent Match!"
        elif overall_score >= 60:
            score_color = "warning"
            score_text = "Good Match"
        else:
            score_color = "error"
            score_text = "Needs Improvement"
        
        # Display overall score
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Match Score", f"{overall_score:.1f}%", delta=None)
        with col2:
            st.metric("Skill Match", f"{match_analysis['skill_match']:.1f}%")
        with col3:
            st.metric("Experience Match", f"{match_analysis['experience_match']:.1f}%")
        
        # Detailed breakdown
        st.subheader("🔍 Detailed Analysis")
        
        # Create visualization
        categories = ['Skills', 'Experience', 'Education']
        scores = [
            match_analysis['skill_match'],
            match_analysis['experience_match'], 
            match_analysis['education_match']
        ]
        
        fig = px.bar(
            x=categories,
            y=scores,
            title="Match Score Breakdown",
            color=scores,
            color_continuous_scale="RdYlGn",
            range_color=[0, 100]
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # AI-generated recommendations
        st.subheader("🤖 AI Recommendations")
        with st.spinner("Generating personalized recommendations..."):
            recommendations_prompt = f"""
            Analyze this job match scenario and provide specific recommendations:
            
            Job Description: {job_description[:1000]}...
            
            Match Scores:
            - Overall: {overall_score:.1f}%
            - Skills: {match_analysis['skill_match']:.1f}%
            - Experience: {match_analysis['experience_match']:.1f}%
            - Education: {match_analysis['education_match']:.1f}%
            
            Provide 5 specific, actionable recommendations to improve the match score.
            """
            
            ai_recommendations = self.ai_handler.generate_ai_response(recommendations_prompt)
            st.write(ai_recommendations)
    
    def render_ai_enhancement_tab(self):
        """Render AI enhancement tab"""
        st.header("✨ AI-Powered Resume Enhancement")
        st.write("Get intelligent suggestions to improve your resume")
        
        # Check if resume is uploaded
        if 'resume_data' not in st.session_state or not st.session_state.resume_data:
            st.warning("⚠️ Please upload a resume in the Resume Analysis tab first.")
            return
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🎯 Enhancement Options")
            
            enhancement_type = st.selectbox(
                "Choose enhancement type:",
                [
                    "General Resume Improvement",
                    "ATS Optimization",
                    "Industry-Specific Enhancement",
                    "Skill Enhancement Suggestions",
                    "Language and Grammar Check",
                    "Format and Structure Review"
                ]
            )
            
            # Industry selection for industry-specific enhancement
            if enhancement_type == "Industry-Specific Enhancement":
                industry = st.selectbox(
                    "Select target industry:",
                    [
                        "Technology/Software",
                        "Healthcare",
                        "Finance/Banking",
                        "Marketing/Sales",
                        "Education",
                        "Engineering",
                        "Consulting",
                        "Other"
                    ]
                )
            else:
                industry = None
            
            # Job description for context (optional)
            st.subheader("📋 Job Context (Optional)")
            job_context = st.text_area(
                "Provide job description for targeted enhancement:",
                height=150,
                placeholder="Paste job description here for more targeted suggestions..."
            )
            
            if st.button("🚀 Generate Enhancement Suggestions", type="primary"):
                with st.spinner("🤖 AI is analyzing your resume and generating suggestions..."):
                    suggestions = self.generate_enhancement_suggestions(
                        enhancement_type, 
                        industry, 
                        job_context
                    )
                    self.display_enhancement_suggestions(suggestions)
        
        with col2:
            st.markdown("""
            ### 💡 Enhancement Types
            
            **General Improvement:**
            - Content optimization
            - Achievement highlighting
            - Action verb suggestions
            
            **ATS Optimization:**
            - Keyword integration
            - Format compatibility
            - Section structure
            
            **Industry-Specific:**
            - Relevant skills focus
            - Industry terminology
            - Best practices
            
            **Skill Enhancement:**
            - Gap identification
            - Learning recommendations
            - Certification suggestions
            """)
    
    def generate_enhancement_suggestions(self, enhancement_type, industry, job_context):
        """Generate AI-powered enhancement suggestions"""
        resume_text = st.session_state.resume_data['text']
        sections = st.session_state.resume_data['sections']
        
        # Create comprehensive prompt
        base_prompt = f"""
        As an expert resume consultant and career advisor, analyze the following resume and provide specific, actionable enhancement suggestions.
        
        Resume Content:
        {resume_text[:2000]}...
        
        Enhancement Focus: {enhancement_type}
        """
        
        if industry:
            base_prompt += f"\nTarget Industry: {industry}"
        
        if job_context:
            base_prompt += f"\nJob Context: {job_context[:500]}..."
        
        enhancement_prompts = {
            "General Resume Improvement": base_prompt + """
            
            Provide 8-10 specific suggestions to improve this resume including:
            1. Content improvements for each section
            2. Achievement quantification opportunities
            3. Action verb enhancements
            4. Structure and flow improvements
            5. Missing information that should be added
            """,
            
            "ATS Optimization": base_prompt + """
            
            Focus on ATS (Applicant Tracking System) optimization:
            1. Keyword optimization suggestions
            2. Format improvements for ATS parsing
            3. Section header standardization
            4. File format recommendations
            5. Common ATS pitfalls to avoid
            """,
            
            "Industry-Specific Enhancement": base_prompt + """
            
            Provide industry-specific enhancement suggestions:
            1. Relevant skills to highlight/add
            2. Industry-specific terminology to use
            3. Certifications or qualifications to pursue
            4. Experience presentation best practices
            5. Industry trends to address
            """,
            
            "Skill Enhancement Suggestions": base_prompt + """
            
            Focus on skill-related improvements:
            1. Technical skills gaps to fill
            2. Soft skills to highlight better
            3. Certification recommendations
            4. Learning path suggestions
            5. Skill presentation improvements
            """,
            
            "Language and Grammar Check": base_prompt + """
            
            Review language and grammar:
            1. Grammar and syntax improvements
            2. Professional tone enhancements
            3. Conciseness improvements
            4. Clarity and readability
            5. Professional language alternatives
            """,
            
            "Format and Structure Review": base_prompt + """
            
            Review format and structure:
            1. Section organization improvements
            2. Visual hierarchy suggestions
            3. Length optimization
            4. Readability enhancements
            5. Professional presentation tips
            """
        }
        
        prompt = enhancement_prompts.get(enhancement_type, base_prompt)
        return self.ai_handler.generate_ai_response(prompt)
    
    def display_enhancement_suggestions(self, suggestions):
        """Display enhancement suggestions"""
        st.subheader("🤖 AI Enhancement Suggestions")
        
        # Display suggestions in an attractive format
        st.markdown(suggestions)
        
        # Action buttons
        st.subheader("📋 Next Steps")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📄 Generate Report"):
                self.generate_enhancement_report(suggestions)
        
        with col2:
            if st.button("📧 Email Report"):
                st.info("Email functionality would be implemented here")
        
        with col3:
            if st.button("💾 Save Suggestions"):
                self.save_suggestions_to_history(suggestions)
        
        with col4:
            if st.button("🔄 Get More Ideas"):
                st.rerun()  # Regenerate suggestions
    
    def render_ats_checker_tab(self):
        """Render ATS checker tab"""
        st.header("📊 ATS Compatibility Checker")
        st.write("Check how well your resume performs with Applicant Tracking Systems")
        
        # Check if resume is uploaded
        if 'resume_data' not in st.session_state or not st.session_state.resume_data:
            st.warning("⚠️ Please upload a resume in the Resume Analysis tab first.")
            return
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🔍 ATS Analysis")
            
            # Job description for targeted ATS scoring
            job_desc_for_ats = st.text_area(
                "Job Description (Optional - for targeted ATS scoring):",
                height=200,
                placeholder="Paste job description here for more accurate ATS scoring..."
            )
            
            if st.button("🚀 Run ATS Analysis", type="primary"):
                with st.spinner("🔍 Analyzing ATS compatibility..."):
                    resume_text = st.session_state.resume_data['text']
                    ats_score, issues, recommendations = self.resume_analyzer.calculate_ats_score(
                        resume_text, job_desc_for_ats
                    )
                    
                    self.display_ats_results(ats_score, issues, recommendations)
        
        with col2:
            st.markdown("""
            ### 🎯 ATS Checker Features
            
            **What we check:**
            - Contact information presence
            - Keyword optimization
            - Format compatibility
            - Section structure
            - File format issues
            
            **ATS Best Practices:**
            - Use standard fonts
            - Avoid graphics/images
            - Include relevant keywords
            - Use simple formatting
            - Save as PDF or DOCX
            
            **Score Ranges:**
            - 90-100: Excellent
            - 70-89: Good
            - 50-69: Fair
            - Below 50: Needs work
            """)
    
    def display_ats_results(self, ats_score, issues, recommendations):
        """Display ATS analysis results"""
        st.subheader("📊 ATS Analysis Results")
        
        # Score display with color coding
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if ats_score >= 90:
                st.success(f"🎉 ATS Score: {ats_score}/100")
                st.success("Excellent ATS compatibility!")
            elif ats_score >= 70:
                st.warning(f"⚠️ ATS Score: {ats_score}/100")
                st.warning("Good compatibility with room for improvement")
            else:
                st.error(f"❌ ATS Score: {ats_score}/100")
                st.error("Needs significant improvement")
        
        with col2:
            st.metric("Issues Found", len(issues))
        
        with col3:
            st.metric("Recommendations", len(recommendations))
        
        # Score visualization
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = ats_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "ATS Compatibility Score"},
            delta = {'reference': 80},
            gauge = {'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}],
                    'threshold': {'line': {'color': "red", 'width': 4},
                                'thickness': 0.75, 'value': 90}}))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Issues and recommendations
        if issues:
            st.subheader("❌ Issues Found")
            for i, issue in enumerate(issues, 1):
                st.write(f"{i}. {issue}")
        
        if recommendations:
            st.subheader("💡 Recommendations")
            for i, rec in enumerate(recommendations, 1):
                st.write(f"{i}. {rec}")
        
        # Additional ATS tips
        with st.expander("📚 Additional ATS Optimization Tips"):
            st.markdown("""
            ### Format Guidelines:
            - Use standard fonts (Arial, Calibri, Times New Roman)
            - Avoid headers, footers, and text boxes
            - Don't use graphics, images, or charts
            - Use simple bullet points (• not fancy symbols)
            
            ### Content Guidelines:
            - Include relevant keywords from job description
            - Use standard section headers
            - Quantify achievements with numbers
            - Include both acronyms and full terms (e.g., "AI (Artificial Intelligence)")
            
            ### File Guidelines:
            - Save as PDF or DOCX
            - Use descriptive filename
            - Avoid password protection
            - Test readability by copying/pasting text
            """)
    
    def render_resume_builder_tab(self):
        """Render resume builder tab"""
        st.header("🔧 AI-Powered Resume Builder")
        st.write("Create a professional resume from scratch with AI assistance")
        
        # Resume builder sections
        st.subheader("📝 Resume Information")
        
        with st.form("resume_builder_form"):
            # Personal Information
            st.markdown("### 👤 Personal Information")
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name*", placeholder="John Smith")
                email = st.text_input("Email*", placeholder="john.smith@email.com")
                phone = st.text_input("Phone*", placeholder="+1 (555) 123-4567")
            
            with col2:
                linkedin = st.text_input("LinkedIn Profile", placeholder="linkedin.com/in/johnsmith")
                github = st.text_input("GitHub Profile", placeholder="github.com/johnsmith")
                website = st.text_input("Website/Portfolio", placeholder="johnsmith.dev")
            
            # Professional Summary
            st.markdown("### 📄 Professional Summary")
            summary = st.text_area(
                "Professional Summary",
                height=100,
                placeholder="Write a brief professional summary highlighting your key skills and experience..."
            )
            
            # Work Experience
            st.markdown("### 💼 Work Experience")
            num_experiences = st.number_input("Number of work experiences", min_value=0, max_value=10, value=2)
            
            experiences = []
            for i in range(int(num_experiences)):
                with st.expander(f"Experience #{i+1}"):
                    exp_col1, exp_col2 = st.columns(2)
                    with exp_col1:
                        job_title = st.text_input(f"Job Title", key=f"job_title_{i}")
                        company = st.text_input(f"Company", key=f"company_{i}")
                    with exp_col2:
                        start_date = st.text_input(f"Start Date", key=f"start_date_{i}", placeholder="MM/YYYY")
                        end_date = st.text_input(f"End Date", key=f"end_date_{i}", placeholder="MM/YYYY or Present")
                    
                    job_description = st.text_area(
                        f"Job Description",
                        key=f"job_desc_{i}",
                        height=100,
                        placeholder="Describe your responsibilities and achievements..."
                    )
                    
                    experiences.append({
                        'title': job_title,
                        'company': company,
                        'start_date': start_date,
                        'end_date': end_date,
                        'description': job_description
                    })
            
            # Education
            st.markdown("### 🎓 Education")
            num_education = st.number_input("Number of education entries", min_value=0, max_value=5, value=1)
            
            education_entries = []
            for i in range(int(num_education)):
                with st.expander(f"Education #{i+1}"):
                    edu_col1, edu_col2 = st.columns(2)
                    with edu_col1:
                        degree = st.text_input(f"Degree", key=f"degree_{i}")
                        institution = st.text_input(f"Institution", key=f"institution_{i}")
                    with edu_col2:
                        grad_date = st.text_input(f"Graduation Date", key=f"grad_date_{i}", placeholder="MM/YYYY")
                        gpa = st.text_input(f"GPA (Optional)", key=f"gpa_{i}")
                    
                    education_entries.append({
                        'degree': degree,
                        'institution': institution,
                        'graduation_date': grad_date,
                        'gpa': gpa
                    })
            
            # Skills
            st.markdown("### 🛠️ Skills")
            technical_skills = st.text_input("Technical Skills", placeholder="Python, Java, React, AWS, etc.")
            soft_skills = st.text_input("Soft Skills", placeholder="Leadership, Communication, Problem-solving, etc.")
            
            # Generate Resume Button
            submit_button = st.form_submit_button("🚀 Generate Resume", type="primary")
            
            if submit_button:
                if full_name and email and phone:
                    with st.spinner("🤖 AI is building your resume..."):
                        resume_data = {
                            'personal_info': {
                                'name': full_name,
                                'email': email,
                                'phone': phone,
                                'linkedin': linkedin,
                                'github': github,
                                'website': website
                            },
                            'summary': summary,
                            'experiences': experiences,
                            'education': education_entries,
                            'technical_skills': technical_skills.split(',') if technical_skills else [],
                            'soft_skills': soft_skills.split(',') if soft_skills else []
                        }
                        
                        # Generate resume document
                        self.generate_resume_document(resume_data)
                else:
                    st.error("⚠️ Please fill in all required fields (Name, Email, Phone)")
    
    def generate_resume_document(self, resume_data):
        """Generate a resume document from the provided data"""
        try:
            # Create Word document
            doc = Document()
            
            # Header with name and contact info
            header = doc.sections[0].header
            header_para = header.paragraphs[0]
            header_para.text = f"{resume_data['personal_info']['name']}"
            
            # Contact information
            contact_info = []
            if resume_data['personal_info']['email']:
                contact_info.append(resume_data['personal_info']['email'])
            if resume_data['personal_info']['phone']:
                contact_info.append(resume_data['personal_info']['phone'])
            if resume_data['personal_info']['linkedin']:
                contact_info.append(resume_data['personal_info']['linkedin'])
            
            contact_para = doc.add_paragraph(' | '.join(contact_info))
            contact_para.alignment = 1  # Center alignment
            
            # Professional Summary
            if resume_data['summary']:
                doc.add_heading('Professional Summary', level=2)
                doc.add_paragraph(resume_data['summary'])
            
            # Work Experience
            if resume_data['experiences']:
                doc.add_heading('Professional Experience', level=2)
                for exp in resume_data['experiences']:
                    if exp['title'] and exp['company']:
                        # Job title and company
                        job_para = doc.add_paragraph()
                        job_run = job_para.add_run(f"{exp['title']} - {exp['company']}")
                        job_run.bold = True
                        
                        # Dates
                        if exp['start_date'] or exp['end_date']:
                            date_range = f"{exp['start_date']} - {exp['end_date']}"
                            doc.add_paragraph(date_range)
                        
                        # Description
                        if exp['description']:
                            doc.add_paragraph(exp['description'])
                        
                        doc.add_paragraph()  # Add spacing
            
            # Education
            if resume_data['education']:
                doc.add_heading('Education', level=2)
                for edu in resume_data['education']:
                    if edu['degree'] and edu['institution']:
                        edu_para = doc.add_paragraph()
                        edu_run = edu_para.add_run(f"{edu['degree']}")
                        edu_run.bold = True
                        
                        doc.add_paragraph(f"{edu['institution']}")
                        
                        if edu['graduation_date']:
                            doc.add_paragraph(f"Graduated: {edu['graduation_date']}")
                        
                        if edu['gpa']:
                            doc.add_paragraph(f"GPA: {edu['gpa']}")
            
            # Skills
            if resume_data['technical_skills'] or resume_data['soft_skills']:
                doc.add_heading('Skills', level=2)
                
                if resume_data['technical_skills']:
                    tech_para = doc.add_paragraph()
                    tech_run = tech_para.add_run("Technical Skills: ")
                    tech_run.bold = True
                    tech_para.add_run(', '.join([skill.strip() for skill in resume_data['technical_skills']]))
                
                if resume_data['soft_skills']:
                    soft_para = doc.add_paragraph()
                    soft_run = soft_para.add_run("Soft Skills: ")
                    soft_run.bold = True
                    soft_para.add_run(', '.join([skill.strip() for skill in resume_data['soft_skills']]))
            
            # Save document to memory
            doc_buffer = io.BytesIO()
            doc.save(doc_buffer)
            doc_buffer.seek(0)
            
            # Provide download button
            st.success("✅ Resume generated successfully!")
            st.download_button(
                label="📄 Download Resume (DOCX)",
                data=doc_buffer.getvalue(),
                file_name=f"{resume_data['personal_info']['name'].replace(' ', '_')}_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
            # Display preview
            st.subheader("👀 Resume Preview")
            st.info("📄 Your resume has been generated and is ready for download!")
            
        except Exception as e:
            st.error(f"❌ Error generating resume: {str(e)}")
    
    def render_templates_tab(self):
        """Render templates tab"""
        st.header("📋 Professional Resume Templates")
        st.write("Choose from AI-optimized resume templates")
        
        # Template categories
        template_categories = {
            "🔧 Technical/IT": [
                "Software Engineer",
                "Data Scientist", 
                "DevOps Engineer",
                "Full-Stack Developer",
                "Machine Learning Engineer"
            ],
            "💼 Business/Management": [
                "Project Manager",
                "Business Analyst",
                "Marketing Manager",
                "Sales Executive",
                "Operations Manager"
            ],
            "🎨 Creative/Design": [
                "Graphic Designer",
                "UX/UI Designer",
                "Content Creator",
                "Digital Marketer",
                "Brand Manager"
            ],
            "🏥 Healthcare/Science": [
                "Nurse",
                "Research Scientist",
                "Medical Assistant",
                "Healthcare Administrator",
                "Laboratory Technician"
            ]
        }
        
        # Category selection
        selected_category = st.selectbox("Choose template category:", list(template_categories.keys()))
        
        # Template selection within category
        templates_in_category = template_categories[selected_category]
        
        cols = st.columns(3)
        for i, template in enumerate(templates_in_category):
            with cols[i % 3]:
                with st.container():
                    st.markdown(f"""
                    <div class="feature-card" style="height: 200px;">
                        <h3>{template}</h3>
                        <p>Optimized for {template.lower()} positions</p>
                        <p>✅ ATS-friendly</p>
                        <p>✅ Modern design</p>
                        <p>✅ Customizable</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Use {template} Template", key=f"template_{i}"):
                        st.success(f"✅ {template} template selected!")
                        st.info("Template customization feature would be implemented here.")
        
        # Template customization section
        st.subheader("🎨 Template Customization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Color Scheme")
            color_scheme = st.selectbox(
                "Choose color scheme:",
                ["Professional Blue", "Classic Black", "Modern Purple", "Creative Teal", "Elegant Gray"]
            )
            
            st.markdown("### Font Style")
            font_style = st.selectbox(
                "Choose font style:",
                ["Modern (Calibri)", "Classic (Times New Roman)", "Clean (Arial)", "Professional (Helvetica)"]
            )
        
        with col2:
            st.markdown("### Layout Style")
            layout_style = st.selectbox(
                "Choose layout:",
                ["Single Column", "Two Column", "Timeline Style", "Skills-Focused", "Experience-Heavy"]
            )
            
            st.markdown("### Section Order")
            section_order = st.multiselect(
                "Customize section order:",
                ["Summary", "Experience", "Education", "Skills", "Projects", "Certifications"],
                default=["Summary", "Experience", "Education", "Skills"]
            )
        
        if st.button("🚀 Apply Template Customization", type="primary"):
            st.success("✅ Template customized successfully!")
            st.info("Customized template generation would be implemented here.")
    
    def render_career_insights_tab(self):
        """Render career insights tab"""
        st.header("📈 Career Insights & Analytics")
        st.write("Track your resume performance and career progress")
        
        # Check if there's analysis history
        if not st.session_state.analysis_history:
            st.info("📊 No analysis history available. Upload and analyze resumes to see insights!")
            return
        
        # Career metrics dashboard
        st.subheader("🎯 Career Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Resumes Analyzed",
                len(st.session_state.analysis_history),
                delta=1 if st.session_state.analysis_history else 0
            )
        
        with col2:
            avg_ats_score = 85  # Placeholder calculation
            st.metric("Avg ATS Score", f"{avg_ats_score}%", delta="5%")
        
        with col3:
            job_applications = 12  # Placeholder
            st.metric("Job Applications", job_applications, delta=3)
        
        with col4:
            interviews = 4  # Placeholder
            st.metric("Interviews", interviews, delta=1)
        
        # Progress tracking
        st.subheader("📊 Progress Tracking")
        
        # Sample data for demonstration
        progress_data = pd.DataFrame({
            'Date': pd.date_range('2025-01-01', periods=10, freq='W'),
            'ATS_Score': [65, 68, 72, 75, 78, 80, 83, 85, 87, 90],
            'Skill_Match': [60, 65, 70, 73, 76, 79, 82, 84, 86, 88],
            'Applications': [2, 3, 4, 3, 5, 4, 6, 5, 7, 6]
        })
        
        # Progress visualization
        fig_progress = px.line(
            progress_data, 
            x='Date', 
            y=['ATS_Score', 'Skill_Match'],
            title="Resume Performance Over Time",
            labels={'value': 'Score (%)', 'variable': 'Metric'}
        )
        st.plotly_chart(fig_progress, use_container_width=True)
        
        # Application tracking
        st.subheader("📧 Application Tracking")
        
        application_status = pd.DataFrame({
            'Status': ['Applied', 'Reviewed', 'Interview Scheduled', 'Rejected', 'Offer'],
            'Count': [15, 8, 4, 6, 1]
        })
        
        fig_applications = px.pie(
            application_status,
            values='Count',
            names='Status',
            title="Application Status Distribution"
        )
        st.plotly_chart(fig_applications, use_container_width=True)
        
        # Skills gap analysis
        st.subheader("🛠️ Skills Gap Analysis")
        
        skills_gap_data = pd.DataFrame({
            'Skill': ['Python', 'Machine Learning', 'AWS', 'Docker', 'React', 'SQL'],
            'Current_Level': [85, 70, 60, 45, 80, 90],
            'Required_Level': [90, 85, 80, 70, 85, 95],
            'Gap': [5, 15, 20, 25, 5, 5]
        })
        
        fig_skills = px.bar(
            skills_gap_data,
            x='Skill',
            y=['Current_Level', 'Required_Level'],
            title="Skills Gap Analysis",
            barmode='group'
        )
        st.plotly_chart(fig_skills, use_container_width=True)
        
        # Recommendations
        st.subheader("💡 Career Recommendations")
        
        recommendations = [
            "🎯 Focus on improving AWS cloud skills - 20% gap identified",
            "📚 Consider Docker certification to bridge containerization gap",
            "💼 Your ATS scores are improving consistently - keep optimizing!",
            "🔍 Machine Learning skills need attention for target roles",
            "✅ SQL proficiency is excellent - highlight this strength"
        ]
        
        for rec in recommendations:
            st.write(f"• {rec}")
        
        # Export functionality
        st.subheader("📤 Export Career Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Export Progress Report"):
                self.export_progress_report(progress_data, skills_gap_data)
        
        with col2:
            if st.button("📈 Generate Career Summary"):
                self.generate_career_summary()
        
        with col3:
            if st.button("🎯 Get AI Career Advice"):
                self.get_ai_career_advice()
    
    def render_customization_tab(self):
        """Render customization tab"""
        st.header("🎨 Resume Customization Studio")
        st.write("Customize and personalize your resume appearance and content")
        
        # Check if resume data exists
        if 'resume_data' not in st.session_state or not st.session_state.resume_data:
            st.warning("⚠️ Please upload a resume in the Resume Analysis tab first.")
            return
        
        # Customization options
        st.subheader("🎨 Visual Customization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌈 Color & Style")
            
            color_theme = st.selectbox(
                "Color Theme:",
                ["Professional Blue", "Modern Purple", "Classic Black", "Creative Teal", "Elegant Gray", "Custom"]
            )
            
            if color_theme == "Custom":
                primary_color = st.color_picker("Primary Color", "#1f77b4")
                secondary_color = st.color_picker("Secondary Color", "#ff7f0e")
            
            font_family = st.selectbox(
                "Font Family:",
                ["Calibri", "Arial", "Times New Roman", "Helvetica", "Georgia"]
            )
            
            font_size = st.slider("Base Font Size", 10, 14, 11)
            
        with col2:
            st.markdown("### 📄 Layout Options")
            
            layout_type = st.selectbox(
                "Layout Type:",
                ["Single Column", "Two Column", "Modern Sidebar", "Timeline Style"]
            )
            
            spacing = st.selectbox(
                "Spacing:",
                ["Compact", "Standard", "Spacious"]
            )
            
            margins = st.selectbox(
                "Margins:",
                ["Narrow", "Standard", "Wide"]
            )
        
        # Content customization
        st.subheader("📝 Content Customization")
        
        # Section visibility
        st.markdown("### 👁️ Section Visibility")
        
        sections_available = [
            "Professional Summary", "Work Experience", "Education", 
            "Technical Skills", "Soft Skills", "Projects", 
            "Certifications", "Awards", "Languages", "Interests"
        ]
        
        visible_sections = st.multiselect(
            "Select sections to include:",
            sections_available,
            default=sections_available[:6]
        )
        
        # Section ordering
        st.markdown("### 📋 Section Order")
        section_order = st.selectbox(
            "Primary focus:",
            ["Experience-First", "Skills-First", "Education-First", "Custom Order"]
        )
        
        if section_order == "Custom Order":
            custom_order = []
            for section in visible_sections:
                position = st.number_input(
                    f"Position for {section}:",
                    min_value=1,
                    max_value=len(visible_sections),
                    value=visible_sections.index(section) + 1,
                    key=f"order_{section}"
                )
                custom_order.append((section, position))
            
            # Sort by position
            custom_order.sort(key=lambda x: x[1])
            ordered_sections = [item[0] for item in custom_order]
            st.write("**Section Order Preview:**", ordered_sections)
        
        # Content enhancement options
        st.subheader("✨ Content Enhancement")
        
        enhancement_options = st.multiselect(
            "Apply enhancements:",
            [
                "Quantify achievements with metrics",
                "Add action verbs to descriptions",
                "Include relevant keywords",
                "Optimize for ATS scanning",
                "Add professional summary",
                "Include skill proficiency levels"
            ]
        )
        
        # Language and tone
        st.markdown("### 🗣️ Language & Tone")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tone = st.selectbox(
                "Writing Tone:",
                ["Professional", "Confident", "Dynamic", "Conservative", "Creative"]
            )
        
        with col2:
            industry_focus = st.selectbox(
                "Industry Focus:",
                ["Technology", "Finance", "Healthcare", "Marketing", "General", "Custom"]
            )
        
        # Preview and apply
        st.subheader("👀 Preview & Apply")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Preview Changes", type="secondary"):
                self.preview_customization(
                    color_theme, layout_type, visible_sections, 
                    enhancement_options, tone, industry_focus
                )
        
        with col2:
            if st.button("✅ Apply Customization", type="primary"):
                self.apply_customization(
                    color_theme, layout_type, visible_sections,
                    enhancement_options, tone, industry_focus
                )
        
        with col3:
            if st.button("🔄 Reset to Default"):
                st.rerun()
        
        # Advanced customization
        with st.expander("🔧 Advanced Customization"):
            st.markdown("### Custom CSS Styling")
            custom_css = st.text_area(
                "Add custom CSS (for advanced users):",
                height=100,
                placeholder="Enter custom CSS styles here..."
            )
            
            st.markdown("### Custom Sections")
            custom_section_name = st.text_input("Custom Section Name:")
            custom_section_content = st.text_area(
                "Custom Section Content:",
                height=100
            )
            
            if st.button("➕ Add Custom Section"):
                if custom_section_name and custom_section_content:
                    st.success(f"✅ Custom section '{custom_section_name}' added!")
    
    def preview_customization(self, color_theme, layout_type, visible_sections, enhancement_options, tone, industry_focus):
        """Preview customization changes"""
        st.subheader("👀 Customization Preview")
        
        preview_info = f"""
        **Visual Settings:**
        - Color Theme: {color_theme}
        - Layout: {layout_type}
        
        **Content Settings:**
        - Visible Sections: {len(visible_sections)} sections
        - Enhancements: {len(enhancement_options)} applied
        - Tone: {tone}
        - Industry Focus: {industry_focus}
        
        **Sections to Include:**
        {', '.join(visible_sections)}
        
        **Applied Enhancements:**
        {', '.join(enhancement_options) if enhancement_options else 'None'}
        """
        
        st.info(preview_info)
        st.success("✅ Preview generated! Use 'Apply Customization' to save changes.")
    
    def apply_customization(self, color_theme, layout_type, visible_sections, enhancement_options, tone, industry_focus):
        """Apply customization to resume"""
        with st.spinner("🎨 Applying customization..."):
            # Here you would implement the actual customization logic
            # This would involve modifying the resume data and regenerating the document
            
            customization_settings = {
                'color_theme': color_theme,
                'layout_type': layout_type,
                'visible_sections': visible_sections,
                'enhancement_options': enhancement_options,
                'tone': tone,
                'industry_focus': industry_focus,
                'applied_at': datetime.now().isoformat()
            }
            
            # Save customization to session state
            st.session_state.resume_data['customization'] = customization_settings
            
            st.success("✅ Customization applied successfully!")
            st.info("📄 Your customized resume is ready. Use the Resume Builder to generate the updated document.")
    
    # Utility methods
    def generate_analysis_report(self, sections):
        """Generate comprehensive analysis report"""
        try:
            report_content = f"""
# Resume Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Personal Information
- Name: {sections['personal_info'].get('name', 'Not found')}
- Email: {sections['personal_info'].get('email', 'Not found')}
- Phone: {sections['personal_info'].get('phone', 'Not found')}
- LinkedIn: {sections['personal_info'].get('linkedin', 'Not provided')}

## Skills Analysis
Technical Skills Found: {', '.join(sections['skills'].get('parsed_skills', [])) or 'None identified'}

## Sections Present
- Experience: {'✅' if sections['experience'] else '❌'}
- Education: {'✅' if sections['education'] else '❌'}
- Skills: {'✅' if sections['skills'] else '❌'}
- Projects: {'✅' if sections['projects'] else '❌'}
- Certifications: {'✅' if sections['certifications'] else '❌'}

## Recommendations
1. Ensure all contact information is present and up-to-date
2. Quantify achievements with specific metrics
3. Include relevant technical skills for your target industry
4. Optimize for ATS compatibility

---
Generated by Resume AI Assistant
            """
            
            st.download_button(
                "📄 Download Analysis Report",
                report_content,
                file_name="resume_analysis_report.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
    
    def generate_enhancement_report(self, suggestions):
        """Generate enhancement suggestions report"""
        report_content = f"""
# Resume Enhancement Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## AI-Powered Suggestions

{suggestions}

---

## Action Items
□ Review all suggestions carefully
□ Implement high-priority changes first
□ Test ATS compatibility after changes
□ Update resume with quantified achievements
□ Proofread for grammar and clarity

---
Generated by Resume AI Assistant
        """
        
        st.download_button(
            "📄 Download Enhancement Report",
            report_content,
            file_name="resume_enhancement_report.md",
            mime="text/markdown"
        )
    
    def save_suggestions_to_history(self, suggestions):
        """Save suggestions to analysis history"""
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'enhancement_suggestions',
            'content': suggestions
        }
        
        st.session_state.analysis_history.append(history_entry)
        st.success("✅ Suggestions saved to history!")
    
    def export_progress_report(self, progress_data, skills_gap_data):
        """Export progress report"""
        try:
            # Create comprehensive progress report
            report_data = {
                'progress_data': progress_data.to_dict('records'),
                'skills_gap_data': skills_gap_data.to_dict('records'),
                'export_date': datetime.now().isoformat(),
                'user_id': hashlib.md5(str(id(self)).encode()).hexdigest()[:8]
            }
            
            report_json = json.dumps(report_data, indent=2)
            
            st.download_button(
                "📊 Download Progress Report (JSON)",
                report_json,
                file_name=f"career_progress_report_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
            
        except Exception as e:
            st.error(f"Error exporting report: {str(e)}")
    
    def generate_career_summary(self):
        """Generate AI-powered career summary"""
        summary_prompt = """
        Based on the user's resume analysis history and progress data, generate a comprehensive career summary including:
        
        1. Current career stage and strengths
        2. Key achievements and progress made
        3. Areas for improvement
        4. Career trajectory recommendations
        5. Next steps for professional development
        
        Make it personalized and actionable.
        """
        
        career_summary = self.ai_handler.generate_ai_response(summary_prompt)
        
        st.subheader("🎯 AI-Generated Career Summary")
        st.write(career_summary)
        
        # Option to save summary
        if st.button("💾 Save Career Summary"):
            self.save_suggestions_to_history(career_summary)
    
    def get_ai_career_advice(self):
        """Get personalized AI career advice"""
        advice_prompt = """
        Provide personalized career advice including:
        
        1. Industry trends relevant to the user's profile
        2. Skill development recommendations
        3. Networking suggestions
        4. Career transition opportunities
        5. Long-term career planning advice
        
        Make the advice specific and actionable.
        """
        
        career_advice = self.ai_handler.generate_ai_response(advice_prompt)
        
        st.subheader("🤖 AI Career Advice")
        st.write(career_advice)

# Main app runner
def main():
    app = ResumeAIApp()
    app.run()

if __name__ == "__main__":
    main()