from extract_text import extract_text
from rank import rank_candidates

job_text = extract_text("job_description.txt")
ranked = rank_candidates("resumes", job_text)

print("CANDIDATE RANKING")
print("-" * 40)
for position, c in enumerate(ranked, start=1):
    print(f"{position}. {c['name']} - {c['score']}%")
    print("   Missing:", c["missing"])