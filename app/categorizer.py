import re
import json

class EmailCategorizer:
    def __init__(self, config_file='app/config.json'):
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            return json.load(f)

    def categorize_email(self, email_subject, email_sender):
        for category, keywords in self.config['categories'].items():
            if any(re.search(keyword, email_subject, re.IGNORECASE) for keyword in keywords) or \
               any(re.search(keyword, email_sender, re.IGNORECASE) for keyword in keywords):
                return category
        return "uncategorized"

    def categorize_emails(self, emails):
        categorized_emails = {}
        for email in emails:
            email_subject = email['subject']
            email_sender = email['from']
            category = self.categorize_email(email_subject, email_sender)
            if category not in categorized_emails:
                categorized_emails[category] = []
            categorized_emails[category].append(email)
        return categorized_emails
