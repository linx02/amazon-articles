from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import argparse

# Parse command-line arguments
argparser = argparse.ArgumentParser()

argparser.add_argument("--url", type=str, required=True)
url = argparser.parse_args().url

# Setup Chrome options (optional)
chrome_options = webdriver.ChromeOptions()

# Setup WebDriver with ChromeDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL
driver.get(url)

# Wait for the toggle button to be present and click it to expand the content
try:
    # Wait for the toggle button to be clickable
    toggle_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#productFactsToggleButton > a'))
    )
    toggle_button.click()
    time.sleep(5)
except Exception as e:
    print(f"Error clicking the toggle button: {e}")


product_title = driver.find_element(By.CSS_SELECTOR, '#productTitle').text

try:
    reviews_link = driver.find_element(By.CSS_SELECTOR, '#cr-pagination-footer-0 > a').get_attribute('href')
except Exception as e:
    reviews_link = driver.find_element(By.CSS_SELECTOR, '[data-hook="see-all-reviews-link-foot"]').get_attribute('href')

image = driver.find_element(By.CSS_SELECTOR, '#landingImage').get_attribute('src')

# Wait for the expanded content to be visible
try:
    # Wait for the expanded content to be visible
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="productFactsDesktopExpander"]'))
    )
    element = driver.find_element(By.XPATH, '//*[@id="productFactsDesktopExpander"]/div[1]')
    element_text = element.text
except Exception as e:
    print(f"Error waiting for content to load: {e}")

try:
    # Wait for the reviews link to be visible
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#featurebullets_feature_div'))
    )
    element = driver.find_element(By.CSS_SELECTOR, '#featurebullets_feature_div')
    element_text = element.text
except Exception as e:
    print(f"Error waiting for reviews link to load: {e}")

driver.get(reviews_link)

time.sleep(5)

review_elements = driver.find_elements(By.CSS_SELECTOR, '[data-hook="review-body"] > span')

review_texts = [elem.text for elem in review_elements]

data = {
    "product_title": product_title,
    "product_facts": element_text,
    "reviews": review_texts,
    "image": image
}

# Save the data to a JSON file
with open(f'{url.split('dp/')[1].split('/')[0]}.info.json', 'w') as f:
    json.dump(data, f, indent=4)

# Close the browser
driver.quit()