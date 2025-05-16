import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

from utils import extract_comment_id

load_dotenv()

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--lang=ko-KR")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

video_url = os.getenv("YOUTUBE_LINK")
driver.get(video_url)

time.sleep(5)
driver.execute_script("window.scrollTo(0, 600);")
time.sleep(5)
driver.execute_script("window.scrollTo(0, 1200);")
time.sleep(5)

badges = driver.find_elements(By.CSS_SELECTOR, "#pinned-comment-badge")
badge = badges[0]
children = badge.find_elements(By.XPATH, "./*")
if len(children) > 0:
    parent = badge.find_element(By.XPATH, "..")
    try:
        header_author = parent.find_element(By.CSS_SELECTOR, "#header-author")
        links = header_author.find_elements(By.TAG_NAME, "a")
        if links:
            last_link = links[-1]
            comment_id = extract_comment_id(last_link.get_attribute("href"))
            print(f"고정 댓글: {comment_id}")
    except Exception as e:
        print(f"오류: {e}")
else:
    print("고정 댓글 X")

driver.quit()
