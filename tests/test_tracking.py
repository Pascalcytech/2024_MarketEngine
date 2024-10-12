# test_tracking.py
import unittest
from tracking.email_tracker import EmailTracker
from tracking.response_analyzer import ResponseAnalyzer
from unittest.mock import patch


class TestEmailTracker(unittest.TestCase):

    @patch('smtplib.SMTP')
    def test_check_email_delivery(self, mock_smtp):
        tracker = EmailTracker("smtp.gmail.com", 587, "sender@example.com", "password")
        result = tracker.check_email_delivery("recipient@example.com")
        self.assertIn("valid", result)


class TestResponseAnalyzer(unittest.TestCase):

    def test_classify_response(self):
        analyzer = ResponseAnalyzer()
        automated_response = "I am currently out of the office."
        human_response = "Thank you for your message."

        self.assertEqual(analyzer.classify_response(automated_response), "Automated Response")
        self.assertEqual(analyzer.classify_response(human_response), "Positive Human Response")

    def test_extract_key_phrases(self):
        analyzer = ResponseAnalyzer()
        response = "We are interested in your AI solution."
        key_phrases = analyzer.extract_key_phrases(response)
        self.assertIn("AI solution", key_phrases)


if __name__ == "__main__":
    unittest.main()
