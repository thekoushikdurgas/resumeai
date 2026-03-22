import React, { forwardRef, useState, useRef } from 'react';
import { type Resume } from '../../types';
import { EditableField } from '../common/EditableField';
import { PhoneIcon, MailIcon, LocationIcon, LinkedInIcon, GithubIcon, WebIcon, SparklesIcon, PlusIcon, UploadIcon, GraduationCapIcon, BriefcaseIcon, CertificateIcon, TrashIcon, PencilIcon } from '../common/icons';
import { produce } from 'immer';
import { templateStyles } from './templateStyles';
import { PhotoViewModal } from '../modals/PhotoViewModal';

interface ResumePreviewProps {
  data: Resume;
  setData: (data: Resume) => void;
  template: 'classic' | 'modern' | 'compact';
  aiProvider: 'gemini' | 'huggingface';
  onEnhance: (sectionContent: string | string[], enhancementType: 'objective' | 'description' | 'hobbies' | 'education_description') => Promise<string>;
  isAiEnabled: boolean;
  onPhotoUpload: (file: File) => void;
  onEnhancePhoto: () => void;
  isEnhancingPhoto: boolean;
  isUploadingPhoto: boolean;
  isReadOnly?: boolean;
}

interface SkillBarProps {
  name: string;
  level: number;
  onUpdate: (field: string, value: any) => void;
  onDelete: () => void;
  isReadOnly?: boolean;
}

