import sys
from PyQt5.QtWidgets import QApplication
from app.gui import EmailOrganizerGUI

def main():
    # Create the QApplication instance
    app = QApplication(sys.argv)

    # Create and show the main window
    gui = EmailOrganizerGUI()
    gui.show()

    # Execute the application's main loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
