from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

# Get the ChromeDriver path from the environment variable
chrome_driver_path = os.getenv("CHROME_DRIVER_PATH", "C:/Pascal/ChromeDriver/chromedriver-win64/chromedriver-win64/chromedriver.exe")

# Create a Service object and pass it to the Chrome WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open a website
driver.get("https://www.google.com")

# Close the browser
driver.quit()
