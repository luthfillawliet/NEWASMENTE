from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up WebDriver (assuming you're using Chrome)
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

# Open the webpage
driver.get('https://example.com')

try:
    # Wait until the parent div is present
    parent_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'div'))
    )

    # Search for the child span with title "whatsapp" within the parent div
    child_span = WebDriverWait(parent_div, 10).until(
        EC.presence_of_element_located((By.XPATH, './/span[@title="whatsapp"]'))
    )

    # Print the text content of the span or perform other actions
    print(child_span.text)
    
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()
