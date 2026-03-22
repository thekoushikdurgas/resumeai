"use client";

import React, { useRef, useState, useEffect, useMemo } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { ResumePreview } from "@/components/editor/ResumePreview";
import { ResumeSkeleton } from "@/components/editor/ResumeSkeleton";
import { type Resume, type Skill, type SuggestedSkill, type ATSScoreResult } from "@/types/resume";
import * as resumeApi from "@/lib/resumeApiClient";
import { RESUME_AI_API_KEY } from "@/lib/config";
import { useHistoryState, HistoryEntry } from "@/hooks/useHistoryState";
import { SkillSuggestionModal } from "@/components/modals/SkillSuggestionModal";
import { ImageCropModal } from "@/components/modals/ImageCropModal";
import { produce } from "immer";
import { PublishModal } from "@/components/modals/PublishModal";
import { HistorySidebar } from "@/components/layout/HistorySidebar";
import { HistoryIcon } from "@/components/common/icons";
import { useDebounce } from "@/hooks/useDebounce";
import { ATSScoreModal } from "@/components/modals/ATSScoreModal";
import { ProfilePage } from "@/components/ProfilePage";
import { LinkedInImportModal } from "@/components/modals/LinkedInImportModal";
import type { AppUser } from "@/types/user";
import type { LatexTemplate } from "@/types/latex";
import * as resumeService from "@/services/graphql/resumeService";
import { useAuth } from "@/context/AuthContext";
import { setResumeEditorStore } from "@/context/ResumeContext";
import { LoginForm } from "@/components/LoginForm";

const MAX_AI_INPUT_CHARS = 750000; // ~750KB JSON string, a safe proxy for token limits.

const isResumeTooLargeForAI = (resume: Resume): boolean => {
    try {
        const jsonString = JSON.stringify(resume);
        return jsonString.length > MAX_AI_INPUT_CHARS;
    } catch (e) {
        console.error("Failed to stringify resume data:", e);
        return true;
    }
};

declare global {
  interface Window {
    jspdf: any;
    html2canvas: any;
    docx: any;
    FileSaver: any;
  }
}

const initialResumeData: Resume = {
  personalDetails: {
    name: 'KOUSHIK CHANDRA SAHA',
    title: 'Full Stack Developer & DC Analytics',
    email: 'koushikchandrasaha558@gmail.com',
    phone: '9933454265 & 8167334088',
    location: '13/23 Edison Road, B-zone, Durgapur, Paschim Bardhaman, West Bengal, Pin code: 713205',
    linkedin: '@koushikchandrasaha',
    github: '@thekoushikdurgas',
    website: 'www.thekoushikdurgas.com',
    photo: '',
  },
  objective: 'To work with an organization with great enthusiasm and energy, where I can contribute my best and get an opportunity to learn and grow with the organization.',
  experience: [
    { id: 'exp1', company: 'Deloitte USI', role: 'DC analyst', employmentType: 'Full-time', location: 'Durgapur, India', locationType: 'On-site', isCurrent: true, startDate: 'January 2024', endDate: 'Present', description: ['I worked on many projects or data analysist in this Company'], skills: ['Data Analysis'], media: [] },
    { id: 'exp2', company: 'Karmaa Lab', role: 'Full Stack Developer', employmentType: 'Internship', location: 'Remote', locationType: 'Remote', isCurrent: false, startDate: 'October 2023', endDate: 'December 2023', description: ['I worked on many projects or Software in this Company'], skills: ['React', 'Node.js'], media: [] },
    { id: 'exp3', company: 'Flexon Technologies Limited', role: 'PHP developer', employmentType: 'Internship', location: 'Durgapur, India', locationType: 'On-site', isCurrent: false, startDate: 'June 2023', endDate: 'July 2023', description: ['Created a project called Student management software'], skills: ['PHP', 'MySQL'], media: [] },
  ],
  education: [
    { id: 'edu1', institution: 'NATIONAL INSTITUTE OF TECHNOLOGY, ARUNACHAL PRADESH', degree: 'COMPUTER SCIENCE AND ENGINEERING, CLASS OF 2019', duration: '2019 - 2023', score: 'Overall Grade Point: 7.3', description: ['Key project: AI-powered resume editor.'] },
    { id: 'edu2', institution: 'BIDHAN CHANDRA INSTITUTION', degree: 'COMPUTER SCIENCE, CLASS OF 2017', duration: '2017 - 2019', score: '80% Marks', description: [] },
    { id: 'edu3', institution: 'SUREN CHANDRA MODERN SCHOOL (H.S.)', degree: 'COMPUTER SCIENCE, CLASS OF 2007', duration: '2007 - 2017', score: '85% Marks', description: [] },
  ],
  backendSkills: [
    { id: 'bs1', name: 'Node.js', level: 90 },
    { id: 'bs2', name: 'Express.js', level: 90 },
    { id: 'bs3', name: 'MongoDB', level: 90 },
    { id: 'bs4', name: 'MySQL', level: 90 },
    { id: 'bs5', name: 'PHP', level: 90 },
    { id: 'bs6', name: 'Firebase', level: 50 },
    { id: 'bs7', name: 'Heroku', level: 100 },
    { id: 'bs8', name: 'Netlify', level: 100 },
    { id: 'bs9', name: 'SQLite', level: 100 },
  ],
  frontendSkills: [
    { id: 'fs1', name: 'HTML5', level: 100 },
    { id: 'fs2', name: 'CSS3', level: 100 },
    { id: 'fs3', name: 'JavaScript', level: 90 },
    { id: 'fs4', name: 'React', level: 90 },
    { id: 'fs5', name: 'WordPress', level: 50 },
    { id: 'fs6', name: 'Bootstrap 5', level: 100 },
    { id: 'fs7', name: 'Tailwind CSS', level: 100 },
    { id: 'fs8', name: 'Sass', level: 50 },
    { id: 'fs9', name: 'Git', level: 90 },
    { id: 'fs10', name: 'GitHub', level: 90 },
    { id: 'fs11', name: 'Django', level: 100 },
  ],
  programmingSkills: [
    { id: 'ps1', name: 'C or C++', level: 100 },
    { id: 'ps2', name: 'Java', level: 90 },
    { id: 'ps3', name: 'Python', level: 100 },
    { id: 'ps4', name: 'Data Structures and Algorithms', level: 80 },
    { id: 'ps5', name: 'Program Management', level: 50 },
    { id: 'ps6', name: 'HackerRank', level: 100 },
    { id: 'ps7', name: 'CodeChef', level: 100 },
    { id: 'ps8', name: 'Codeforces', level: 100 },
  ],
  cloudSkills: [
    { id: 'cs1', name: 'AWS', level: 80 },
    { id: 'cs2', name: 'GCD', level: 50 },
  ],
  certificates: [
    { id: 'cert1', name: 'GOOGLE ASSOCIATE CLOUD ENGINEER' }
  ],
  hobbies: [
    { id: 'hob1', name: 'Reading' },
    { id: 'hob2', name: 'Playing Cricket & Volleyball & Badminton' },
    { id: 'hob3', name: 'Tabla' },
    { id: 'hob4', name: 'Painting' },
    { id: 'hob5', name: 'Travelling' },
  ],
};

