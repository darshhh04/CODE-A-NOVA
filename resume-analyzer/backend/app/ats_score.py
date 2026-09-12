
import re

EMAIL_PATTERN = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"


def phone_number(text: str) -> bool:

    candidates = re.findall(r"[\d][\d\-.\s()]{6,}\d", text)
    for candidate in candidates:
        digit_count = len(re.sub(r"\D", "", candidate))
        if 7 <= digit_count <= 15:
            return True
    return False


SECTION_PATTERNS = {
    "Experience": [r"work experience", r"\bexperience\b", r"employment history"],
    "Education": [r"\beducation\b"],
    "Skills": [r"\bskills\b", r"technical skills"],
}

MIN_WORD_COUNT = 150   
MAX_WORD_COUNT = 1200  


def check_ats_compatibility(raw_text: str) -> dict:

    issues = []
    checks_passed = 0
    total_checks = 0

    total_checks += 1
    if re.search(EMAIL_PATTERN, raw_text):
        checks_passed += 1
    else:
        issues.append("No email address detected — ATS systems typically need one to route your application.")

    total_checks += 1
    if phone_number(raw_text):
        checks_passed += 1
    else:
        issues.append("No phone number detected.")

    text_lower = raw_text.lower()
    for section_name, patterns in SECTION_PATTERNS.items():
        total_checks += 1
        found = any(re.search(pattern, text_lower) for pattern in patterns)
        if found:
            checks_passed += 1
        else:
            issues.append(f"No clear \"{section_name}\" section header found.")

    word_count = len(raw_text.split())
    total_checks += 1
    if MIN_WORD_COUNT <= word_count <= MAX_WORD_COUNT:
        checks_passed += 1
    elif word_count < MIN_WORD_COUNT:
        issues.append(f"Resume looks short ({word_count} words) — may read as incomplete to an ATS.")
    else:
        issues.append(f"Resume looks long ({word_count} words) — consider trimming to 1-2 pages.")

    ats_score = round((checks_passed / total_checks) * 100, 1)

    return {
        "ats_score": ats_score,
        "issues": issues,
    }