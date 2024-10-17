import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin, urlparse


class ContactMethodRecognitionSelenium:

    def __init__(self, company_url):
        self.company_url = company_url
        self.visited_urls = set()  # Keep track of visited URLs
        self.results = {'email': None, 'form': None}  # Store email and form result
        self.max_urls = 20  # Maximum number of URLs to crawl
        self.current_count = 0  # Current count of crawled URLs

        # Initialize the undetected Chrome driver
        self.driver = uc.Chrome()

    def extract_emails(self, content):
        # Regex pattern to find email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(email_pattern, content)

    def extract_forms(self, soup, url):
        # Extract form details, but only if 'contact-us' is in the URL
        if 'contact-us' in url.lower():
            forms = soup.find_all('form')
            if forms:  # If any form is found
                return url  # Return the current page's URL instead of the form's action URL
        return None

    def crawl_page(self, url):
        if self.current_count >= self.max_urls or ('email' in self.results and self.results['email']) or self.results['form']:
            return  # Stop if max URL count is reached or both email/form have been found

        try:
            # Visit the page using Selenium
            print(f"\n---\nNew page: {url}")
            self.driver.get(url)
            time.sleep(3)  # Allow time for the page to fully load

            # Get page content after it's loaded
            content = self.driver.page_source

            # Use BeautifulSoup to parse the content
            soup = BeautifulSoup(content, 'html.parser')

            # Extract forms from the content, but only if 'contact-us' is in the URL
            found_form = self.extract_forms(soup, url)
            if found_form and not self.results['form']:
                self.results['form'] = url  # Store the URL of the page with the form
                self.results['email'] = None  # Email remains empty
                print(f"Found form on {url}: {url}")
                return  # Return immediately if a form is found

            # Extract emails from the content if no form has been found yet
            found_emails = self.extract_emails(content)
            if found_emails and not self.results['email']:
                self.results['email'] = found_emails[0]  # Store only the first email
                print(f"Found email on {url}: {found_emails[0]}")

            # Extract all links on the page
            links = soup.find_all('a', href=True)

            # Prioritize links containing "Contact-us"
            prioritized_links = [link for link in links if 'contact-us' in link['href'].lower()]

            # Add non-duplicate prioritized links to the crawling list
            for link in prioritized_links:
                href = link['href']
                full_url = urljoin(url, href)
                if full_url not in self.visited_urls:
                    print(f"Moving to prioritized link: {full_url}")
                    self.visited_urls.add(full_url)
                    self.current_count += 1
                    self.crawl_page(full_url)  # Recursively crawl the prioritized page
                    if self.current_count >= self.max_urls or self.results['form']:
                        return  # Stop if maximum URL count or form found

            # Iterate through other links if the limit isn't reached
            if self.current_count < self.max_urls:
                for link in links:
                    href = link['href']
                    full_url = urljoin(url, href)
                    # Check if it's a valid URL and not already visited
                    if urlparse(full_url).netloc == urlparse(self.company_url).netloc and full_url not in self.visited_urls:
                        print(f"Moving to new link: {full_url}")
                        self.visited_urls.add(full_url)
                        self.current_count += 1
                        self.crawl_page(full_url)  # Recursively crawl the linked page
                        if self.current_count >= self.max_urls:
                            return  # Stop if maximum URL count is reached

        except Exception as e:
            print(f"Failed to access {url}: {str(e)}")

    def find_contact_methods(self):
        # Start crawling from the initial URL
        print(f"Starting crawl at: {self.company_url}")
        self.visited_urls.add(self.company_url)
        self.crawl_page(self.company_url)
        self.driver.quit()  # Close the browser after crawling

        # Return results with either a form or an email
        return {
            'email': self.results.get('email'),
            'form': self.results.get('form')
        }


# Example usage
if __name__ == "__main__":

    # Initialize the ContactMethodRecognitionSelenium with the company URL
    recognizer = ContactMethodRecognitionSelenium('https://www.loreal-paris.fr/')

    # Find contact methods
    contact_methods = recognizer.find_contact_methods()

    # Print the results
    print("\nContact Methods:")
    print(f"Email: {contact_methods.get('email')}")
    print(f"Form: {contact_methods.get('form')}")
