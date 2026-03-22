import React, { useRef, useMemo, useState, useEffect } from 'react';
import { UploadIcon, DownloadIcon, BrandIcon, SparklesIcon, SunIcon, MoonIcon, GlobeIcon, LatexIcon, LogoutIcon, CheckBadgeIcon, WordIcon, FileTextIcon, JsonIcon, UserIcon, LinkedInSolidIcon } from '../common/icons';
import type { AppUser } from "@/types/user";
import type { LatexTemplate } from "@/types/latex";

interface SidebarProps {
  onFileUpload: (file: File) => void;
  onImportFromLinkedIn: () => void;
  onExportPdf: () => void;
  onExportLatex: () => void;
  onExportDocx: () => void;
  onExportTxt: () => void;
  onExportJson: () => void;
  onSuggestSkills: () => void;
  onCheckATSScore: () => void;
  onPublish: () => void;
  currentTemplate: string;
  onTemplateChange: (template: 'classic' | 'modern' | 'compact') => void;
  latexTemplate: LatexTemplate;
  onLatexTemplateChange: (template: LatexTemplate) => void;
  onToggleTheme: () => void;
  currentTheme: 'light' | 'dark';
  aiProvider: 'gemini' | 'huggingface';
  onAiProviderChange: (provider: 'gemini' | 'huggingface') => void;
  isAiEnabled: boolean;
  isSaving: boolean;
  user: AppUser | null;
  onSignOut: () => void;
  onNavigateToProfile: () => void;
}

const SidebarButton: React.FC<{
  onClick: () => void;
  disabled?: boolean;
  title: string;
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'accent' | 'tertiary';
  className?: string;
}> = ({ onClick, disabled, title, children, variant = 'primary', className = '' }) => {
  const baseClasses = 'w-full flex items-center justify-center gap-2 font-semibold py-2.5 px-4 rounded-lg transition-all duration-200 ease-in-out shadow-sm disabled:cursor-not-allowed disabled:opacity-60';
  
  const variantClasses = {
    primary: 'bg-primary text-white hover:bg-blue-600 focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800 disabled:bg-blue-300 dark:disabled:bg-blue-800',
    secondary: 'bg-secondary text-white hover:bg-green-600 focus:ring-4 focus:ring-green-300 dark:focus:ring-green-800 disabled:bg-green-300 dark:disabled:bg-green-800',
    accent: 'bg-purple-600 text-white hover:bg-purple-700 focus:ring-4 focus:ring-purple-300 dark:focus:ring-purple-800 disabled:bg-purple-300 dark:disabled:bg-purple-800',
    tertiary: 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 shadow-none disabled:bg-gray-100 dark:disabled:bg-gray-800',
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      title={title}
    >
      {children}
    </button>
  );
};

const ExportMenuItem: React.FC<{ onClick: () => void; disabled?: boolean; children: React.ReactNode; title: string; }> = ({ onClick, disabled, children, title }) => (
    <button
        onClick={onClick}
        disabled={disabled}
        title={title}
        className="w-full flex items-center gap-3 text-left px-3 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
    >
        {children}
    </button>
);

