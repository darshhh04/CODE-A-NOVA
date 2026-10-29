import re
import pandas as pd
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("english"))


def clean_text(text):
    text = re.sub(r"^.{0,100}?\(reuters\)\s*-?\s*", "", str(text), flags=re.I)
    text = text.lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    words = [w for w in text.split() if w not in stop_words and w != "reuters"]
    return " ".join(words)


if __name__ == "__main__":
    data = pd.read_csv("data/news.csv")

    print("Before:", data["content"][0][:200])
    data["clean_content"] = data["content"].apply(clean_text)
    print("After:", data["clean_content"][0][:200])

    data.to_csv("data/clean_news.csv", index=False)
    print("Saved data/clean_news.csv")