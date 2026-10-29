from skills import find_skills


def calculate_match(resume_text, job_text):
    job_skills = find_skills(job_text)
    resume_skills = find_skills(resume_text)

    matched = [s for s in job_skills if s in resume_skills]

    missing = [s for s in job_skills if s not in resume_skills]

    if len(job_skills) == 0:
        score = 0
    else:
        score = round(len(matched) / len(job_skills) * 100, 1)

    return {"score": score, "matched": matched, "missing": missing}