from PyQt6.QtWidgets import *
from ui.login_win import Ui_MainWindow  
from database.db import check_login
from users.client import client_window
from users.guest import guest_window
from users.admin import admin_window
from users.manager import manager_window


            
class login_window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_enter.clicked.connect(self.login)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_guest.clicked.connect(self.open_guest)

    def login(self):
        username = self.lineEdit_login.text().strip()
        password = self.lineEdit_password.text().strip()
        if not username or not password:
            QMessageBox.warning(self, 'error', 'enter login or pass')
            return

        user = check_login(username, password)
        if not user:
            QMessageBox.warning(self, 'error', 'incorrect login or pass')
            return
        
        role = user['role']
        if role == 'client':
            self.win = client_window(user['id'], user['full_name'])
        elif role == 'admin':
            self.win = admin_window(user['full_name'])
        elif role == 'manager':
            self.win = manager_window(user['full_name'])
        else:
            QMessageBox.warning(self, 'error', f'{role} dosent exists')
            return
        
        self.win.show()
        self.close()


    def open_guest(self):
        self.win = guest_window()
        self.win.show()
        self.close()
                  




    
