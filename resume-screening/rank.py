import os
from extract_text import extract_text
from match import calculate_match


def rank_candidates(resumes_folder, job_text):
    candidates = []

    for name in os.listdir(resumes_folder):
        path = os.path.join(resumes_folder, name)
        try:
            resume_text = extract_text(path)
        except ValueError:
            continue  

        result = calculate_match(resume_text, job_text)
        result["name"] = name
        candidates.append(result)

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates