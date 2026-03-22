import React, { useState } from 'react';
import { GlobeIcon, CopyIcon, CheckIcon } from '../common/icons';

interface PublishModalProps {
  isOpen: boolean;
  onClose: () => void;
  publishUrl: string;
}

export const PublishModal: React.FC<PublishModalProps> = ({ isOpen, onClose, publishUrl }) => {
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(publishUrl).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }).catch(err => {
      console.error('Failed to copy text: ', err);
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4" aria-modal="true" role="dialog">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-lg flex flex-col animate-fade-in-up">
        <header className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <GlobeIcon className="w-6 h-6 text-primary dark:text-blue-400" />
            <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Your Resume is Published</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors text-3xl font-light" aria-label="Close modal">&times;</button>
        </header>
        <main className="flex-1 p-6 overflow-y-auto">
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            Anyone with this link can view a read-only version of your resume. Share it with recruiters and on your social profiles.
          </p>
          <div className="flex items-center gap-2">
            <input 
              type="text"
              readOnly
              value={publishUrl}
              className="w-full bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg p-2 text-sm text-gray-700 dark:text-gray-200"
            />
            <button
              onClick={handleCopy}
              className="flex items-center justify-center gap-2 bg-secondary text-white font-semibold py-2 px-4 rounded-lg hover:bg-green-600 transition-colors shadow-sm w-32"
            >
              {copied ? (
                <>
                  <CheckIcon />
                  <span>Copied!</span>
                </>
              ) : (
                <>
                  <CopyIcon />
                  <span>Copy Link</span>
                </>
              )}
            </button>
          </div>
        </main>
        <footer className="p-6 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-200 dark:border-gray-700 rounded-b-2xl flex justify-end">
          <button onClick={onClose} className="px-4 py-2 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-600">
            Done
          </button>
        </footer>
      </div>
    </div>
  );
};
