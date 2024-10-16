from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
import time
import os


class SmartFormFiller:
    def __init__(self, driver_path, browser='chrome'):
        if browser == 'chrome':
            chrome_service = ChromeService(driver_path)
            self.driver = webdriver.Chrome(service=chrome_service)
        else:
            raise ValueError("Unsupported browser. Use 'chrome'.")

    def get_form_fields(self):
        # Locate visible input fields, textareas, or select dropdowns within the form
        fields = self.driver.find_elements(By.XPATH, "//input | //textarea | //select")
        return [field for field in fields if field.is_displayed()]  # Only interact with visible fields

    def find_label_for_field(self, field):
        # Attempt to locate the label element by checking the "for" attribute or surrounding elements
        try:
            field_id = field.get_attribute('id')
            if field_id:
                label = self.driver.find_element(By.XPATH, f"//label[@for='{field_id}']")
                return label.text
            else:
                # If no "for" attribute, look for nearby <label> or preceding text
                label = field.find_element(By.XPATH, "./preceding::label[1]")
                return label.text
        except:
            return None

    def determine_field_type(self, label_text, field):
        # Analyze the label or input field to decide what type of information is expected
        label_text = label_text.lower() if label_text else ""
        field_type = field.get_attribute('type')  # get the input field's type

        if 'name' in label_text or 'full name' in label_text:
            return 'name'
        elif 'email' in label_text or field_type == 'email':
            return 'email'
        elif 'company' in label_text:
            return 'company'
        elif 'message' in label_text or field.tag_name == 'textarea':
            return 'message'
        elif field_type == 'password':
            return 'password'
        elif field_type == 'tel' or 'phone' in label_text:
            return 'phone'
        else:
            return 'text'  # default to general text if no specific type is determined

    def fill_field(self, field, field_type, form_data):
        # Fill the field based on its type and available form data
        value = form_data.get(field_type, "default value")
        field.send_keys(value)

    def scroll_into_view(self, element):
        # Scroll the element into view to ensure it's interactable
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def fill_form(self, form_url, form_data):
        try:
            # Step 1: Load the form page
            self.driver.get(form_url)
            time.sleep(2)  # Wait for the page to fully load

            # Step 2: Get all form fields (input, textarea, select)
            form_fields = self.get_form_fields()

            # Step 3: Iterate over fields and fill them
            for field in form_fields:
                label_text = self.find_label_for_field(field)  # Find the associated label
                if label_text is None or 'cookie' in label_text.lower():  # Skip cookie-related fields
                    continue

                field_type = self.determine_field_type(label_text, field)  # Determine the field type

                # Ensure the field is interactable
                try:
                    self.scroll_into_view(field)
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(field))
                    self.fill_field(field, field_type, form_data)  # Fill the field with appropriate data
                except TimeoutException:
                    print(f"Field with label '{label_text}' is not interactable.")
                except ElementNotInteractableException:
                    print(f"Field with label '{label_text}' is not clickable.")

            # Step 4: Submit the form (assuming submit button is a <button> or <input type="submit">)
            submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit'] | //button[@type='submit']")

            # Scroll to and click the submit button
            self.scroll_into_view(submit_button)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(submit_button))
            submit_button.click()
            time.sleep(2)  # Wait for submission to complete

            return "Form submitted successfully!"
        except Exception as e:
            return f"Failed to submit form: {str(e)}"
        finally:
            self.driver.quit()


# Example usage
if __name__ == "__main__":
    # Set the path to your ChromeDriver
    driver_path = os.getenv("CHROME_DRIVER_PATH", "C:/Pascal/ChromeDriver/chromedriver-win64/chromedriver-win64/chromedriver.exe")

    # Initialize the SmartFormFiller
    form_filler = SmartFormFiller(driver_path)

    # Example form data, based on expected field types
    form_data = {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'company': 'Acme Inc.',
        'message': 'Hello, this is a test submission.',
        'phone': '1234567890'
    }

    # Fill and submit the form
    result = form_filler.fill_form('https://www.roboform.com/filling-test-all-fields', form_data)
    print(result)
