import concurrent.futures
import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

MODEL_NAME = "gemini-3.5-flash" 


def build_prompt(resume_text, jd_text, match_score: float, missing_keywords: list[str]):
    missing_str = ", ".join(missing_keywords) if missing_keywords else "none"
    return f"""You are a resume reviewer. Given a resume, a job description, a computed
TF-IDF match score, and keywords missing from the resume, produce 3 to 5
actionable suggestions to improve the resume for this specific job.

Match score: {match_score}%
Missing keywords: {missing_str}

Resume:
{resume_text}

Job description:
{jd_text}

Respond with ONLY valid JSON, no markdown code fences, no extra commentary,
in exactly this shape:
{{"suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"]}}
"""


def parse_llm_response(raw_text) -> list[str]:
   
    text = str(raw_text).strip()

    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()

    parsed = json.loads(text)
    suggestions = parsed.get("suggestions", [])

    if not isinstance(suggestions, list) or not suggestions:
        raise ValueError("LLM response had no usable 'suggestions' list")

    return [str(item) for item in suggestions]


def _call_gemini(prompt: str) -> str:

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    return response.text


def get_llm_feedback(
    resume_text: str,
    jd_text: str,
    match_score: float,
    missing_keywords: list[str],
    timeout: int = 15,
) -> dict:
    
    if not GEMINI_API_KEY:
        return {
            "suggestions": [],
            "source": "fallback",
            "error": "GEMINI_API_KEY not configured",
        }

    prompt = build_prompt(resume_text, jd_text, match_score, missing_keywords)

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    try:
        future = executor.submit(_call_gemini, prompt)
        raw_text = future.result(timeout=timeout)
        suggestions = parse_llm_response(raw_text)
        return {"suggestions": suggestions, "source": "llm"}

    except Exception as e:
        return {"suggestions": [], "source": "fallback", "error": str(e)}

    finally:
        executor.shutdown(wait=False)