
import concurrent.futures
import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

MODEL_NAME = "gemini-3.5-flash"  


def build_prompt(resume_text: str, jd_text: str, match_score: float, missing_keywords: list[str]) -> str:

    missing_str = ", ".join(missing_keywords) if missing_keywords else "none"
    return f"""You are an AI resume reviewer. Analyze the resume against the job description
and identify the most important writing and content improvements.

Match score: {match_score}%
Missing keywords (already identified separately — do not repeat these,
focus on writing quality and content instead): {missing_str}

Resume:
{resume_text}

Job description:
{jd_text}

Review these areas:
- Grammar, spelling, and wording issues
- Weak bullet points and how to improve them
- Resume summary improvement
- Project description improvement
- Why the match score is what it is

Only suggest changes relevant to the provided resume and job description.
Do not invent skills, experience, projects, achievements, or information.

Be brief. Every list item must be ONE short, direct sentence — 15 words or
fewer. No multi-sentence explanations, no "for example" tangents, no
restating the problem before the fix. State the concrete action only.
score_explanation and summary_improvement: 1-2 short sentences maximum,
same direct style.

Return ONLY valid JSON in this exact structure:
{{
  "score_explanation": "Brief explanation of why the score is high or low.",
  "grammar_issues": ["issue 1", "issue 2"],
  "bullet_improvements": ["improvement 1", "improvement 2"],
  "summary_improvement": "Improved summary or advice.",
  "project_improvements": ["improvement 1", "improvement 2"],
  "recommendations": ["recommendation 1", "recommendation 2", "recommendation 3"]
}}
"""



STRING_FIELDS = ["score_explanation", "summary_improvement"]
LIST_FIELDS = ["grammar_issues", "bullet_improvements", "project_improvements", "recommendations"]


def parse_llm_response(raw_text) -> dict:
  
    text = str(raw_text).strip()

    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()

    parsed = json.loads(text) 
    if not isinstance(parsed, dict):
        raise ValueError(f"Expected a JSON object, got {type(parsed).__name__}")

    result = {}
    for field in STRING_FIELDS:
        value = parsed.get(field, "")
        result[field] = str(value) if value else ""

    for field in LIST_FIELDS:
        value = parsed.get(field, [])
        if not isinstance(value, list):
            value = []
  
        result[field] = [str(item) for item in value]


    has_content = any(result[f] for f in STRING_FIELDS) or any(result[f] for f in LIST_FIELDS)
    if not has_content:
        raise ValueError("LLM response had no usable content in any field")

    return result


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
    
    empty_feedback = {field: "" for field in STRING_FIELDS}
    empty_feedback.update({field: [] for field in LIST_FIELDS})

    if not GEMINI_API_KEY:
        return {**empty_feedback, "source": "fallback", "error": "GEMINI_API_KEY not configured"}

    prompt = build_prompt(resume_text, jd_text, match_score, missing_keywords)

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    try:
        future = executor.submit(_call_gemini, prompt)
        raw_text = future.result(timeout=timeout)
        feedback = parse_llm_response(raw_text)
        return {**feedback, "source": "llm"}

    except Exception as e:
     
        return {**empty_feedback, "source": "fallback", "error": str(e)}

    finally:
       
        executor.shutdown(wait=False)