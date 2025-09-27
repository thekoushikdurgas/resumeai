"""
Demo script for Resume/CV AI Application
Demonstrates key features and functionality.
"""

import sys
import os
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def create_sample_resume():
    """Create a sample resume for demonstration"""
    from app.models.resume_model import ParsedResume, ContactInfo, WorkExperience, Education, Skill, Project
    
    # Create contact info
    contact_info = ContactInfo(
        name="John Doe",
        email="john.doe@email.com",
        phone="(555) 123-4567",
        location="New York, NY",
        linkedin="linkedin.com/in/johndoe",
        github="github.com/johndoe"
    )
    
    # Create work experience
    work_experience = [
        WorkExperience(
            title="Senior Software Engineer",
            company="Tech Corp",
            start_date="2020",
            end_date="Present",
            description="Lead development of web applications using Python and Django",
            achievements=[
                "Improved system performance by 40%",
                "Led a team of 5 developers",
                "Implemented CI/CD pipeline reducing deployment time by 60%"
            ],
            technologies=["Python", "Django", "PostgreSQL", "AWS", "Docker"]
        ),
        WorkExperience(
            title="Software Engineer",
            company="StartupXYZ",
            start_date="2018",
            end_date="2020",
            description="Developed full-stack web applications",
            achievements=[
                "Built scalable microservices architecture",
                "Reduced bug reports by 30% through improved testing"
            ],
            technologies=["Python", "JavaScript", "React", "MongoDB", "Redis"]
        )
    ]
    
    # Create education
    education = [
        Education(
            degree="Bachelor of Science in Computer Science",
            institution="University of Technology",
            graduation_date="2018",
            gpa="3.8"
        )
    ]
    
    # Create skills
    skills = [
        Skill(name="Python", category="Programming Languages", proficiency="Expert"),
        Skill(name="Django", category="Frameworks", proficiency="Advanced"),
        Skill(name="JavaScript", category="Programming Languages", proficiency="Advanced"),
        Skill(name="React", category="Frameworks", proficiency="Intermediate"),
        Skill(name="PostgreSQL", category="Databases", proficiency="Advanced"),
        Skill(name="AWS", category="Cloud Platforms", proficiency="Intermediate"),
        Skill(name="Docker", category="DevOps", proficiency="Intermediate"),
        Skill(name="Git", category="Tools", proficiency="Advanced"),
        Skill(name="Leadership", category="Soft Skills", proficiency="Advanced"),
        Skill(name="Problem Solving", category="Soft Skills", proficiency="Expert")
    ]
    
    # Create projects
    projects = [
        Project(
            name="E-commerce Platform",
            description="Built a scalable e-commerce platform serving 10,000+ users",
            technologies=["Python", "Django", "PostgreSQL", "Redis", "AWS"],
            url="https://github.com/johndoe/ecommerce-platform"
        ),
        Project(
            name="Machine Learning Pipeline",
            description="Developed ML pipeline for customer behavior analysis",
            technologies=["Python", "scikit-learn", "Pandas", "NumPy", "Docker"]
        )
    ]
    
    # Create resume
    resume = ParsedResume(
        contact_info=contact_info,
        summary="Experienced software engineer with 5+ years of experience in Python development, web applications, and team leadership. Passionate about building scalable solutions and mentoring junior developers.",
        work_experience=work_experience,
        education=education,
        skills=skills,
        projects=projects,
        parse_confidence=95.0
    )
    
    return resume

def create_sample_job():
    """Create a sample job description for demonstration"""
    return """
    Senior Python Developer
    
    Company: InnovateTech Solutions
    Location: San Francisco, CA (Remote OK)
    
    Job Description:
    We are seeking a Senior Python Developer to join our growing team. You will be responsible for developing and maintaining our core platform, working with modern technologies, and mentoring junior developers.
    
    Requirements:
    - 5+ years of Python development experience
    - Strong experience with Django or Flask
    - Experience with PostgreSQL or similar databases
    - Knowledge of AWS or similar cloud platforms
    - Experience with Docker and containerization
    - Strong problem-solving skills
    - Leadership experience preferred
    
    Responsibilities:
    - Develop and maintain web applications
    - Design and implement APIs
    - Optimize database queries and application performance
    - Mentor junior developers
    - Participate in code reviews
    - Collaborate with cross-functional teams
    
    Benefits:
    - Competitive salary
    - Health insurance
    - 401k matching
    - Flexible work hours
    - Remote work options
    """

