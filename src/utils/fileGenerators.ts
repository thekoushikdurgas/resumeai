import type { Resume, Skill } from '../types';

declare global {
  interface Window {
    docx: any;
    FileSaver: any;
  }
}

export const generateTxtContent = (resume: Resume): string => {
    const { personalDetails, objective, experience, education, backendSkills, frontendSkills, programmingSkills, cloudSkills, certificates, hobbies } = resume;
    
    const divider = '\n' + '='.repeat(50) + '\n\n';
    
    let txt = `${personalDetails.name.toUpperCase()}\n`;
    txt += `${personalDetails.title}\n\n`;

    txt += `CONTACT\n`;
    txt += `--------------------\n`;
    txt += `Email: ${personalDetails.email}\n`;
    txt += `Phone: ${personalDetails.phone}\n`;
    txt += `Location: ${personalDetails.location}\n`;
    if (personalDetails.linkedin) txt += `LinkedIn: ${personalDetails.linkedin}\n`;
    if (personalDetails.github) txt += `GitHub: ${personalDetails.github}\n`;
    if (personalDetails.website) txt += `Website: ${personalDetails.website}\n\n`;

    txt += divider;

    txt += `OBJECTIVE\n\n${objective}\n\n`;

    txt += divider;

    txt += `EXPERIENCE\n\n`;
    experience.forEach(exp => {
        txt += `${exp.role.toUpperCase()} | ${exp.company}\n`;
        // FIX: The 'duration' property does not exist on type 'Experience'. Replaced with 'startDate' and 'endDate'.
        txt += `${exp.startDate} - ${exp.endDate}\n`;
        exp.description.forEach(desc => {
            txt += `  - ${desc}\n`;
        });
        txt += `\n`;
    });

    txt += divider;

    txt += `EDUCATION\n\n`;
    education.forEach(edu => {
        txt += `${edu.institution.toUpperCase()}\n`;
        txt += `${edu.degree} (${edu.duration})\n`;
        txt += `Score: ${edu.score}\n`;
        if(edu.description.length > 0) {
            edu.description.forEach(desc => {
                txt += `  - ${desc}\n`;
            });
        }
        txt += `\n`;
    });

    txt += divider;
    
    txt += `SKILLS\n\n`;
    if (backendSkills.length > 0) txt += `Backend: ${backendSkills.map(s => s.name).join(', ')}\n`;
    if (frontendSkills.length > 0) txt += `Frontend: ${frontendSkills.map(s => s.name).join(', ')}\n`;
    if (programmingSkills.length > 0) txt += `Programming: ${programmingSkills.map(s => s.name).join(', ')}\n`;
    if (cloudSkills.length > 0) txt += `Cloud: ${cloudSkills.map(s => s.name).join(', ')}\n\n`;
    
    if (certificates.length > 0) {
        txt += divider;
        txt += `CERTIFICATES\n\n`;
        certificates.forEach(cert => {
            txt += `- ${cert.name}\n`;
        });
        txt += `\n`;
    }

    if (hobbies.length > 0) {
        txt += divider;
        txt += `HOBBIES\n\n`;
        txt += hobbies.map(h => h.name).join(', ');
        txt += `\n`;
    }

    return txt;
};

export const generateDocxBlob = (resume: Resume): Promise<Blob> => {
    return new Promise((resolve, reject) => {
        const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, TabStopType, TabStopPosition, UnderlineType } = window.docx;
        if (!Document) {
            reject(new Error("docx library not loaded"));
            return;
        }

        const contactInfo = [
            resume.personalDetails.email,
            resume.personalDetails.phone,
            resume.personalDetails.location,
            resume.personalDetails.linkedin,
            resume.personalDetails.github,
            resume.personalDetails.website
        ].filter(Boolean).join(' | ');

        const children = [
            new Paragraph({
                children: [new TextRun({ text: resume.personalDetails.name, bold: true, size: 48 })],
                alignment: AlignmentType.CENTER,
            }),
            new Paragraph({
                children: [new TextRun({ text: resume.personalDetails.title, size: 28, color: "555555" })],
                alignment: AlignmentType.CENTER,
            }),
             new Paragraph({
                children: [new TextRun({ text: contactInfo, size: 20, color: "555555" })],
                alignment: AlignmentType.CENTER,
                spacing: { after: 200 },
            }),
        ];
        
        const addSection = (title: string, content: any[]) => {
            if (content.length > 0) {
                children.push(new Paragraph({
                    children: [new TextRun({ text: title, bold: true, size: 28, allCaps: true, color: "333333" })],
                    spacing: { before: 300, after: 100 },
                    border: { bottom: { color: "auto", space: 1, value: "single", size: 6 } },
                }));
                children.push(...content);
            }
        };

        addSection('Objective', [new Paragraph({ children: [new TextRun(resume.objective)] })]);
        
        addSection('Experience', resume.experience.flatMap(exp => [
            new Paragraph({
                children: [
                    new TextRun({ text: exp.company, bold: true, size: 24 }),
                    // FIX: The 'duration' property does not exist on type 'Experience'. Replaced with 'startDate' and 'endDate'.
                    new TextRun({ text: `\t${exp.startDate} - ${exp.endDate}`, bold: true, size: 24 }),
                ],
                tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
            }),
            new Paragraph({ children: [new TextRun({ text: exp.role, italics: true, size: 22 })] }),
            ...exp.description.map(desc => new Paragraph({ text: desc, bullet: { level: 0 } }))
        ]));

        addSection('Education', resume.education.flatMap(edu => [
            new Paragraph({
                children: [
                    new TextRun({ text: edu.institution, bold: true, size: 24 }),
                    new TextRun({ text: `\t${edu.duration}`, bold: true, size: 24 }),
                ],
                tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
            }),
            new Paragraph({ children: [
                new TextRun({ text: edu.degree, italics: true, size: 22 }),
                new TextRun({ text: ` | Score: ${edu.score}`, italics: true, size: 22 })
            ] }),
            ...edu.description.map(desc => new Paragraph({ text: desc, bullet: { level: 0 } }))
        ]));

        const skillContent: any[] = [];
        const createSkillPara = (title: string, skills: Skill[]) => {
            if(skills.length > 0) {
                skillContent.push(new Paragraph({
                    children: [
                        new TextRun({ text: `${title}: `, bold: true }),
                        new TextRun(skills.map(s => s.name).join(', ')),
                    ]
                }));
            }
        };
        createSkillPara('Backend', resume.backendSkills);
        createSkillPara('Frontend', resume.frontendSkills);
        createSkillPara('Programming', resume.programmingSkills);
        createSkillPara('Cloud', resume.cloudSkills);
        addSection('Skills', skillContent);
        
        addSection('Certificates', resume.certificates.map(cert => new Paragraph({ text: cert.name, bullet: { level: 0 } })));
        addSection('Hobbies', [new Paragraph(resume.hobbies.map(h => h.name).join(', '))]);

        const doc = new Document({
            sections: [{ children }]
        });

        Packer.toBlob(doc).then(resolve);
    });
};
