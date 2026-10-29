import os
from extract_text import extract_text
from match import calculate_match

job_text = extract_text("job_description.txt")

for name in os.listdir("resumes"):
    resume_text = extract_text(os.path.join("resumes", name))
    result = calculate_match(resume_text, job_text)
    print("=====", name, "=====")
    print("Score:  ", result["score"], "%")
    print("Matched:", result["matched"])
    print("Missing:", result["missing"])