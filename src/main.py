from . import config
from .scraper import setup_driver, scrape_hashtag
from .storage import save_parquet
from .processing import clean_text
from .analysis import add_sentiment, aggregate_signals
import pandas as pd, os

def run_pipeline():
    driver = setup_driver(headless=True)
    all_tweets = []

    for tag in config.HASHTAGS:
        tweets = scrape_hashtag(driver, tag.strip("#"), limit=config.TARGET_TWEETS//len(config.HASHTAGS))
        all_tweets.extend(tweets)
    driver.quit()

    # Save raw
    path = os.path.join(config.OUTPUT_DIR, "tweets.parquet")
    save_parquet(all_tweets, path)

    # Processing
    df = pd.read_parquet(path)
    df["clean_text"] = df["content"].map(clean_text)
    df = add_sentiment(df)

    # Analysis
    signals = aggregate_signals(df, window=config.AGGREGATION_WINDOW)
    print(signals.head())
    signals.to_csv(os.path.join(config.OUTPUT_DIR, "signals.csv"))

if __name__ == "__main__":
    run_pipeline()