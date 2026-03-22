import React, { useState } from 'react';
import { LinkedInSolidIcon } from '../common/icons';

interface LinkedInImportModalProps {
  isOpen: boolean;
  onClose: () => void;
  isLoading: boolean;
  error: string | null;
  onImport: (url: string) => void;
}

export const LinkedInImportModal: React.FC<LinkedInImportModalProps> = ({
  isOpen,
  onClose,
  isLoading,
  error,
  onImport,
}) => {
  const [url, setUrl] = useState('');

  if (!isOpen) {
    return null;
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url.trim()) {
      onImport(url.trim());
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4" aria-modal="true" role="dialog">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-lg flex flex-col animate-fade-in-up">
        <header className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <LinkedInSolidIcon className="w-6 h-6 text-[#0077B5]" />
            <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Import from LinkedIn</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors text-3xl font-light" aria-label="Close modal">&times;</button>
        </header>
        
        <form onSubmit={handleSubmit}>
            <main className="flex-1 p-6 overflow-y-auto">
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                Enter your public LinkedIn profile URL. Our AI will analyze it and automatically populate your resume.
              </p>
              
               {error && (
                <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md dark:bg-red-900/50 dark:text-red-200 dark:border-red-600 mb-4" role="alert">
                    <p className="font-bold">Import Error</p>
                    <p>{error}</p>
                </div>
              )}

              <div>
                <label htmlFor="linkedin-url" className="text-sm font-medium text-gray-700 dark:text-gray-300">LinkedIn Profile URL</label>
                 <input
                    id="linkedin-url"
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://www.linkedin.com/in/your-profile"
                    required
                    className="w-full px-4 py-2 mt-1 text-gray-800 dark:text-gray-200 bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>
            </main>
            
            <footer className="p-6 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-200 dark:border-gray-700 rounded-b-2xl flex justify-end gap-3">
                <button type="button" onClick={onClose} className="px-4 py-2 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-600">Cancel</button>
                <button 
                    type="submit"
                    disabled={isLoading || !url.trim()}
                    className="w-40 flex items-center justify-center gap-2 px-4 py-2 text-sm font-semibold text-white bg-primary rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed shadow-sm dark:disabled:bg-gray-600"
                >
                    {isLoading ? (
                         <>
                            <div className="w-5 h-5 border-2 border-blue-200 border-t-white rounded-full animate-spin"></div>
                            <span>Importing...</span>
                        </>
                    ) : (
                        "Import Profile"
                    )}
                </button>
            </footer>
        </form>
      </div>
    </div>
  );
};
