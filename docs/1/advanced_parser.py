# Advanced Resume Parser
# Enhanced resume parsing utilities with deep text analysis

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import pandas as pd

# Enhanced data structures
@dataclass
class ContactInfo:
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None

@dataclass
class WorkExperience:
    title: Optional[str] = None
    company: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_months: Optional[int] = None
    description: Optional[str] = None
    achievements: List[str] = None
    technologies: List[str] = None
    
    def __post_init__(self):
        if self.achievements is None:
            self.achievements = []
        if self.technologies is None:
            self.technologies = []

@dataclass
class Education:
    degree: Optional[str] = None
    institution: Optional[str] = None
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None
    relevant_coursework: List[str] = None
    honors: List[str] = None
    
    def __post_init__(self):
        if self.relevant_coursework is None:
            self.relevant_coursework = []
        if self.honors is None:
            self.honors = []

@dataclass
class Project:
    name: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = None
    url: Optional[str] = None
    date: Optional[str] = None
    
    def __post_init__(self):
        if self.technologies is None:
            self.technologies = []

@dataclass
class Skill:
    name: str
    category: str = "General"
    proficiency: str = "Intermediate"
    years_experience: Optional[int] = None

@dataclass
class ParsedResume:
    contact_info: ContactInfo
    summary: Optional[str] = None
    work_experience: List[WorkExperience] = None
    education: List[Education] = None
    skills: List[Skill] = None
    projects: List[Project] = None
    certifications: List[str] = None
    languages: List[str] = None
    parse_confidence: float = 0.0
    
    def __post_init__(self):
        if self.work_experience is None:
            self.work_experience = []
        if self.education is None:
            self.education = []
        if self.skills is None:
            self.skills = []
        if self.projects is None:
            self.projects = []
        if self.certifications is None:
            self.certifications = []
        if self.languages is None:
            self.languages = []

