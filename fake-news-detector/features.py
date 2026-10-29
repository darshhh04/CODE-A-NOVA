import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


def get_features():
    data = pd.read_csv("data/clean_news.csv")
    data = data.dropna(subset=["clean_content"]) 

    text = data["clean_content"]
    labels = data["label"]

    train_text, test_text, y_train, y_test = train_test_split(
        text, labels, test_size=0.2, random_state=42
    )

    vectorizer = TfidfVectorizer(max_features=5000)

    X_train = vectorizer.fit_transform(train_text)
    X_test = vectorizer.transform(test_text)

    return X_train, X_test, y_train, y_test, vectorizer


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, vectorizer = get_features()
    print("Training data shape:", X_train.shape)
    print("Testing data shape: ", X_test.shape)
    print("Some words the model will use:")
    print(list(vectorizer.get_feature_names_out()[:20]))