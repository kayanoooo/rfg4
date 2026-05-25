from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QComboBox, QStatusBar
)
from ui.order_form import ORDER_STATUSES


class Ui_ManagerWindow:
    def setupUi(self, Window):
        Window.resize(1100, 700)
        Window.setWindowTitle('Пиццерия — Менеджер')

        self.centralwidget = QWidget(Window)
        Window.setCentralWidget(self.centralwidget)
        main = QVBoxLayout(self.centralwidget)

        top = QHBoxLayout()
        self.labelCurrentUser = QLabel('Менеджер')
        self.pushButtonLogout = QPushButton('Выйти')
        top.addWidget(QLabel('Управление заказами'))
        top.addStretch()
        top.addWidget(self.labelCurrentUser)
        top.addWidget(self.pushButtonLogout)
        main.addLayout(top)

        ctrl = QHBoxLayout()
        self.comboStatus = QComboBox()
        self.comboStatus.addItems(ORDER_STATUSES)
        self.pushButtonApply = QPushButton('Применить статус')
        self.pushButtonRefresh = QPushButton('Обновить')
        ctrl.addWidget(QLabel('Новый статус:'))
        ctrl.addWidget(self.comboStatus)
        ctrl.addWidget(self.pushButtonApply)
        ctrl.addStretch()
        ctrl.addWidget(self.pushButtonRefresh)
        main.addLayout(ctrl)

        self.tableWidgetOrders = QTableWidget(0, 8)
        self.tableWidgetOrders.setHorizontalHeaderLabels(
            ['ID', 'Клиент', 'Дата', 'Тип', 'Адрес', 'Комментарий', 'Сумма', 'Статус'])
        self.tableWidgetOrders.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableWidgetOrders.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        main.addWidget(self.tableWidgetOrders)

        self.statusbar = QStatusBar(Window)
        Window.setStatusBar(self.statusbar)