export const Sidebar: React.FC<SidebarProps> = ({ 
    onFileUpload, 
    onImportFromLinkedIn,
    onExportPdf,
    onExportLatex,
    onExportDocx,
    onExportTxt,
    onExportJson,
    onSuggestSkills,
    onCheckATSScore, 
    onPublish,
    currentTemplate, 
    onTemplateChange,
    latexTemplate,
    onLatexTemplateChange,
    onToggleTheme,
    currentTheme,
    aiProvider,
    onAiProviderChange,
    isAiEnabled,
    isSaving,
    user,
    onSignOut,
    onNavigateToProfile
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isExportMenuOpen, setIsExportMenuOpen] = useState(false);
  const exportMenuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
        if (exportMenuRef.current && !exportMenuRef.current.contains(event.target as Node)) {
            setIsExportMenuOpen(false);
        }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const templates = useMemo(() => [
    { id: 'classic', name: 'Classic' },
    { id: 'modern', name: 'Modern' },
    { id: 'compact', name: 'Compact' },
  ], []);

  const latexTemplates = useMemo(() => [
    { id: 'professional', name: 'Professional' },
    { id: 'academic', name: 'Academic' },
    { id: 'minimalist', name: 'Minimalist' },
  ], []);

  const acceptedFileTypes = aiProvider === 'huggingface' 
    ? ".txt,.jpg,.jpeg,.png" 
    : ".pdf,.docx,.txt,.jpg,.jpeg,.png";
  
  const uploadHintText = aiProvider === 'huggingface'
    ? "Hugging Face parser accepts .txt and image files (PNG, JPG)."
    : "Upload a file (PDF, DOCX, PNG, JPG) and our AI will parse it for you to edit.";

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileUpload(file);
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const Section: React.FC<{title: string, children: React.ReactNode}> = ({ title, children }) => (
    <div className="flex flex-col gap-3">
        <h2 className="text-sm font-semibold text-gray-500 dark:text-gray-400 tracking-wider uppercase">{title}</h2>
        <div className="flex flex-col gap-2">
            {children}
        </div>
    </div>
  );


  return (
    <aside className="w-full md:w-72 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col shadow-md md:h-screen">
      <div className="p-6 flex items-center justify-between flex-shrink-0">
        <div className="flex items-center gap-3">
            <BrandIcon />
            <h1 className="text-xl font-bold text-text-primary dark:text-gray-100">AI Resume Editor</h1>
        </div>
        <button 
            onClick={onToggleTheme} 
            className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors" 
            aria-label={`Switch to ${currentTheme === 'light' ? 'dark' : 'light'} mode`}
        >
            {currentTheme === 'light' ? <MoonIcon className="text-gray-600"/> : <SunIcon className="text-yellow-400"/>}
        </button>
      </div>

      <div className="flex-1 flex flex-col gap-8 overflow-y-auto p-6">
        {/* --- Actions --- */}
        <div className="flex flex-col gap-4">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
            accept={acceptedFileTypes}
          />
          <SidebarButton
            onClick={handleUploadClick}
            disabled={!isAiEnabled}
            title={!isAiEnabled ? `The ${aiProvider} provider is not configured.` : "Upload your resume file"}
            variant="primary"
          >
            <UploadIcon />
            <span>Upload Resume</span>
          </SidebarButton>
          <SidebarButton
            onClick={onImportFromLinkedIn}
            disabled={!isAiEnabled}
            title={!isAiEnabled ? `The ${aiProvider} provider is not configured.` : "Import data from a LinkedIn profile"}
            variant="primary"
            className="bg-[#0077B5] text-white hover:bg-[#005E90] focus:ring-4 focus:ring-sky-300 dark:focus:ring-sky-800 disabled:bg-sky-300 dark:disabled:bg-sky-800"
          >
            <LinkedInSolidIcon />
            <span>Import from LinkedIn</span>
          </SidebarButton>
          <SidebarButton
            onClick={onSuggestSkills}
            disabled={!isAiEnabled}
            title={!isAiEnabled ? `The ${aiProvider} provider is not configured.` : "Get AI skill suggestions"}
            variant="accent"
          >
            <SparklesIcon />
            <span>Suggest Skills</span>
          </SidebarButton>
          <SidebarButton
            onClick={onCheckATSScore}
            disabled={!isAiEnabled}
            title={!isAiEnabled ? `The ${aiProvider} provider is not configured.` : "Check your resume's ATS score"}
            variant="primary"
            className="bg-teal-600 text-white hover:bg-teal-700 focus:ring-4 focus:ring-teal-300 dark:focus:ring-teal-800 disabled:bg-teal-300 dark:disabled:bg-teal-800"
          >
            <CheckBadgeIcon />
            <span>Check ATS Score</span>
          </SidebarButton>

          <div className="relative" ref={exportMenuRef}>
              <SidebarButton
                  onClick={() => setIsExportMenuOpen(prev => !prev)}
                  title="Export resume in various formats"
                  variant="secondary"
              >
                  <DownloadIcon />
                  <span>Export Resume</span>
              </SidebarButton>
              {isExportMenuOpen && (
                  <div className="absolute bottom-full mb-2 w-full bg-white dark:bg-gray-700 rounded-lg shadow-lg border border-gray-200 dark:border-gray-600 z-10 p-2 space-y-1 animate-fade-in-up">
                      <ExportMenuItem onClick={onExportPdf} title="Export as PDF">
                          <DownloadIcon /><span>PDF Document</span>
                      </ExportMenuItem>
                      <ExportMenuItem onClick={onExportLatex} disabled={!isAiEnabled} title={!isAiEnabled ? `The ${aiProvider} provider is not configured.` : "Export as LaTeX (.tex)"}>
                          <LatexIcon /><span>LaTeX (.tex)</span>
                      </ExportMenuItem>
                      <ExportMenuItem onClick={onExportDocx} title="Export as Word (.docx)">
                          <WordIcon /><span>Word (.docx)</span>
                      </ExportMenuItem>
                      <ExportMenuItem onClick={onExportTxt} title="Export as Plain Text (.txt)">
                          <FileTextIcon /><span>Plain Text (.txt)</span>
                      </ExportMenuItem>
                      <ExportMenuItem onClick={onExportJson} title="Export as JSON Data">
                          <JsonIcon /><span>JSON Data</span>
                      </ExportMenuItem>
                  </div>
              )}
          </div>

          <SidebarButton
              onClick={onPublish}
              title="Publish and get a shareable link"
              variant="secondary"
              className="bg-indigo-600 text-white hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-300 dark:focus:ring-indigo-800 disabled:bg-indigo-300 dark:disabled:bg-indigo-800"
          >
              <GlobeIcon />
              <span>Publish & Share</span>
          </SidebarButton>
        </div>
        
        <hr className="border-gray-200 dark:border-gray-700" />
        
        {/* --- Templates --- */}
        <Section title="Preview Templates">
            {templates.map(template => (
              <button
                key={template.id}
                onClick={() => onTemplateChange(template.id as any)}
                className={`
                  w-full text-left font-semibold py-2 px-4 rounded-lg transition-colors text-sm
                  ${currentTemplate === template.id 
                    ? 'bg-primary text-white shadow-sm' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600'
                  }`}
              >
                {template.name}
              </button>
            ))}
        </Section>
        
        {/* --- LaTeX Templates --- */}
        <Section title="LaTeX Export Templates">
            {latexTemplates.map(template => (
              <button
                key={template.id}
                onClick={() => onLatexTemplateChange(template.id as any)}
                className={`
                  w-full text-left font-semibold py-2 px-4 rounded-lg transition-colors text-sm
                  ${latexTemplate === template.id 
                    ? 'bg-primary text-white shadow-sm' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600'
                  }`}
              >
                {template.name}
              </button>
            ))}
        </Section>

        <hr className="border-gray-200 dark:border-gray-700" />

        {/* --- AI Provider --- */}
        <Section title="AI Provider">
          <div className="grid grid-cols-2 gap-2">
              <button
                  onClick={() => onAiProviderChange('gemini')}
                  className={`w-full text-center font-semibold py-2 px-2 rounded-lg transition-colors text-sm ${aiProvider === 'gemini' ? 'bg-primary text-white shadow-sm' : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600'}`}
              >
                  Gemini
              </button>
              <button
                  onClick={() => onAiProviderChange('huggingface')}
                  className={`w-full text-center font-semibold py-2 px-2 rounded-lg transition-colors text-sm ${aiProvider === 'huggingface' ? 'bg-primary text-white shadow-sm' : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600'}`}
              >
                  Hugging Face
              </button>
          </div>
          {!isAiEnabled && (
              <p className="text-xs text-accent dark:text-red-400 p-2 bg-red-100 dark:bg-red-900/40 rounded-md">
                  The {aiProvider === 'gemini' ? 'Gemini API key' : 'Hugging Face provider'} is not configured. AI features are disabled.
              </p>
          )}
        </Section>
      </div>
      
      <div className="p-6 flex-shrink-0">
        {user && (
            <div className="p-3 bg-gray-100 dark:bg-gray-900/50 rounded-lg mb-4">
                <p className="text-xs text-gray-600 dark:text-gray-400">Signed in as:</p>
                <p className="text-sm font-semibold text-gray-800 dark:text-gray-200 truncate">{user.email}</p>
                 <div className="flex items-center gap-2 mt-3">
                    <button
                        onClick={onNavigateToProfile}
                        title="View your profile"
                        className="w-full flex items-center justify-center gap-2 text-sm font-semibold py-1.5 px-3 rounded-md transition-colors bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600"
                    >
                        <UserIcon />
                        <span>Profile</span>
                    </button>
                    <button
                        onClick={onSignOut}
                        className="w-full flex items-center justify-center gap-2 text-sm font-semibold py-1.5 px-3 rounded-md transition-colors bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600"
                    >
                        <LogoutIcon />
                        <span>Sign Out</span>
                    </button>
                </div>
            </div>
        )}
        <div className="text-xs text-gray-500 dark:text-gray-400">
            <div className="flex items-center gap-2 mb-1">
              <div className={`w-2 h-2 rounded-full transition-colors ${isSaving ? 'bg-yellow-500 animate-pulse' : 'bg-green-500'}`}></div>
              <span>{isSaving ? 'Saving...' : 'All changes saved'}</span>
            </div>
            <p>{uploadHintText}</p>
        </div>
      </div>
    </aside>
  );
};
