/**
 * REST client for backend(dev)/resumeai (AI + binary routes).
 */

import { RESUME_AI_API_KEY, RESUME_AI_URL } from "@/lib/config";
import type { ATSScoreResult, Resume, SuggestedSkill } from "@/types/resume";

const headers = (): HeadersInit => {
  const h: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (RESUME_AI_API_KEY) {
    h["X-API-Key"] = RESUME_AI_API_KEY;
  }
  return h;
};

function formatHttpError(status: number, detail: string): string {
  if (status === 502 || status === 503 || status === 504) {
    return "Resume service is temporarily unavailable. Please try again later.";
  }
  return detail || `HTTP ${status}`;
}

async function parseJson<T>(res: Response): Promise<T> {
  const text = await res.text();
  if (!res.ok) {
    let detail = text;
    try {
      const j = JSON.parse(text) as { detail?: unknown; message?: string };
      const d = j.detail;
      if (typeof d === "string") detail = d;
      else if (Array.isArray(d) && d.length) detail = String(d[0]);
      else detail = j.message || text;
    } catch {
      /* ignore */
    }
    throw new Error(formatHttpError(res.status, detail));
  }
  return text ? (JSON.parse(text) as T) : ({} as T);
}

export async function parseResumeFile(file: File): Promise<Resume> {
  const fd = new FormData();
  fd.append("file", file);
  const res = await fetch(`${RESUME_AI_URL}/ai/parse`, {
    method: "POST",
    headers: RESUME_AI_API_KEY ? { "X-API-Key": RESUME_AI_API_KEY } : {},
    body: fd,
  });
  return parseJson<Resume>(res);
}

export async function enhanceSection(
  content: string | string[],
  enhancementType: "objective" | "description" | "hobbies" | "education_description"
): Promise<string> {
  const res = await fetch(`${RESUME_AI_URL}/ai/enhance`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ content, enhancement_type: enhancementType }),
  });
  const data = await parseJson<{ result: string }>(res);
  return data.result;
}

export async function suggestSkills(
  title: string,
  experienceText: string
): Promise<SuggestedSkill[]> {
  const res = await fetch(`${RESUME_AI_URL}/ai/skills`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ title, experience_text: experienceText }),
  });
  const data = await parseJson<{ skills: SuggestedSkill[] }>(res);
  return data.skills;
}

export async function checkATSScore(
  resume: Resume,
  jobDescription?: string | null
): Promise<ATSScoreResult> {
  const res = await fetch(`${RESUME_AI_URL}/ai/ats-score`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ resume, job_description: jobDescription ?? null }),
  });
  return parseJson<ATSScoreResult>(res);
}

export async function improveResumeForATS(
  resume: Resume,
  options?: { atsResult?: ATSScoreResult | null; jobDescription?: string | null }
): Promise<Resume> {
  const body: Record<string, unknown> = { resume };
  if (options?.jobDescription) body.job_description = options.jobDescription;
  if (options?.atsResult) body.ats_result = options.atsResult;
  const res = await fetch(`${RESUME_AI_URL}/ai/ats-improve`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify(body),
  });
  return parseJson<Resume>(res);
}

function mapLatexTemplate(
  t: "professional" | "academic" | "minimalist" | "minimal"
): "professional" | "academic" | "minimalist" | "minimal" {
  if (t === "minimal") return "minimal";
  return t;
}

export async function generateLatex(
  resume: Resume,
  template: "professional" | "academic" | "minimalist" | "minimal"
): Promise<string> {
  const res = await fetch(`${RESUME_AI_URL}/ai/latex`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ resume, template: mapLatexTemplate(template) }),
  });
  const data = await parseJson<{ latex: string }>(res);
  return data.latex;
}

export async function enhancePhotoFile(file: File): Promise<string> {
  const fd = new FormData();
  fd.append("file", file);
  const res = await fetch(`${RESUME_AI_URL}/ai/photo`, {
    method: "POST",
    headers: RESUME_AI_API_KEY ? { "X-API-Key": RESUME_AI_API_KEY } : {},
    body: fd,
  });
  const data = await parseJson<{ imageBase64?: string; image_base64?: string }>(res);
  return data.imageBase64 ?? data.image_base64 ?? "";
}

export async function importLinkedIn(url: string): Promise<Resume> {
  const res = await fetch(`${RESUME_AI_URL}/ai/linkedin`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ url }),
  });
  return parseJson<Resume>(res);
}