interface Change {
  description: string;
  timestamp: number;
}

const getArrayChanges = (prev: any[], curr: any[], itemName: string): string[] => {
    if (curr.length > prev.length) return [`Added an item to ${itemName}`];
    if (curr.length < prev.length) return [`Removed an item from ${itemName}`];
    if (JSON.stringify(prev) !== JSON.stringify(curr)) return [`Modified ${itemName}`];
    return [];
};

const generateChangeLog = (history: HistoryEntry<Resume>[], present: number): Change[] => {
    const changes: Change[] = [];
    for (let i = 1; i <= present; i++) {
        const prev = history[i-1].state;
        const curr = history[i].state;
        const timestamp = history[i].timestamp;
        const stepChanges: string[] = [];

        if (JSON.stringify(prev.personalDetails) !== JSON.stringify(curr.personalDetails)) {
            stepChanges.push("Updated personal details");
        }
        if (prev.objective !== curr.objective) {
            stepChanges.push("Updated objective");
        }

        const sections: { key: keyof Resume, name: string }[] = [
            { key: 'experience', name: 'Experience' },
            { key: 'education', name: 'Education' },
            { key: 'backendSkills', name: 'Backend Skills' },
            { key: 'frontendSkills', name: 'Frontend Skills' },
            { key: 'programmingSkills', name: 'Programming Skills' },
            { key: 'cloudSkills', name: 'Cloud Skills' },
            { key: 'certificates', name: 'Certificates' },
            { key: 'hobbies', name: 'Hobbies' },
        ];
        
        sections.forEach(section => {
            stepChanges.push(...getArrayChanges(prev[section.key] as any[], curr[section.key] as any[], section.name));
        });

        if (stepChanges.length > 0) {
            changes.push({ description: stepChanges.join(', '), timestamp });
        }
    }
    return changes;
};

