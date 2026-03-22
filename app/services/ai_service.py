"""AI operations: Gemini primary, Hugging Face fallback for text tasks."""

from __future__ import annotations

import base64
import io
import json
import re
from typing import Any, List, Literal, Optional

import httpx

from app.core.config import get_settings
from app.core.exceptions import AIServiceError
from app.models.resume import ATSScoreResult, Resume, SuggestedSkill
from app.utils.logger import get_logger

logger = get_logger(__name__)

EnhancementType = Literal["objective", "description", "hobbies", "education_description"]
LatexTemplate = Literal["professional", "academic", "minimalist", "minimal"]


def _require_gemini_key() -> None:
    if not get_settings().GEMINI_API_KEY:
        raise AIServiceError("GEMINI_API_KEY is not configured")


def _import_genai():
    import google.generativeai as genai

    s = get_settings()
    _require_gemini_key()
    genai.configure(api_key=s.GEMINI_API_KEY)
    return genai


def _resume_to_text(resume: Resume) -> str:
    parts = [
        f"Title: {resume.personalDetails.title}",
        f"Objective: {resume.objective}",
        "Experience: "
        + "; ".join(
            f"{e.role} at {e.company}: {', '.join(e.description)}" for e in resume.experience
        ),
        "Education: "
        + "; ".join(f"{edu.degree} from {edu.institution}" for edu in resume.education),
        "Skills: "
        + ", ".join(
            s.name
            for s in (
                resume.backendSkills
                + resume.frontendSkills
                + resume.programmingSkills
                + resume.cloudSkills
            )
        ),
    ]
    return "\n".join(parts)


def _extract_json(text: str) -> Any:
    text = text.strip()
    m = re.search(r"```json\s*([\s\S]*?)\s*```", text)
    if m:
        return json.loads(m.group(1))
    return json.loads(text)


async def parse_resume_file(file_bytes: bytes, mime_type: str) -> Resume:
    """Multimodal parse: PDF/image/DOCX as bytes."""
    s = get_settings()
    if s.AI_PROVIDER == "huggingface":
        return await _hf_parse_resume(file_bytes, mime_type)
    genai = _import_genai()
    model = genai.GenerativeModel(s.GEMINI_PARSE_MODEL)
    prompt = """Parse the provided resume document and extract structured JSON.
    Sections: personal details, objective, experience, education, skills (backend, frontend, programming, cloud),
    certificates, hobbies. Generate unique string IDs for list items. Skills level 0-100.
    Return ONLY valid JSON matching the Resume schema.
    """
    try:
        resp = model.generate_content(
            [
                prompt,
                {"mime_type": mime_type or "application/octet-stream", "data": file_bytes},
            ],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )
        raw = (resp.text or "").strip()
        data = json.loads(raw)
        pd = data.get("personalDetails", {})
        pd["photo"] = ""
        data["personalDetails"] = pd
        return Resume.model_validate(data)
    except Exception as e:
        logger.exception("parse_resume_file failed")
        raise AIServiceError(f"Failed to parse resume: {e}") from e


async def _hf_parse_resume(file_bytes: bytes, mime_type: str) -> Resume:
    raise AIServiceError("Hugging Face resume parsing is not implemented; use AI_PROVIDER=gemini")


async def enhance_section(
    content: str | List[str],
    enhancement_type: EnhancementType,
) -> str:
    if isinstance(content, list):
        body = "\n".join(f"- {c}" for c in content)
    else:
        body = content
    s = get_settings()
    if s.AI_PROVIDER == "huggingface":
        return await _hf_enhance_section(body, enhancement_type)
    genai = _import_genai()
    model = genai.GenerativeModel(s.GEMINI_PARSE_MODEL)
    prompts = {
        "objective": f"Rewrite this resume objective to be professional and concise. Return only the text.\n\n{body}",
        "description": f"Enhance these job bullet points: action verbs, metrics. Return bullets separated by newlines starting with '- '.\n\n{body}",
        "education_description": f"Enhance education bullet points. Return bullets with '- '.\n\n{body}",
        "hobbies": f"Rewrite hobbies for a resume. Return lines with '- '.\n\n{body}",
    }
    prompt = prompts[enhancement_type]
    try:
        resp = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(temperature=0.7),
        )
        return (resp.text or "").strip()
    except Exception as e:
        raise AIServiceError(str(e)) from e


