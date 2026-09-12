export default function ResultsPanel({ missingKeywords, suggestions, feedbackSource }) {
  return (
    <div className="results-panel">
      <div>
        <h3>Missing Keywords</h3>
        {missingKeywords.length === 0 ? (
          <p>No significant missing keywords found.</p>
        ) : (
          <ul className="keyword-list">
            {missingKeywords.map((keyword) => (
              <li key={keyword} className="keyword-chip">{keyword}</li>
            ))}
          </ul>
        )}
      </div>
      <div>
        <h3>AI Suggestions</h3>
        {feedbackSource === "fallback" ? (
          <p className="fallback-note">
            AI suggestions are unavailable right now. Showing keyword-match results only.
          </p>
        ) : (
          <ul>
            {suggestions.map((suggestion, index) => <li key={index}>{suggestion}</li>)}
          </ul>
        )}
      </div>
    </div>
  );
}