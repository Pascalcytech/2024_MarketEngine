# settings.py
import os

class Config:
    # Web Crawler settings
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

    # SMTP Settings
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = os.getenv("SMTP_PORT", 587)
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your-email@gmail.com")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your-password")

    # LLM API settings (e.g., GPT-4)
    LLM_API_KEY = os.getenv("LLM_API_KEY", "")

    # Web Form Automation (Selenium) settings
    CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", "")

    # Email tracking API (e.g., SendGrid)
    EMAIL_TRACKING_API_KEY = os.getenv("EMAIL_TRACKING_API_KEY", "your-sendgrid-api-key")

    # Database settings
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_NAME = os.getenv("DB_NAME", "market_engine_db")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "market_engine.log")

# Usage Example
config = Config()
