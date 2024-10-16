from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailSender:

    def __init__(self, sendgrid_api_key, sender_email):
        self.sendgrid_api_key = sendgrid_api_key
        self.sender_email = sender_email

    def send_email(self, recipient_email, subject, body):
        try:
            # Create the email using SendGrid's Mail object
            message = Mail(
                from_email=self.sender_email,
                to_emails=recipient_email,
                subject=subject,
                plain_text_content=body
            )

            # Send the email via SendGrid API
            sg = SendGridAPIClient(self.sendgrid_api_key)
            response = sg.send(message)

            # Return a success message
            return f"Email sent to {recipient_email}, Status Code: {response.status_code}"
        except Exception as e:
            return f"Failed to send email: {str(e)}"


# Example usage
if __name__ == "__main__":
    sendgrid_api_key = ""
    email_sender = EmailSender(sendgrid_api_key, "pascal.kau@cyje.fr")
    result = email_sender.send_email("lavache78960@gmail.com", "Test of SendGrid email sender",
                                     "This is a personalized email body sent via SendGrid.")
    print(result)
