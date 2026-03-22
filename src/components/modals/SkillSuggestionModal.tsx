import React, { useState, useEffect } from 'react';
import { type SuggestedSkill } from '../../types';
import { SparklesIcon } from '../common/icons';

interface SkillSuggestionModalProps {
  isOpen: boolean;
  onClose: () => void;
  isLoading: boolean;
  error: string | null;
  suggestedSkills: SuggestedSkill[];
  onAddSkills: (skills: SuggestedSkill[]) => void;
}

export const SkillSuggestionModal: React.FC<SkillSuggestionModalProps> = ({
  isOpen,
  onClose,
  isLoading,
  error,
  suggestedSkills,
  onAddSkills,
}) => {
  const [selectedSkills, setSelectedSkills] = useState<SuggestedSkill[]>([]);

  useEffect(() => {
    // Reset selected skills when the modal is opened with new suggestions
    if (isOpen) {
      setSelectedSkills([]);
    }
  }, [isOpen, suggestedSkills]);

  if (!isOpen) {
    return null;
  }

  const handleToggleSkill = (skill: SuggestedSkill) => {
    setSelectedSkills(prev =>
      prev.some(s => s.name === skill.name)
        ? prev.filter(s => s.name !== skill.name)
        : [...prev, skill]
    );
  };

  const handleAddSelectedSkills = () => {
    onAddSkills(selectedSkills);
    onClose();
  };
  
  const groupedSkills: Record<string, SuggestedSkill[]> = {};
  suggestedSkills.forEach(skill => {
    const category = skill.category || 'Other';
    if (!groupedSkills[category]) {
      groupedSkills[category] = [];
    }
    groupedSkills[category].push(skill);
  });


  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4" aria-modal="true" role="dialog">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col animate-fade-in-up">
        <header className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <SparklesIcon className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">AI Skill Suggestions</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors text-3xl font-light" aria-label="Close modal">&times;</button>
        </header>
        
        <main className="flex-1 p-6 overflow-y-auto">
          {isLoading && (
             <div className="flex flex-col items-center justify-center text-center text-gray-600 dark:text-gray-400 py-10">
                <div className="w-12 h-12 border-4 border-purple-200 border-t-purple-600 dark:border-purple-700 dark:border-t-purple-400 rounded-full animate-spin mb-4"></div>
                <p className="font-semibold">Generating skill suggestions...</p>
                <p className="text-sm">Gemini is finding relevant skills based on your profile.</p>
            </div>
          )}
          {error && (
            <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md dark:bg-red-900/50 dark:text-red-200 dark:border-red-600" role="alert">
                <p className="font-bold">An Error Occurred</p>
                <p>{error}</p>
            </div>
          )}
          {!isLoading && !error && suggestedSkills.length === 0 && (
            <div className="text-center text-gray-500 dark:text-gray-400 py-10">
                <p>No new skill suggestions found at this time.</p>
                <p className="text-sm">Try adding more details to your job experience.</p>
            </div>
          )}
          {!isLoading && !error && suggestedSkills.length > 0 && (
            <div className="space-y-4">
              {Object.entries(groupedSkills).map(([category, skills]) => (
                <div key={category}>
                  <h3 className="text-md font-semibold text-gray-700 dark:text-gray-300 mb-2 capitalize border-b dark:border-gray-700 pb-1">{category}</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                    {skills.map(skill => (
                      <label key={skill.name} className={`flex items-center gap-2 p-3 rounded-lg cursor-pointer transition-all border-2 ${selectedSkills.some(s => s.name === skill.name) ? 'bg-purple-100 border-purple-400 dark:bg-purple-900/50 dark:border-purple-600' : 'bg-gray-50 border-gray-200 hover:border-purple-300 dark:bg-gray-900/50 dark:border-gray-700 dark:hover:border-purple-700'}`}>
                        <input
                          type="checkbox"
                          checked={selectedSkills.some(s => s.name === skill.name)}
                          onChange={() => handleToggleSkill(skill)}
                          className="form-checkbox h-5 w-5 text-purple-600 rounded border-gray-300 focus:ring-purple-500 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-purple-600 dark:ring-offset-gray-800"
                        />
                        <span className="font-medium text-gray-800 dark:text-gray-200 text-sm">{skill.name}</span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </main>
        
        <footer className="p-6 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-200 dark:border-gray-700 rounded-b-2xl flex justify-end gap-3">
            <button onClick={onClose} className="px-4 py-2 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-600">Cancel</button>
            <button 
                onClick={handleAddSelectedSkills} 
                disabled={selectedSkills.length === 0}
                className="px-4 py-2 text-sm font-semibold text-white bg-primary rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed shadow-sm dark:disabled:bg-gray-600"
            >
                Add {selectedSkills.length > 0 ? `${selectedSkills.length} ` : ''}Skills
            </button>
        </footer>
      </div>
    </div>
  );
};
