# AI Resume Screening System (Code-a-Nova)

Analyzes resumes and ranks candidates based on job requirements.

## Features
- Resume text extraction (PDF, DOCX, TXT)
- Skill matching with the job description
- Candidate ranking system

## How it works
1. `extract_text.py` reads the text from each resume.
2. `skills.py` finds known skills in the resume and the job description.
3. `match.py` gives each resume a score: matched skills / required skills x 100.
4. `rank.py` sorts candidates from highest to lowest score.
5. `app.py` is a simple Streamlit web page for the whole process.

## Run it
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tech
Python, pdfplumber, python-docx, Streamlit