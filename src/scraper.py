from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from .utils import logger, human_sleep
import re, datetime

RE_STATUS_ID = re.compile(r"/status/(\d+)")

def setup_driver(headless=True, profile_path=None):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    if profile_path:
        opts.add_argument(f"--user-data-dir={profile_path}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    return driver

def scrape_hashtag(driver, hashtag, limit=100):
    """Scrape tweets from a given hashtag page"""
    url = f"https://twitter.com/search?q=%23{hashtag}&f=live"
    driver.get(url)
    tweets = []
    seen = set()

    while len(tweets) < limit:
        articles = driver.find_elements(By.CSS_SELECTOR, "article[role='article']")
        for art in articles:
            try:
                link = art.find_element(By.XPATH, ".//a[contains(@href,'/status/')]").get_attribute("href")
                tid = RE_STATUS_ID.search(link).group(1)
                if tid in seen: continue
                seen.add(tid)

                text = art.text
                timestamp = art.find_element(By.TAG_NAME, "time").get_attribute("datetime")
                tweets.append({"tweet_id": tid, "content": text, "timestamp": timestamp})
                if len(tweets) >= limit: break
            except: continue

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        human_sleep()
    logger.info(f"Collected {len(tweets)} tweets for {hashtag}")
    return tweets
