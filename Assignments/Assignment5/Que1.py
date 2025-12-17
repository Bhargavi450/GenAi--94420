# 1. Scrape Internship information and batches from Sunbeam website.

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://sunbeaminfo.in")

print("Initial Page Title:", driver.title)

driver.implicitly_wait(10)
time.sleep(3)
 
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

links = driver.find_elements(By.TAG_NAME, "a")

print("\nInternship / Training / Batch Information:\n")

count = 0
for link in links:
    text = link.text.strip()
    url = link.get_attribute("href")
   
    if url and (
        "intern" in url.lower() or
        "training" in url.lower() or
        "batch" in url.lower() or
        "program" in url.lower()
    ):
        print("Title :", text if text else "No visible text")
        print("Link  :", url)
        print("-" * 40)
        count += 1

print("Total relevant links found:", count)

driver.quit()
