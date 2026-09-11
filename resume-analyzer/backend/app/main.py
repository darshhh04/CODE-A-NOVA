from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import upload, match, feedback

app = FastAPI(title="AI Resume Analyzer API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(match.router, prefix="/api", tags=["match"])
app.include_router(feedback.router, prefix="/api", tags=["feedback"])


@app.get("/")
def health_check():
    return {"status": "ok"}