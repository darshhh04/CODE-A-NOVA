import pandas as pd

fake = pd.read_csv("data/Fake.csv")
real = pd.read_csv("data/True.csv")

fake["label"] = 0
real["label"] = 1


data = pd.concat([fake, real])

data = data[["title", "text", "label"]]
data["content"] = data["title"] + " " + data["text"]

data = data.sample(frac=1, random_state=42).reset_index(drop=True)

print("Shape:", data.shape)
print(data["label"].value_counts())
print(data.head())

data.to_csv("data/news.csv", index=False)