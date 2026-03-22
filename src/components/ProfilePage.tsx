import React from 'react';
import type { AppUser } from "@/types/user";
import { produce } from 'immer';
import type { Resume } from '../types';
import { EditableField } from "@/components/common/EditableField";
import { MailIcon, UserIcon as ProfileIcon, BriefcaseIcon, ArrowLeftIcon, PlusIcon, PhoneIcon, LocationIcon, LinkedInIcon, GithubIcon, WebIcon, TrashIcon } from "@/components/common/icons";

interface ProfilePageProps {
  user: AppUser;
  resumeData: Resume;
  setResumeData: (data: Resume) => void;
  onBackToEditor: () => void;
}

const SectionCard: React.FC<{ title: string; onAddItem?: () => void; children: React.ReactNode }> = ({ title, onAddItem, children }) => (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 mb-6 last:mb-0">
        <header className="flex justify-between items-center p-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-bold text-gray-800 dark:text-gray-100">{title}</h2>
            {onAddItem && (
                <button
                    onClick={onAddItem}
                    className="flex items-center gap-1.5 text-sm font-semibold py-1.5 px-3 rounded-lg transition-colors bg-secondary text-white hover:bg-green-600"
                    title={`Add new ${title.slice(0, -1)}`}
                >
                    <PlusIcon className="w-4 h-4" />
                    <span>Add</span>
                </button>
            )}
        </header>
        <div className="p-4 space-y-4">
            {children}
        </div>
    </div>
);

const DetailItem: React.FC<{ label: string; value: string; onSave: (value: string) => void; icon: React.ReactNode; }> = ({ label, value, onSave, icon }) => (
    <div className="flex items-start gap-4 py-2">
        <div className="flex-shrink-0 text-primary dark:text-blue-400 mt-1">{icon}</div>
        <div className="flex-grow">
            <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">{label}</p>
            <EditableField as="p" className="text-gray-800 dark:text-gray-100" value={value} onSave={onSave} />
        </div>
    </div>
);

const FormField: React.FC<{ label: string; children: React.ReactNode; className?: string }> = ({ label, children, className }) => (
    <div className={className}>
        <label className="block text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">{label}</label>
        {children}
    </div>
);

const employmentTypes = ['Full-time', 'Part-time', 'Self-employed', 'Freelance', 'Contract', 'Internship', 'Apprenticeship', 'Seasonal'];
const locationTypes = ['On-site', 'Hybrid', 'Remote'];
const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const currentYear = new Date().getFullYear();
const years = Array.from({ length: currentYear - 1959 }, (_, i) => (currentYear - i).toString());

