from fastapi import APIRouter, UploadFile, File, HTTPException

from app.extraction import extract_text
from app.cleaning import full_clean_resume

router = APIRouter()


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    file_bytes = await file.read()

    try:
        raw_text = extract_text(file.filename, file_bytes)
    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))

    cleaned_text = full_clean_resume(raw_text)

    return {
        "filename": file.filename,
        "char_count": len(raw_text),
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
    }