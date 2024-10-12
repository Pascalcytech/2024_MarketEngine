from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CompanyDiscovery:
    def __init__(self, query):
        self.query = query
        self.search_results = []
        self.driver = None

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(
            executable_path='C:/Pascal/ChromeDriver/chromedriver-win64/chromedriver-win64/chromedriver.exe'),
            options=chrome_options)

    def discover_companies(self):
        self.setup_driver()

        # Navigate to Google search
        search_url = f"https://www.google.com/search?q={self.query}"
        self.driver.get(search_url)

        # Wait for the search results to appear
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3')))
        except Exception as e:
            print("Search results not found or took too long to load:", e)
            self.driver.quit()
            return []

        unique_urls = set()  # To store unique URLs

        # Loop through search results
        while True:
            try:
                # Re-fetch search result links
                links = self.driver.find_elements(By.CSS_SELECTOR, 'h3')
                if not links:
                    break  # Exit if no more links are found

                for link in links:
                    try:
                        href = link.find_element(By.XPATH, './ancestor::a').get_attribute('href')
                        name = link.text.strip()  # Get the text inside the header as the company name

                        if href not in unique_urls:
                            unique_urls.add(href)
                            print(f"Found link: {name} -> {href}")  # Print every link

                    except Exception as e:
                        print(f"Could not find link for header: {e}")

                # Check for the next page of results
                try:
                    next_button = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Next')]")
                    next_button.click()
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3')))
                except Exception:
                    break  # Exit loop if no next button is found

            except Exception as e:
                print(f"Error during link processing: {e}")
                break

        # Now, print all found links and proceed to scrape them
        print("\nAll found links:")
        for url in unique_urls:
            print(url)

        # Now access each link to scrape company names
        for url in unique_urls:
            company_names = self.scrape_company_names(url)
            for company_name in company_names:
                self.search_results.append({'name': company_name, 'url': url})

        self.driver.quit()
        return self.search_results

    def scrape_company_names(self, url):
        company_names = []

        # Navigate to the URL to scrape company names
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h2')))

            # Use appropriate selectors to extract company names
            company_elements = self.driver.find_elements(By.TAG_NAME, 'h2')  # Adjust this as needed
            for element in company_elements:
                company_name = element.text.strip()
                if company_name:  # Add only non-empty names
                    company_names.append(company_name)

        except Exception as e:
            print(f"Error scraping {url}: {e}")

        return company_names


# Example usage
if __name__ == "__main__":
    discovery = CompanyDiscovery('AI companies in Europe')
    results = discovery.discover_companies()
    print(results)
