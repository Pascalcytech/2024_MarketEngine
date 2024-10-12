from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
import time
import os


class FormFiller:
    def __init__(self, driver_path, browser='chrome'):
        if browser == 'chrome':
            chrome_service = ChromeService(driver_path)
            self.driver = webdriver.Chrome(service=chrome_service)
        elif browser == 'firefox':
            firefox_service = FirefoxService(driver_path)
            self.driver = webdriver.Firefox(service=firefox_service)
        else:
            raise ValueError("Unsupported browser. Use 'chrome' or 'firefox'.")

    def fill_form(self, form_url, form_data):
        try:
            self.driver.get(form_url)
            time.sleep(2)  # Allow the page to load

            for field, value in form_data.items():
                form_field = self.driver.find_element(By.NAME, field)
                form_field.send_keys(value)
                time.sleep(1)  # Wait between field inputs for better human emulation

            submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()
            time.sleep(2)  # Allow form submission to complete

            return f"Form submitted successfully to {form_url}"
        except Exception as e:
            return f"Failed to submit form: {str(e)}"
        finally:
            self.driver.quit()


# Example usage
if __name__ == "__main__":
    # Set your driver path
    driver_path = os.getenv("CHROME_DRIVER_PATH", "/path/to/chromedriver")

    # Initialize the FormFiller with Chrome browser
    form_filler = FormFiller(driver_path)

    # Example form data
    form_data = {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'message': 'This is a personalized message for your company.'
    }

    # Fill and submit the form
    result = form_filler.fill_form('https://example.com/contact', form_data)
    print(result)
