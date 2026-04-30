# scrape_sciencedaily_all.py
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

# ------------- User params -------------
URL = "https://www.sciencedaily.com/news/mind_brain/"
HEADLESS = True               # True: không hiện browser window
MAX_CLICKS = 400              # giới hạn số lần click "Load more" (đề phòng loop vô hạn)
MAX_LINKS = 2000              # dừng khi đạt số links mong muốn
CSV_FILE = "sciencedaily_links.csv"
WAIT_AFTER_SCROLL = 1.5       # đợi sau khi scroll
WAIT_AFTER_CLICK = 3.0        # đợi sau khi click load more
# ---------------------------------------

opts = Options()
opts.add_argument("--disable-gpu")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
driver.get(URL)
time.sleep(2)

# XPath: bắt tất cả <a> có href chứa /releases/ OR /news/ và .htm (bắt link bài báo)
LINK_XPATH = "//a[((contains(@href,'/releases/')) or (contains(@href,'/news/'))) and contains(@href, '.htm')]"

all_links = {}  # dict: href -> title

def save_links():
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "link"])
        for href, title in sorted(all_links.items()):
            writer.writerow([title, href])
    print(f"💾 Saved {len(all_links)} links to {CSV_FILE}")

def collect_current_links(verbose=False):
    elems = driver.find_elements(By.XPATH, LINK_XPATH)
    new = 0
    for a in elems:
        href = a.get_attribute("href")
        title = a.text.strip()
        if not href:
            continue
        # normalize: some anchors can be duplicates/have no title -> we still keep them
        if href not in all_links:
            all_links[href] = title
            new += 1
            if verbose:
                print(" + NEW:", title, href)
    return new

# initial collect
collect_current_links(verbose=True)
save_links()

clicks = 0
while clicks < MAX_CLICKS and len(all_links) < MAX_LINKS:
    # scroll to bottom to reveal load button
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(WAIT_AFTER_SCROLL)

    # try to find load more button
    try:
        load_more_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "load_more_stories"))
        )
        # scroll the button into view then click (use JS click to avoid intercept)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_btn)
        time.sleep(0.3)
        try:
            driver.execute_script("arguments[0].click();", load_more_btn)
        except ElementClickInterceptedException:
            # fallback: use normal click
            load_more_btn.click()
        clicks += 1
        print(f"⏳ Clicked 'Load more' #{clicks} - waiting for new content...")
    except TimeoutException:
        print("⚠️ 'Load more' not found -> maybe no more pages or different UI. Stopping.")
        break

    # wait for new anchors to appear (up to timeout)
    prev_count = len(driver.find_elements(By.XPATH, LINK_XPATH))
    end_time = time.time() + WAIT_AFTER_CLICK + 6  # extra leeway
    got_new = False
    while time.time() < end_time:
        time.sleep(0.5)
        curr_count = len(driver.find_elements(By.XPATH, LINK_XPATH))
        if curr_count > prev_count:
            got_new = True
            break

    # collect links after load
    new_added = collect_current_links(verbose=True)
    if new_added:
        print(f"✅ Collected {len(all_links)} links so far (+{new_added}). Auto-saving CSV.")
        save_links()
    else:
        print("ℹ️ No new links found after clicking. Maybe end reached or button loads duplicates.")
        # continue loop to try again or break if repeated no-change
        # let's check a couple more times or break
        # attempt one more time then exit
        # (You can increase MAX_CLICKS to try more)
        # small sleep to avoid hammering
        time.sleep(1)
        # optional: break to avoid infinite loop
        # break

print("\n🎯 Finished. Total links collected:", len(all_links))
save_links()
driver.quit()
