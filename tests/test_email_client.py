import unittest
from app.email_client import EmailClient
from unittest.mock import patch, MagicMock

class TestEmailClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup EmailClient with a mock configuration file
        cls.email_client = EmailClient(config_file='app/config.json')

    def test_login(self):
        # Test successful login to IMAP and SMTP
        with patch.object(self.email_client.imap, 'login', return_value="OK"):
            with patch.object(self.email_client.smtp, 'login', return_value="OK"):
                try:
                    self.email_client.login()
                    login_success = True
                except Exception:
                    login_success = False
                self.assertTrue(login_success, "Login should work with correct credentials.")

    def test_fetch_emails(self):
        # Test fetching emails with mock data
        with patch.object(self.email_client.imap, 'search', return_value=("OK", [b"1 2 3"])):
            with patch.object(self.email_client.imap, 'fetch', return_value=("OK", [(b"1", b"Mock Email Data")])):
                emails = self.email_client.fetch_emails()
                self.assertIsInstance(emails, list, "Fetched emails should be a list.")
                self.assertGreaterEqual(len(emails), 1, "There should be at least one email fetched.")

    def test_send_email(self):
        # Test sending an email
        with patch.object(self.email_client.smtp, 'send_message', return_value="OK") as mock_send:
            try:
                self.email_client.send_email("test@example.com", "Test Subject", "Test Body")
                send_success = True
            except Exception:
                send_success = False
            self.assertTrue(send_success, "Sending email should not raise an exception.")
            mock_send.assert_called_once()

    @classmethod
    def tearDownClass(cls):
        # Clean up after tests
        cls.email_client.close()

if __name__ == '__main__':
    unittest.main()
