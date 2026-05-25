from PyQt6.QtWidgets import *
import sys
from auth.auth import login_window


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow, QDialog { background-color: #4caf50; }
        QPushButton { background-color: #1565c0; color: white; border: none; padding: 5px 14px; }
    """)
    win = login_window()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
