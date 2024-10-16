import re
import nltk
from textblob import TextBlob

# Ensure necessary NLTK resources are available
nltk.download('punkt')

class ResponseAnalyzer:
    def __init__(self):
        pass

    def classify_response(self, response_text):
        automated_patterns = [
            r"out of office", r"auto[-\s]?reply", r"bounce", r"failed to deliver",
            r"undeliverable", r"delivery failure", r"no longer with the company",
            r"moved to a different role", r"thank you for your email",
        ]
        for pattern in automated_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                return "Automated Response"

        # Perform sentiment analysis
        blob = TextBlob(response_text)
        sentiment = blob.sentiment.polarity

        if sentiment >= 0.1:
            return "Positive Human Response"
        elif sentiment <= -0.1:
            return "Negative Human Response"
        else:
            return "Neutral Human Response"

    def extract_key_phrases(self, response_text):
        blob = TextBlob(response_text)
        return blob.noun_phrases


# Example usage
if __name__ == "__main__":
    analyzer = ResponseAnalyzer()
    response = """
    This is surely spam, if you are human send me a message back.
    """

    classification = analyzer.classify_response(response)
    print(f"Response classified as: {classification}")

    key_phrases = analyzer.extract_key_phrases(response)
    print(f"Key phrases: {key_phrases}")
