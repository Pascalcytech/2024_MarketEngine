from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CompanyDiscovery:

    def __init__(self, query):
        self.query = query
        self.search_results = []

    def discover_companies(self):
        # Set up Chrome options for headless mode
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Remove headless mode for debugging
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Define the driver and service
        service = Service(executable_path='C:/Pascal/ChromeDriver/chromedriver-win64/chromedriver-win64/chromedriver.exe')  # Set path to chromedriver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navigate to DuckDuckGo search
        search_url = f"https://duckduckgo.com/?q={self.query}&t=h_"
        driver.get(search_url)

        # Wait for the search results to appear with a longer timeout
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.result__a')))
            time.sleep(5)  # Add sleep to ensure the page is fully loaded
        except Exception as e:
            print("Search results not found or took too long to load.")
            print(driver.page_source)  # Print page source for debugging
            driver.quit()
            return []

        # Extract search result links
        links = driver.find_elements(By.CSS_SELECTOR, 'a.result__a')
        for link in links:
            href = link.get_attribute('href')
            self.search_results.append(href)

        driver.quit()
        return self.search_results


# Example usage
if __name__ == "__main__":
    discovery = CompanyDiscovery('AI companies in Europe')
    print(discovery.discover_companies())
