import unittest
from app.categorizer import EmailCategorizer
from unittest.mock import patch

class TestEmailCategorizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup EmailCategorizer with a mock configuration file
        cls.categorizer = EmailCategorizer(config_file='app/config.json')

    def test_categorize_email(self):
        # Test categorization based on subject
        subject = "Meeting with project team"
        sender = "user@company.com"
        category = self.categorizer.categorize_email(subject, sender)
        self.assertEqual(category, 'work', "The category should be 'work' for a work-related email.")

        # Test categorization based on sender
        subject = "Family gathering"
        sender = "family@family.com"
        category = self.categorizer.categorize_email(subject, sender)
        self.assertEqual(category, 'personal', "The category should be 'personal' for a family email.")

        # Test categorization with unmatched keywords
        subject = "Unknown email content"
        sender = "unknown@unknown.com"
        category = self.categorizer.categorize_email(subject, sender)
        self.assertEqual(category, 'uncategorized', "The category should be 'uncategorized' for unmatched emails.")

    def test_categorize_emails(self):
        # Test categorization of multiple emails
        emails = [
            {'subject': 'Meeting with project team', 'from': 'user@company.com'},
            {'subject': 'Family gathering', 'from': 'family@family.com'},
            {'subject': 'Big sale today!', 'from': 'promotions@shop.com'}
        ]
        categorized_emails = self.categorizer.categorize_emails(emails)
        self.assertIn('work', categorized_emails, "Emails should be categorized as 'work'.")
        self.assertIn('personal', categorized_emails, "Emails should be categorized as 'personal'.")
        self.assertIn('promotions', categorized_emails, "Emails should be categorized as 'promotions'.")

if __name__ == '__main__':
    unittest.main()
