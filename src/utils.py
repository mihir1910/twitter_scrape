import random, time, logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("twitter-scraper")

def human_sleep(min_s=0.7, max_s=1.5):
    """Random human-like sleep to avoid detection"""
    time.sleep(random.uniform(min_s, max_s))
