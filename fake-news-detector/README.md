# AI Fake News Detection (Code-a-Nova)

A model that predicts whether a news article is fake or real.

## Features
- Text preprocessing (lowercase, remove links, punctuation and stopwords)
- NLP feature extraction (TF-IDF)
- Classification model (Logistic Regression)

## Dataset
Kaggle "Fake and Real News Dataset" (Fake.csv and True.csv). Put both files in a `data/` folder.

## Run it
```bash
pip install -r requirements.txt
python load_data.py     # combine and label the data
python preprocess.py    # clean the text
python train.py         # train the model and show accuracy
python predict.py       # predict the article saved in article.txt
```

## Results
Accuracy on unseen test articles: XX% (copy the number printed by train.py)

## Limitations
The model was trained on US political news from 2016-2017, so it works best on similar articles.

## Tech
Python, pandas, NLTK, scikit-learn