import os
import pdfplumber
import docx


def extract_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_from_docx(path):
    document = docx.Document(path)
    return "\n".join(p.text for p in document.paragraphs)


def extract_from_txt(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def extract_text(path):
    path = path.lower()
    if path.endswith(".pdf"):
        return extract_from_pdf(path)
    elif path.endswith(".docx"):
        return extract_from_docx(path)
    elif path.endswith(".txt"):
        return extract_from_txt(path)
    else:
        raise ValueError("Unsupported file type: " + path)


if __name__ == "__main__":
    for name in os.listdir("resumes"):
        text = extract_text(os.path.join("resumes", name))
        print("=====", name, "=====")
        print(text[:300])