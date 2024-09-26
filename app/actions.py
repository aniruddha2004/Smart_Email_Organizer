# app/actions.py
from app.email_client import EmailClient

class EmailActions:
    def __init__(self, email_client):
        self.email_client = email_client

    def mark_as_read(self, email_id):
        try:
            self.email_client.imap.store(email_id, '+FLAGS', '\\Seen')
            return True
        except Exception as e:
            print(f"Failed to mark as read: {e}")
            return False

    def delete_email(self, email_id):
        try:
            self.email_client.imap.store(email_id, '+FLAGS', '\\Deleted')
            self.email_client.imap.expunge()
            return True
        except Exception as e:
            print(f"Failed to delete email: {e}")
            return False

    def archive_email(self, email_id):
        try:
            self.email_client.imap.copy(email_id, '[Gmail]/All Mail')
            self.delete_email(email_id)  # Optionally delete from Inbox
            return True
        except Exception as e:
            print(f"Failed to archive email: {e}")
            return False
