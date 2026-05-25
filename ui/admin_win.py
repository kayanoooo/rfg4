from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QStatusBar
)


class Ui_AdminWindow:
    def setupUi(self, AdminWindow):
        AdminWindow.resize(1200, 800)
        AdminWindow.setWindowTitle('Пиццерия — Администратор')

        self.centralwidget = QWidget(AdminWindow)
        AdminWindow.setCentralWidget(self.centralwidget)
        main = QVBoxLayout(self.centralwidget)

        top = QHBoxLayout()
        self.labelCurrentUser = QLabel('Администратор')
        self.pushButtonLogout = QPushButton('Выйти')
        top.addWidget(QLabel('Панель администратора'))
        top.addStretch()
        top.addWidget(self.labelCurrentUser)
        top.addWidget(self.pushButtonLogout)
        main.addLayout(top)

        self.tabWidgetMain = QTabWidget()
        main.addWidget(self.tabWidgetMain)

        # --- Пользователи ---
        tab = QWidget()
        layout = QVBoxLayout(tab)
        btns = QHBoxLayout()
        self.pushButtonAddUser    = QPushButton('Добавить')
        self.pushButtonEditUser   = QPushButton('Редактировать')
        self.pushButtonDeleteUser = QPushButton('Удалить')
        self.pushButtonRefreshUsers = QPushButton('Обновить')
        for b in (self.pushButtonAddUser, self.pushButtonEditUser,
                  self.pushButtonDeleteUser):
            btns.addWidget(b)
        btns.addStretch()
        btns.addWidget(self.pushButtonRefreshUsers)
        layout.addLayout(btns)
        self.tableWidgetUsers = QTableWidget(0, 6)
        self.tableWidgetUsers.setHorizontalHeaderLabels(['ID', 'Логин', 'Пароль', 'ФИО', 'Контакт', 'Роль'])
        self.tableWidgetUsers.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableWidgetUsers.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.tableWidgetUsers)
        self.tabWidgetMain.addTab(tab, 'Пользователи')

        # --- Товары ---
        tab2 = QWidget()
        layout2 = QVBoxLayout(tab2)
        btns2 = QHBoxLayout()
        self.pushButtonAddItem      = QPushButton('Добавить')
        self.pushButtonDeleteItem   = QPushButton('Удалить выбранный')
        self.pushButtonRefreshItems = QPushButton('Обновить')
        btns2.addWidget(self.pushButtonAddItem)
        btns2.addWidget(self.pushButtonDeleteItem)
        btns2.addStretch()
        btns2.addWidget(self.pushButtonRefreshItems)
        layout2.addLayout(btns2)
        from PyQt6.QtWidgets import QScrollArea
        self.scrollAreaItems = QScrollArea()
        self.scrollAreaItems.setWidgetResizable(True)
        layout2.addWidget(self.scrollAreaItems)
        self.tabWidgetMain.addTab(tab2, 'Товары')

        # --- Заказы ---
        tab_ord = QWidget()
        layout_ord = QVBoxLayout(tab_ord)
        btns_ord = QHBoxLayout()
        self.pushButtonRefreshOrders = QPushButton('Обновить')
        btns_ord.addStretch()
        btns_ord.addWidget(self.pushButtonRefreshOrders)
        layout_ord.addLayout(btns_ord)
        self.tableWidgetOrders = QTableWidget(0, 8)
        self.tableWidgetOrders.setHorizontalHeaderLabels(
            ['ID', 'Клиент', 'Дата', 'Тип', 'Адрес', 'Комментарий', 'Сумма', 'Статус'])
        self.tableWidgetOrders.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout_ord.addWidget(self.tableWidgetOrders)
        self.tabWidgetMain.addTab(tab_ord, 'Заказы')

        # --- Роли ---
        tab3 = QWidget()
        layout3 = QVBoxLayout(tab3)
        btns3 = QHBoxLayout()
        self.pushButtonRefreshRoles = QPushButton('Обновить')
        btns3.addStretch()
        btns3.addWidget(self.pushButtonRefreshRoles)
        layout3.addLayout(btns3)
        self.tableWidgetRoles = QTableWidget(0, 2)
        self.tableWidgetRoles.setHorizontalHeaderLabels(['ID', 'Название роли'])
        self.tableWidgetRoles.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout3.addWidget(self.tableWidgetRoles)
        self.tabWidgetMain.addTab(tab3, 'Роли')

        self.statusbar = QStatusBar(AdminWindow)
        AdminWindow.setStatusBar(self.statusbar)
