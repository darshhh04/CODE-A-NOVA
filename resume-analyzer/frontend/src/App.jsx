import { useState } from "react";
import { uploadResume, getFeedback } from "./api";

import FileUpload from "./components/FileUpload";
import ResultsPanel from "./components/ResultsPanel";
import "./App.css";


const STATUS = {
  IDLE: "idle",
  UPLOADING: "uploading",
  READY: "ready",
  ANALYZING: "analyzing",
  DONE: "done",
  ERROR: "error",
};

function App() {
  const [status, setStatus] = useState(STATUS.IDLE);
  const [selectedFile, setSelectedFile] = useState(null);
  const [resumeText, setResumeText] = useState(null);
  const [jdText, setJdText] = useState("");
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  async function handleFileSelected(file) {
    setSelectedFile(file);
    setResult(null);
    if (!file) return;

    setStatus(STATUS.UPLOADING);
    setErrorMessage(null);
    try {
      const data = await uploadResume(file);
      setResumeText(data.raw_text);
      setStatus(STATUS.READY);
    } catch (err) {
      setErrorMessage(err.message);
      setStatus(STATUS.ERROR);
    }
  }

  async function handleAnalyze() {
    setStatus(STATUS.ANALYZING);
    setErrorMessage(null);
    try {
      const data = await getFeedback(resumeText, jdText);
      setResult(data);
      setStatus(STATUS.DONE);
    } catch (err) {
      setErrorMessage(err.message);
      setStatus(STATUS.ERROR);
    }
  }

  const canAnalyze =
    resumeText && jdText.trim().length > 0 &&
    status !== STATUS.UPLOADING && status !== STATUS.ANALYZING;

  return (
    <div className="app-container">
      <h1>AI Resume Analyzer</h1>

      <FileUpload
        onFileSelected={handleFileSelected}
        selectedFileName={selectedFile?.name}
        disabled={status === STATUS.UPLOADING || status === STATUS.ANALYZING}
      />
      {status === STATUS.UPLOADING && <p className="loading-text">Extracting text from resume…</p>}

      <label htmlFor="jd-textarea">Job Description</label>
      <textarea
        id="jd-textarea"
        value={jdText}
        onChange={(e) => setJdText(e.target.value)}
        placeholder="Paste the job description here…"
        rows={8}
        disabled={status === STATUS.ANALYZING}
      />

      <button onClick={handleAnalyze} disabled={!canAnalyze}>
        {status === STATUS.ANALYZING ? "Analyzing…" : "Analyze Match"}
      </button>

      {status === STATUS.ERROR && errorMessage && <p className="error-text">Error: {errorMessage}</p>}

      {status === STATUS.DONE && result && (
        <div className="results-section">
          <ResultsPanel
            missingKeywords={result.missing_keywords}
            suggestions={result.suggestions}
            feedbackSource={result.feedback_source}
          />
        </div>
      )}
    </div>
  );
}

export default App;