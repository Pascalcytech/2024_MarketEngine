import unittest
from crawler.web_crawler import WebCrawler, run_crawler
from crawler.company_discovery import CompanyDiscovery
from scrapy.utils.log import configure_logging


class TestWebCrawler(unittest.TestCase):

    def test_extract_links(self):
        # Reset the extracted links before running the test
        WebCrawler.extracted_links = []

        # Run the crawler (ensure the start_urls is passed correctly as a string)
        run_crawler("https://companiesmarketcap.com/tech/largest-tech-companies-by-market-cap/")

        # Get the extracted links after the crawl
        links = WebCrawler.extract_links()

        # Assertions to ensure the crawler returns a non-empty list
        self.assertTrue(isinstance(links, list))
        self.assertGreater(len(links), 0, "No links extracted from the page")


class TestCompanyDiscovery(unittest.TestCase):

    def test_discover_companies(self):
        # Initialize CompanyDiscovery and discover companies based on the query
        discovery = CompanyDiscovery(query='technology')
        companies = discovery.discover_companies()

        # Assertions to ensure it returns a non-empty list of companies
        self.assertTrue(isinstance(companies, list))
        self.assertGreater(len(companies), 0, "No companies discovered for the technology industry")


if __name__ == "__main__":
    # Configure logging to reduce Scrapy logs during tests
    configure_logging({"LOG_LEVEL": "ERROR"})

    # Run the unittests
    unittest.main()