export const ProfilePage: React.FC<ProfilePageProps> = ({ user, resumeData, setResumeData, onBackToEditor }) => {
  
    const handleUpdate = (path: (string | number)[], value: any) => {
        setResumeData(produce(resumeData, draft => {
            let current: any = draft;
            for (let i = 0; i < path.length - 1; i++) {
                current = current[path[i]];
            }
            current[path[path.length - 1]] = value;
        }));
    };

    const handleAddItem = (sectionKey: 'experience' | 'education' | 'backendSkills' | 'frontendSkills' | 'programmingSkills' | 'cloudSkills' | 'certificates' | 'hobbies') => {
        const timestamp = Date.now();
        const newItem = produce(resumeData, draft => {
            switch (sectionKey) {
                case 'experience':
                    draft.experience.unshift({
                        id: `exp-${timestamp}`,
                        company: "",
                        role: "",
                        employmentType: "Full-time",
                        location: "",
                        locationType: "On-site",
                        isCurrent: true,
                        startDate: `${months[new Date().getMonth()]} ${new Date().getFullYear()}`,
                        endDate: "Present",
                        description: [""],
                        skills: [],
                        media: [],
                    });
                    break;
                case 'education':
                    draft.education.push({ id: `edu-${timestamp}`, institution: 'New Institution', degree: 'New Degree', duration: 'Year - Year', score: 'N/A', description: [] });
                    break;
                case 'backendSkills':
                case 'frontendSkills':
                case 'programmingSkills':
                case 'cloudSkills':
                    draft[sectionKey].push({ id: `skill-${timestamp}`, name: 'New Skill', level: 75 });
                    break;
                case 'certificates':
                    draft.certificates.push({ id: `cert-${timestamp}`, name: 'New Certificate' });
                    break;
                case 'hobbies':
                    draft.hobbies.push({ id: `hob-${timestamp}`, name: 'New Hobby' });
                    break;
            }
        });
        setResumeData(newItem);
    };

    const handleDeleteItem = (sectionKey: keyof Resume, index: number) => {
        setResumeData(produce(resumeData, draft => {
            (draft[sectionKey] as any[]).splice(index, 1);
        }));
    };

    const handleUpdateDescriptionPoint = (section: 'experience' , itemIndex: number, descIndex: number, value: string) => {
        const newDescription = [...resumeData[section][itemIndex].description];
        newDescription[descIndex] = value;
        handleUpdate([section, itemIndex, 'description'], newDescription);
    };

    const handleDeleteDescriptionPoint = (section: 'experience', itemIndex: number, descIndex: number) => {
        const newDescription = resumeData[section][itemIndex].description.filter((_, i) => i !== descIndex);
        handleUpdate([section, itemIndex, 'description'], newDescription);
    };
    
    const handleAddDescriptionPoint = (section: 'experience', itemIndex: number) => {
        const newDescription = [...resumeData[section][itemIndex].description, 'New point.'];
        handleUpdate([section, itemIndex, 'description'], newDescription);
    };

    return (
        <div className="max-w-4xl mx-auto animate-fade-in-up">
            <header className="flex items-center gap-4 p-4 md:p-6 mb-6">
                <button
                    onClick={onBackToEditor}
                    className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    title="Back to Editor"
                    aria-label="Back to resume editor"
                >
                    <ArrowLeftIcon />
                </button>
                <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Edit Resume Data</h1>
            </header>
            
            <main>
                <SectionCard title="Personal Details">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-2">
                        <div className="flex items-start gap-4 py-2">
                            <div className="flex-shrink-0 text-primary dark:text-blue-400 mt-1"><MailIcon /></div>
                            <div>
                                <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Email Address</p>
                                <p className="text-gray-800 dark:text-gray-100">{user.email || 'No email'}</p>
                            </div>
                        </div>
                        <DetailItem label="Full Name" value={resumeData.personalDetails.name} onSave={val => handleUpdate(['personalDetails', 'name'], val)} icon={<ProfileIcon />} />
                        <DetailItem label="Title" value={resumeData.personalDetails.title} onSave={val => handleUpdate(['personalDetails', 'title'], val)} icon={<BriefcaseIcon className="w-5 h-5"/>} />
                        <DetailItem label="Phone" value={resumeData.personalDetails.phone} onSave={val => handleUpdate(['personalDetails', 'phone'], val)} icon={<PhoneIcon />} />
                        <DetailItem label="Location" value={resumeData.personalDetails.location} onSave={val => handleUpdate(['personalDetails', 'location'], val)} icon={<LocationIcon />} />
                        <DetailItem label="LinkedIn" value={resumeData.personalDetails.linkedin} onSave={val => handleUpdate(['personalDetails', 'linkedin'], val)} icon={<LinkedInIcon />} />
                        <DetailItem label="GitHub" value={resumeData.personalDetails.github} onSave={val => handleUpdate(['personalDetails', 'github'], val)} icon={<GithubIcon />} />
                        <DetailItem label="Website" value={resumeData.personalDetails.website} onSave={val => handleUpdate(['personalDetails', 'website'], val)} icon={<WebIcon />} />
                    </div>
                </SectionCard>

                <SectionCard title="Objective">
                    <EditableField as="div" value={resumeData.objective} onSave={val => handleUpdate(['objective'], val)} isTextArea />
                </SectionCard>

                <SectionCard title="Experience" onAddItem={() => handleAddItem('experience')}>
                    {resumeData.experience.map((exp, index) => {
                        const [startMonth, startYear] = exp.startDate.split(' ');
                        const [endMonth, endYear] = exp.endDate.split(' ');

                        return (
                            <div key={exp.id} className="p-4 border rounded-lg dark:border-gray-700 relative group bg-gray-50 dark:bg-gray-800/50">
                                <button onClick={() => handleDeleteItem('experience', index)} title="Delete Experience" className="absolute top-3 right-3 p-1 text-gray-400 hover:text-red-500 dark:hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <TrashIcon className="w-5 h-5" />
                                </button>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                                    <FormField label="Title" className="md:col-span-2">
                                        <input type="text" value={exp.role} onChange={e => handleUpdate(['experience', index, 'role'], e.target.value)} className="w-full p-2 border rounded-md bg-white dark:bg-gray-700 dark:border-gray-600"/>
                                    </FormField>
                                    <FormField label="Employment type">
                                        <select value={exp.employmentType} onChange={e => handleUpdate(['experience', index, 'employmentType'], e.target.value)} className="w-full p-2 border rounded-md bg-white dark:bg-gray-700 dark:border-gray-600">
                                            {employmentTypes.map(type => <option key={type} value={type}>{type}</option>)}
                                        </select>
                                    </FormField>
                                    <FormField label="Company or organization">
                                        <input type="text" value={exp.company} onChange={e => handleUpdate(['experience', index, 'company'], e.target.value)} className="w-full p-2 border rounded-md bg-white dark:bg-gray-700 dark:border-gray-600"/>
                                    </FormField>

                                    <div className="md:col-span-2 flex items-center gap-2">
                                        <input type="checkbox" id={`isCurrent-${exp.id}`} checked={exp.isCurrent} onChange={e => handleUpdate(['experience', index, 'isCurrent'], e.target.checked)} className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary" />
                                        <label htmlFor={`isCurrent-${exp.id}`} className="text-sm font-medium text-gray-700 dark:text-gray-300">I am currently working in this role</label>
                                    </div>
                                    
                                    <FormField label="Start date">
                                        <div className="flex gap-2">
                                            <select value={startMonth} onChange={e => handleUpdate(['experience', index, 'startDate'], `${e.target.value} ${startYear}`)} className="w-full p-2 border rounded-md bg-white dark:bg-gray-700 dark:border-gray-600">
                                                {months.map(m => <option key={m} value={m}>{m}</option>)}
                                            </select>
                                            <select value={startYear} onChange={e => handleUpdate(['experience', index, 'startDate'], `${startMonth} ${e.target.value}`)} className="w-full p-2 border rounded-md bg-white dark:bg-gray-700 dark:border-gray-600">
                                                {years.map(y => <option key={y} value={y}>{y}</option>)}
                                            </select>
                                        </div>
                                    </FormField>

                                    <FormField label="End date">
                                        <div className="flex gap-2">
                                            <select disabled={exp.isCurrent} value={exp.isCurrent ? months[new Date().getMonth()] : endMonth} onChange={e => handleUpdate(['experience', index, 'endDate'], `${e.target.value} ${endYear}`)} className="w-full p-2 border rounded-md bg-white dark:bg-gray-700 dark:border-gray-600 disabled:bg-gray-100 dark:disabled:bg-gray-700/50">
                                                {months.map(m => <option key={m} value={m}>{m}</option>)}
                                            </select>
                                            <select disabled={exp.isCurrent} value={exp.isCurrent ? currentYear.toString() : endYear} onChange={e => handleUpdate(['experience', index, 'endDate'], `${endMonth} ${e.target.value}`)} className="w-full p-2 border rounded-md bg-white dark:bg-gray-700 dark:border-gray-600 disabled:bg-gray-100 dark:disabled:bg-gray-700/50">
                                                {years.map(y => <option key={y} value={y}>{y}</option>)}
                                            </select>
                                        </div>
                                    </FormField>

                                    <FormField label="Location">
                                        <input type="text" value={exp.location} onChange={e => handleUpdate(['experience', index, 'location'], e.target.value)} className="w-full p-2 border rounded-md bg-white dark:bg-gray-700 dark:border-gray-600"/>
                                    </FormField>

                                    <FormField label="Location type">
                                        <select value={exp.locationType} onChange={e => handleUpdate(['experience', index, 'locationType'], e.target.value)} className="w-full p-2 border rounded-md bg-white dark:bg-gray-700 dark:border-gray-600">
                                            {locationTypes.map(type => <option key={type} value={type}>{type}</option>)}
                                        </select>
                                    </FormField>
                                    
                                    <FormField label="Description" className="md:col-span-2">
                                        <div className="space-y-2">
                                            {exp.description.map((desc, descIndex) => (
                                                <EditableField key={descIndex} as="div" className="text-sm w-full" value={desc} onSave={val => handleUpdateDescriptionPoint('experience', index, descIndex, val)} onDelete={() => handleDeleteDescriptionPoint('experience', index, descIndex)} isTextArea />
                                            ))}
                                            <button onClick={() => handleAddDescriptionPoint('experience', index)} className="text-xs text-secondary mt-1 hover:underline">Add description point</button>
                                        </div>
                                    </FormField>
                                </div>
                            </div>
                        )
                    })}
                </SectionCard>
                
                <SectionCard title="Education" onAddItem={() => handleAddItem('education')}>
                    {resumeData.education.map((edu, index) => (
                        <div key={edu.id} className="p-4 border rounded-lg dark:border-gray-700">
                             <EditableField as="h3" className="font-bold" value={edu.institution} onSave={val => handleUpdate(['education', index, 'institution'], val)} onDelete={() => handleDeleteItem('education', index)} />
                             <EditableField as="p" className="text-sm" value={`${edu.degree} | ${edu.duration} | ${edu.score}`} onSave={val => {
                                 const parts = val.split('|').map(p => p.trim());
                                 handleUpdate(['education', index, 'degree'], parts[0] || '');
                                 handleUpdate(['education', index, 'duration'], parts[1] || '');
                                 handleUpdate(['education', index, 'score'], parts[2] || '');
                             }} />
                        </div>
                    ))}
                </SectionCard>

                <SectionCard title="Skills">
                    {(['frontendSkills', 'backendSkills', 'programmingSkills', 'cloudSkills'] as const).map(skillType => (
                        <div key={skillType} className="mb-4 last:mb-0">
                            <div className="flex justify-between items-center">
                                <h4 className="font-semibold capitalize text-gray-700 dark:text-gray-300">{skillType.replace('Skills', ' Skills')}</h4>
                                <button onClick={() => handleAddItem(skillType)} className="text-xs text-secondary">Add Skill</button>
                            </div>
                            <div className="space-y-2 mt-2">
                                {resumeData[skillType].map((skill, index) => (
                                    <div key={skill.id} className="flex items-center gap-4">
                                        <div className="flex-1">
                                            <EditableField as="p" className="text-sm" value={skill.name} onSave={val => handleUpdate([skillType, index, 'name'], val)} onDelete={() => handleDeleteItem(skillType, index)} />
                                        </div>
                                        <div className="w-20">
                                            <EditableField as="p" className="text-sm text-right" value={String(skill.level)} onSave={val => handleUpdate([skillType, index, 'level'], parseInt(val, 10) || 0)} />
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </SectionCard>

                <SectionCard title="Certificates" onAddItem={() => handleAddItem('certificates')}>
                    {resumeData.certificates.map((cert, index) => (
                        <div key={cert.id} className="py-1">
                            <EditableField as="div" className="text-sm" value={cert.name} onSave={val => handleUpdate(['certificates', index, 'name'], val)} onDelete={() => handleDeleteItem('certificates', index)} />
                        </div>
                    ))}
                </SectionCard>

                 <SectionCard title="Hobbies" onAddItem={() => handleAddItem('hobbies')}>
                    {resumeData.hobbies.map((hobby, index) => (
                        <div key={hobby.id} className="py-1">
                            <EditableField as="div" className="text-sm" value={hobby.name} onSave={val => handleUpdate(['hobbies', index, 'name'], val)} onDelete={() => handleDeleteItem('hobbies', index)} />
                        </div>
                    ))}
                </SectionCard>
            </main>
        </div>
    );
};