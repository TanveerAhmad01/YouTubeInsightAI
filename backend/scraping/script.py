import time
import re
import csv
import os
import requests
from tqdm import tqdm
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# Define output paths
CSV_FILE = os.path.join("backend", "Data", "youtube_comments.csv")
LOG_FILE = os.path.join("backend", "Data", "error_log.txt")

# Ensure Data folder exists
os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def is_connected():
    try:
        requests.get('https://www.google.com/', timeout=5)
        return True
    except requests.ConnectionError:
        return False

def save_comments_to_csv(comments, filename=CSV_FILE):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Comment'])
        for comment in comments:
            writer.writerow([comment])

def log_error(message):
    with open(LOG_FILE, "a", encoding='utf-8') as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] {message}\n")

def scrape_youtube_comments(url, max_comments=100):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(2)

    comments = set()
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    try:
        pbar = tqdm(total=max_comments, desc="Scraping Comments", ncols=100)

        while len(comments) < max_comments:
            if not is_connected():
                print("\n⚠️ Internet connection lost. Saving scraped comments so far...")
                save_comments_to_csv(list(comments))
                driver.quit()
                return list(comments)

            comment_elements = driver.find_elements(By.CSS_SELECTOR, "#content-text")
            new_comments = [remove_emojis(elem.text) for elem in comment_elements if elem.text.strip()]
            previous_count = len(comments)
            comments.update(new_comments)

            added_now = len(comments) - previous_count
            pbar.update(added_now)

            if added_now == 0:
                print("✅ No new comments after scrolling. Stopping...")
                break

            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)

            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                print("✅ Reached end of comments.")
                break
            last_height = new_height

        pbar.close()

    except WebDriverException as e:
        print(f"\n❌ WebDriver Exception occurred: {e}. Saving comments...")
        log_error(str(e))
    except Exception as e:
        print(f"\n❌ Unknown error occurred: {e}. Saving comments...")
        log_error(str(e))
    finally:
        driver.quit()

    save_comments_to_csv(list(comments))
    return list(comments)[:max_comments]

if __name__ == "__main__":
    # Remove previous file if exists
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)

    video_url = input("Enter YouTube video URL: ")
    print("🔎 Scraping comments, please wait...\n")
    comments = scrape_youtube_comments(video_url)

    print(f"\n✅ Scraping complete! {len(comments)} comments saved into '{CSV_FILE}'.")
