# test_nlp.py
import unittest
from nlp.content_extraction import ContentExtractor
from nlp.message_personalization import MessagePersonalizer


class TestContentExtractor(unittest.TestCase):

    def test_extract_about_us(self):
        extractor = ContentExtractor("https://example.com")
        content = extractor.extract_about_us()
        self.assertTrue(isinstance(content, str))
        self.assertGreater(len(content), 0, "No content extracted from about us page")


class TestMessagePersonalizer(unittest.TestCase):

    def test_personalize_message(self):
        template = """
        Dear [Company Name],

        We are excited to present our AI assistant that could help [Company Name] achieve its goals.
        """
        personalizer = MessagePersonalizer(template, "fake-api-key")
        message = personalizer.personalize_message("Test Corp", "We are a company focused on innovation.")
        self.assertIn("Test Corp", message)
        self.assertIn("innovation", message)


if __name__ == "__main__":
    unittest.main()
