import React from 'react';
import { SparklesIcon, UploadIcon } from '../common/icons';

interface PhotoViewModalProps {
  isOpen: boolean;
  onClose: () => void;
  photoSrc: string | null;
  onUploadClick: () => void;
  onEnhance: () => void;
  isEnhancing: boolean;
  isAiEnabledForEnhance: boolean;
}

export const PhotoViewModal: React.FC<PhotoViewModalProps> = ({
  isOpen,
  onClose,
  photoSrc,
  onUploadClick,
  onEnhance,
  isEnhancing,
  isAiEnabledForEnhance,
}) => {
  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4" aria-modal="true" role="dialog">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-md max-h-[90vh] flex flex-col animate-fade-in-up">
        <header className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Profile Photo</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors text-3xl font-light" aria-label="Close modal">&times;</button>
        </header>
        
        <main className="flex-1 p-6 overflow-y-auto flex flex-col justify-center items-center">
            <div className="w-64 h-64 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-700 border-4 border-gray-300 dark:border-gray-600 flex items-center justify-center">
                <img 
                    src={photoSrc || "https://picsum.photos/256/256"} 
                    alt="Profile" 
                    className="object-cover w-full h-full"
                />
            </div>
        </main>
        
        <footer className="p-6 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-200 dark:border-gray-700 rounded-b-2xl flex justify-between items-center gap-3">
             <div className="flex items-center gap-3">
                <button 
                    onClick={onEnhance}
                    disabled={isEnhancing || !isAiEnabledForEnhance || !photoSrc}
                    className="flex items-center justify-center gap-2 bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors shadow-sm disabled:bg-purple-300 dark:disabled:bg-purple-800 disabled:cursor-not-allowed"
                    title={!isAiEnabledForEnhance ? "Photo enhancement is only available with the Gemini provider." : !photoSrc ? "No photo to enhance." : "Enhance photo with AI"}
                >
                    {isEnhancing ? (
                        <>
                            <div className="w-5 h-5 border-2 border-purple-200 border-t-white rounded-full animate-spin"></div>
                            <span>Enhancing...</span>
                        </>
                    ) : (
                        <>
                            <SparklesIcon />
                            <span>Enhance Photo</span>
                        </>
                    )}
                </button>
                <button 
                    onClick={onUploadClick}
                    className="flex items-center justify-center gap-2 bg-primary text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors shadow-sm"
                >
                    <UploadIcon />
                    <span>Change Photo</span>
                </button>
            </div>
            <button onClick={onClose} className="px-4 py-2 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-600">
                Close
            </button>
        </footer>
      </div>
    </div>
  );
};
