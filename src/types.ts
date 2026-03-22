
export interface PersonalDetails {
  name: string;
  title: string;
  email: string;
  phone: string;
  location: string;
  linkedin: string;
  github: string;
  website: string;
  photo: string;
}

export interface Experience {
  id: string;
  company: string;
  role: string;
  employmentType: string;
  location: string;
  locationType: string;
  isCurrent: boolean;
  startDate: string; // e.g., "January 2024"
  endDate: string; // e.g., "December 2024" or "Present"
  description: string[];
  skills: string[];
  media: string[];
}

export interface Education {
  id: string;
  institution: string;
  degree: string;
  duration: string;
  score: string;
  description: string[];
}

export interface Skill {
  id: string;
  name: string;
  level: number; // 0-100
}

export interface Certificate {
  id: string;
  name: string;
}

export interface Hobby {
    id: string;
    name: string;
}

export interface SuggestedSkill {
  name: string;
  category: 'Frontend' | 'Backend' | 'Programming' | 'Cloud';
}

export interface Resume {
  personalDetails: PersonalDetails;
  objective: string;
  experience: Experience[];
  education: Education[];
  backendSkills: Skill[];
  frontendSkills: Skill[];
  programmingSkills: Skill[];
  cloudSkills: Skill[];
  certificates: Certificate[];
  hobbies: Hobby[];
}

export interface ATSScoreResult {
  score: number;
  summary: string;
  strengths: string[];
  improvements: string[];
}