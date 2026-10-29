import os
from extract_text import extract_text
from skills import find_skills

job_text = extract_text("job_description.txt")
job_skills = find_skills(job_text)
print("JOB NEEDS:", job_skills)
print()

for name in os.listdir("resumes"):
    resume_text = extract_text(os.path.join("resumes", name))
    print(name, "->", find_skills(resume_text))