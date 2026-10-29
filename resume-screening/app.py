import os
import shutil
import streamlit as st
from rank import rank_candidates

st.title("Darshan's AI Resume Screening System")

job_text = st.text_area("Paste the job description here", height=200)
files = st.file_uploader(
    "Upload resumes (PDF, DOCX or TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)

if st.button("Rank Candidates"):
    if not job_text.strip() or not files:
        st.warning("Please paste a job description and upload at least one resume.")
    else:
        if os.path.exists("uploads"):
            shutil.rmtree("uploads")
        os.makedirs("uploads")

        for f in files:
            with open(os.path.join("uploads", f.name), "wb") as out:
                out.write(f.getbuffer())

        ranked = rank_candidates("uploads", job_text)

        st.header("Ranking")
        for position, c in enumerate(ranked, start=1):
            st.subheader(f"{position}. {c['name']} - {c['score']}%")
            st.write("Matched skills:", ", ".join(c["matched"]) or "None")
            st.write("Missing skills:", ", ".join(c["missing"]) or "None")