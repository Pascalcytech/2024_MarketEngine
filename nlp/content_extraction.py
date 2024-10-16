# content_extraction.py
import requests
from bs4 import BeautifulSoup


class ContentExtractor:

    def __init__(self, company_url):
        self.company_url = company_url

    def extract_about_us(self):
        # Attempt to locate and scrape the "About Us" page
        potential_urls = [
            f"{self.company_url}/about",
            f"{self.company_url}/about-us",
            f"{self.company_url}/company/about"
        ]

        about_content = None
        for url in potential_urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Example: extract paragraphs from the page
                    about_content = " ".join([p.get_text() for p in soup.find_all('p')])
                    if about_content:
                        break
            except requests.exceptions.RequestException:
                continue

        if about_content:
            return about_content.strip()
        else:
            return "No 'About Us' page found"


# Example usage
if __name__ == "__main__":
    extractor = ContentExtractor('https://www.mobileye.com/')
    print(extractor.extract_about_us())