async def _hf_enhance_section(body: str, enhancement_type: EnhancementType) -> str:
    s = get_settings()
    if not s.HF_API_KEY:
        raise AIServiceError("HF_API_KEY is not configured")
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    payload = {
        "inputs": f"<s>[INST] Improve this resume {enhancement_type} text:\n{body}\n[/INST]",
        "parameters": {"max_new_tokens": 512},
    }
    async with httpx.AsyncClient(timeout=s.AI_TIMEOUT_SECONDS) as client:
        r = await client.post(url, json=payload, headers={"Authorization": f"Bearer {s.HF_API_KEY}"})
        r.raise_for_status()
        data = r.json()
    if isinstance(data, list) and data and "generated_text" in data[0]:
        return data[0]["generated_text"].strip()
    raise AIServiceError("Unexpected Hugging Face response")


async def suggest_skills(title: str, experience_text: str) -> List[SuggestedSkill]:
    s = get_settings()
    if s.AI_PROVIDER == "huggingface":
        return await _hf_suggest_skills(title, experience_text)
    genai = _import_genai()
    model = genai.GenerativeModel(s.GEMINI_PARSE_MODEL)
    prompt = f"""Suggest up to 15 technical skills for job title "{title}" and descriptions:
{experience_text}
Return JSON array of objects with "name" and "category" (Frontend|Backend|Programming|Cloud only).
"""
    try:
        resp = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        arr = json.loads(resp.text or "[]")
        out: List[SuggestedSkill] = []
        for item in arr:
            out.append(SuggestedSkill.model_validate(item))
        return out[:15]
    except Exception as e:
        raise AIServiceError(str(e)) from e


async def _hf_suggest_skills(title: str, experience_text: str) -> List[SuggestedSkill]:
    s = get_settings()
    if not s.HF_API_KEY:
        raise AIServiceError("HF_API_KEY is not configured")
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    prompt = (
        f'List skills as JSON array of {{"name","category"}} for title "{title}" '
        f"and experience: {experience_text[:4000]}"
    )
    async with httpx.AsyncClient(timeout=s.AI_TIMEOUT_SECONDS) as client:
        r = await client.post(
            url,
            json={"inputs": prompt, "parameters": {"max_new_tokens": 512}},
            headers={"Authorization": f"Bearer {s.HF_API_KEY}"},
        )
        r.raise_for_status()
        data = r.json()
    text = data[0]["generated_text"] if isinstance(data, list) else str(data)
    try:
        m = re.search(r"\[[\s\S]*\]", text)
        if m:
            arr = json.loads(m.group(0))
            return [SuggestedSkill.model_validate(x) for x in arr[:15]]
    except Exception:
        pass
    return []


async def check_ats_score(resume: Resume, job_description: Optional[str] = None) -> ATSScoreResult:
    s = get_settings()
    genai = _import_genai()
    model = genai.GenerativeModel(s.GEMINI_PRO_MODEL)
    jd = job_description or "General role matching the candidate title."
    prompt = f"""ATS analysis for resume. Job context: {jd}
Resume text:
{_resume_to_text(resume)}
Return JSON with score (0-100), summary (one sentence), strengths (2-3 strings), improvements (2-4 actionable strings).
"""
    try:
        resp = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        return ATSScoreResult.model_validate(json.loads(resp.text or "{}"))
    except Exception as e:
        raise AIServiceError(str(e)) from e


