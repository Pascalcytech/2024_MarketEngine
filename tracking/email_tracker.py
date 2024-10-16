# email_tracker.py
import smtplib
from email.utils import parseaddr
import requests


class EmailTracker:

    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def check_email_delivery(self, recipient_email):
        try:
            # Establish a connection with the SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            # Verify if the email address exists using VRFY (limited support)
            code, message = server.verify(recipient_email)
            server.quit()

            if code == 250:
                return f"Email address {recipient_email} is valid."
            else:
                return f"Failed to verify email address: {recipient_email} - {message.decode()}"
        except Exception as e:
            return f"Error checking delivery: {str(e)}"

    def track_via_api(self, message_id, api_key, service="sendgrid"):
        # Example integration with a third-party email tracking service
        if service == "sendgrid":
            url = f"https://api.sendgrid.com/v3/messages/{message_id}"
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            response = requests.get(url, headers=headers)
            return response.json()
        else:
            return "Unsupported tracking service."


# Example usage
if __name__ == "__main__":
    tracker = EmailTracker("smtp.gmail.com", 587, "lavache78960@gmail.com", "password")
    delivery_status = tracker.check_email_delivery("pascal.kau8@gmail.com")
    print(delivery_status)

    # Example for API-based tracking
    message_id = "12345"
    api_key = "your-api-key"
    status = tracker.track_via_api(message_id, api_key, service="sendgrid")
    print(status)
