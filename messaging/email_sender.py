# email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:

    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient_email, subject, body):
        try:
            # Create the email
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            # Establish a connection with the SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            # Send the email
            server.sendmail(self.sender_email, recipient_email, msg.as_string())
            server.quit()
            return f"Email sent to {recipient_email}"
        except Exception as e:
            return f"Failed to send email: {str(e)}"


# Example usage
if __name__ == "__main__":
    email_sender = EmailSender("smtp.gmail.com", 587, "your-email@example.com", "your-password")
    result = email_sender.send_email("recipient@example.com", "Personalized Subject",
                                     "This is a personalized email body.")
    print(result)