const ActionButton: React.FC<{
    onClick: () => void;
    title: string;
    children: React.ReactNode;
    className?: string;
    disabled?: boolean;
}> = ({ onClick, title, children, className, disabled }) => (
    <button
        onClick={onClick}
        disabled={disabled}
        className={`pdf-hide transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
        title={title}
    >
        {children}
    </button>
);


const EnhanceButton: React.FC<{
    onClick: () => void;
    isLoading: boolean;
    loadingText: string;
    disabled?: boolean;
}> = ({ onClick, isLoading, loadingText, disabled }) => (
    <ActionButton
        onClick={onClick}
        disabled={isLoading || disabled}
        className="flex items-center gap-1.5 text-xs text-purple-700 dark:text-purple-400 font-semibold py-1 px-2 rounded-md hover:bg-purple-100 dark:hover:bg-purple-900/50"
        title={disabled ? "The selected AI provider is not configured." : "Enhance with AI"}
    >
        {isLoading ? (
            <>
                <div className="w-4 h-4 border-2 border-purple-200 border-t-purple-600 dark:border-purple-700 dark:border-t-purple-400 rounded-full animate-spin"></div>
                <span>{loadingText}</span>
            </>
        ) : (
            <>
                <SparklesIcon className="w-4 h-4" />
                <span>Enhance</span>
            </>
        )}
    </ActionButton>
);

const AddItemButton: React.FC<{onClick: () => void}> = ({onClick}) => (
    <ActionButton
        onClick={onClick}
        className="flex items-center gap-1 text-xs text-secondary dark:text-green-400 font-semibold py-1 px-2 rounded-md hover:bg-green-100 dark:hover:bg-green-900/50"
        title="Add new item"
    >
        <PlusIcon className="w-3 h-3" />
        <span>Add Item</span>
    </ActionButton>
);

const SkillBar: React.FC<SkillBarProps> = ({ name, level, onUpdate, onDelete, isReadOnly }) => {
  return (
    <div className="flex items-center gap-2">
        <div className="flex-grow flex items-center gap-2">
            <EditableField as="span" className="text-sm font-medium w-40 truncate" value={name} onSave={(val) => onUpdate('name', val)} disabled={isReadOnly} onDelete={!isReadOnly ? onDelete : undefined} />
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                <div className="bg-purple-600 dark:bg-purple-500 h-3 rounded-full transition-all duration-300" style={{ width: `${level}%` }}></div>
            </div>
            <div className="flex items-baseline w-14 text-right">
                <EditableField as="span" className="text-sm font-semibold" value={level.toString()} onSave={(val) => onUpdate('level', Math.max(0, Math.min(100, parseInt(val, 10) || 0)))} disabled={isReadOnly} />
                <span className="text-xs">%</span>
            </div>
        </div>
    </div>
  );
}

export const ResumePreview = forwardRef<HTMLDivElement, ResumePreviewProps>(({ data, setData, template, aiProvider, onEnhance, isAiEnabled, onPhotoUpload, onEnhancePhoto, isEnhancingPhoto, isUploadingPhoto, isReadOnly = false }, ref) => {
  const [enhancingSection, setEnhancingSection] = useState<string | null>(null);
  const photoInputRef = useRef<HTMLInputElement>(null);
  const [isPhotoViewModalOpen, setIsPhotoViewModalOpen] = useState(false);
  
  const styles = templateStyles[template] || templateStyles.classic;

  const handleUpdate = <T,>(path: (string | number)[], value: T) => {
    setData(produce(data, draft => {
      let current: any = draft;
      for (let i = 0; i < path.length - 1; i++) {
        current = current[path[i]];
      }
      current[path[path.length - 1]] = value;
    }));
  };
  
 type DeletableSection = 'experience' | 'education' | 'backendSkills' | 'frontendSkills' | 'programmingSkills' | 'cloudSkills' | 'certificates' | 'hobbies';

 const handleDeleteItem = (sectionKey: DeletableSection, index: number) => {
    setData(produce(data, draft => {
        const section = draft[sectionKey] as any[];
        if (Array.isArray(section)) {
            section.splice(index, 1);
        }
    }));
 };


  const handleAddItem = (sectionKey: 'experience' | 'education' | 'backendSkills' | 'frontendSkills' | 'programmingSkills' | 'cloudSkills' | 'certificates' | 'hobbies') => {
    setData(produce(data, draft => {
        const timestamp = Date.now();
        switch (sectionKey) {
            case 'experience':
                draft.experience.push({
                  id: `exp-${timestamp}`,
                  company: 'Company Name',
                  role: 'Job Title',
                  employmentType: 'Full-time',
                  location: '',
                  locationType: 'On-site',
                  isCurrent: false,
                  startDate: 'Month Year',
                  endDate: 'Month Year',
                  description: ['Responsibility or achievement'],
                  skills: [],
                  media: [],
                });
                break;
            case 'education':
                draft.education.push({ id: `edu-${timestamp}`, institution: 'New Institution', degree: 'New Degree', duration: 'Year - Year', score: 'Grade / GPA', description: ['Relevant project or coursework.'] });
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
    }));
  };

  const handleEnhanceObjective = async () => {
    if (enhancingSection || !isAiEnabled) return;
    setEnhancingSection('objective');
    try {
      const enhancedObjective = await onEnhance(data.objective, 'objective');
      handleUpdate(['objective'], enhancedObjective.trim());
    } catch (e) {
      console.error("Failed to enhance objective", e);
    } finally {
      setEnhancingSection(null);
    }
  };

  const handleEnhanceEducation = async (index: number) => {
    if (enhancingSection || !isAiEnabled) return;
    const sectionId = `education-${index}`;
    setEnhancingSection(sectionId);
    try {
        const enhancedText = await onEnhance(data.education[index].description, 'education_description');
        const enhancedArray = enhancedText.split('\n').map(line => line.replace(/^- /, '').trim()).filter(Boolean);
        handleUpdate(['education', index, 'description'], enhancedArray);
    } catch (e) {
        console.error(`Failed to enhance education ${index}`, e);
    } finally {
        setEnhancingSection(null);
    }
  };
  
  const handleEnhanceExperience = async (index: number) => {
    if (enhancingSection || !isAiEnabled) return;
    const sectionId = `experience-${index}`;
    setEnhancingSection(sectionId);
    try {
        const enhancedText = await onEnhance(data.experience[index].description, 'description');
        const enhancedArray = enhancedText.split('\n').map(line => line.replace(/^- /, '').trim()).filter(Boolean);
        handleUpdate(['experience', index, 'description'], enhancedArray);
    } catch (e) {
        console.error(`Failed to enhance experience ${index}`, e);
    } finally {
        setEnhancingSection(null);
    }
  };
  
  const handleEnhanceHobbies = async () => {
    if (enhancingSection || !isAiEnabled) return;
    setEnhancingSection('hobbies');
    try {
        const hobbyNames = data.hobbies.map(h => h.name);
        const enhancedText = await onEnhance(hobbyNames, 'hobbies');
        const enhancedNames = enhancedText.split('\n').map(line => line.replace(/^- /, '').trim()).filter(Boolean);
        
        const newHobbies = enhancedNames.map((name, i) => ({
            id: data.hobbies[i]?.id || `hob-${Date.now()}-${i}`,
            name: name
        }));
        handleUpdate(['hobbies'], newHobbies);
    } catch (e) {
        console.error("Failed to enhance hobbies", e);
    } finally {
        setEnhancingSection(null);
    }
  };

  const handlePhotoContainerClick = () => {
    if (isReadOnly) return;
    if (data.personalDetails.photo) {
      setIsPhotoViewModalOpen(true);
    } else {
      photoInputRef.current?.click();
    }
  };
  
  const handleChangePhotoClickFromModal = () => {
    setIsPhotoViewModalOpen(false);
    photoInputRef.current?.click();
  };

  const handlePhotoFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (file) {
          onPhotoUpload(file);
      }
      event.target.value = '';
  };

  const Section: React.FC<{children: React.ReactNode, className?: string}> = ({ children, className }) => (
    <div className={`${styles.section} ${className}`}>
      {children}
    </div>
  );

  const ResumeLayout: React.FC<{left: React.ReactNode, right: React.ReactNode}> = ({ left, right }) => {
    if (template === 'modern') {
      return (
        <div className={styles.mainGrid}>
          {left}
          {right}
        </div>
      );
    }
    return (
      <div className={styles.mainGrid}>
        <aside className={styles.leftColumn}>
          {left}
        </aside>
        <main className={styles.rightColumn}>
          {right}
        </main>
      </div>
    );
  }

  const leftContent = (
    <>
      <Section>
        <div className={styles.contactSection}>
            <div className={styles.contactItem}>
              <PhoneIcon className={styles.contactIcon} />
              <EditableField as="p" value={data.personalDetails.phone} onSave={(val) => handleUpdate(['personalDetails', 'phone'], val)} disabled={isReadOnly} />
            </div>
            <div className={styles.contactItem}>
              <LocationIcon className={styles.contactIcon} />
              <EditableField as="p" value={data.personalDetails.location} onSave={(val) => handleUpdate(['personalDetails', 'location'], val)} disabled={isReadOnly} />
            </div>
            <div className={styles.contactItem}>
              <MailIcon className={styles.contactIcon} />
              <EditableField as="p" value={data.personalDetails.email} onSave={(val) => handleUpdate(['personalDetails', 'email'], val)} disabled={isReadOnly} />
            </div>
            <div className={styles.contactItem}>
              <WebIcon className={styles.contactIcon} />
              <EditableField as="p" value={data.personalDetails.website} onSave={(val) => handleUpdate(['personalDetails', 'website'], val)} disabled={isReadOnly} />
            </div>
            <div className={styles.contactItem}>
              <LinkedInIcon className={styles.contactIcon} />
              <EditableField as="p" value={data.personalDetails.linkedin} onSave={(val) => handleUpdate(['personalDetails', 'linkedin'], val)} disabled={isReadOnly} />
            </div>
            <div className={styles.contactItem}>
              <GithubIcon className={styles.contactIcon} />
              <EditableField as="p" value={data.personalDetails.github} onSave={(val) => handleUpdate(['personalDetails', 'github'], val)} disabled={isReadOnly} />
            </div>
        </div>
      </Section>
      
      <Section>
        <div className="flex justify-between items-center mb-2">
          <h2 className={styles.sectionTitle}>QUALIFICATIONS</h2>
          {!isReadOnly && <AddItemButton onClick={() => handleAddItem('education')} />}
        </div>
        <div className={styles.timelineContainer}>
          {data.education.map((edu, index) => (
            <div key={edu.id} className={`${styles.timelineItem} group`}>
                <div className={styles.timelineIconContainer}>
                    <GraduationCapIcon className={styles.timelineIcon} />
                </div>
                <div className={styles.timelineContent}>
                    <div className="flex justify-between items-start mb-1">
                      <div>
                        <EditableField as="h3" className={styles.educationInstitution} value={edu.institution} onSave={(val) => handleUpdate(['education', index, 'institution'], val)} disabled={isReadOnly} onDelete={!isReadOnly ? () => handleDeleteItem('education', index) : undefined} />
                        <EditableField as="p" className={styles.educationDegree} value={edu.degree} onSave={(val) => handleUpdate(['education', index, 'degree'], val)} disabled={isReadOnly} onDelete={!isReadOnly ? () => handleDeleteItem('education', index) : undefined}/>
                        <EditableField as="p" className={styles.educationDetails} value={edu.duration} onSave={(val) => handleUpdate(['education', index, 'duration'], val)} disabled={isReadOnly} onDelete={!isReadOnly ? () => handleDeleteItem('education', index) : undefined}/>
                        <EditableField as="p" className={styles.educationDetails} value={edu.score} onSave={(val) => handleUpdate(['education', index, 'score'], val)} disabled={isReadOnly} onDelete={!isReadOnly ? () => handleDeleteItem('education', index) : undefined}/>
                      </div>
                      {!isReadOnly && (
                        <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity pdf-hide">
                           <EnhanceButton
                              isLoading={enhancingSection === `education-${index}`}
                              onClick={() => handleEnhanceEducation(index)}
                              loadingText="Improving..."
                              disabled={!isAiEnabled}
                          />
                        </div>
                      )}
                    </div>
                    <ul className={styles.jobDescriptionList}>
                      {edu.description.map((desc, descIndex) => (
                          <li key={descIndex}>
                              <EditableField as="span" value={desc} onSave={(val) => handleUpdate(['education', index, 'description', descIndex], val)} disabled={isReadOnly} onDelete={!isReadOnly ? () => {
                                  const newDescription = data.education[index].description.filter((_, i) => i !== descIndex);
                                  handleUpdate(['education', index, 'description'], newDescription);
                              } : undefined} />
                          </li>
                      ))}
                    </ul>
                </div>
            </div>
          ))}
        </div>
      </Section>

      <Section>
        <div className={`${styles.hobbiesSectionTitleContainer} flex justify-between items-center`}>
          <h2 className={styles.sectionTitle}>HOBBIES</h2>
          {!isReadOnly && (
            <div className="flex items-center gap-2">
              <EnhanceButton 
                  isLoading={enhancingSection === 'hobbies'} 
                  onClick={handleEnhanceHobbies}
                  loadingText="Improving hobbies..."
                  disabled={!isAiEnabled}
              />
              <AddItemButton onClick={() => handleAddItem('hobbies')} />
            </div>
          )}
        </div>
        <ul className={styles.hobbiesList}>
          {data.hobbies.map((hobby, index) => (
            <li key={hobby.id} className={`${template === 'modern' ? 'bg-gray-100 dark:bg-gray-800 py-1 px-3 rounded-full' : ''}`}>
              <EditableField as="span" value={hobby.name} onSave={(val) => handleUpdate(['hobbies', index, 'name'], val)} disabled={isReadOnly} onDelete={!isReadOnly ? () => handleDeleteItem('hobbies', index) : undefined} />
            </li>
          ))}
        </ul>
      </Section>
    </>
  );

  const rightContent = (
    <>
      <Section>
        <div className={styles.objectiveSectionTitleContainer}>
          <h2 className={styles.sectionTitle}>OBJECTIVES</h2>
          {!isReadOnly && (
            <EnhanceButton 
              isLoading={enhancingSection === 'objective'} 
              onClick={handleEnhanceObjective}
              loadingText="Improving objective..."
              disabled={!isAiEnabled}
            />
          )}
        </div>
        <EditableField as="p" className="text-sm" value={data.objective} onSave={(val) => handleUpdate(['objective'], val)} disabled={isReadOnly} />
      </Section>

      <Section>
        <div className="flex justify-between items-center mb-2">
          <h2 className={styles.jobSectionTitle}>JOBS AND INTERNSHIPS</h2>
          {!isReadOnly && <AddItemButton onClick={() => handleAddItem('experience')} />}
        </div>
        <div className={styles.timelineContainer}>
          {data.experience.map((exp, index) => (
            <div key={exp.id} className={`${styles.timelineItem} group`}>
                <div className={styles.timelineIconContainer}>
                    <BriefcaseIcon className={styles.timelineIcon} />
                </div>
                <div className={styles.timelineContent}>
                    <div className={styles.jobHeader}>
                        <div className={styles.jobTitleContainer}>
                            <EditableField as="h3" className={styles.jobCompany} value={exp.company} onSave={(val) => handleUpdate(['experience', index, 'company'], val)} disabled={isReadOnly} onDelete={!isReadOnly ? () => handleDeleteItem('experience', index) : undefined} />
                            <div className={styles.jobRoleDuration}>
                            <EditableField as="span" value={exp.role} onSave={(val) => handleUpdate(['experience', index, 'role'], val)} disabled={isReadOnly} onDelete={!isReadOnly ? () => handleDeleteItem('experience', index) : undefined}/>
                            <span> (</span>
                            <EditableField
                              as="span"
                              value={`${exp.startDate} – ${exp.endDate}`}
                              onSave={(val) => {
                                setData(
                                  produce(data, (draft) => {
                                    const parts = val.split(/\s*[–-]\s*/).map((s) => s.trim());
                                    const row = draft.experience[index];
                                    row.startDate = parts[0] || row.startDate;
                                    row.endDate = parts[1] ?? parts[0] ?? row.endDate;
                                  })
                                );
                              }}
                              disabled={isReadOnly}
                              onDelete={!isReadOnly ? () => handleDeleteItem("experience", index) : undefined}
                            />
                            <span>)</span>
                            </div>
                        </div>
                         {!isReadOnly && (
                           <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity pdf-hide">
                              <EnhanceButton 
                                  isLoading={enhancingSection === `experience-${index}`} 
                                  onClick={() => handleEnhanceExperience(index)}
                                  loadingText="Improving..."
                                  disabled={!isAiEnabled}
                              />
                          </div>
                         )}
                    </div>
                    <ul className={styles.jobDescriptionList}>
                        {exp.description.map((desc, descIndex) => (
                            <li key={descIndex}>
                                <EditableField as="span" value={desc} onSave={(val) => handleUpdate(['experience', index, 'description', descIndex], val)} disabled={isReadOnly} onDelete={!isReadOnly ? () => {
                                    const newDescription = data.experience[index].description.filter((_, i) => i !== descIndex);
                                    handleUpdate(['experience', index, 'description'], newDescription);
                                } : undefined} />
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
          ))}
        </div>
      </Section>

      <Section>
        <h2 className={styles.sectionTitle}>SKILLS</h2>
        <div className={styles.skillsSection}>
            <div>
                <div className="flex justify-between items-center">
                    <h3 className={styles.skillCategoryTitle}>Backend End Development</h3>
                    {!isReadOnly && <AddItemButton onClick={() => handleAddItem('backendSkills')} />}
                </div>
                <div className={styles.skillGrid}>
                  {data.backendSkills.map((skill, index) => <SkillBar key={skill.id} name={skill.name} level={skill.level} onUpdate={(field, value) => handleUpdate(['backendSkills', index, field], value)} onDelete={() => handleDeleteItem('backendSkills', index)} isReadOnly={isReadOnly} />)}
                </div>
            </div>
             <div>
                <div className="flex justify-between items-center">
                    <h3 className={styles.skillCategoryTitle}>Front End Development</h3>
                    {!isReadOnly && <AddItemButton onClick={() => handleAddItem('frontendSkills')} />}
                </div>
                <div className={styles.skillGrid}>
                  {data.frontendSkills.map((skill, index) => <SkillBar key={skill.id} name={skill.name} level={skill.level} onUpdate={(field, value) => handleUpdate(['frontendSkills', index, field], value)} onDelete={() => handleDeleteItem('frontendSkills', index)} isReadOnly={isReadOnly} />)}
                </div>
            </div>
            <div>
                <div className="flex justify-between items-center">
                    <h3 className={styles.skillCategoryTitle}>Programming</h3>
                    {!isReadOnly && <AddItemButton onClick={() => handleAddItem('programmingSkills')} />}
                </div>
                <div className={styles.skillGrid}>
                    {data.programmingSkills.map((skill, index) => <SkillBar key={skill.id} name={skill.name} level={skill.level} onUpdate={(field, value) => handleUpdate(['programmingSkills', index, field], value)} onDelete={() => handleDeleteItem('programmingSkills', index)} isReadOnly={isReadOnly} />)}
                </div>
            </div>
             <div>
                <div className="flex justify-between items-center">
                    <h3 className={styles.skillCategoryTitle}>Cloud Computing</h3>
                    {!isReadOnly && <AddItemButton onClick={() => handleAddItem('cloudSkills')} />}
                </div>
                <div className={styles.skillGrid}>
                    {data.cloudSkills.map((skill, index) => <SkillBar key={skill.id} name={skill.name} level={skill.level} onUpdate={(field, value) => handleUpdate(['cloudSkills', index, field], value)} onDelete={() => handleDeleteItem('cloudSkills', index)} isReadOnly={isReadOnly} />)}
                </div>
            </div>
        </div>
      </Section>

      <Section>
        <div className="flex justify-between items-center mb-2">
          <h2 className={styles.sectionTitle}>CERTIFICATE</h2>
          {!isReadOnly && <AddItemButton onClick={() => handleAddItem('certificates')} />}
        </div>
        <div className={styles.timelineContainer}>
          {data.certificates.map((cert, index) => (
            <div key={cert.id} className={styles.timelineItem}>
              <div className={styles.timelineIconContainer}>
                  <CertificateIcon className={styles.timelineIcon} />
              </div>
              <div className={`${styles.timelineContent} flex justify-between items-center`}>
                  <EditableField as="p" className="font-semibold" value={cert.name} onSave={(val) => handleUpdate(['certificates', index, 'name'], val)} disabled={isReadOnly} onDelete={!isReadOnly ? () => handleDeleteItem('certificates', index) : undefined} />
              </div>
            </div>
          ))}
        </div>
      </Section>

      <footer className={styles.footer}>
        <p>I hereby declare that the information given above are true and authenticate to the best of my knowledge. I assure you that given a chance. I would prove my worth by honest discharge of my duty.</p>
      </footer>
    </>
  );


  return (
    <div ref={ref} className={styles.container}>
      {!isReadOnly && (
        <>
            <PhotoViewModal
                isOpen={isPhotoViewModalOpen}
                onClose={() => setIsPhotoViewModalOpen(false)}
                photoSrc={data.personalDetails.photo}
                onUploadClick={handleChangePhotoClickFromModal}
                onEnhance={onEnhancePhoto}
                isEnhancing={isEnhancingPhoto}
                isAiEnabledForEnhance={isAiEnabled && aiProvider === 'gemini'}
            />
            <input
                type="file"
                ref={photoInputRef}
                onChange={handlePhotoFileChange}
                className="hidden"
                accept="image/png, image/jpeg, image/webp"
            />
        </>
      )}
      <header className={styles.header}>
        <div className={styles.headerInfo}>
          <EditableField as="h1" className={styles.name} value={data.personalDetails.name} onSave={(val) => handleUpdate(['personalDetails', 'name'], val)} disabled={isReadOnly} />
          <EditableField as="p" className={styles.title} value={data.personalDetails.title} onSave={(val) => handleUpdate(['personalDetails', 'title'], val)} disabled={isReadOnly} />
        </div>
        <div 
            className={`${styles.headerPhotoContainer} relative group ${isReadOnly ? 'cursor-default' : 'cursor-pointer'}`}
            onClick={handlePhotoContainerClick}
            role={isReadOnly ? undefined : "button"}
            tabIndex={isReadOnly ? -1 : 0}
            onKeyDown={(e) => { if (!isReadOnly && (e.key === 'Enter' || e.key === ' ')) handlePhotoContainerClick(); }}
            title={isReadOnly ? "Profile Photo" : (data.personalDetails.photo ? "View or change photo" : "Upload photo")}
        >
          {data.personalDetails.photo ? (
             <>
                <img src={data.personalDetails.photo} alt="Profile" className={styles.headerPhoto} />
                {!isReadOnly && (
                    <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 flex items-center justify-center transition-opacity duration-300 cursor-pointer pdf-hide rounded-full">
                        <div className="text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-center">
                            <PencilIcon className="w-6 h-6 mx-auto"/>
                            <span className="font-semibold text-sm block">Edit</span>
                        </div>
                    </div>
                )}
             </>
          ) : (
            <div className={`w-full h-full rounded-full border-2 border-dashed border-gray-400 dark:border-gray-500 flex flex-col items-center justify-center text-gray-500 dark:text-gray-400 ${!isReadOnly && 'hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors'}`}>
                {isReadOnly ? (
                    <span className="text-xs font-semibold">No Photo</span>
                ) : (
                    <>
                        <UploadIcon />
                        <span className="text-xs font-semibold mt-1">Add Photo</span>
                    </>
                )}
            </div>
          )}
          {(isUploadingPhoto || isEnhancingPhoto) && !isReadOnly && (
            <div className="absolute inset-0 bg-black bg-opacity-60 flex flex-col items-center justify-center transition-opacity duration-300 cursor-wait pdf-hide rounded-full text-white text-center">
                <div className="w-8 h-8 border-2 border-gray-200 border-t-white rounded-full animate-spin"></div>
                <span className="text-xs font-semibold mt-2">{isEnhancingPhoto ? 'Enhancing...' : 'Uploading...'}</span>
            </div>
          )}
        </div>
      </header>
      
      <ResumeLayout left={leftContent} right={rightContent} />
    </div>
  );
});

ResumePreview.displayName = 'ResumePreview';
