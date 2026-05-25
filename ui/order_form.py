from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QSpinBox, QHeaderView
)

ORDER_TYPES = ['В зале', 'Доставка', 'Навынос']
ORDER_STATUSES = ['Ожидает приготовления', 'Готовится', 'Готов', 'Доставляется', 'Выдан', 'Отменён']


class OrderFormDialog(QDialog):
    def __init__(self, parent, menu_items, order=None, existing_items=None,
                 is_admin=False, users=None):
        super().__init__(parent)
        self.is_admin = is_admin
        self.setWindowTitle('Новый заказ' if order is None else 'Редактировать заказ')
        self.resize(640, 540)

        main = QVBoxLayout(self)
        grid = QGridLayout()
        r = 0

        self.comboUser = QComboBox()
        if is_admin and users:
            for u in users:
                self.comboUser.addItem(f"{u['full_name']} ({u['username']})", u['id'])
            grid.addWidget(QLabel('Клиент *'), r, 0)
            grid.addWidget(self.comboUser, r, 1)
            r += 1
            if order:
                idx = self.comboUser.findData(order.get('user_id'))
                if idx >= 0:
                    self.comboUser.setCurrentIndex(idx)

        self.comboOrderType = QComboBox()
        self.comboOrderType.addItems(ORDER_TYPES)
        grid.addWidget(QLabel('Тип заказа *'), r, 0)
        grid.addWidget(self.comboOrderType, r, 1)
        r += 1

        self.labelAddress = QLabel('Адрес доставки *')
        self.lineEditAddress = QLineEdit()
        grid.addWidget(self.labelAddress, r, 0)
        grid.addWidget(self.lineEditAddress, r, 1)
        r += 1

        grid.addWidget(QLabel('Комментарий'), r, 0)
        self.lineEditComment = QLineEdit()
        grid.addWidget(self.lineEditComment, r, 1)
        r += 1

        self.labelStatus = QLabel('Статус')
        self.comboStatus = QComboBox()
        self.comboStatus.addItems(ORDER_STATUSES)
        grid.addWidget(self.labelStatus, r, 0)
        grid.addWidget(self.comboStatus, r, 1)
        self.labelStatus.setVisible(is_admin)
        self.comboStatus.setVisible(is_admin)

        main.addLayout(grid)
        main.addWidget(QLabel('Состав заказа:'))

        self.tableItems = QTableWidget(len(menu_items), 3)
        self.tableItems.setHorizontalHeaderLabels(['Позиция', 'Цена', 'Кол-во'])
        self.tableItems.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tableItems.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        qty_map = {it['item_id']: it['quantity'] for it in (existing_items or [])}
        self._spinners = []
        for i, item in enumerate(menu_items):
            self.tableItems.setItem(i, 0, QTableWidgetItem(item['name']))
            self.tableItems.setItem(i, 1, QTableWidgetItem(f"{float(item['price']):.2f}"))
            spin = QSpinBox()
            spin.setRange(0, 99)
            spin.setValue(qty_map.get(item['item_id'], 0))
            self.tableItems.setCellWidget(i, 2, spin)
            self._spinners.append((item, spin))

        main.addWidget(self.tableItems)

        btns = QHBoxLayout()
        btns.addStretch()
        self.pushButtonSave = QPushButton('Сохранить')
        self.pushButtonCancel = QPushButton('Отмена')
        btns.addWidget(self.pushButtonSave)
        btns.addWidget(self.pushButtonCancel)
        main.addLayout(btns)

        if order:
            idx = self.comboOrderType.findText(order.get('order_type', ''))
            if idx >= 0:
                self.comboOrderType.setCurrentIndex(idx)
            self.lineEditAddress.setText(order.get('delivery_address') or '')
            self.lineEditComment.setText(order.get('customer_comment') or '')
            if is_admin:
                idx = self.comboStatus.findText(order.get('status', ''))
                if idx >= 0:
                    self.comboStatus.setCurrentIndex(idx)

        self.comboOrderType.currentTextChanged.connect(
            lambda t: (self.labelAddress.setVisible(t == 'Доставка'),
                       self.lineEditAddress.setVisible(t == 'Доставка')))
        self.comboOrderType.currentTextChanged.emit(self.comboOrderType.currentText())

        self.pushButtonSave.clicked.connect(self.accept)
        self.pushButtonCancel.clicked.connect(self.reject)

    def get_data(self):
        order_type = self.comboOrderType.currentText()
        address = self.lineEditAddress.text().strip() if order_type == 'Доставка' else ''
        comment = self.lineEditComment.text().strip()
        status = self.comboStatus.currentText() if self.is_admin else 'Ожидает приготовления'
        user_id = self.comboUser.currentData() if self.comboUser.count() else None
        items = [(item, spin.value()) for item, spin in self._spinners if spin.value() > 0]
        return order_type, address, comment, status, items, user_id

    def validate(self):
        order_type, address, _, _, items, _ = self.get_data()
        if order_type == 'Доставка' and not address:
            return False, 'Укажите адрес доставки'
        if not items:
            return False, 'Добавьте хотя бы одну позицию'
        return True, ''
