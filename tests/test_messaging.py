# test_messaging.py
import unittest
from messaging.email_sender import EmailSender
from messaging.form_filler import FormFiller
from unittest.mock import patch


class TestEmailSender(unittest.TestCase):

    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        email_sender = EmailSender("smtp.gmail.com", 587, "sender@example.com", "password")
        result = email_sender.send_email("recipient@example.com", "Test Subject", "Test Body")
        self.assertIn("Email sent", result)


class TestFormFiller(unittest.TestCase):

    @patch('selenium.webdriver.Chrome')
    def test_fill_form(self, mock_driver):
        form_filler = FormFiller("/path/to/chromedriver")
        form_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'message': 'Hello, this is a test.'
        }
        result = form_filler.fill_form('https://example.com/contact', form_data)
        self.assertIn("Form submitted", result)


if __name__ == "__main__":
    unittest.main()
