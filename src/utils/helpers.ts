import { type Resume } from '../types';

const MAX_AI_INPUT_CHARS = 750000; // ~750KB JSON string, a safe proxy for token limits.

export const isResumeTooLargeForAI = (resume: Resume): boolean => {
    try {
        const jsonString = JSON.stringify(resume);
        return jsonString.length > MAX_AI_INPUT_CHARS;
    } catch (e) {
        console.error("Failed to stringify resume data:", e);
        return true;
    }
};

export const imageUrlToBase64 = async (url: string): Promise<string> => {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Failed to fetch image: ${response.statusText}`);
    }
    const blob = await response.blob();
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result as string);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
};

export const validateLatexCode = (code: string): boolean => {
    const trimmedCode = code.trim();

    if (!trimmedCode.startsWith('\\documentclass') || !trimmedCode.endsWith('\\end{document}')) {
        console.error("Validation failed: Missing documentclass or end document.");
        return false;
    }

    if (trimmedCode.includes('<<') || trimmedCode.includes('>>')) {
        console.error("Validation failed: Un-replaced placeholders found.");
        return false;
    }

    const beginCount = (trimmedCode.match(/\\begin{/g) || []).length;
    const endCount = (trimmedCode.match(/\\end{/g) || []).length;
    if (beginCount !== endCount) {
        console.error(`Validation failed: Mismatched begin/end blocks. Begins: ${beginCount}, Ends: ${endCount}`);
        return false;
    }
    
    if (trimmedCode.length < 150) { 
         console.error("Validation failed: Generated code is too short to be a valid document.");
         return false;
    }

    return true;
};
