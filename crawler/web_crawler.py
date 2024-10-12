import scrapy
from scrapy.crawler import CrawlerProcess


class WebCrawler(scrapy.Spider):
    name = "company_spider"
    extracted_links = []

    def __init__(self, start_urls):
        super().__init__()  # Call parent constructor
        self.start_urls = start_urls

    def parse(self, response):
        # Extract company URLs
        for company_url in response.css('a::attr(href)').getall():
            full_url = response.urljoin(company_url)
            WebCrawler.extracted_links.append(full_url)  # Store extracted links

    @staticmethod
    def extract_links():
        return WebCrawler.extracted_links


def run_crawler(start_urls):
    process = CrawlerProcess()
    process.crawl(WebCrawler, start_urls=[start_urls])  # Wrap the URL in a list
    process.start()


# Example of running the crawler and getting the links
if __name__ == "__main__":
    extracted_links = run_crawler('https://companiesmarketcap.com/tech/largest-tech-companies-by-market-cap/')
    print("Extracted links:", WebCrawler.extract_links())
