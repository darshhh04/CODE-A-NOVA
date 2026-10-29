import pickle
from preprocess import clean_text

with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


def predict_news(article):
    cleaned = clean_text(article)                  
    features = vectorizer.transform([cleaned])     
    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features)[0].max()

    label = "REAL" if prediction == 1 else "FAKE"
    return label, round(confidence * 100, 1)


if __name__ == "__main__":
    with open("article.txt", encoding="utf-8") as f:
        article = f.read()

    label, confidence = predict_news(article)
    print("Prediction:", label)
    print("Confidence:", confidence, "%")