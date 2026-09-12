
function scoreColor(score) {
  if (score >= 40) return "#4ade80"; 
  if (score >= 15) return "#facc15"; 
  return "#f87171"; 
}

export default function MatchScore({ score }) {
  const clampedScore = Math.max(0, Math.min(100, score));

  return (
    <div className="match-score">
      <div className="match-score-header">
        <span>Match Score</span>
        <span>{clampedScore.toFixed(1)}%</span>
      </div>
      <div className="match-score-track">
        <div
          className="match-score-fill"
          style={{
            width: `${clampedScore}%`,
            backgroundColor: scoreColor(clampedScore),
          }}
        />
      </div>
    </div>
  );
}