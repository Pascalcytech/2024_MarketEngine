# company_discovery.py
import requests
from bs4 import BeautifulSoup


class CompanyDiscovery:

    def __init__(self, query):
        self.query = query
        self.search_results = []

    def discover_companies(self):
        search_url = f"https://duckduckgo.com/html/?q={self.query}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            url = link['href']
            if 'http' in url:
                self.search_results.append(url)

        return self.search_results


# Example usage
if __name__ == "__main__":
    discovery = CompanyDiscovery('AI companies in Europe')
    print(discovery.search_companies())
