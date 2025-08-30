import pandas as pd, os
from .utils import logger

def save_parquet(tweets, path):
    df = pd.DataFrame(tweets)
    if os.path.exists(path):
        existing = pd.read_parquet(path)
        df = pd.concat([existing, df]).drop_duplicates(subset="tweet_id")
    df.to_parquet(path, index=False)
    logger.info(f"Saved {len(df)} unique tweets to {path}")
