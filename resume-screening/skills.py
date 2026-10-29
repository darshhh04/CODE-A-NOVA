import re

SKILLS = [
    "python", "java", "javascript", "c++", "sql", "html", "css",
    "react", "node.js", "express.js", "mongodb", "mysql", "git",
    "machine learning", "deep learning", "nlp", "pandas", "numpy",
    "scikit-learn", "flask", "django", "fastapi", "docker", "aws",
    "data analysis", "rest api", "tensorflow", "figma", "photoshop",
]


def find_skills(text):
    
    text = text.lower()
    found = []
    for skill in SKILLS:
       
        pattern = r"(?<![a-z0-9+#.])" + re.escape(skill) + r"(?![a-z0-9+#])"
        if re.search(pattern, text):
            found.append(skill)
    return found