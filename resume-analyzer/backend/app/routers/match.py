from fastapi import APIRouter
from pydantic import BaseModel

from app.matching import compute_match

router = APIRouter()


class MatchRequest(BaseModel):
   
    resume_text: str
    jd_text: str


@router.post("/match")
def match_resume_to_jd(payload: MatchRequest):
 
    return compute_match(payload.resume_text, payload.jd_text)