import React from 'react';
import { type ATSScoreResult } from '../../types';
import { CheckBadgeIcon, SparklesIcon } from '../common/icons';

interface ATSScoreModalProps {
  isOpen: boolean;
  onClose: () => void;
  isLoading: boolean;
  error: string | null;
  result: ATSScoreResult | null;
  onAiUpdate: () => void;
  isUpdating: boolean;
}

const ScoreCircle: React.FC<{ score: number }> = ({ score }) => {
    const circumference = 2 * Math.PI * 54; // 2 * pi * radius
    const offset = circumference - (score / 100) * circumference;

    let strokeColor = 'stroke-accent';
    if (score >= 80) {
        strokeColor = 'stroke-secondary';
    } else if (score >= 60) {
        strokeColor = 'stroke-yellow-500';
    }

    return (
        <div className="relative w-40 h-40">
            <svg className="w-full h-full" viewBox="0 0 120 120">
                <circle
                    className="text-gray-200 dark:text-gray-700"
                    strokeWidth="12"
                    stroke="currentColor"
                    fill="transparent"
                    r="54"
                    cx="60"
                    cy="60"
                />
                <circle
                    className={`transition-all duration-1000 ease-out ${strokeColor}`}
                    strokeWidth="12"
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                    strokeLinecap="round"
                    fill="transparent"
                    r="54"
                    cx="60"
                    cy="60"
                    transform="rotate(-90 60 60)"
                />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-4xl font-bold text-gray-800 dark:text-gray-100">{score}</span>
                <span className="text-sm font-semibold text-gray-500 dark:text-gray-400">/ 100</span>
            </div>
        </div>
    );
};


export const ATSScoreModal: React.FC<ATSScoreModalProps> = ({
  isOpen,
  onClose,
  isLoading,
  error,
  result,
  onAiUpdate,
  isUpdating,
}) => {
  if (!isOpen) {
    return null;
  }

  const renderContent = () => {
    if (isLoading) {
        return (
            <div className="flex flex-col items-center justify-center text-center text-gray-600 dark:text-gray-400 py-10">
                <div className="w-12 h-12 border-4 border-blue-200 border-t-primary dark:border-blue-700 dark:border-t-blue-400 rounded-full animate-spin mb-4"></div>
                <p className="font-semibold">Analyzing for ATS Compatibility...</p>
                <p className="text-sm">Our AI is checking your resume against key criteria.</p>
            </div>
        );
    }
    if (error) {
        return (
            <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md dark:bg-red-900/50 dark:text-red-200 dark:border-red-600" role="alert">
                <p className="font-bold">Analysis Failed</p>
                <p>{error}</p>
            </div>
        );
    }
    if (result) {
        return (
            <div className="space-y-6">
                <div className="flex flex-col sm:flex-row items-center gap-6 text-center sm:text-left">
                    <ScoreCircle score={result.score} />
                    <div>
                        <h3 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Your ATS Score is {result.score}</h3>
                        <p className="text-gray-600 dark:text-gray-300 mt-1">{result.summary}</p>
                        <p className="text-xs text-gray-500 mt-2">A score of 80+ is recommended for optimal compatibility.</p>
                    </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-green-50 dark:bg-green-900/40 p-4 rounded-lg">
                        <h4 className="font-semibold text-green-800 dark:text-green-300 mb-2">Strengths</h4>
                        <ul className="list-disc list-inside space-y-1 text-sm text-green-700 dark:text-green-200">
                            {result.strengths.map((item, i) => <li key={i}>{item}</li>)}
                        </ul>
                    </div>
                    <div className="bg-yellow-50 dark:bg-yellow-900/40 p-4 rounded-lg">
                        <h4 className="font-semibold text-yellow-800 dark:text-yellow-300 mb-2">Areas for Improvement</h4>
                        <ul className="list-disc list-inside space-y-1 text-sm text-yellow-700 dark:text-yellow-200">
                             {result.improvements.map((item, i) => <li key={i}>{item}</li>)}
                        </ul>
                    </div>
                </div>
            </div>
        );
    }
    return null;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4" aria-modal="true" role="dialog">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col animate-fade-in-up">
        <header className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <CheckBadgeIcon className="w-6 h-6 text-primary dark:text-blue-400" />
            <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">ATS Score Analysis</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors text-3xl font-light" aria-label="Close modal">&times;</button>
        </header>
        
        <main className="flex-1 p-6 overflow-y-auto">
          {renderContent()}
        </main>
        
        <footer className="p-6 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-200 dark:border-gray-700 rounded-b-2xl flex justify-between items-center">
            <button
              onClick={onAiUpdate}
              disabled={isLoading || isUpdating || !!error}
              className="flex items-center justify-center gap-2 bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors shadow-sm disabled:bg-purple-300 dark:disabled:bg-purple-800 disabled:cursor-not-allowed"
              title={error ? "Cannot update when an error is present" : "Let AI improve your resume and re-check the score"}
            >
              {isUpdating ? (
                <>
                  <div className="w-5 h-5 border-2 border-purple-200 border-t-white rounded-full animate-spin"></div>
                  <span>Updating...</span>
                </>
              ) : (
                <>
                  <SparklesIcon />
                  <span>AI Analysis & Update</span>
                </>
              )}
            </button>
            <button onClick={onClose} className="px-4 py-2 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-600">
                Close
            </button>
        </footer>
      </div>
    </div>
  );
};
