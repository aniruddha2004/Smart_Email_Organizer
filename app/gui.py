import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QLineEdit, QListWidget, QListWidgetItem, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from app.email_client import EmailClient
from app.categorizer import EmailCategorizer
from app.prioritizer import EmailPrioritizer


class EmailFetcher(QThread):
    emails_fetched = pyqtSignal(list)  # Signal to emit the fetched emails

    def __init__(self, email_client, num_emails, last_fetch_index):
        super().__init__()
        self.email_client = email_client
        self.num_emails = num_emails
        self.last_fetch_index = last_fetch_index

    def run(self):
        try:
            emails = self.email_client.fetch_emails(num_emails=self.num_emails, last_fetch_index=self.last_fetch_index)
            self.emails_fetched.emit(emails)  # Emit the fetched emails
        except Exception as e:
            print(f"Failed to fetch emails in thread: {str(e)}")


class EmailOrganizerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.email_client = None
        self.categorizer = EmailCategorizer()
        self.prioritizer = EmailPrioritizer()
        self.fetch_thread = None
        self.last_fetch_index = 0

    def initUI(self):
        self.setWindowTitle('Intelligent Email Organizer')
        self.setWindowIcon(QIcon('app/resources/icon.png'))
        self.setGeometry(100, 100, 1000, 700)
        
        # Load the stylesheet
        with open("app/resources/styles.qss", "r") as style_file:
            self.setStyleSheet(style_file.read())

        # Main layout
        layout = QVBoxLayout()

        # Email and Password Input Fields
        self.email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Status Label
        self.status_label = QLabel('Status: Not connected')
        layout.addWidget(self.status_label)

        # Connect Button
        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.connect_to_email)
        layout.addWidget(self.connect_button)

        # Number of Emails to Fetch Dropdown
        self.num_emails_label = QLabel('Number of Emails to Fetch:')
        self.num_emails_dropdown = QComboBox()
        self.num_emails_dropdown.addItems([str(i) for i in range(10, 151, 10)])  # Dropdown from 10 to 150
        layout.addWidget(self.num_emails_label)
        layout.addWidget(self.num_emails_dropdown)

        # Fetch Emails Button
        self.fetch_button = QPushButton('Fetch Emails')
        self.fetch_button.setEnabled(False)
        self.fetch_button.clicked.connect(self.start_fetching_emails)
        layout.addWidget(self.fetch_button)

        # Email List with Categories and Priority
        self.email_list = QListWidget()
        layout.addWidget(self.email_list)

        # Log Output Area
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        # Set the layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def connect_to_email(self):
        email = self.email_input.text()
        password = self.password_input.text()

        try:
            self.email_client = EmailClient(email=email, password=password)  # Pass GUI inputs
            self.email_client.login()
            self.status_label.setText('Status: Connected')
            self.log_output.append('Connected to email successfully.')
            self.fetch_button.setEnabled(True)
        except Exception as e:
            self.status_label.setText('Status: Connection Failed')
            self.log_output.append(f'Failed to connect: {str(e)}')

    def start_fetching_emails(self):
        if not self.email_client:
            self.log_output.append('Not connected to email.')
            return

        num_emails = int(self.num_emails_dropdown.currentText())

        self.fetch_thread = EmailFetcher(self.email_client, num_emails, self.last_fetch_index)
        self.fetch_thread.emails_fetched.connect(self.process_emails)
        self.fetch_thread.start()
        self.log_output.append(f'Fetching {num_emails} emails starting from index {self.last_fetch_index}...')

    def process_emails(self, emails):
        categorized_emails = self.categorizer.categorize_emails(emails)
        prioritized_emails = self.prioritizer.prioritize_emails(emails)
        self.display_emails(categorized_emails, prioritized_emails)

        # Update the last fetch index
        self.last_fetch_index += len(emails)

    def display_emails(self, categorized_emails, prioritized_emails):
        self.email_list.clear()
        self.log_output.append('Displaying categorized and prioritized emails.')

        for category, email_list in categorized_emails.items():
            category_item = QListWidgetItem(f"Category: {category}")
            category_item.setFont(QFont("Arial", 12, QFont.Bold))
            category_item.setTextAlignment(Qt.AlignCenter)
            self.email_list.addItem(category_item)

            for email in email_list:
                # Find the corresponding prioritized email
                priority = next((e['priority'] for e in prioritized_emails if e['subject'] == email['subject']), 'Unknown')
                email_item = QListWidgetItem(f"Subject: {email['subject']}\nFrom: {email['from']}\nPriority: {priority}")
                email_item.setToolTip(email['body'])
                email_item.setFont(QFont("Arial", 10))
                email_item.setTextAlignment(Qt.AlignLeft)
                self.email_list.addItem(email_item)

    def closeEvent(self, event):
        if self.email_client:
            self.email_client.close()
        if self.fetch_thread and self.fetch_thread.isRunning():
            self.fetch_thread.quit()
            self.fetch_thread.wait()


def main():
    app = QApplication(sys.argv)
    gui = EmailOrganizerGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
