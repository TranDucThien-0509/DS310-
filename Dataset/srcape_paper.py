import csv
import time
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

input_file = "space_time.csv"
output_file = "articles_output.csv"
backup_file = "articles_output_backup.csv"

# Backup file cũ
if os.path.exists(output_file):
    shutil.copy(output_file, backup_file)
    print(f"Đã backup file cũ sang {backup_file}")

# Khởi tạo Chrome với option bỏ qua SSL
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--headless')  # chạy không mở cửa sổ Chrome (tuỳ chọn)
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)

# Tạo file output (append mode)
file_exists = os.path.exists(output_file)
with open(output_file, "a", newline="", encoding="utf-8") as out:
    writer = csv.DictWriter(
        out,
        fieldnames=["title", "link", "date_posted", "headline", "source", "abstract", "full_story"]
    )

    # Ghi header nếu file trống
    if not file_exists or os.stat(output_file).st_size == 0:
        writer.writeheader()

    # Mở file input
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            title = row["title"]
            link = row["link"]
            print(f"Đang cào: {title} — {link}")

            success = False
            for attempt in range(3):  # retry 3 lần
                try:
                    driver.get(link)
                    time.sleep(2)

                    # Lấy dữ liệu
                    date_posted = driver.find_element(By.ID, "date_posted").text.strip()
                    headline = driver.find_element(By.ID, "headline").text.strip()
                    source = driver.find_element(By.ID, "source").text.strip()
                    abstract = driver.find_element(By.ID, "abstract").text.strip()
                    full_story = driver.find_element(By.ID, "story_text").text.strip()

                    # Ghi CSV
                    writer.writerow({
                        "title": title,
                        "link": link,
                        "date_posted": date_posted,
                        "headline": headline,
                        "source": source,
                        "abstract": abstract,
                        "full_story": full_story
                    })
                    success = True
                    break  # thoát vòng retry nếu thành công

                except WebDriverException as e:
                    print(f"!! Lỗi khi cào link {link} (lần {attempt+1}/3): {e}")
                    time.sleep(2)  # đợi rồi retry

            if not success:
                # Nếu retry 3 lần vẫn lỗi, ghi dữ liệu rỗng
                writer.writerow({
                    "title": title,
                    "link": link,
                    "date_posted": "",
                    "headline": "",
                    "source": "",
                    "abstract": "",
                    "full_story": ""
                })

driver.quit()
print(f"DONE — dữ liệu đã được lưu vào {output_file}")