def demo_resume_analysis():
    """Demonstrate resume analysis functionality"""
    print("🔍 Resume Analysis Demo")
    print("=" * 40)
    
    try:
        from app.core.vector_db import VectorDatabase
        from app.core.ai_handler import AIHandler
        from app.core.resume_analyzer import ResumeAnalyzer
        
        # Create sample resume
        resume = create_sample_resume()
        print(f"✅ Created sample resume for {resume.contact_info.name}")
        
        # Initialize components
        vector_db = VectorDatabase(persist_directory="./demo_vectordb")
        ai_handler = AIHandler()
        analyzer = ResumeAnalyzer(vector_db, ai_handler)
        
        # Parse resume
        parsed_resume = analyzer.parse_resume(
            f"""
            {resume.contact_info.name}
            {resume.contact_info.email} | {resume.contact_info.phone} | {resume.contact_info.location}
            
            {resume.summary}
            
            EXPERIENCE
            {chr(10).join([f"{exp.title} | {exp.company} | {exp.start_date}-{exp.end_date}" for exp in resume.work_experience])}
            
            EDUCATION
            {chr(10).join([f"{edu.degree} | {edu.institution} | {edu.graduation_date}" for edu in resume.education])}
            
            SKILLS
            {', '.join([skill.name for skill in resume.skills])}
            """
        )
        
        print(f"✅ Resume parsed with {parsed_resume.parse_confidence:.1f}% confidence")
        print(f"✅ Found {len(parsed_resume.skills)} skills")
        print(f"✅ Found {len(parsed_resume.work_experience)} work experiences")
        
        # Analyze resume
        analysis = analyzer.analyze_resume(parsed_resume)
        print(f"✅ Analysis completed with {analysis.overall_score:.1f}/100 score")
        
        # Clean up
        vector_db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Resume analysis demo failed: {e}")
        return False

def demo_job_matching():
    """Demonstrate job matching functionality"""
    print("\n🎯 Job Matching Demo")
    print("=" * 40)
    
    try:
        from app.core.vector_db import VectorDatabase
        from app.core.ai_handler import AIHandler
        from app.core.job_matcher import JobMatcher
        
        # Create sample resume and job
        resume = create_sample_resume()
        job_description = create_sample_job()
        
        # Initialize components
        vector_db = VectorDatabase(persist_directory="./demo_vectordb")
        ai_handler = AIHandler()
        matcher = JobMatcher(vector_db, ai_handler)
        
        # Match resume to job
        match_result = matcher.match_resume_to_job(resume, job_description)
        
        print(f"✅ Job matching completed")
        print(f"✅ Overall match score: {match_result.get('match_score', 0):.1f}%")
        print(f"✅ Skill match: {match_result.get('skill_match', 0):.1f}%")
        print(f"✅ Experience match: {match_result.get('experience_match', 0):.1f}%")
        
        if match_result.get('matched_skills'):
            print(f"✅ Matched skills: {', '.join(match_result['matched_skills'][:5])}")
        
        if match_result.get('missing_skills'):
            print(f"⚠️ Missing skills: {', '.join(match_result['missing_skills'][:5])}")
        
        # Clean up
        vector_db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Job matching demo failed: {e}")
        return False

def demo_vector_search():
    """Demonstrate vector search functionality"""
    print("\n🔍 Vector Search Demo")
    print("=" * 40)
    
    try:
        from app.core.vector_db import VectorDatabase
        from app.core.ai_handler import AIHandler
        from app.core.resume_analyzer import ResumeAnalyzer
        from app.models.resume_model import ResumeMetadata
        
        # Initialize components
        vector_db = VectorDatabase(persist_directory="./demo_vectordb")
        ai_handler = AIHandler()
        analyzer = ResumeAnalyzer(vector_db, ai_handler)
        
        # Create and add sample resumes
        resume1 = create_sample_resume()
        resume1.contact_info.name = "John Doe"
        
        resume2 = create_sample_resume()
        resume2.contact_info.name = "Jane Smith"
        resume2.contact_info.email = "jane.smith@email.com"
        resume2.summary = "Frontend developer with React and JavaScript experience"
        
        # Add resumes to vector database
        metadata1 = ResumeMetadata(
            file_name="john_doe_resume.pdf",
            file_type="pdf",
            file_size=1024,
            upload_date=ai_handler.datetime.now(),
            experience_years=5,
            education_level="Bachelor"
        )
        
        metadata2 = ResumeMetadata(
            file_name="jane_smith_resume.pdf",
            file_type="pdf",
            file_size=1024,
            upload_date=ai_handler.datetime.now(),
            experience_years=3,
            education_level="Bachelor"
        )
        
        vector_db.add_resume(resume1, metadata1)
        vector_db.add_resume(resume2, metadata2)
        
        print("✅ Added sample resumes to vector database")
        
        # Search for similar resumes
        search_query = "Python developer with Django experience"
        similar_resumes = vector_db.search_similar_resumes(search_query, 5)
        
        print(f"✅ Found {len(similar_resumes)} similar resumes")
        for i, result in enumerate(similar_resumes, 1):
            similarity = 1 - result['distance']
            print(f"   {i}. {result['metadata']['name']} (similarity: {similarity:.2f})")
        
        # Clean up
        vector_db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Vector search demo failed: {e}")
        return False

