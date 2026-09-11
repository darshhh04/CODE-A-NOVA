from fastapi import APIRouter, UploadFile, File, HTTPException

from app.extraction import extract_text

router = APIRouter()


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    file_bytes = await file.read()

    try:
        text = extract_text(file.filename, file_bytes)
    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))

    return {
        "filename": file.filename,
        "char_count": len(text),
        "text": text,
    }