import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration from environment variables
GMAIL_USER = os.getenv('GMAIL_USER', 'sthefanyshanebautista@gmail.com')  # Set your email
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD', 'lise fjfs tpyh plqf')  # Set your app password

def send_email(to_email, subject, message):
    """Send an email using Gmail."""
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully!")
            return "Email sent successfully."
    except smtplib.SMTPAuthenticationError:
        print("Authentication error. Check your credentials.")
        return "Failed to send email: Authentication error."
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        return f"Failed to send email: {e}"
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Failed to send email: {e}"

# Example usage:
if __name__ == "__main__":
    recipient = "recipient@example.com"
    subject = "Test Email"
    body = "Hello! This is a test email sent using Python."
    print(send_email(recipient, subject, body))