const validateLatexCode = (code: string): boolean => {
    const trimmedCode = code.trim();

    if (!trimmedCode.startsWith('\\documentclass') || !trimmedCode.endsWith('\\end{document}')) {
        console.error("Validation failed: Missing documentclass or end document.");
        return false;
    }

    if (trimmedCode.includes('<<') || trimmedCode.includes('>>')) {
        console.error("Validation failed: Un-replaced placeholders found.");
        return false;
    }

    const beginCount = (trimmedCode.match(/\\begin{/g) || []).length;
    const endCount = (trimmedCode.match(/\\end{/g) || []).length;
    if (beginCount !== endCount) {
        console.error(`Validation failed: Mismatched begin/end blocks. Begins: ${beginCount}, Ends: ${endCount}`);
        return false;
    }
    
    if (trimmedCode.length < 150) { 
         console.error("Validation failed: Generated code is too short to be a valid document.");
         return false;
    }

    return true;
};

const generateTxtContent = (resume: Resume): string => {
    const { personalDetails, objective, experience, education, backendSkills, frontendSkills, programmingSkills, cloudSkills, certificates, hobbies } = resume;
    
    const divider = '\n' + '='.repeat(50) + '\n\n';
    
    let txt = `${personalDetails.name.toUpperCase()}\n`;
    txt += `${personalDetails.title}\n\n`;

    txt += `CONTACT\n`;
    txt += `--------------------\n`;
    txt += `Email: ${personalDetails.email}\n`;
    txt += `Phone: ${personalDetails.phone}\n`;
    txt += `Location: ${personalDetails.location}\n`;
    if (personalDetails.linkedin) txt += `LinkedIn: ${personalDetails.linkedin}\n`;
    if (personalDetails.github) txt += `GitHub: ${personalDetails.github}\n`;
    if (personalDetails.website) txt += `Website: ${personalDetails.website}\n\n`;

    txt += divider;

    txt += `OBJECTIVE\n\n${objective}\n\n`;

    txt += divider;

    txt += `EXPERIENCE\n\n`;
    experience.forEach(exp => {
        txt += `${exp.role.toUpperCase()} | ${exp.company}\n`;
        txt += `${exp.startDate} - ${exp.endDate}\n`;
        exp.description.forEach(desc => {
            txt += `  - ${desc}\n`;
        });
        txt += `\n`;
    });

    txt += divider;

    txt += `EDUCATION\n\n`;
    education.forEach(edu => {
        txt += `${edu.institution.toUpperCase()}\n`;
        txt += `${edu.degree} (${edu.duration})\n`;
        txt += `Score: ${edu.score}\n`;
        if(edu.description.length > 0) {
            edu.description.forEach(desc => {
                txt += `  - ${desc}\n`;
            });
        }
        txt += `\n`;
    });

    txt += divider;
    
    txt += `SKILLS\n\n`;
    if (backendSkills.length > 0) txt += `Backend: ${backendSkills.map(s => s.name).join(', ')}\n`;
    if (frontendSkills.length > 0) txt += `Frontend: ${frontendSkills.map(s => s.name).join(', ')}\n`;
    if (programmingSkills.length > 0) txt += `Programming: ${programmingSkills.map(s => s.name).join(', ')}\n`;
    if (cloudSkills.length > 0) txt += `Cloud: ${cloudSkills.map(s => s.name).join(', ')}\n\n`;
    
    if (certificates.length > 0) {
        txt += divider;
        txt += `CERTIFICATES\n\n`;
        certificates.forEach(cert => {
            txt += `- ${cert.name}\n`;
        });
        txt += `\n`;
    }

    if (hobbies.length > 0) {
        txt += divider;
        txt += `HOBBIES\n\n`;
        txt += hobbies.map(h => h.name).join(', ');
        txt += `\n`;
    }

    return txt;
};

const generateDocxBlob = (resume: Resume): Promise<Blob> => {
    return new Promise((resolve, reject) => {
        const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, TabStopType, TabStopPosition, UnderlineType } = window.docx;
        if (!Document) {
            reject(new Error("docx library not loaded"));
            return;
        }

        const contactInfo = [
            resume.personalDetails.email,
            resume.personalDetails.phone,
            resume.personalDetails.location,
            resume.personalDetails.linkedin,
            resume.personalDetails.github,
            resume.personalDetails.website
        ].filter(Boolean).join(' | ');

        const children = [
            new Paragraph({
                children: [new TextRun({ text: resume.personalDetails.name, bold: true, size: 48 })],
                alignment: AlignmentType.CENTER,
            }),
            new Paragraph({
                children: [new TextRun({ text: resume.personalDetails.title, size: 28, color: "555555" })],
                alignment: AlignmentType.CENTER,
            }),
             new Paragraph({
                children: [new TextRun({ text: contactInfo, size: 20, color: "555555" })],
                alignment: AlignmentType.CENTER,
                spacing: { after: 200 },
            }),
        ];

        // Fix: Changed type annotation for 'content' from '(Paragraph | any)[]' to 'any[]'. 'Paragraph' is a value from the dynamically loaded docx library, not a TypeScript type.
        const addSection = (title: string, content: any[]) => {
            if (content.length > 0) {
                children.push(new Paragraph({
                    children: [new TextRun({ text: title, bold: true, size: 28, allCaps: true, color: "333333" })],
                    spacing: { before: 300, after: 100 },
                    border: { bottom: { color: "auto", space: 1, value: "single", size: 6 } },
                }));
                children.push(...content);
            }
        };

        addSection('Objective', [new Paragraph({ children: [new TextRun(resume.objective)] })]);
        
        addSection('Experience', resume.experience.flatMap(exp => [
            new Paragraph({
                children: [
                    new TextRun({ text: exp.company, bold: true, size: 24 }),
                    new TextRun({ text: `\t${exp.startDate} - ${exp.endDate}`, bold: true, size: 24 }),
                ],
                tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
            }),
            new Paragraph({ children: [new TextRun({ text: exp.role, italics: true, size: 22 })] }),
            ...exp.description.map(desc => new Paragraph({ text: desc, bullet: { level: 0 } }))
        ]));

        addSection('Education', resume.education.flatMap(edu => [
            new Paragraph({
                children: [
                    new TextRun({ text: edu.institution, bold: true, size: 24 }),
                    new TextRun({ text: `\t${edu.duration}`, bold: true, size: 24 }),
                ],
                tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
            }),
            new Paragraph({ children: [
                new TextRun({ text: edu.degree, italics: true, size: 22 }),
                new TextRun({ text: ` | Score: ${edu.score}`, italics: true, size: 22 })
            ] }),
            ...edu.description.map(desc => new Paragraph({ text: desc, bullet: { level: 0 } }))
        ]));

        const skillContent: unknown[] = [];
        const createSkillPara = (title: string, skills: Skill[]) => {
            if(skills.length > 0) {
                skillContent.push(new Paragraph({
                    children: [
                        new TextRun({ text: `${title}: `, bold: true }),
                        new TextRun(skills.map(s => s.name).join(', ')),
                    ]
                }));
            }
        };
        createSkillPara('Backend', resume.backendSkills);
        createSkillPara('Frontend', resume.frontendSkills);
        createSkillPara('Programming', resume.programmingSkills);
        createSkillPara('Cloud', resume.cloudSkills);
        addSection('Skills', skillContent);
        
        addSection('Certificates', resume.certificates.map(cert => new Paragraph({ text: cert.name, bullet: { level: 0 } })));
        addSection('Hobbies', [new Paragraph(resume.hobbies.map(h => h.name).join(', '))]);

        const doc = new Document({
            sections: [{ children }]
        });

        Packer.toBlob(doc).then(resolve);
    });
};

export function ResumeEditor() {
  const {
    state: resumeData,
    setState: setResumeData,
    resetState: resetResumeData,
    loadState: loadHistoryState,
    undo,
    redo,
    canUndo,
    canRedo,
    history,
    present,
  } = useHistoryState<Resume>(initialResumeData);

  const { user: authUser, isLoading: authLoading, logout } = useAuth();
  const user: AppUser | null = authUser
    ? { id: authUser.uuid, email: authUser.email }
    : null;

  const [activeResumeId, setActiveResumeId] = useState<string | null>(null);

  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [template, setTemplate] = useState<'classic' | 'modern' | 'compact'>('classic');
  const [latexTemplate, setLatexTemplate] = useState<LatexTemplate>("professional");
  const [aiProvider, setAiProvider] = useState<"gemini" | "huggingface">("gemini");
  const isAiEnabled = Boolean(RESUME_AI_API_KEY) || process.env.NODE_ENV === "development";
  const resumePreviewRef = useRef<HTMLDivElement>(null);
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  });
  const [imageToCrop, setImageToCrop] = useState<string | null>(null);
  const [isEnhancingPhoto, setIsEnhancingPhoto] = useState(false);
  const [isUploadingPhoto, setIsUploadingPhoto] = useState(false);

  const [isPublishedView, setIsPublishedView] = useState(false);
  const [isPublishModalOpen, setIsPublishModalOpen] = useState(false);
  const [publishedUrl, setPublishedUrl] = useState('');
  const [isHistorySidebarOpen, setIsHistorySidebarOpen] = useState(false);
  const [changeLog, setChangeLog] = useState<Change[]>([]);
  
  const [isATSModalOpen, setIsATSModalOpen] = useState(false);
  const [isCheckingATSScore, setIsCheckingATSScore] = useState(false);
  const [isUpdatingWithAI, setIsUpdatingWithAI] = useState(false);
  const [atsScoreResult, setAtsScoreResult] = useState<ATSScoreResult | null>(null);
  const [atsScoreError, setAtsScoreError] = useState<string | null>(null);
  
  const [currentView, setCurrentView] = useState<'editor' | 'profile'>('editor');

  const [isLinkedInModalOpen, setIsLinkedInModalOpen] = useState(false);
  const [isScrapingLinkedIn, setIsScrapingLinkedIn] = useState(false);
  const [linkedInError, setLinkedInError] = useState<string | null>(null);

  const [isSuggestingSkills, setIsSuggestingSkills] = useState(false);
  const [skillSuggestions, setSkillSuggestions] = useState<SuggestedSkill[]>([]);
  const [skillSuggestionError, setSkillSuggestionError] = useState<string | null>(null);
  const [isSuggestionModalOpen, setIsSuggestionModalOpen] = useState(false);

  const historyState = useMemo(() => ({ history, present }), [history, present]);
  const debouncedHistoryState = useDebounce(historyState, 1500);

  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [theme]);

  // This effect handles URL parsing for shared links.
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const resumeDataParam = params.get('resume');

    if (resumeDataParam) {
        setIsPublishedView(true);
        setIsLoading(true);
        try {
            const decodedUriComponent = decodeURIComponent(atob(resumeDataParam));
            const parsedResume = JSON.parse(decodedUriComponent);
            resetResumeData(parsedResume);
        } catch (error) {
            console.error("Failed to parse resume data from URL", error);
            setError("The shared resume link is invalid or corrupted.");
        } finally {
            setIsLoading(false);
        }
    } else {
        setIsPublishedView(false);
    }
  }, [resetResumeData]);

  // Load resumes from GraphQL when the user logs in.
  useEffect(() => {
    if (isPublishedView || !authUser) {
      if (!authUser) {
        resetResumeData(initialResumeData);
        setCurrentView("editor");
        setActiveResumeId(null);
      }
      return;
    }

    let cancelled = false;
    (async () => {
      setIsLoading(true);
      setLoadingMessage("Loading your resume...");
      setError(null);
      try {
        const list = await resumeService.listResumes();
        if (cancelled) return;
        if (list.length > 0) {
          setActiveResumeId(list[0].id);
          resetResumeData(list[0].resumeData);
        } else {
          const newUserData = produce(initialResumeData, (draft) => {
            draft.personalDetails.email = authUser.email || "";
          });
          resetResumeData(newUserData);
          setActiveResumeId(null);
        }
      } catch (err) {
        console.error("Failed to load resume:", err);
        setError("Could not load saved resumes. You can still edit locally.");
      } finally {
        if (!cancelled) {
          setIsLoading(false);
          setLoadingMessage("");
        }
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [authUser, isPublishedView, resetResumeData]);

  // Persist history to GraphQL (debounced).
  useEffect(() => {
    if (!authUser || isPublishedView || history.length <= 1) {
      return;
    }

    const save = async () => {
      setIsSaving(true);
      setError(null);
      try {
        const saved = await resumeService.saveResume({
          id: activeResumeId ?? undefined,
          resumeData,
        });
        setActiveResumeId(saved.id);
      } catch (err) {
        console.error("Failed to save resume:", err);
        setError("Failed to save changes to the server.");
      } finally {
        setIsSaving(false);
      }
    };

    save();
  }, [debouncedHistoryState, authUser, isPublishedView, history.length, resumeData, activeResumeId]);
  
  useEffect(() => {
    const newLog = generateChangeLog(history, present);
    setChangeLog(newLog);
  }, [history, present]);

  const handleToggleTheme = () => {
    setTheme(prevTheme => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  const handleFileUpload = async (file: File) => {
    setIsSuggestionModalOpen(false);
    setSkillSuggestions([]);
    setSkillSuggestionError(null);
    
    const MAX_FILE_SIZE_MB = 2;
    const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;
    if (file.size > MAX_FILE_SIZE_BYTES) {
        setError(`File is too large. Please upload a file smaller than ${MAX_FILE_SIZE_MB}MB to prevent AI processing errors.`);
        return;
    }
    
    setIsLoading(true);
    setLoadingMessage(`Parsing your resume…`);
    setError(null);
    try {
      const parsedData = await resumeApi.parseResumeFile(file);
      resetResumeData(parsedData);
    } catch (e: any) {
      console.error(e);
      setError(e.message || 'Failed to parse the resume. Please try a different file.');
    } finally {
      setIsLoading(false);
      setLoadingMessage('');
    }
  };

  const handleExportPdf = () => {
    if (!resumePreviewRef.current || !window.jspdf || !window.html2canvas) {
        alert("PDF generation libraries not loaded yet.");
        return;
    }
    const { jsPDF } = window.jspdf;
    const resumeElement = resumePreviewRef.current;
    
    resumeElement.classList.add('pdf-export-mode');
    
    const originalBorder = resumeElement.style.border;
    resumeElement.style.border = 'none';

    window.html2canvas(resumeElement, {
      scale: 2,
      useCORS: true,
      logging: false,
      backgroundColor: theme === 'light' ? '#ffffff' : '#1f2937',
    }).then((canvas: HTMLCanvasElement) => {
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({ orientation: 'portrait', unit: 'px', format: [canvas.width, canvas.height] });
      pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
      pdf.save(`${resumeData.personalDetails.name.replace(' ', '_')}_Resume.pdf`);
    }).catch((err: unknown) => {
        console.error("Error generating PDF:", err);
        setError("Could not generate PDF.");
    }).finally(() => {
        resumeElement.style.border = originalBorder;
        resumeElement.classList.remove('pdf-export-mode');
    });
  };
  
  const handlePublish = () => {
    try {
        const jsonString = JSON.stringify(resumeData);
        const encodedData = btoa(encodeURIComponent(jsonString)); 
        const url = `${window.location.origin}${window.location.pathname}?resume=${encodedData}`;
        setPublishedUrl(url);
        setIsPublishModalOpen(true);
    } catch (error) {
        console.error("Failed to publish resume:", error);
        setError("Could not generate a shareable link. The resume data might be too large.");
    }
  };

  const handleSuggestSkills = async () => {
    setIsSuggestionModalOpen(true);
    setIsSuggestingSkills(true);
    setSkillSuggestionError(null);
    setSkillSuggestions([]);
    
    if (!isAiEnabled) {
        setSkillSuggestionError("Resume AI is not configured. Set NEXT_PUBLIC_RESUME_AI_API_KEY.");
        setIsSuggestingSkills(false);
        return;
    }

    try {
      const title = resumeData.personalDetails.title;
      const experience = resumeData.experience.map(exp => 
        `- ${exp.role} at ${exp.company}:\n${exp.description.join('\n')}`
      ).join('\n\n');

      const suggestions = await resumeApi.suggestSkills(title, experience);

      const existingSkills = new Set([
        ...resumeData.backendSkills.map(s => s.name.toLowerCase()),
        ...resumeData.frontendSkills.map(s => s.name.toLowerCase()),
        ...resumeData.programmingSkills.map(s => s.name.toLowerCase()),
        ...resumeData.cloudSkills.map(s => s.name.toLowerCase()),
      ]);
      const newSuggestions = suggestions.filter(s => !existingSkills.has(s.name.toLowerCase()));
      setSkillSuggestions(newSuggestions);
    } catch (e) {
      console.error(e);
      setSkillSuggestionError("Failed to get skill suggestions. Please try again.");
    } finally {
      setIsSuggestingSkills(false);
    }
  };
  
  const handleEnhanceSection = async (
    sectionContent: string | string[],
    enhancementType: 'objective' | 'description' | 'hobbies' | 'education_description'
  ): Promise<string> => {
      return resumeApi.enhanceSection(sectionContent, enhancementType);
  };
  
  const handleCheckATSScore = async () => {
    if (isResumeTooLargeForAI(resumeData)) {
        setAtsScoreResult(null);
        setAtsScoreError("Your resume contains too much text for the AI to analyze. Please reduce its length and try again.");
        setIsCheckingATSScore(false);
        setIsATSModalOpen(true);
        return;
    }

    setIsATSModalOpen(true);
    setIsCheckingATSScore(true);
    setAtsScoreError(null);
    setAtsScoreResult(null);

    if (!isAiEnabled) {
        setAtsScoreError("Resume AI is not configured (missing API key).");
        setIsCheckingATSScore(false);
        return;
    }

    try {
        const result = await resumeApi.checkATSScore(resumeData);
        setAtsScoreResult(result);
    } catch (e: any) {
        console.error(e);
        setAtsScoreError(`Failed to get ATS score. ${e.message}`);
    } finally {
        setIsCheckingATSScore(false);
    }
  };
  
  const handleAiUpdateResume = async () => {
    if (isResumeTooLargeForAI(resumeData)) {
        setAtsScoreError("Your resume contains too much text for the AI to process. Please reduce its length before attempting an update.");
        return;
    }

    setIsUpdatingWithAI(true);
    setIsCheckingATSScore(true);
    setAtsScoreResult(null);
    setAtsScoreError(null);

    if (!isAiEnabled) {
        setAtsScoreError("Resume AI is not configured (missing API key).");
        setIsUpdatingWithAI(false);
        setIsCheckingATSScore(false);
        return;
    }

    try {
        const enhancedResume = await resumeApi.improveResumeForATS(resumeData, {
          atsResult: atsScoreResult ?? undefined,
        });

        setResumeData(enhancedResume);

        const newResult = await resumeApi.checkATSScore(enhancedResume);

        setAtsScoreResult(newResult);

    } catch (e: any) {
        console.error(e);
        setAtsScoreError(`Failed to update resume with AI. ${e.message}`);
    } finally {
        setIsUpdatingWithAI(false);
        setIsCheckingATSScore(false);
    }
  };

  const handleAddSkills = (skillsToAdd: SuggestedSkill[]) => {
    if (skillsToAdd.length === 0) return;

    const nextState = produce(resumeData, draft => {
        skillsToAdd.forEach((skill, index) => {
            const newSkill: Skill = {
                id: `new-skill-${Date.now()}-${index}`,
                name: skill.name,
                level: 75,
            };
            switch (skill.category) {
                case 'Frontend': draft.frontendSkills.push(newSkill); break;
                case 'Backend': draft.backendSkills.push(newSkill); break;
                case 'Programming': draft.programmingSkills.push(newSkill); break;
                case 'Cloud': draft.cloudSkills.push(newSkill); break;
                default: draft.programmingSkills.push(newSkill); break;
            }
        });
    });

    setResumeData(nextState);
  };
  
  const handlePhotoSelectForCrop = (file: File) => {
    if (!file) return;

    const allowedTypes = ['image/png', 'image/jpeg', 'image/webp'];
    const maxSizeInBytes = 5 * 1024 * 1024; // 5MB

    if (!allowedTypes.includes(file.type)) {
      setError("Invalid file type. Please upload a PNG, JPG, or WEBP image.");
      return;
    }

    if (file.size > maxSizeInBytes) {
      setError(`File is too large. Please upload an image smaller than ${maxSizeInBytes / 1024 / 1024}MB.`);
      return;
    }
    
    setError(null);

    const reader = new FileReader();
    reader.onloadend = () => {
        setImageToCrop(reader.result as string);
    };
    reader.onerror = () => {
        setError("Failed to read the photo file.");
    };
    reader.readAsDataURL(file);
  };
  
  const handlePhotoCropped = async (base64String: string) => {
    setImageToCrop(null);
    setResumeData(
      produce(resumeData, (draft) => {
        draft.personalDetails.photo = base64String;
      })
    );
  };

  const handleEnhancePhoto = async () => {
    if (!isAiEnabled || !resumeData.personalDetails.photo) {
      setError("Photo enhancement requires an existing photo and a configured Resume AI URL/key.");
      return;
    }

    setIsEnhancingPhoto(true);
    setError(null);

    try {
      const blob = await fetch(resumeData.personalDetails.photo).then((r) => r.blob());
      const file = new File([blob], "photo.jpg", { type: blob.type || "image/jpeg" });
      const enhanced = await resumeApi.enhancePhotoFile(file);
      const url = enhanced.startsWith("data:") ? enhanced : `data:image/png;base64,${enhanced}`;
      setResumeData(
        produce(resumeData, (draft) => {
          draft.personalDetails.photo = url;
        })
      );
    } catch (e: unknown) {
      console.error("Failed to enhance photo", e);
      setError(e instanceof Error ? e.message : "An error occurred while enhancing the photo.");
    } finally {
      setIsEnhancingPhoto(false);
    }
  };

  const handleSignOut = async () => {
    try {
      await logout();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to sign out.");
    }
  };

  const handleExportLatex = async () => {
    if (isResumeTooLargeForAI(resumeData)) {
      setError("Your resume contains too much text to generate a LaTeX file. Please reduce its length and try again.");
      return;
    }

    if (!isAiEnabled) {
      setError("LaTeX export requires Resume AI to be configured.");
      return;
    }

    setIsLoading(true);
    setLoadingMessage("Generating & Validating LaTeX...");
    setError(null);

    try {
      const latexCode = await resumeApi.generateLatex(resumeData, latexTemplate);
        
        const cleanedCode = latexCode.replace(/^```latex\s*|```\s*$/g, '').trim();

        if (!validateLatexCode(cleanedCode)) {
            throw new Error("The AI generated invalid LaTeX code. This can happen occasionally. Please try exporting again, or select a different template.");
        }

        const blob = new Blob([cleanedCode], { type: 'text/x-latex' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${resumeData.personalDetails.name.replace(/\s+/g, '_')}_Resume.tex`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (e: any) {
        console.error(e);
        setError(e.message || 'Failed to generate LaTeX code. Please try again.');
    } finally {
        setIsLoading(false);
        setLoadingMessage('');
    }
  };

  const handleExportJson = () => {
    const jsonString = JSON.stringify(resumeData, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    if (window.FileSaver) {
        window.FileSaver.saveAs(blob, `${resumeData.personalDetails.name.replace(/\s+/g, '_')}_Resume.json`);
    }
  };

  const handleExportTxt = () => {
    const txtContent = generateTxtContent(resumeData);
    const blob = new Blob([txtContent], { type: 'text/plain;charset=utf-8' });
    if (window.FileSaver) {
        window.FileSaver.saveAs(blob, `${resumeData.personalDetails.name.replace(/\s+/g, '_')}_Resume.txt`);
    }
  };
  
  const handleExportDocx = async () => {
    if (!window.docx || !window.FileSaver) {
        setError("Word export library not loaded. Please try again in a moment.");
        return;
    }
    setIsLoading(true);
    setLoadingMessage("Generating Word document...");
    try {
        const blob = await generateDocxBlob(resumeData);
        window.FileSaver.saveAs(blob, `${resumeData.personalDetails.name.replace(/\s+/g, '_')}_Resume.docx`);
    } catch (e) {
        console.error("Failed to generate DOCX:", e);
        setError("An error occurred while generating the Word document.");
    } finally {
        setIsLoading(false);
        setLoadingMessage("");
    }
  };

  const handleImportFromLinkedIn = async (url: string) => {
    if (!isAiEnabled) {
      setLinkedInError("Resume AI is not configured.");
      return;
    }
    setIsScrapingLinkedIn(true);
    setLinkedInError(null);
    try {
      const scrapedData = await resumeApi.importLinkedIn(url);
      resetResumeData(scrapedData);
      setIsLinkedInModalOpen(false);
    } catch (e: unknown) {
      console.error("Failed to import LinkedIn profile:", e);
      const message = e instanceof Error ? e.message : "Unexpected error while importing from LinkedIn.";
      setLinkedInError(`Import failed: ${message}`);
    } finally {
      setIsScrapingLinkedIn(false);
    }
  };

  useEffect(() => {
    setResumeEditorStore({
      resumeData,
      setResumeData,
      isLoading,
      loadingMessage,
      error,
      isSaving,
      template,
      setTemplate,
      latexTemplate,
      setLatexTemplate,
      aiProvider,
      setAiProvider,
      isAiEnabled,
      history,
      present,
      canUndo,
      canRedo,
      undo,
      redo,
      isHistorySidebarOpen,
      setIsHistorySidebarOpen,
      changeLog,
      theme,
      handleToggleTheme,
      currentView,
      setCurrentView,
      handleFileUpload,
      handleExportPdf,
      handleExportLatex,
      handleExportDocx,
      handleExportTxt,
      handleExportJson,
      handleSuggestSkills,
      handleCheckATSScore,
      handlePublish,
      handlePhotoCropped,
      handlePhotoSelectForCrop,
      handleEnhancePhoto,
      handleEnhanceSection,
      handleAiUpdateResume,
      handleSignOut,
      isATSModalOpen,
      setIsATSModalOpen,
      isSuggestionModalOpen,
      setIsSuggestionModalOpen,
      isLinkedInModalOpen,
      setIsLinkedInModalOpen,
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps -- editor API snapshot
  });

  if (authLoading) {
    return <ResumeSkeleton message="Signing in…" />;
  }

  if (!authUser) {
    return <LoginForm />;
  }

  if (isLoading && !isPublishedView) {
    return <ResumeSkeleton message={loadingMessage || "Loading…"} />;
  }

  if (isPublishedView) {
    return (
        <div className="flex flex-col min-h-screen font-sans bg-gray-100 dark:bg-gray-900 text-text-primary dark:text-gray-200">
            <main className="flex-1 p-4 md:p-8 overflow-y-auto">
                {error && (
                    <div className="bg-red-100 border border-accent text-accent px-4 py-3 rounded-md relative mb-4 dark:bg-red-900/50 dark:text-red-200 dark:border-red-700" role="alert">
                        <strong className="font-bold">Error: </strong>
                        <span className="block sm:inline">{error}</span>
                    </div>
                )}
                <div className="max-w-4xl mx-auto">
                    <ResumePreview
                        ref={resumePreviewRef}
                        data={resumeData}
                        setData={() => {}} 
                        template={template}
                        aiProvider={aiProvider}
                        onEnhance={async () => ''}
                        isAiEnabled={false}
                        onPhotoUpload={() => {}}
                        onEnhancePhoto={() => {}}
                        isEnhancingPhoto={false}
                        isUploadingPhoto={false}
                        isReadOnly={true}
                    />
                </div>
                <footer className="text-center text-sm text-gray-500 py-4 mt-4">
                    <p>Powered by AI Resume Editor. <a href={window.location.origin + window.location.pathname} className="text-primary hover:underline font-semibold">Create your own resume!</a></p>
                </footer>
            </main>
        </div>
    );
  }

  return (
    <div className="relative flex flex-col md:flex-row min-h-screen font-sans bg-gray-100 dark:bg-gray-900 text-text-primary dark:text-gray-200">
      <ATSScoreModal 
        isOpen={isATSModalOpen}
        onClose={() => setIsATSModalOpen(false)}
        isLoading={isCheckingATSScore}
        error={atsScoreError}
        result={atsScoreResult}
        onAiUpdate={handleAiUpdateResume}
        isUpdating={isUpdatingWithAI}
      />
      <SkillSuggestionModal
        isOpen={isSuggestionModalOpen}
        onClose={() => setIsSuggestionModalOpen(false)}
        isLoading={isSuggestingSkills}
        error={skillSuggestionError}
        suggestedSkills={skillSuggestions}
        onAddSkills={handleAddSkills}
      />
      <ImageCropModal
        isOpen={!!imageToCrop}
        onClose={() => setImageToCrop(null)}
        imageSrc={imageToCrop}
        onCropComplete={handlePhotoCropped}
      />
      <LinkedInImportModal
          isOpen={isLinkedInModalOpen}
          onClose={() => {
              setIsLinkedInModalOpen(false);
              setLinkedInError(null);
          }}
          onImport={handleImportFromLinkedIn}
          isLoading={isScrapingLinkedIn}
          error={linkedInError}
      />
      <Sidebar
        onFileUpload={handleFileUpload}
        onImportFromLinkedIn={() => setIsLinkedInModalOpen(true)}
        onExportPdf={handleExportPdf}
        onExportLatex={handleExportLatex}
        onExportDocx={handleExportDocx}
        onExportTxt={handleExportTxt}
        onExportJson={handleExportJson}
        onSuggestSkills={handleSuggestSkills}
        onCheckATSScore={handleCheckATSScore}
        onPublish={handlePublish}
        currentTemplate={template}
        onTemplateChange={setTemplate}
        latexTemplate={latexTemplate}
        onLatexTemplateChange={setLatexTemplate}
        onToggleTheme={handleToggleTheme}
        currentTheme={theme}
        aiProvider={aiProvider}
        onAiProviderChange={setAiProvider}
        isAiEnabled={isAiEnabled}
        isSaving={isSaving}
        user={user}
        onSignOut={handleSignOut}
        onNavigateToProfile={() => setCurrentView('profile')}
      />
      <main className="flex-1 p-4 md:p-8 overflow-y-auto md:h-screen">
        {isLoading ? (
          <ResumeSkeleton message={loadingMessage} />
        ) : (
          <>
            {error && (
              <div className="bg-red-100 border border-accent text-accent px-4 py-3 rounded-md relative mb-4 dark:bg-red-900/50 dark:text-red-200 dark:border-red-700" role="alert">
                <strong className="font-bold">Error: </strong>
                <span className="block sm:inline">{error}</span>
              </div>
            )}
            {currentView === 'editor' && (
                <div className="max-w-4xl mx-auto">
                    <ResumePreview
                        ref={resumePreviewRef}
                        data={resumeData}
                        setData={setResumeData}
                        template={template}
                        aiProvider={aiProvider}
                        onEnhance={handleEnhanceSection}
                        isAiEnabled={isAiEnabled}
                        onPhotoUpload={handlePhotoSelectForCrop}
                        onEnhancePhoto={handleEnhancePhoto}
                        isEnhancingPhoto={isEnhancingPhoto}
                        isUploadingPhoto={isUploadingPhoto}
                    />
                </div>
            )}
             {currentView === 'profile' && user && (
                <ProfilePage 
                    user={user}
                    resumeData={resumeData}
                    setResumeData={setResumeData}
                    onBackToEditor={() => setCurrentView('editor')}
                />
            )}
          </>
        )}
      </main>
      <HistorySidebar
        isOpen={isHistorySidebarOpen}
        onClose={() => setIsHistorySidebarOpen(false)}
        changeLog={changeLog}
        onUndo={undo}
        onRedo={redo}
        canUndo={canUndo}
        canRedo={canRedo}
      />
       {!isPublishedView && !isHistorySidebarOpen && (currentView === 'editor' || currentView === 'profile') && (
         <button
            onClick={() => setIsHistorySidebarOpen(true)}
            className="pdf-hide fixed top-1/2 right-0 -translate-y-1/2 bg-white dark:bg-gray-700 text-gray-600 dark:text-gray-200 p-2 rounded-l-lg shadow-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors z-30"
            title="Show Change History"
         >
            <HistoryIcon className="w-6 h-6" />
         </button>
       )}
      <PublishModal
        isOpen={isPublishModalOpen}
        onClose={() => setIsPublishModalOpen(false)}
        publishUrl={publishedUrl}
      />
    </div>
  );
}

export default ResumeEditor;
