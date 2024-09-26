import re
import json

class EmailPrioritizer:
    def __init__(self, config_file='app/config.json'):
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            return json.load(f)

    def prioritize_email(self, email_subject):
        for keyword in self.config['priority_keywords']:
            if re.search(keyword, email_subject, re.IGNORECASE):
                return "High Priority"
        return "Normal Priority"

    def prioritize_emails(self, emails):
        prioritized_emails = []
        for email in emails:
            priority = self.prioritize_email(email['subject'])
            email['priority'] = priority
            prioritized_emails.append(email)
        return prioritized_emails
