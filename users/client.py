from PyQt6.QtWidgets import QMessageBox
from ui.client_win import Ui_MainWindow
from users.base_window import BaseWindow
from database.db import (
    all_menu_items, all_orders, one_order,
    add_order, add_order_item, delete_order
)

_PENDING = 'Ожидает приготовления'


class client_window(Ui_MainWindow, BaseWindow):
    def __init__(self, user_id, full_name=''):
        super().__init__()
        self.setupUi(self)
        self.user_id = user_id
        self.label_currentuser.setText(full_name or 'client')

        self.pushButton_backlogin.clicked.connect(self.back_to_login)
        self.pushButton_refresh.clicked.connect(self.load_menu)
        self.pushButtonAddOrder.clicked.connect(self.add_order)
        self.pushButtonDeleteOrder.clicked.connect(self.delete_order)
        self.pushButtonRefreshOrders.clicked.connect(self.load_orders)

        self._setup_scroll_area(self.scrollArea_menu)
        self.load_menu()
        self.load_orders()

    def load_orders(self):
        orders = all_orders(self.user_id)
        self._fill_tables(self.tableWidgetOrders, orders,
                          ['order_id', 'order_date', 'order_type',
                           'delivery_address', 'customer_comment', 'total_amount', 'status'])

    def _selected_order_id(self):
        row = self.tableWidgetOrders.currentRow()
        if row < 0:
            QMessageBox.warning(self, '', 'Выберите заказ')
            return None
        return int(self.tableWidgetOrders.item(row, 0).text())

    def add_order(self):
        from ui.order_form import OrderFormDialog
        dlg = OrderFormDialog(self, all_menu_items())
        if dlg.exec() != dlg.DialogCode.Accepted:
            return
        ok, msg = dlg.validate()
        if not ok:
            QMessageBox.warning(self, 'Ошибка', msg)
            return
        order_type, address, comment, _, items, _ = dlg.get_data()
        order_id = add_order(self.user_id, order_type, address, comment,
                             sum(float(i['price']) * q for i, q in items))
        if order_id:
            for i, q in items:
                add_order_item(order_id, i['item_id'], q, float(i['price']))
            self.load_orders()

    def delete_order(self):
        order_id = self._selected_order_id()
        if order_id is None:
            return
        order = one_order(order_id)
        if order.get('status') != _PENDING:
            QMessageBox.warning(self, '', f'Удалить можно только заказы «{_PENDING}»')
            return
        if QMessageBox.question(self, '', f'Удалить заказ #{order_id}?') == QMessageBox.StandardButton.Yes:
            delete_order(order_id)
            self.load_orders()
