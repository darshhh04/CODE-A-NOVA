from fastapi import APIRouter
from pydantic import BaseModel

from app.matching import compute_match
from app.llm_feedback import get_llm_feedback

router = APIRouter()


class FeedbackRequest(BaseModel):
    resume_text: str
    jd_text: str


@router.post("/feedback")
def get_feedback(payload: FeedbackRequest):

    match_result = compute_match(payload.resume_text, payload.jd_text)

    feedback = get_llm_feedback(
        resume_text=payload.resume_text,
        jd_text=payload.jd_text,
        match_score=match_result["match_score"],
        missing_keywords=match_result["missing_keywords"],
    )

    if feedback["source"] == "fallback":
   
        print(f"[feedback] LLM call fell back: {feedback['error']}")

    return {
        "match_score": match_result["match_score"],
        "missing_keywords": match_result["missing_keywords"],
        "feedback_source": feedback["source"],
 
        "feedback_error": feedback.get("error"),
        "score_explanation": feedback["score_explanation"],
        "grammar_issues": feedback["grammar_issues"],
        "bullet_improvements": feedback["bullet_improvements"],
        "summary_improvement": feedback["summary_improvement"],
        "project_improvements": feedback["project_improvements"],
        "recommendations": feedback["recommendations"],
    }