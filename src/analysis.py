import pandas as pd, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def vectorize_texts(texts, max_features=5000):
    vec = TfidfVectorizer(max_features=max_features)
    return vec.fit_transform(texts)

def add_sentiment(df):
    sid = SentimentIntensityAnalyzer()
    df["sentiment"] = df["clean_text"].apply(lambda t: sid.polarity_scores(t)["compound"])
    return df

def aggregate_signals(df, window="5T"):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")
    return df.resample(window).agg(
        count=("tweet_id","count"),
        avg_sent=("sentiment","mean")
    )