class AdvancedResumeParser:
    """Advanced resume parser with deep text analysis capabilities"""
    
    def __init__(self):
        self.technical_skills = self._load_technical_skills()
        self.soft_skills = self._load_soft_skills()
        self.degree_patterns = self._load_degree_patterns()
        self.company_indicators = self._load_company_indicators()
        
    def parse_resume(self, text: str) -> ParsedResume:
        """Parse resume text into structured data"""
        
        # Clean and preprocess text
        cleaned_text = self._clean_text(text)
        sections = self._identify_sections(cleaned_text)
        
        # Parse each section
        contact_info = self._parse_contact_info(cleaned_text)
        summary = self._parse_summary(sections.get('summary', ''))
        work_experience = self._parse_work_experience(sections.get('experience', ''))
        education = self._parse_education(sections.get('education', ''))
        skills = self._parse_skills(sections.get('skills', ''))
        projects = self._parse_projects(sections.get('projects', ''))
        certifications = self._parse_certifications(cleaned_text)
        languages = self._parse_languages(cleaned_text)
        
        # Calculate parse confidence
        confidence = self._calculate_parse_confidence({
            'contact_info': contact_info,
            'work_experience': work_experience,
            'education': education,
            'skills': skills
        })
        
        return ParsedResume(
            contact_info=contact_info,
            summary=summary,
            work_experience=work_experience,
            education=education,
            skills=skills,
            projects=projects,
            certifications=certifications,
            languages=languages,
            parse_confidence=confidence
        )
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Fix common encoding issues
        text = text.replace('\u2022', '•')  # Bullet points
        text = text.replace('\u2013', '-')  # En dash
        text = text.replace('\u2014', '—')  # Em dash
        text = text.replace('\u201c', '"')  # Left double quote
        text = text.replace('\u201d', '"')  # Right double quote
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common formatting issues
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between camelCase
        
        return text.strip()
    
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify and extract resume sections"""
        
        section_patterns = {
            'summary': [
                r'(?:PROFESSIONAL\s+)?SUMMARY(?:\s+OF\s+QUALIFICATIONS)?',
                r'PROFILE',
                r'OBJECTIVE',
                r'CAREER\s+OBJECTIVE',
                r'EXECUTIVE\s+SUMMARY'
            ],
            'experience': [
                r'(?:PROFESSIONAL\s+)?(?:WORK\s+)?EXPERIENCE',
                r'EMPLOYMENT(?:\s+HISTORY)?',
                r'CAREER(?:\s+HISTORY)?',
                r'PROFESSIONAL\s+BACKGROUND'
            ],
            'education': [
                r'EDUCATION(?:AL\s+BACKGROUND)?',
                r'ACADEMIC\s+BACKGROUND',
                r'QUALIFICATIONS',
                r'DEGREES?'
            ],
            'skills': [
                r'(?:TECHNICAL\s+)?SKILLS',
                r'COMPETENCIES',
                r'CORE\s+COMPETENCIES',
                r'EXPERTISE',
                r'PROFICIENCIES'
            ],
            'projects': [
                r'PROJECTS?',
                r'KEY\s+PROJECTS',
                r'NOTABLE\s+PROJECTS',
                r'PORTFOLIO'
            ],
            'certifications': [
                r'CERTIFICATIONS?',
                r'LICENSES?',
                r'CREDENTIALS',
                r'PROFESSIONAL\s+CERTIFICATIONS?'
            ]
        }
        
        sections = {}
        text_lines = text.split('\n')
        
        for section_name, patterns in section_patterns.items():
            section_content = self._extract_section_content(text_lines, patterns)
            if section_content:
                sections[section_name] = section_content
        
        return sections
    
    def _extract_section_content(self, lines: List[str], patterns: List[str]) -> str:
        """Extract content for a specific section"""
        
        section_start = -1
        section_end = len(lines)
        
        # Find section start
        for i, line in enumerate(lines):
            for pattern in patterns:
                if re.search(pattern, line.upper().strip()):
                    section_start = i
                    break
            if section_start != -1:
                break
        
        if section_start == -1:
            return ""
        
        # Find section end (next major section or end of document)
        all_patterns = []
        for pattern_list in [
            ['SUMMARY', 'PROFILE', 'OBJECTIVE'],
            ['EXPERIENCE', 'EMPLOYMENT', 'CAREER'],
            ['EDUCATION', 'ACADEMIC'],
            ['SKILLS', 'COMPETENCIES'],
            ['PROJECTS?', 'PORTFOLIO'],
            ['CERTIFICATIONS?', 'LICENSES?']
        ]:
            all_patterns.extend(pattern_list)
        
        for i in range(section_start + 1, len(lines)):
            line_upper = lines[i].upper().strip()
            for pattern in all_patterns:
                if re.match(f'^{pattern}', line_upper) and len(line_upper) < 50:
                    section_end = i
                    break
            if section_end != len(lines):
                break
        
        # Extract content
        content_lines = lines[section_start + 1:section_end]
        return '\n'.join(content_lines).strip()
    
    def _parse_contact_info(self, text: str) -> ContactInfo:
        """Parse contact information"""
        
        contact = ContactInfo()
        
        # Name extraction (usually in first few lines)
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            if self._is_likely_name(line):
                contact.name = line
                break
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact.email = emails[0]
        
        # Phone extraction
        phone_patterns = [
            r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            r'\+?([0-9]{1,4})[-.\s]?\(?([0-9]{1,4})\)?[-.\s]?([0-9]{1,4})[-.\s]?([0-9]{1,4})'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                if isinstance(phones[0], tuple):
                    contact.phone = '-'.join(filter(None, phones[0]))
                else:
                    contact.phone = phones[0]
                break
        
        # LinkedIn extraction
        linkedin_pattern = r'linkedin\.com/in/([\w\-]+)'
        linkedin_matches = re.findall(linkedin_pattern, text.lower())
        if linkedin_matches:
            contact.linkedin = f"linkedin.com/in/{linkedin_matches[0]}"
        
        # GitHub extraction
        github_pattern = r'github\.com/([\w\-]+)'
        github_matches = re.findall(github_pattern, text.lower())
        if github_matches:
            contact.github = f"github.com/{github_matches[0]}"
        
        # Website extraction
        website_patterns = [
            r'https?://([\w\.-]+\.[\w]{2,})',
            r'www\.([\w\.-]+\.[\w]{2,})',
        ]
        
        for pattern in website_patterns:
            websites = re.findall(pattern, text.lower())
            if websites:
                contact.website = websites[0]
                break
        
        # Location extraction
        location_pattern = r'(?:^|\n)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?,\s*[A-Z]{2}(?:\s*\d{5})?)'
        locations = re.findall(location_pattern, text)
        if locations:
            contact.location = locations[0]
        
        return contact
    
    def _is_likely_name(self, line: str) -> bool:
        """Check if a line likely contains a name"""
        
        line = line.strip()
        
        # Skip if empty or too short
        if len(line) < 2:
            return False
        
        # Skip if contains obvious non-name content
        if any(keyword in line.lower() for keyword in [
            'email', 'phone', '@', '.com', 'resume', 'cv', 'curriculum'
        ]):
            return False
        
        # Check if it looks like a name
        words = line.split()
        
        # Should have 2-4 words
        if not (2 <= len(words) <= 4):
            return False
        
        # Each word should start with capital and be mostly letters
        for word in words:
            if not word[0].isupper() or not word.replace("'", "").replace("-", "").isalpha():
                return False
        
        return True
    
    def _parse_summary(self, text: str) -> Optional[str]:
        """Parse professional summary"""
        if not text or len(text.strip()) < 20:
            return None
        
        # Clean up the summary
        summary = re.sub(r'\n+', ' ', text.strip())
        summary = re.sub(r'\s+', ' ', summary)
        
        return summary
    
    def _parse_work_experience(self, text: str) -> List[WorkExperience]:
        """Parse work experience section"""
        
        if not text:
            return []
        
        experiences = []
        
        # Split by job entries (look for patterns that indicate new jobs)
        job_separator_patterns = [
            r'\n(?=[A-Z][^a-z]*\|)',  # Title | Company pattern
            r'\n(?=[A-Z][a-z].*(?:at|@)\s+[A-Z])',  # Title at Company pattern
            r'\n(?=[A-Z][A-Za-z\s]+\n[A-Z][A-Za-z\s]+\|)',  # Multi-line title/company
        ]
        
        # Try to split the text into job entries
        job_entries = [text]  # Start with whole text
        
        for pattern in job_separator_patterns:
            new_entries = []
            for entry in job_entries:
                parts = re.split(pattern, entry)
                new_entries.extend([part.strip() for part in parts if part.strip()])
            job_entries = new_entries
            if len(job_entries) > 1:
                break
        
        # Parse each job entry
        for entry in job_entries:
            if len(entry.strip()) < 20:  # Skip very short entries
                continue
                
            experience = self._parse_single_experience(entry)
            if experience.title or experience.company:
                experiences.append(experience)
        
        return experiences
    
    def _parse_single_experience(self, text: str) -> WorkExperience:
        """Parse a single work experience entry"""
        
        experience = WorkExperience()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return experience
        
        # Parse first line (usually title and company)
        first_line = lines[0]
        
        # Pattern: Title | Company | Date
        if '|' in first_line:
            parts = [part.strip() for part in first_line.split('|')]
            if len(parts) >= 2:
                experience.title = parts[0]
                experience.company = parts[1]
                if len(parts) >= 3:
                    start_date, end_date = self._parse_date_range(parts[2])
                    experience.start_date = start_date
                    experience.end_date = end_date
        
        # Pattern: Title at/@ Company
        elif ' at ' in first_line or ' @ ' in first_line:
            separator = ' at ' if ' at ' in first_line else ' @ '
            parts = first_line.split(separator, 1)
            if len(parts) == 2:
                experience.title = parts[0].strip()
                experience.company = parts[1].strip()
        
        # If no clear pattern, assume first line is title
        else:
            experience.title = first_line
            # Look for company in second line
            if len(lines) > 1:
                second_line = lines[1]
                if not self._looks_like_date(second_line) and not second_line.startswith('•'):
                    experience.company = second_line
        
        # Look for dates in subsequent lines
        if not experience.start_date:
            for line in lines[1:3]:  # Check next 2 lines
                if self._looks_like_date(line):
                    start_date, end_date = self._parse_date_range(line)
                    experience.start_date = start_date
                    experience.end_date = end_date
                    break
        
        # Parse achievements (bullet points)
        achievements = []
        technologies = []
        
        for line in lines:
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                achievement = line[1:].strip()
                achievements.append(achievement)
                
                # Extract technologies from achievements
                tech_matches = self._extract_technologies_from_text(achievement)
                technologies.extend(tech_matches)
        
        experience.achievements = achievements
        experience.technologies = list(set(technologies))  # Remove duplicates
        
        # Calculate duration
        if experience.start_date and experience.end_date:
            experience.duration_months = self._calculate_duration_months(
                experience.start_date, experience.end_date
            )
        
        return experience
    
    def _parse_education(self, text: str) -> List[Education]:
        """Parse education section"""
        
        if not text:
            return []
        
        education_entries = []
        
        # Split by education entries
        entries = re.split(r'\n(?=[A-Z][a-zA-Z\s]*(?:of|in)\s)', text)
        
        for entry in entries:
            if len(entry.strip()) < 10:
                continue
                
            education = Education()
            lines = [line.strip() for line in entry.split('\n') if line.strip()]
            
            if not lines:
                continue
            
            # Parse degree and institution from first line
            first_line = lines[0]
            
            # Pattern: Degree | Institution
            if '|' in first_line:
                parts = [part.strip() for part in first_line.split('|')]
                education.degree = parts[0]
                if len(parts) > 1:
                    education.institution = parts[1]
            
            # Pattern: Degree, Institution or Degree - Institution
            elif ',' in first_line or ' - ' in first_line:
                separator = ',' if ',' in first_line else ' - '
                parts = first_line.split(separator, 1)
                education.degree = parts[0].strip()
                if len(parts) > 1:
                    education.institution = parts[1].strip()
            
            # Look for graduation date and GPA in subsequent lines
            for line in lines[1:]:
                if self._looks_like_date(line):
                    education.graduation_date = line
                elif 'gpa' in line.lower():
                    gpa_match = re.search(r'gpa:?\s*([\d.]+)', line.lower())
                    if gpa_match:
                        education.gpa = gpa_match.group(1)
                elif line.startswith('•') or 'relevant' in line.lower():
                    # Coursework or honors
                    if 'coursework' in line.lower():
                        coursework = re.sub(r'^[•\-\*]\s*', '', line)
                        coursework = re.sub(r'.*coursework:?\s*', '', coursework, flags=re.IGNORECASE)
                        education.relevant_coursework = [c.strip() for c in coursework.split(',')]
                    else:
                        honor = re.sub(r'^[•\-\*]\s*', '', line)
                        education.honors.append(honor)
            
            education_entries.append(education)
        
        return education_entries
    
    def _parse_skills(self, text: str) -> List[Skill]:
        """Parse skills section"""
        
        if not text:
            return []
        
        skills = []
        
        # Look for categorized skills (e.g., "Programming Languages: Python, Java")
        category_pattern = r'([A-Za-z\s&]+):\s*([^\n]+)'
        category_matches = re.findall(category_pattern, text)
        
        for category, skills_text in category_matches:
            category = category.strip()
            skill_names = [s.strip() for s in skills_text.split(',')]
            
            for skill_name in skill_names:
                if skill_name:
                    skill = Skill(name=skill_name, category=category)
                    skills.append(skill)
        
        # Also look for uncategorized skills
        remaining_text = text
        for category, skills_text in category_matches:
            remaining_text = remaining_text.replace(f"{category}: {skills_text}", "")
        
        # Find individual skills in remaining text
        individual_skills = self._find_skills_in_text(remaining_text)
        for skill_name in individual_skills:
            skill = Skill(name=skill_name, category=self._categorize_skill(skill_name))
            skills.append(skill)
        
        return skills
    
    def _parse_projects(self, text: str) -> List[Project]:
        """Parse projects section"""
        
        if not text:
            return []
        
        projects = []
        
        # Split by project entries
        project_entries = re.split(r'\n(?=[A-Z][^a-z\n]*(?:\||$))', text)
        
        for entry in project_entries:
            if len(entry.strip()) < 10:
                continue
                
            project = Project()
            lines = [line.strip() for line in entry.split('\n') if line.strip()]
            
            if not lines:
                continue
            
            # First line usually contains project name and possibly date
            first_line = lines[0]
            
            if '|' in first_line:
                parts = [part.strip() for part in first_line.split('|')]
                project.name = parts[0]
                if len(parts) > 1 and self._looks_like_date(parts[1]):
                    project.date = parts[1]
            else:
                project.name = first_line
            
            # Look for description and technologies in subsequent lines
            description_lines = []
            for line in lines[1:]:
                if line.startswith('•') or line.startswith('-'):
                    description_lines.append(line[1:].strip())
                elif 'technologies:' in line.lower() or 'tech stack:' in line.lower():
                    tech_text = re.sub(r'.*(?:technologies|tech stack):?\s*', '', line, flags=re.IGNORECASE)
                    project.technologies = [t.strip() for t in tech_text.split(',')]
                elif line.startswith('http') or 'github.com' in line.lower():
                    project.url = line
                else:
                    description_lines.append(line)
            
            if description_lines:
                project.description = ' '.join(description_lines)
            
            # Extract technologies from description if not found explicitly
            if not project.technologies and project.description:
                project.technologies = self._extract_technologies_from_text(project.description)
            
            projects.append(project)
        
        return projects
    
    def _parse_certifications(self, text: str) -> List[str]:
        """Parse certifications from text"""
        
        certifications = []
        
        # Look for certification patterns
        cert_patterns = [
            r'(?:certified|certification)\s+[^\n]+',
            r'[A-Z]{2,}\s+certified',
            r'(?:AWS|Google|Microsoft|Oracle|Cisco|CompTIA)\s+[^\n]+',
            r'Professional\s+[^\n]+',
        ]
        
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            certifications.extend(matches)
        
        # Clean and deduplicate
        cleaned_certs = []
        for cert in certifications:
            cert = cert.strip()
            if cert and cert not in cleaned_certs:
                cleaned_certs.append(cert)
        
        return cleaned_certs
    
    def _parse_languages(self, text: str) -> List[str]:
        """Parse languages from text"""
        
        languages = []
        
        # Look for language section
        lang_pattern = r'(?:languages?|linguistic):\s*([^\n]+)'
        lang_matches = re.findall(lang_pattern, text, re.IGNORECASE)
        
        for match in lang_matches:
            langs = [l.strip() for l in match.split(',')]
            languages.extend(langs)
        
        # Common languages to look for
        common_languages = [
            'English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese',
            'Korean', 'Arabic', 'Hindi', 'Portuguese', 'Russian', 'Italian'
        ]
        
        for lang in common_languages:
            if lang.lower() in text.lower() and lang not in languages:
                languages.append(lang)
        
        return languages
    
    # Helper methods
    
    def _looks_like_date(self, text: str) -> bool:
        """Check if text looks like a date range"""
        date_patterns = [
            r'\d{4}\s*[-–]\s*\d{4}',
            r'\d{1,2}/\d{4}\s*[-–]\s*\d{1,2}/\d{4}',
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',
            r'Present|Current|Now'
        ]
        
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in date_patterns)
    
    def _parse_date_range(self, date_str: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse date range from string"""
        
        # Common date range patterns
        patterns = [
            r'(\w+\s+\d{4})\s*[-–]\s*(\w+\s+\d{4})',
            r'(\d{1,2}/\d{4})\s*[-–]\s*(\d{1,2}/\d{4})',
            r'(\d{4})\s*[-–]\s*(\d{4})',
            r'(\w+\s+\d{4})\s*[-–]\s*(Present|Current|Now)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_str, re.IGNORECASE)
            if match:
                start_date, end_date = match.groups()
                if end_date.lower() in ['present', 'current', 'now']:
                    end_date = 'Present'
                return start_date, end_date
        
        return None, None
    
    def _calculate_duration_months(self, start_date: str, end_date: str) -> int:
        """Calculate duration in months between dates"""
        # This is a simplified version - would need more robust date parsing
        try:
            if end_date.lower() == 'present':
                end_year = datetime.now().year
            else:
                end_year = int(re.search(r'\d{4}', end_date).group())
            
            start_year = int(re.search(r'\d{4}', start_date).group())
            
            return max(0, (end_year - start_year) * 12)
        except:
            return 0
    
    def _find_skills_in_text(self, text: str) -> List[str]:
        """Find individual skills in text"""
        found_skills = []
        text_lower = text.lower()
        
        # Check against known technical skills
        for skill in self.technical_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _categorize_skill(self, skill_name: str) -> str:
        """Categorize a skill by name"""
        
        skill_lower = skill_name.lower()
        
        # Programming languages
        if skill_lower in ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust']:
            return 'Programming Languages'
        
        # Frameworks
        if skill_lower in ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express']:
            return 'Frameworks'
        
        # Databases
        if skill_lower in ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite']:
            return 'Databases'
        
        # Cloud platforms
        if skill_lower in ['aws', 'azure', 'gcp', 'google cloud']:
            return 'Cloud Platforms'
        
        # Tools
        if skill_lower in ['git', 'docker', 'kubernetes', 'jenkins', 'jira']:
            return 'Tools'
        
        return 'General'
    
    def _extract_technologies_from_text(self, text: str) -> List[str]:
        """Extract technology names from text"""
        
        technologies = []
        text_lower = text.lower()
        
        for tech in self.technical_skills:
            if tech.lower() in text_lower:
                technologies.append(tech)
        
        return technologies
    
    def _calculate_parse_confidence(self, parsed_data: Dict) -> float:
        """Calculate confidence score for parsing quality"""
        
        confidence = 0.0
        total_weight = 0.0
        
        # Contact info weight: 30%
        contact_weight = 0.3
        contact_score = 0.0
        
        contact_info = parsed_data['contact_info']
        if contact_info.name:
            contact_score += 0.3
        if contact_info.email:
            contact_score += 0.4
        if contact_info.phone:
            contact_score += 0.3
        
        confidence += contact_score * contact_weight
        total_weight += contact_weight
        
        # Work experience weight: 40%
        experience_weight = 0.4
        experience_score = 0.0
        
        experiences = parsed_data['work_experience']
        if experiences:
            exp_quality = 0.0
            for exp in experiences:
                if exp.title and exp.company:
                    exp_quality += 0.5
                if exp.achievements:
                    exp_quality += 0.3
                if exp.start_date:
                    exp_quality += 0.2
            
            experience_score = min(1.0, exp_quality / len(experiences))
        
        confidence += experience_score * experience_weight
        total_weight += experience_weight
        
        # Education weight: 15%
        education_weight = 0.15
        education_score = 0.0
        
        education = parsed_data['education']
        if education:
            for edu in education:
                if edu.degree and edu.institution:
                    education_score += 0.8
                    break
        
        confidence += education_score * education_weight
        total_weight += education_weight
        
        # Skills weight: 15%
        skills_weight = 0.15
        skills_score = 0.0
        
        skills = parsed_data['skills']
        if skills:
            skills_score = min(1.0, len(skills) / 10.0)  # Max confidence at 10+ skills
        
        confidence += skills_score * skills_weight
        total_weight += skills_weight
        
        return min(100.0, (confidence / total_weight) * 100) if total_weight > 0 else 0.0
    
    # Data loading methods
    
    def _load_technical_skills(self) -> List[str]:
        """Load list of technical skills"""
        return [
            # Programming Languages
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust',
            'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'SQL', 'HTML', 'CSS', 'SASS', 'LESS',
            
            # Frameworks & Libraries
            'React', 'Angular', 'Vue', 'Svelte', 'Node.js', 'Express', 'Django', 'Flask', 'FastAPI',
            'Spring', 'Hibernate', 'Laravel', 'Rails', 'ASP.NET', 'jQuery', 'Bootstrap', 'Tailwind',
            
            # Databases
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch', 'SQLite', 'Oracle', 'Cassandra',
            
            # Cloud & DevOps
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'GitHub Actions',
            'Terraform', 'Ansible', 'Chef', 'Puppet', 'Nginx', 'Apache',
            
            # Tools & Other
            'Git', 'SVN', 'Jira', 'Confluence', 'Slack', 'Teams', 'Figma', 'Sketch', 'Photoshop'
        ]
    
    def _load_soft_skills(self) -> List[str]:
        """Load list of soft skills"""
        return [
            'Leadership', 'Communication', 'Teamwork', 'Problem Solving', 'Analytical Thinking',
            'Creativity', 'Adaptability', 'Time Management', 'Project Management', 'Mentoring',
            'Collaboration', 'Critical Thinking', 'Decision Making', 'Negotiation', 'Presentation'
        ]
    
    def _load_degree_patterns(self) -> List[str]:
        """Load degree patterns for recognition"""
        return [
            r'Ph\.?D\.?', r'Doctor(?:ate)?', r'M\.?S\.?', r'M\.?A\.?', r'MBA', r'Master',
            r'B\.?S\.?', r'B\.?A\.?', r'Bachelor', r'A\.?A\.?', r'A\.?S\.?', r'Associate'
        ]
    
    def _load_company_indicators(self) -> List[str]:
        """Load indicators that help identify company names"""
        return [
            'Inc', 'Corp', 'Corporation', 'LLC', 'Ltd', 'Limited', 'Company', 'Co',
            'Technologies', 'Solutions', 'Systems', 'Services', 'Consulting', 'Group'
        ]
    
    def to_dict(self, parsed_resume: ParsedResume) -> Dict:
        """Convert ParsedResume to dictionary"""
        return asdict(parsed_resume)
    
    def to_json(self, parsed_resume: ParsedResume) -> str:
        """Convert ParsedResume to JSON string"""
        return json.dumps(self.to_dict(parsed_resume), indent=2, default=str)