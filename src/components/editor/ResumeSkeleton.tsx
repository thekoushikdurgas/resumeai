import React from 'react';

const SkeletonBlock: React.FC<{ className?: string }> = ({ className }) => (
  <div className={`bg-gray-200 dark:bg-gray-700 rounded animate-pulse ${className}`} />
);

const SkeletonHeader = () => (
    <div className="flex flex-col-reverse sm:flex-row items-center sm:items-start justify-between mb-8 gap-4 sm:gap-0">
        <div className="mt-4 sm:mt-0">
            <SkeletonBlock className="h-10 w-64 mb-2" />
            <SkeletonBlock className="h-6 w-48" />
        </div>
        <SkeletonBlock className="w-24 h-24 sm:w-32 sm:h-32 rounded-full flex-shrink-0" />
    </div>
);

const SkeletonSection: React.FC = () => (
    <div className="bg-gray-50 dark:bg-gray-800/50 p-6 rounded-lg">
        <SkeletonBlock className="h-6 w-32 mb-4" />
        <SkeletonBlock className="h-4 w-full mb-2" />
        <SkeletonBlock className="h-4 w-full mb-2" />
        <SkeletonBlock className="h-4 w-5/6" />
    </div>
)

const SkeletonSidebar = () => (
    <div className="space-y-6">
        <SkeletonSection />
        <SkeletonSection />
    </div>
);

const SkeletonMainContent = () => (
    <div className="space-y-6">
        <SkeletonSection />
        <SkeletonSection />
        <SkeletonSection />
    </div>
);


interface ResumeSkeletonProps {
  message: string;
}

export const ResumeSkeleton: React.FC<ResumeSkeletonProps> = ({ message }) => {
  return (
    <div className="bg-white dark:bg-gray-900 p-4 sm:p-8 shadow-lg border border-border-color dark:border-gray-700 relative overflow-hidden">
        <div className="absolute inset-0 bg-white/70 dark:bg-gray-900/70 backdrop-blur-sm flex flex-col items-center justify-center z-10 text-center">
            <div className="w-16 h-16 border-4 border-t-4 border-gray-200 border-t-primary rounded-full animate-spin"></div>
            <p className="text-text-primary dark:text-white mt-4 text-xl font-semibold">{message}</p>
            <p className="text-gray-600 dark:text-gray-400 mt-1">Please wait a moment...</p>
        </div>
        
        {/* Skeleton Layout */}
        <div className="opacity-40">
            <SkeletonHeader />
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                <div className="col-span-1 lg:col-span-4">
                    <SkeletonSidebar />
                </div>
                <div className="col-span-1 lg:col-span-8">
                    <SkeletonMainContent />
                </div>
            </div>
        </div>
    </div>
  );
};
