from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service

# Set the path to your Microsoft Edge WebDriver
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service)

try:
    # Open Google in Edge browser
    driver.get('https://www.google.com')
    time.sleep(5)
    # Locate the search box and send "crocodile" to it
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys('crocodile')
    search_box.send_keys(Keys.RETURN)  # Press Enter to perform the search

    # Wait for a few seconds to see the results
    time.sleep(5)

    # Optionally, you can print the title of the first result page
    print(driver.title)

finally:
    # Close the browser
    driver.quit()
