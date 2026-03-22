import type { HistoryEntry } from '../hooks/useHistoryState';
import type { Resume } from '../types';

interface Change {
  description: string;
  timestamp: number;
}

const getArrayChanges = (prev: any[], curr: any[], itemName: string): string[] => {
    if (curr.length > prev.length) return [`Added an item to ${itemName}`];
    if (curr.length < prev.length) return [`Removed an item from ${itemName}`];
    if (JSON.stringify(prev) !== JSON.stringify(curr)) return [`Modified ${itemName}`];
    return [];
};

export const generateChangeLog = (history: HistoryEntry<Resume>[], present: number): Change[] => {
    const changes: Change[] = [];
    for (let i = 1; i <= present; i++) {
        const prev = history[i-1].state;
        const curr = history[i].state;
        const timestamp = history[i].timestamp;
        const stepChanges: string[] = [];

        if (JSON.stringify(prev.personalDetails) !== JSON.stringify(curr.personalDetails)) {
            stepChanges.push("Updated personal details");
        }
        if (prev.objective !== curr.objective) {
            stepChanges.push("Updated objective");
        }

        const sections: { key: keyof Resume, name: string }[] = [
            { key: 'experience', name: 'Experience' },
            { key: 'education', name: 'Education' },
            { key: 'backendSkills', name: 'Backend Skills' },
            { key: 'frontendSkills', name: 'Frontend Skills' },
            { key: 'programmingSkills', name: 'Programming Skills' },
            { key: 'cloudSkills', name: 'Cloud Skills' },
            { key: 'certificates', name: 'Certificates' },
            { key: 'hobbies', name: 'Hobbies' },
        ];
        
        sections.forEach(section => {
            stepChanges.push(...getArrayChanges(prev[section.key] as any[], curr[section.key] as any[], section.name));
        });

        if (stepChanges.length > 0) {
            changes.push({ description: stepChanges.join(', '), timestamp });
        }
    }
    return changes;
};
