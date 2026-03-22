interface TemplateStyleDefinition {
    container: string;
    header: string;
    headerInfo: string;
    headerPhotoContainer: string;
    headerPhoto: string;
    name: string;
    title: string;
    mainGrid: string;
    leftColumn: string;
    rightColumn: string;
    section: string;
    sectionTitle: string;
    contactSection: string;
    contactItem: string;
    contactIcon: string;
    timelineContainer: string;
    timelineItem: string;
    timelineIconContainer: string;
    timelineIcon: string;
    timelineContent: string;
    educationInstitution: string;
    educationDegree: string;
    educationDetails: string;
    hobbiesSectionTitleContainer: string;
    hobbiesList: string;
    objectiveSectionTitleContainer: string;
    jobSectionTitle: string;
    jobHeader: string;
    jobTitleContainer: string;
    jobCompany: string;
    jobRoleDuration: string;
    jobDescriptionList: string;
    skillsSection: string;
    skillCategoryTitle: string;
    skillGrid: string;
    footer: string;
}

interface TemplateStyles {
  [key: string]: TemplateStyleDefinition;
}

export const templateStyles: TemplateStyles = {
  classic: {
    container: "bg-white dark:bg-gray-900 p-4 sm:p-8 shadow-lg border border-gray-200 dark:border-gray-700 text-text-primary dark:text-gray-300",
    header: "flex flex-col-reverse sm:flex-row items-center text-center sm:text-left justify-between pb-8 mb-8 border-b-2 border-gray-100 dark:border-gray-700",
    headerInfo: "flex-1",
    headerPhotoContainer: "w-28 h-28 sm:w-36 sm:h-36 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden border-4 border-white dark:border-gray-800 flex-shrink-0 shadow-md",
    headerPhoto: "object-cover w-full h-full",
    name: "text-4xl sm:text-5xl font-bold tracking-tight text-gray-800 dark:text-gray-100",
    title: "text-lg sm:text-xl text-purple-700 dark:text-purple-400 font-medium mt-1",
    mainGrid: "grid grid-cols-1 lg:grid-cols-12 gap-x-12",
    leftColumn: "col-span-1 lg:col-span-4 space-y-8",
    rightColumn: "col-span-1 lg:col-span-8 space-y-8",
    section: "py-4",
    sectionTitle: "text-xl font-bold text-purple-800 dark:text-purple-400 mb-4 pb-2 border-b-2 border-purple-100 dark:border-purple-900",
    contactSection: "space-y-4 text-sm",
    contactItem: "flex items-center gap-3",
    contactIcon: "text-purple-700 dark:text-purple-400 w-5 h-5 flex-shrink-0",
    timelineContainer: "relative border-l-2 border-purple-200 dark:border-purple-700 ml-3 py-4",
    timelineItem: "mb-6 last:mb-0 pl-10 relative",
    timelineIconContainer: "absolute -left-4 top-0 flex items-center justify-center bg-purple-600 rounded-full h-7 w-7 ring-4 ring-white dark:ring-gray-900",
    timelineIcon: "text-white w-4 h-4",
    timelineContent: "",
    educationInstitution: "font-bold",
    educationDegree: "text-sm",
    educationDetails: "text-sm text-gray-600 dark:text-gray-400",
    hobbiesSectionTitleContainer: "flex justify-between items-center",
    hobbiesList: "list-disc list-inside text-sm pl-2 space-y-1",
    objectiveSectionTitleContainer: "flex justify-between items-center",
    jobSectionTitle: "text-xl font-bold text-purple-800 dark:text-purple-400 mb-4 pb-2 border-b-2 border-purple-100 dark:border-purple-900",
    jobHeader: "flex justify-between items-start",
    jobTitleContainer: "",
    jobCompany: "font-bold text-lg",
    jobRoleDuration: "text-sm font-medium",
    jobDescriptionList: "list-disc list-inside text-sm text-gray-600 dark:text-gray-400 mt-2 space-y-1 pl-2",
    skillsSection: "space-y-6",
    skillCategoryTitle: "font-semibold text-md text-gray-700 dark:text-gray-300 mb-3",
    skillGrid: "grid grid-cols-1 gap-y-3",
    footer: "text-xs text-gray-500 dark:text-gray-500 italic mt-8 text-center pt-4 border-t border-gray-100 dark:border-gray-700",
  },
  modern: {
    container: "bg-white dark:bg-gray-900 p-6 sm:p-10 text-gray-800 dark:text-gray-200 font-sans",
    header: "text-center mb-10 border-b pb-6 border-gray-200 dark:border-gray-700",
    headerInfo: "",
    headerPhotoContainer: "hidden",
    headerPhoto: "",
    name: "text-4xl sm:text-5xl font-extrabold tracking-tight text-gray-900 dark:text-gray-50",
    title: "text-lg sm:text-xl text-primary dark:text-blue-400 font-normal mt-2",
    mainGrid: "flex flex-col gap-8",
    leftColumn: "space-y-8",
    rightColumn: "space-y-8",
    section: "",
    sectionTitle: "text-sm font-bold uppercase tracking-wider text-primary dark:text-blue-400 mb-4 pb-2 border-b-2 border-primary dark:border-blue-400",
    contactSection: "space-y-3 text-sm flex flex-col items-center text-center",
    contactItem: "flex items-center gap-2",
    contactIcon: "text-primary dark:text-blue-400 w-5 h-5 flex-shrink-0",
    timelineContainer: "relative border-l-2 border-primary/20 dark:border-blue-400/20 ml-4 py-4",
    timelineItem: "mb-8 last:mb-0 pl-10 relative",
    timelineIconContainer: "absolute -left-[0.8rem] top-0 flex items-center justify-center bg-primary dark:bg-blue-400 rounded-full h-6 w-6 ring-4 ring-white dark:ring-gray-900",
    timelineIcon: "text-white w-4 h-4",
    timelineContent: "",
    educationInstitution: "font-semibold text-gray-900 dark:text-gray-100",
    educationDegree: "text-sm",
    educationDetails: "text-sm text-gray-500 dark:text-gray-400",
    hobbiesSectionTitleContainer: "flex justify-between items-center mb-2",
    hobbiesList: "flex flex-wrap gap-2 text-sm",
    objectiveSectionTitleContainer: "flex justify-between items-center mb-2",
    jobSectionTitle: "text-sm font-bold uppercase tracking-wider text-primary dark:text-blue-400 mb-4 pb-2 border-b-2 border-primary dark:border-blue-400",
    jobHeader: "flex justify-between items-start",
    jobTitleContainer: "",
    jobCompany: "font-semibold text-lg text-gray-900 dark:text-gray-100",
    jobRoleDuration: "text-sm font-medium text-gray-600 dark:text-gray-400",
    jobDescriptionList: "list-disc list-inside text-sm text-gray-700 dark:text-gray-300 mt-2 space-y-1",
    skillsSection: "space-y-6",
    skillCategoryTitle: "font-semibold text-md text-gray-800 dark:text-gray-200 mb-3",
    skillGrid: "grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-3",
    footer: "text-xs text-gray-400 dark:text-gray-600 mt-10 text-center border-t dark:border-gray-700 pt-4",
  },
  compact: {
    container: "bg-white dark:bg-gray-800 p-4 shadow-md border border-gray-200 dark:border-gray-700 text-gray-800 dark:text-gray-300 text-xs",
    header: "flex items-start justify-between mb-4 pb-4 border-b border-gray-200 dark:border-gray-700",
    headerInfo: "flex-grow",
    headerPhotoContainer: "w-20 h-20 rounded-md bg-gray-200 dark:bg-gray-700 overflow-hidden border-2 border-gray-300 dark:border-gray-600 flex-shrink-0",
    headerPhoto: "object-cover w-full h-full",
    name: "text-2xl font-bold text-gray-900 dark:text-gray-50",
    title: "text-sm text-secondary dark:text-green-400 font-semibold",
    mainGrid: "grid grid-cols-12 gap-x-4",
    leftColumn: "col-span-4 space-y-3",
    rightColumn: "col-span-8 space-y-3",
    section: "py-1",
    sectionTitle: "text-base font-bold text-secondary dark:text-green-400 mb-1 border-b-2 border-gray-200 dark:border-gray-600 pb-1",
    contactSection: "space-y-2",
    contactItem: "flex items-center gap-2",
    contactIcon: "text-secondary dark:text-green-400 w-4 h-4 flex-shrink-0",
    timelineContainer: "relative border-l border-gray-200 dark:border-gray-600 ml-2 py-2",
    timelineItem: "mb-4 last:mb-0 pl-6 relative",
    timelineIconContainer: "absolute -left-[0.45rem] top-0.5 flex items-center justify-center bg-secondary rounded-full h-3 w-3 ring-2 ring-white dark:ring-gray-800",
    timelineIcon: "hidden",
    timelineContent: "",
    educationInstitution: "font-bold text-sm",
    educationDegree: "text-xs",
    educationDetails: "text-xs text-gray-500 dark:text-gray-400",
    hobbiesSectionTitleContainer: "flex justify-between items-center mb-1",
    hobbiesList: "list-disc list-inside",
    objectiveSectionTitleContainer: "flex justify-between items-center mb-1",
    jobSectionTitle: "text-base font-bold text-secondary dark:text-green-400 mb-1 border-b-2 border-gray-200 dark:border-gray-600 pb-1",
    jobHeader: "flex justify-between items-start",
    jobTitleContainer: "",
    jobCompany: "font-bold text-sm",
    jobRoleDuration: "font-medium",
    jobDescriptionList: "list-disc list-inside text-gray-600 dark:text-gray-400 mt-1",
    skillsSection: "space-y-2",
    skillCategoryTitle: "font-semibold uppercase text-gray-600 dark:text-gray-400 mb-1 text-xs",
    skillGrid: "grid grid-cols-1 gap-x-4 gap-y-1",
    footer: "text-[10px] text-gray-400 dark:text-gray-500 italic mt-2 text-center",
  },
};
