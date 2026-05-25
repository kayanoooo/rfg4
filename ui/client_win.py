from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QScrollArea, QStatusBar
)


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.resize(960, 720)
        MainWindow.setWindowTitle('Пиццерия — Клиент')

        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        main = QVBoxLayout(self.centralwidget)

        # Top bar
        top_frame = QWidget()
        top = QHBoxLayout(top_frame)
        top.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel('Клиент:')
        self.label_currentuser = QLabel('Клиент')
        self.pushButton_backlogin = QPushButton('К авторизации')
        top.addWidget(self.label)
        top.addWidget(self.label_currentuser)
        top.addStretch()
        top.addWidget(self.pushButton_backlogin)
        main.addWidget(top_frame)

        # Tabs
        self.tabWidget = QTabWidget()
        main.addWidget(self.tabWidget)

        # --- Menu tab ---
        self.tabMenu = QWidget()
        menu_layout = QVBoxLayout(self.tabMenu)
        menu_btn_row = QHBoxLayout()
        self.pushButton_refresh = QPushButton('Обновить меню')
        menu_btn_row.addWidget(self.pushButton_refresh)
        menu_btn_row.addStretch()
        menu_layout.addLayout(menu_btn_row)
        self.scrollArea_menu = QScrollArea()
        self.scrollArea_menu.setWidgetResizable(True)
        menu_layout.addWidget(self.scrollArea_menu)
        self.tabWidget.addTab(self.tabMenu, 'Меню')

        # --- Orders tab ---
        self.tabOrders = QWidget()
        orders_layout = QVBoxLayout(self.tabOrders)
        order_btn_row = QHBoxLayout()
        self.pushButtonAddOrder = QPushButton('Новый заказ')
        self.pushButtonEditOrder = QPushButton('Редактировать')
        self.pushButtonDeleteOrder = QPushButton('Удалить')
        self.pushButtonRefreshOrders = QPushButton('Обновить')
        order_btn_row.addWidget(self.pushButtonAddOrder)
        order_btn_row.addWidget(self.pushButtonEditOrder)
        order_btn_row.addWidget(self.pushButtonDeleteOrder)
        order_btn_row.addStretch()
        order_btn_row.addWidget(self.pushButtonRefreshOrders)
        orders_layout.addLayout(order_btn_row)
        self.tableWidgetOrders = QTableWidget(0, 7)
        self.tableWidgetOrders.setHorizontalHeaderLabels(
            ['ID', 'Дата', 'Тип', 'Адрес', 'Комментарий', 'Сумма', 'Статус'])
        self.tableWidgetOrders.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableWidgetOrders.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        orders_layout.addWidget(self.tableWidgetOrders)
        self.tabWidget.addTab(self.tabOrders, 'Мои заказы')

        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
