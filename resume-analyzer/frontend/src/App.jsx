import { useState } from "react";


const API_URL = "http://localhost:8000/api/upload";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handleUpload() {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setError(null);
    setResult(null);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const body = await response.json();
        throw new Error(body.detail || "Upload failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>AI Resume Analyzer</h1>

      <input
        type="file"
        accept=".pdf,.docx"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload} disabled={!file}>
        Upload & Extract Text
      </button>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {result && (
        <div>
          <p>
            <strong>{result.filename}</strong> — {result.char_count} characters
          </p>
          <pre style={{ whiteSpace: "pre-wrap", background: "#f4f4f4", padding: "1rem" }}>
            {result.text}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;