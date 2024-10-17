# main.py
import time
from config.settings import Config
from config.logger import setup_logger
from crawler.web_crawler import WebCrawler
from crawler.company_discovery import CompanyDiscovery
from crawler.contact_method_recognition import ContactMethodRecognitionSelenium
from nlp.content_extraction import ContentExtractor
from nlp.message_personalization import MessagePersonalizer
from messaging.email_sender import EmailSender
from messaging.form_filler import SmartFormFiller  # Corrected class name here
from tracking.email_tracker import EmailTracker
from tracking.response_analyzer import ResponseAnalyzer

# Set up logger
logger = setup_logger(__name__)


def main():
    logger.info("Starting Market Engine System...")

    # Step 1: Discover Companies
    industry = "technology"  # Example industry, can be dynamic or based on user input
    query = f"{industry} companies"  # Use industry in search query
    discovery = CompanyDiscovery(query)

    logger.info(f"Discovering companies in the {industry} industry.")
    companies = discovery.discover_companies()

    # Check if any companies were discovered
    if not companies:
        logger.warning("No companies found. Exiting.")
        return

    logger.info(f"Discovered {len(companies)} companies.")

    # Step 2: Web Crawling and Contact Method Discovery
    recognizer = ContactMethodRecognitionSelenium()
    email_sender = EmailSender(Config.SMTP_SERVER, Config.SMTP_PORT, Config.SENDER_EMAIL, Config.SENDER_PASSWORD)
    form_filler = SmartFormFiller(Config.CHROME_DRIVER_PATH)  # Ensure correct instantiation of SmartFormFiller

    for company in companies:
        company_name = company['name']
        company_url = company['url']
        logger.info(f"Processing company: {company_name}, URL: {company_url}")

        # Initialize web crawler
        crawler = WebCrawler(company_url)
        crawler_links = crawler.extract_links()
        if not crawler_links:
            logger.warning(f"No links found for {company_name}. Skipping.")
            continue

        logger.info(f"Extracted {len(crawler_links)} links from {company_url}")

        # Recognize and extract contact methods (email or form)
        contact_methods = recognizer.recognize_methods(crawler_links)
        if not contact_methods.get('email') and not contact_methods.get('form'):
            logger.warning(f"No contact method found for {company_name}. Skipping.")
            continue

        # Step 3: Content Extraction and Message Personalization
        extractor = ContentExtractor(company_url)
        about_us_content = extractor.extract_about_us()
        if not about_us_content:
            logger.warning(f"No content found for {company_name} 'About Us' page. Using default messaging.")
            about_us_content = "We are a company focused on driving innovation."

        template = """
        Dear [Company Name],

        We are excited to present our AI assistant that could help [Company Name] achieve its goals of [mission/goals].
        """
        # personalizer = MessagePersonalizer(template, Config.LLM_API_KEY)
        # personalized_message = personalizer.personalize_message(company_name, about_us_content)
        # logger.info(f"Should have generated personalized message for {company_name}.")

        # Step 4: Message Delivery (Email or Form Submission)
        if contact_methods.get('email'):
            email = contact_methods['email']
            subject = f"AI Assistant for {company_name}"
            logger.info(f"Sending email to {company_name} at {email}.")
            result = email_sender.send_email("lavache78960@gmail.com", subject, template)
            logger.info(result)

        elif contact_methods.get('form'):
            form_url = contact_methods['form']
            form_data = {
                'name': 'Market Engine',
                'email': Config.SENDER_EMAIL,
                'message': template
            }
            logger.info(f"Filling form for {company_name} at {form_url}.")
            result = form_filler.fill_form(form_url, form_data)
            logger.info(result)

        time.sleep(2)  # Small delay between requests to avoid being flagged as spam

    # Step 5: Tracking Success Rates
    # tracker = EmailTracker(Config.SMTP_SERVER, Config.SMTP_PORT, Config.SENDER_EMAIL, Config.SENDER_PASSWORD)
    # analyzer = ResponseAnalyzer()

    """
    logger.info("Tracking email deliveries and responses.")
    for company in companies:
        if contact_methods.get('email'):
            delivery_status = tracker.check_email_delivery(contact_methods['email'])
            logger.info(f"Delivery status for {company['name']}: {delivery_status}")
            response = "Thank you for your message, we'll get back to you soon."  # Placeholder response
            classification = analyzer.classify_response(response)
            logger.info(f"Response classification for {company['name']}: {classification}")

    logger.info("Market Engine System Completed.")
    """

if __name__ == "__main__":
    main()