async def improve_resume_for_ats(resume: Resume, job_description: Optional[str] = None) -> Resume:
    s = get_settings()
    genai = _import_genai()
    model = genai.GenerativeModel(s.GEMINI_PRO_MODEL)
    jd = job_description or resume.personalDetails.title
    prompt = f"""Optimize this resume JSON for ATS for role context: {jd}.
Return ONLY valid JSON with same structure. Do not change IDs. Keep photo as empty string.
Input:
{json.dumps(resume.model_dump(), ensure_ascii=False)}
"""
    try:
        resp = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.4,
            ),
        )
        data = json.loads(resp.text or "{}")
        data["personalDetails"]["photo"] = resume.personalDetails.photo
        return Resume.model_validate(data)
    except Exception as e:
        raise AIServiceError(str(e)) from e


async def generate_latex(resume: Resume, template: LatexTemplate = "professional") -> str:
    s = get_settings()
    genai = _import_genai()
    model = genai.GenerativeModel(s.GEMINI_PRO_MODEL)
    styles = {
        "professional": "modern professional LaTeX with titlesec, fontawesome5",
        "academic": "academic CV style",
        "minimalist": "minimal whitespace-focused layout",
        "minimal": "minimal whitespace-focused layout",
    }
    style = styles.get(template, styles["professional"])
    prompt = f"""Expert LaTeX writer. Produce compilable LaTeX only, {style}.
Omit empty sections. Escape LaTeX special chars.
Data:
{json.dumps(resume.model_dump(), ensure_ascii=False)}
"""
    try:
        resp = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(temperature=0.2),
        )
        return (resp.text or "").strip()
    except Exception as e:
        raise AIServiceError(str(e)) from e


async def enhance_photo(image_bytes: bytes, mime_type: str) -> str:
    """Return data URL base64. Uses Gemini image model when supported; else PIL enhancement."""
    s = get_settings()
    genai = _import_genai()
    model = genai.GenerativeModel(s.GEMINI_IMAGE_MODEL)
    prompt = (
        "Enhance this professional headshot: lighting and sharpness. "
        "Keep identity unchanged. Return image."
    )
    try:
        resp = model.generate_content(
            [prompt, {"mime_type": mime_type or "image/jpeg", "data": image_bytes}],
        )
        # Some SDK versions return inline image parts
        if resp.candidates:
            for part in resp.candidates[0].content.parts:
                if getattr(part, "inline_data", None) is not None:
                    b64 = base64.b64encode(part.inline_data.data).decode("ascii")
                    mt = part.inline_data.mime_type or "image/png"
                    return f"data:{mt};base64,{b64}"
    except Exception as e:
        logger.warning("Gemini photo enhancement failed, using PIL fallback: %s", e)

    try:
        from PIL import Image, ImageEnhance, ImageFilter

        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = ImageEnhance.Sharpness(img).enhance(1.15)
        img = ImageEnhance.Contrast(img).enhance(1.05)
        img = img.filter(ImageFilter.DetailFilter())
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=92)
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        return f"data:image/jpeg;base64,{b64}"
    except Exception as e:
        raise AIServiceError(f"Photo enhancement failed: {e}") from e


async def scrape_linkedin(url: str) -> Resume:
    s = get_settings()
    genai = _import_genai()
    model = genai.GenerativeModel(s.GEMINI_PRO_MODEL)
    prompt = f"""From public LinkedIn URL {url}, extract resume JSON if possible.
Do not invent facts; use empty strings/arrays when unknown.
Return JSON with personalDetails, objective, experience, education, backendSkills, frontendSkills,
programmingSkills, cloudSkills, certificates, hobbies. photo must be "".
"""
    try:
        resp = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.1,
            ),
        )
        data = json.loads(resp.text or "{}")
        data.setdefault("personalDetails", {})["photo"] = ""
        return Resume.model_validate(data)
    except Exception as e:
        raise AIServiceError(str(e)) from e
