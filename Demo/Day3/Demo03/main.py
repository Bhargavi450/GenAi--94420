from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options=Options()
chrome_options.add_argument("--headless")
driver=webdriver.Chrome(options=chrome_options)

driver.get("https://github.com/Bhargavi450/GenAi--94420")
print("Page Title:",driver.title)

driver.implicitly_wait(5)

last_items=driver.find_elements(By.TAG_NAME,"li")
for item in last_items:
    print(item.text)
    
driver.quit()