# contact_method_recognition.py
import re
import requests
from bs4 import BeautifulSoup


class ContactMethodRecognition:

    def __init__(self, company_url):
        self.company_url = company_url
        self.emails = []
        self.forms = []

    def extract_emails(self):
        # Fetch webpage content
        response = requests.get(self.company_url)
        content = response.text

        # Regex pattern to find email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        self.emails = re.findall(email_pattern, content)

        return self.emails

    def extract_contact_forms(self):
        # Fetch webpage content
        response = requests.get(self.company_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all forms in the webpage
        self.forms = soup.find_all('form')

        return self.forms


# Example usage
if __name__ == "__main__":
    recognizer = ContactMethodRecognition('https://example.com')
    print("Emails found:", recognizer.extract_emails())
    print("Forms found:", recognizer.extract_contact_forms())