def demo_ats_checker():
    """Demonstrate ATS checker functionality"""
    print("\n📊 ATS Checker Demo")
    print("=" * 40)
    
    try:
        from app.core.ai_handler import AIHandler
        from app.core.ats_checker import ATSChecker
        
        # Initialize components
        ai_handler = AIHandler()
        ats_checker = ATSChecker(ai_handler)
        
        # Create sample resume
        resume = create_sample_resume()
        resume.raw_text = f"""
        {resume.contact_info.name}
        {resume.contact_info.email} | {resume.contact_info.phone} | {resume.contact_info.location}
        
        PROFESSIONAL SUMMARY
        {resume.summary}
        
        WORK EXPERIENCE
        Senior Software Engineer | Tech Corp | 2020-Present
        - Improved system performance by 40%
        - Led a team of 5 developers
        - Implemented CI/CD pipeline
        
        EDUCATION
        Bachelor of Science in Computer Science | University of Technology | 2018
        
        SKILLS
        Python, Django, JavaScript, React, PostgreSQL, AWS, Docker, Git
        """
        
        # Check ATS compatibility
        ats_result = ats_checker.check_ats_compatibility(resume)
        
        print(f"✅ ATS check completed")
        print(f"✅ Overall ATS score: {ats_result.ats_score:.1f}/100")
        print(f"✅ Format score: {ats_result.format_score:.1f}/100")
        print(f"✅ Keyword score: {ats_result.keyword_score:.1f}/100")
        print(f"✅ Structure score: {ats_result.structure_score:.1f}/100")
        
        if ats_result.compatibility_issues:
            print(f"⚠️ Issues found: {len(ats_result.compatibility_issues)}")
            for issue in ats_result.compatibility_issues[:3]:
                print(f"   - {issue}")
        
        return True
        
    except Exception as e:
        print(f"❌ ATS checker demo failed: {e}")
        return False

def cleanup_demo_files():
    """Clean up demo files"""
    print("\n🧹 Cleaning up demo files...")
    
    import shutil
    
    demo_dirs = ["./demo_vectordb"]
    
    for demo_dir in demo_dirs:
        if Path(demo_dir).exists():
            shutil.rmtree(demo_dir)
            print(f"✅ Removed {demo_dir}")

def main():
    """Run all demos"""
    print("🎬 Resume AI Application Demo")
    print("=" * 50)
    print("This demo showcases the key features of the Resume AI application.")
    print("Note: Some features may require API keys to work fully.")
    print()
    
    demos = [
        ("Resume Analysis", demo_resume_analysis),
        ("Job Matching", demo_job_matching),
        ("Vector Search", demo_vector_search),
        ("ATS Checker", demo_ats_checker)
    ]
    
    passed = 0
    total = len(demos)
    
    for demo_name, demo_func in demos:
        try:
            if demo_func():
                passed += 1
                print(f"✅ {demo_name} demo completed successfully")
            else:
                print(f"❌ {demo_name} demo failed")
        except Exception as e:
            print(f"❌ {demo_name} demo failed with exception: {e}")
    
    print(f"\n{'='*50}")
    print(f"Demo Results: {passed}/{total} demos completed successfully")
    
    if passed == total:
        print("🎉 All demos completed! The application is working correctly.")
    else:
        print("⚠️ Some demos failed. This may be due to missing API keys or dependencies.")
    
    # Clean up
    cleanup_demo_files()
    
    print("\n🚀 To run the full application:")
    print("   python launch.py --setup  # First time setup")
    print("   python launch.py --run    # Run the application")
    print("   python launch.py --demo   # Run in demo mode")

if __name__ == "__main__":
    main()
