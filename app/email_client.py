import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json


class EmailClient:
    def __init__(self, email=None, password=None, config_file='app/config.json'):
        # Load the configuration file
        self.config = self.load_config(config_file)
        self.imap_server = self.config['imap_server']
        self.imap_port = self.config.get('imap_port', 993)  # Use default port 993 for IMAP SSL
        self.smtp_server = self.config['smtp_server']
        self.smtp_port = self.config['smtp_port']
        self.email_address = email or self.config['email']
        self.password = password or self.config['password']
        self.imap = None
        self.smtp = None

    def load_config(self, config_file):
        """Load configuration settings from a JSON file."""
        with open(config_file, 'r') as f:
            return json.load(f)

    def login(self):
        """Login to IMAP and SMTP servers using the provided credentials."""
        # Initialize the IMAP client and connect to the server
        self.imap = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        try:
            # Attempt to log in
            self.imap.login(self.email_address, self.password)
            print("IMAP Login successful")
        except imaplib.IMAP4.error as e:
            print(f"Failed to login to IMAP: {e}")
            raise

        # Initialize the SMTP client and connect to the server
        self.smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.smtp.starttls()  # Secure the SMTP connection
        try:
            self.smtp.login(self.email_address, self.password)
            print("SMTP Login successful")
        except smtplib.SMTPAuthenticationError as e:
            print(f"Failed to login to SMTP: {e}")
            raise

    def fetch_emails(self, folder='inbox', num_emails=50, last_fetch_index=0):
        """Fetch emails from the specified folder and return a list of email data."""
        try:
            self.imap.select(folder)
            status, messages = self.imap.search(None, 'ALL')
            email_ids = messages[0].split()
            total_emails = len(email_ids)
            emails_to_fetch = min(num_emails, total_emails - last_fetch_index)

            emails = []
            for i in range(last_fetch_index, last_fetch_index + emails_to_fetch):
                e_id = email_ids[i]
                status, msg_data = self.imap.fetch(e_id, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg['subject']
                        from_address = msg['from']

                        # Try to decode the email body safely
                        body = self.get_email_body(msg)

                        emails.append({
                            'subject': subject,
                            'from': from_address,
                            'body': body
                        })
            return emails
        except Exception as e:
            print(f"Failed to fetch emails: {str(e)}")
            return []

    def get_email_body(self, msg):
        """Extract and decode the email body from the email message object."""
        body = None
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                # Look for the email body (text/plain or text/html)
                if "attachment" not in content_disposition:
                    if content_type == "text/plain" or content_type == "text/html":
                        try:
                            body = part.get_payload(decode=True).decode(errors='ignore')
                        except Exception as e:
                            print(f"Failed to decode part: {e}")
        else:
            # If the email is not multipart, get the payload directly
            try:
                body = msg.get_payload(decode=True).decode(errors='ignore')
            except Exception as e:
                print(f"Failed to decode singlepart message: {e}")

        return body if body else "No content available"

    def send_email(self, to_address, subject, body):
        """Send an email to the specified address with the given subject and body."""
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        self.smtp.send_message(msg)

    def close(self):
        """Logout from IMAP and quit SMTP connections."""
        if self.imap:
            self.imap.logout()
        if self.smtp:
            self.smtp.quit()


if __name__ == '__main__':
    # Example usage of the EmailClient class
    client = EmailClient(config_file='app/config.json')

    try:
        client.login()
        emails = client.fetch_emails()
        print(f"Fetched {len(emails)} emails.")
        for email in emails:
            print(f"Subject: {email['subject']}")
            print(f"From: {email['from']}")
            print(f"Body: {email['body']}\n")
    finally:
        client.close()
