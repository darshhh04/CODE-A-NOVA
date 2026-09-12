
function ListSection({ title, items }) {
  if (!items || items.length === 0) return null;
  return (
    <section>
      <h3>{title}</h3>
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </section>
  );
}

export default function ResultsPanel({
  matchScore,
  missingKeywords = [],
  feedbackSource,
  scoreExplanation = "",
  grammarIssues = [],
  bulletImprovements = [],
  summaryImprovement = "",
  projectImprovements = [],
  recommendations = [],
}) {
  const isFallback = feedbackSource === "fallback";

  return (
    <div className="results-panel">

      <section>
        <h3>Missing Keywords</h3>
        {missingKeywords.length === 0 ? (
          <p>No significant missing keywords found.</p>
        ) : (
          <ul className="keyword-list">
            {missingKeywords.map((keyword) => (
              <li key={keyword} className="keyword-chip">
                {keyword}
              </li>
            ))}
          </ul>
        )}
      </section>

      {isFallback ? (

        <p className="fallback-note">
          AI writing feedback is unavailable right now. Showing keyword-match
          results only.
        </p>
      ) : (
        <>
          {scoreExplanation && (
            <section>
              <h3>Why This Score</h3>
              <p>{scoreExplanation}</p>
            </section>
          )}

          <ListSection title="Grammar & Wording" items={grammarIssues} />
          <ListSection title="Bullet Point Improvements" items={bulletImprovements} />

          {summaryImprovement && (
            <section>
              <h3>Summary Improvement</h3>
              <p>{summaryImprovement}</p>
            </section>
          )}

          <ListSection title="Project Description Improvements" items={projectImprovements} />
          <ListSection title="Recommendations" items={recommendations} />
        </>
      )}
    </div>
  );
}