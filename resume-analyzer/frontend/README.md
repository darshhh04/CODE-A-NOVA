# AI Resume Analyzer

An AI-powered resume analyzer that compares a resume with a job description and provides a match score, ATS compatibility score, missing keywords, and AI-based improvement suggestions.

---

## ✨ Features

- 📄 **Resume Upload** — Upload resumes in PDF or DOCX format
- 🧹 **Text Extraction & Cleaning** — Extract and clean resume text
- 🎯 **JD Match Score** — Compare resume and job description using TF-IDF and cosine similarity
- 🔍 **Missing Keywords** — Find important keywords missing from the resume
- ✅ **ATS Compatibility** — Check resume structure using rule-based ATS checks
- 🤖 **AI Feedback** — Generate feedback using Google Gemini
- ✍️ **Resume Improvements** — Get suggestions for grammar, bullet points, summary, and projects
- 🛡️ **Graceful Fallback** — Basic matching still works if the AI service is unavailable

---

## 🚀 Demo

### 🌐 Live Demo

**Live Application:** [ai-resume-analyzer-darshan.netlify.app/](https://ai-resume-analyzer-darshan.netlify.app/)



### 📸 Screenshot

![AI Resume Analyzer](resume-analyzer/backend/docs/heropage_2.png)


---

## 🛠️ Tech Stack

### Frontend

- React
- Vite
- CSS

### Backend

- Python
- FastAPI
- scikit-learn
- pdfplumber
- python-docx
- Google Gemini API

---

## ⚙️ How It Works

```text
Resume Upload
      ↓
Text Extraction
      ↓
Text Cleaning
      ↓
ATS Compatibility Check
      ↓
Resume + Job Description
      ↓
TF-IDF Matching
      ↓
Missing Keywords
      ↓
Gemini AI Feedback
      ↓
Results
```

---

## 🧠 Key Concepts

- Natural Language Processing
- TF-IDF and Cosine Similarity
- Rule-based ATS Analysis
- Resume Text Extraction
- LLM-based Feedback
- REST API
- React + FastAPI

---

## 📁 Project Structure

```text
resume-analyzer/
│
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── feedback.py
│   │   │   ├── match.py
│   │   │   └── upload.py
│   │   │
│   │   ├── ats_score.py
│   │   ├── cleaning.py
│   │   ├── extraction.py
│   │   ├── llm_feedback.py
│   │   ├── main.py
│   │   └── matching.py
│   │
│   ├── requirements.txt
│   └── .env
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── FileUpload.jsx
    │   │   ├── MatchScore.jsx
    │   │   └── ResultsPanel.jsx
    │   │
    │   ├── api.js
    │   ├── App.jsx
    │   ├── App.css
    │   └── main.jsx
    │
    └── package.json
```

---

## 💻 Getting Started

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd resume-analyzer
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 🔌 API

### `POST /api/upload`

Uploads a PDF/DOCX resume and returns extracted text and ATS information.

### `POST /api/match`

Compares the resume with a job description and returns:

- Match score
- Missing keywords

### `POST /api/feedback`

Returns:

- Match score
- Missing keywords
- Score explanation
- Grammar issues
- Bullet improvements
- Summary suggestions
- Project suggestions
- Recommendations

---

## ⚠️ Limitations

- TF-IDF matching is based mainly on word overlap.
- ATS score is a rule-based estimate, not a specific ATS simulation.
- AI feedback depends on Gemini API availability and limits.
- Currently supports PDF and DOCX resumes.

---

## 🔮 Future Improvements

- [ ] Improve semantic matching using embeddings
- [ ] Add more advanced ATS checks
- [ ] Add LinkedIn/GitHub/portfolio analysis
- [ ] Add resume keyword and repetition analysis
- [ ] Support multiple resumes for comparison

---


### 👨‍💻 Built by

**Darshan Bhatarkar**
