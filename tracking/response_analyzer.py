# response_analyzer.py
import re
import textblob
from textblob import TextBlob


class ResponseAnalyzer:

    def __init__(self):
        # Load any NLP models or configurations here if needed
        pass

    def classify_response(self, response_text):
        """
        Classifies the email response as automated or human based on content analysis.
        """
        # Define common patterns for automated responses (e.g., out-of-office, bounce-back)
        automated_patterns = [
            r"out of office",
            r"auto[-\s]?reply",
            r"bounce",
            r"failed to deliver",
            r"undeliverable",
            r"delivery failure",
            r"no longer with the company",
            r"moved to a different role",
            r"thank you for your email",
        ]

        for pattern in automated_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                return "Automated Response"

        # Perform sentiment analysis or other text analysis to determine authenticity
        blob = TextBlob(response_text)
        sentiment = blob.sentiment.polarity

        if sentiment >= 0.1:
            return "Positive Human Response"
        elif sentiment <= -0.1:
            return "Negative Human Response"
        else:
            return "Neutral Human Response"

    def extract_key_phrases(self, response_text):
        """
        Extracts key phrases from the response to identify actionable insights.
        """
        blob = TextBlob(response_text)
        return blob.noun_phrases


# Example usage
if __name__ == "__main__":
    analyzer = ResponseAnalyzer()
    response = """
    Hi, thank you for your email. Unfortunately, I am currently out of the office and will not be able to respond until next week.
    """

    classification = analyzer.classify_response(response)
    print(f"Response classified as: {classification}")

    key_phrases = analyzer.extract_key_phrases(response)
    print(f"Key phrases: {key_phrases}")
