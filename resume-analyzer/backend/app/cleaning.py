import re

NOISES = [
    r"references available (upon|on) request",
    r"curriculum vitae",
    r"page \d+ of \d+",
    r"confidential",
]


def fix_lines(text):

    lines = text.split("\n")
    joined_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            joined_lines.append("")  
            continue

        if joined_lines and joined_lines[-1]:
            prev_line = joined_lines[-1]
            prev_ends_sentence = prev_line.rstrip().endswith((".", "!", "?", ":"))
            current_starts_lowercase = stripped[0].islower()

            if not prev_ends_sentence and current_starts_lowercase:
                joined_lines[-1] = prev_line.rstrip() + " " + stripped
                continue

        joined_lines.append(stripped)

    return "\n".join(joined_lines)


def remove_noise(text):
    cleaned = text
    for pattern in NOISES:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    return cleaned


def clean_text(text):
 
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text) -> list[str]:

    return re.findall(r"\b\w+\b", text)


def full_clean_resume(raw_text: str) -> str:
    text = fix_lines(raw_text)
    text = remove_noise(text)
    text = clean_text(text)
    return text