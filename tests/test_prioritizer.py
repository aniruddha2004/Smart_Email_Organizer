import unittest
from app.prioritizer import EmailPrioritizer
from unittest.mock import patch

class TestEmailPrioritizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup EmailPrioritizer with a mock configuration file
        cls.prioritizer = EmailPrioritizer(config_file='app/config.json')

    def test_prioritize_email(self):
        # Test high priority based on subject
        subject = "Urgent: Complete the report"
        priority = self.prioritizer.prioritize_email(subject)
        self.assertEqual(priority, 'High Priority', "The email should be marked as 'High Priority'.")

        # Test normal priority
        subject = "Team meeting"
        priority = self.prioritizer.prioritize_email(subject)
        self.assertEqual(priority, 'Normal Priority', "The email should be marked as 'Normal Priority'.")

        # Test low priority with no matching keywords
        subject = "Weekly newsletter"
        priority = self.prioritizer.prioritize_email(subject)
        self.assertEqual(priority, 'Normal Priority', "The email should be marked as 'Normal Priority'.")

    def test_prioritize_emails(self):
        # Test prioritization of multiple emails
        emails = [
            {'subject': 'Urgent: Complete the report', 'from': 'manager@company.com'},
            {'subject': 'Team meeting', 'from': 'user@company.com'},
            {'subject': 'Weekly newsletter', 'from': 'newsletter@news.com'}
        ]
        prioritized_emails = self.prioritizer.prioritize_emails(emails)
        self.assertTrue(any(email['priority'] == 'High Priority' for email in prioritized_emails),
                        "There should be at least one 'High Priority' email.")
        self.assertTrue(any(email['priority'] == 'Normal Priority' for email in prioritized_emails),
                        "There should be at least one 'Normal Priority' email.")

if __name__ == '__main__':
    unittest.main()
