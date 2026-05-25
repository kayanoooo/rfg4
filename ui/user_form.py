from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton
)


class UserFormDialog(QDialog):
    def __init__(self, parent, roles, user=None):
        super().__init__(parent)
        self.setWindowTitle('Новый пользователь' if user is None else 'Редактировать пользователя')
        self.resize(360, 240)

        main = QVBoxLayout(self)
        grid = QGridLayout()

        self.lineEditUsername = QLineEdit()
        self.lineEditPassword = QLineEdit()
        self.lineEditFullName = QLineEdit()
        self.lineEditContact = QLineEdit()
        self.comboBoxRole = QComboBox()

        for role in roles:
            self.comboBoxRole.addItem(role['role_name'], role['id'])

        for i, (lbl, w) in enumerate([
            ('Логин *',  self.lineEditUsername),
            ('Пароль *', self.lineEditPassword),
            ('ФИО *',    self.lineEditFullName),
            ('Контакт',  self.lineEditContact),
            ('Роль *',   self.comboBoxRole),
        ]):
            grid.addWidget(QLabel(lbl), i, 0)
            grid.addWidget(w, i, 1)
        main.addLayout(grid)

        btns = QHBoxLayout()
        btns.addStretch()
        self.pushButtonSave = QPushButton('Сохранить')
        self.pushButtonCancel = QPushButton('Отмена')
        btns.addWidget(self.pushButtonSave)
        btns.addWidget(self.pushButtonCancel)
        main.addLayout(btns)

        if user:
            self.lineEditUsername.setText(user.get('username', ''))
            self.lineEditPassword.setText(user.get('password', ''))
            self.lineEditFullName.setText(user.get('full_name', ''))
            self.lineEditContact.setText(user.get('contact_info', ''))
            idx = self.comboBoxRole.findData(user.get('role_id'))
            if idx >= 0:
                self.comboBoxRole.setCurrentIndex(idx)

        self.pushButtonSave.clicked.connect(self.accept)
        self.pushButtonCancel.clicked.connect(self.reject)

    def get_data(self):
        return (
            self.lineEditUsername.text().strip(),
            self.lineEditPassword.text().strip(),
            self.lineEditFullName.text().strip(),
            self.lineEditContact.text().strip(),
            self.comboBoxRole.currentData(),
        )

    def validate(self):
        username, password, full_name, _, role_id = self.get_data()
        if not username:
            return False, 'Введите логин'
        if not password:
            return False, 'Введите пароль'
        if not full_name:
            return False, 'Введите ФИО'
        if role_id is None:
            return False, 'Выберите роль'
        return True, ''
