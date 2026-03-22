import React from 'react';
import { CloseIcon, HistoryIcon, UndoIcon, RedoIcon } from '../common/icons';

interface Change {
  description: string;
  timestamp: number;
}

interface HistorySidebarProps {
  isOpen: boolean;
  onClose: () => void;
  changeLog: Change[];
  onUndo: () => void;
  onRedo: () => void;
  canUndo: boolean;
  canRedo: boolean;
}

// Helper to format time
const timeAgo = (timestamp: number) => {
    const now = Date.now();
    const seconds = Math.floor((now - timestamp) / 1000);
    if (seconds < 10) return "Just now";
    
    let interval = seconds / 31536000;
    if (interval > 1) return Math.floor(interval) + " years ago";
    interval = seconds / 2592000;
    if (interval > 1) return Math.floor(interval) + " months ago";
    interval = seconds / 86400;
    if (interval > 1) return Math.floor(interval) + " days ago";
    interval = seconds / 3600;
    if (interval > 1) return Math.floor(interval) + " hours ago";
    interval = seconds / 60;
    if (interval > 1) return Math.floor(interval) + " minutes ago";
    return Math.floor(seconds) + " seconds ago";
};

export const HistorySidebar: React.FC<HistorySidebarProps> = ({ isOpen, onClose, changeLog, onUndo, onRedo, canUndo, canRedo }) => {
  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-30 md:hidden" 
          onClick={onClose}
          aria-hidden="true"
        ></div>
      )}
      <aside className={`pdf-hide fixed top-0 right-0 h-full w-80 bg-white dark:bg-gray-800 shadow-2xl z-40 transform transition-transform duration-300 ease-in-out ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <header className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
            <div className="flex items-center gap-2">
              <HistoryIcon className="w-6 h-6 text-primary dark:text-blue-400" />
              <h2 className="text-lg font-bold text-gray-800 dark:text-gray-100">Change History</h2>
            </div>
            <button onClick={onClose} className="p-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors" aria-label="Close history sidebar">
              <CloseIcon className="w-6 h-6 text-gray-500 dark:text-gray-400" />
            </button>
          </header>
          
          {/* Log List */}
          <div className="flex-1 overflow-y-auto p-4">
            {changeLog.length === 0 ? (
              <div className="text-center text-gray-500 dark:text-gray-400 mt-8 flex flex-col items-center">
                 <HistoryIcon className="w-12 h-12 mb-4 text-gray-300 dark:text-gray-600" />
                 <p className="font-semibold">No Changes Yet</p>
                 <p className="text-sm">Your edits to the resume will appear here.</p>
              </div>
            ) : (
              <ul className="border-l-2 border-gray-200 dark:border-gray-700 ml-1.5">
                {[...changeLog].reverse().map((change, index) => (
                  <li key={index} className="relative mb-6">
                    <div className="absolute -left-[9px] top-1 w-4 h-4 bg-primary rounded-full border-2 border-white dark:border-gray-800"></div>
                    <div className="ml-6">
                      <p className="text-sm font-medium text-gray-800 dark:text-gray-200 capitalize">{change.description}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{timeAgo(change.timestamp)}</p>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
          
          {/* Footer with Undo/Redo */}
          <footer className="p-4 border-t border-gray-200 dark:border-gray-700 flex-shrink-0">
            <div className="flex items-center gap-2">
                <button
                    onClick={onUndo}
                    disabled={!canUndo}
                    title="Undo last action"
                    className="w-full flex items-center justify-center gap-2 font-semibold py-2 px-4 rounded-lg transition-all duration-200 ease-in-out shadow-none disabled:cursor-not-allowed disabled:opacity-60 bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 dark:disabled:bg-gray-800"
                >
                    <UndoIcon />
                    <span>Undo</span>
                </button>
                <button
                    onClick={onRedo}
                    disabled={!canRedo}
                    title="Redo last action"
                    className="w-full flex items-center justify-center gap-2 font-semibold py-2 px-4 rounded-lg transition-all duration-200 ease-in-out shadow-none disabled:cursor-not-allowed disabled:opacity-60 bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 dark:disabled:bg-gray-800"
                >
                    <RedoIcon />
                    <span>Redo</span>
                </button>
            </div>
          </footer>
        </div>
      </aside>
    </>
  );
};
