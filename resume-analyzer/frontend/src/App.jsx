import { useState, useRef, useEffect } from "react";
import { uploadResume, getFeedback } from "./api";
import FileUpload from "./components/FileUpload";
import ResultsPanel from "./components/ResultsPanel";
import "./App.css";
import MatchScore from "./components/MatchScore";

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
  const [atsResult, setAtsResult] = useState(null);
  const [jdText, setJdText] = useState("");
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const resultsRef = useRef(null);

  useEffect(() => {
    if (status === STATUS.DONE && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [status]);

  async function handleFileSelected(file) {
    setSelectedFile(file);
    setResult(null);
    setAtsResult(null);

    if (!file) return;

    setStatus(STATUS.UPLOADING);
    setErrorMessage(null);

    try {
      const data = await uploadResume(file);
      setResumeText(data.raw_text);
      setAtsResult({ score: data.ats_score, issues: data.ats_issues });
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
    resumeText &&
    jdText.trim().length > 0 &&
    status !== STATUS.UPLOADING &&
    status !== STATUS.ANALYZING;

  return (
    <div className="app-container">
      <h1><span style={{ color: 'yellow' }}>Darshan's</span> AI RESUME ANALYZER</h1>

      <FileUpload
        onFileSelected={handleFileSelected}
        selectedFileName={selectedFile?.name}
        disabled={status === STATUS.UPLOADING || status === STATUS.ANALYZING}
      />
      {status === STATUS.UPLOADING && (
        <p className="loading-text">Extracting text from resume…</p>
      )}

      <label htmlFor="jd-textarea" className="jd"></label>
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

      {status === STATUS.ERROR && errorMessage && (
        <p className="error-text">Error: {errorMessage}</p>
      )}

      {status === STATUS.DONE && result && (
        <div className="results-section" ref={resultsRef}>
          {atsResult && (
            <div className="ats-panel">
              <p className="match-score-text">
                ATS Score: {atsResult.score.toFixed(1)}%
              </p>
              {atsResult.issues.length === 0 ? (
                <p>No ATS issues found.</p>
              ) : (
                <ul>
                  {atsResult.issues.map((issue, index) => (
                    <li key={index}>{issue}</li>
                  ))}
                </ul>
              )}
            </div>
          )}
          <MatchScore score={result.match_score} />
          <ResultsPanel
            matchScore={result.match_score}
            missingKeywords={result.missing_keywords}
            feedbackSource={result.feedback_source}
            scoreExplanation={result.score_explanation}
            grammarIssues={result.grammar_issues}
            bulletImprovements={result.bullet_improvements}
            summaryImprovement={result.summary_improvement}
            projectImprovements={result.project_improvements}
            recommendations={result.recommendations}
          />
        </div>
      )}
    </div>
  );
}

export default App;
