# Intelligent Email Organizer

## Overview
The Intelligent Email Organizer is a Python-based application that categorizes, prioritizes, and organizes your emails automatically. It provides a user-friendly GUI built with PyQt5 for easy email management, featuring automated actions and flexible email fetching capabilities.

## Features
- **Email Categorization**: Automatically categorize emails into predefined categories like Work, Personal, Promotions, etc.
- **Email Prioritization**: Assign priority levels (e.g., High Priority, Normal Priority) based on email content.
- **Incremental Email Fetching**: Fetch emails in customizable batches, avoiding overload by limiting the number of emails fetched in each session.
- **Automated Actions**: Mark emails as read, delete, or archive based on rules.
- **GUI with PyQt5**: Easy-to-use interface for email management.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone [https://github.com/aniruddha2004/Smart_Email_Organizer.git](https://github.com/aniruddha2004/Smart_Email_Organizer.git)
   cd Smart_Email_Organizer
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt 
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt 
   ```

4. **Configuration:**

   - Edit the config.json file under app/ to add your IMAP and SMTP server details if required.
   - Alternatively, you can enter your email and password directly in the GUI during runtime.

## Usage

1. **Run the Application:**

   ```bash
   python main.py
   ```

2. **GUI Operations:**

   - Enter your email and password in the GUI.
   - Click the `Connect` button to log in.
   - Use the dropdown to select the number of emails to fetch.
   - Click the `Fetch Emails` button to start fetching and organizing your emails.

## Testing

1. **Run Unit Tests:**

   ```bash
   pytest tests/
   ```

## Dependencies

- Python 3.7+
- PyQt5
- imaplib, smtplib
- email
- json

## Contributing

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -am 'Add new feature').
4. Push to the branch (git push origin feature-branch).
5. Create a new Pull Request.


## Author

**Aniruddha Ghosh**

For any issues or feature requests, please contact by [aniruddhag2004@gmail.com](mailto:aniruddhag2004@gmail.com)
