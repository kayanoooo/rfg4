from PyQt6.QtWidgets import QMessageBox
from ui.manager_win import Ui_ManagerWindow
from users.base_window import BaseWindow
from database.db import all_orders, set_order_status


class manager_window(BaseWindow, Ui_ManagerWindow):
    def __init__(self, full_name=''):
        super().__init__()
        self.setupUi(self)
        self.labelCurrentUser.setText(full_name or 'manager')

        self.pushButtonLogout.clicked.connect(self.back_to_login)
        self.pushButtonRefresh.clicked.connect(self.load_orders)
        self.pushButtonApply.clicked.connect(self.apply_status)

        self.load_orders()

    def load_orders(self):
        self._fill_tables(self.tableWidgetOrders, all_orders(),
                          ['order_id', 'full_name', 'order_date', 'order_type',
                           'delivery_address', 'customer_comment', 'total_amount', 'status'])

    def apply_status(self):
        row = self.tableWidgetOrders.currentRow()
        if row < 0:
            QMessageBox.warning(self, '', 'Выберите заказ')
            return
        order_id = int(self.tableWidgetOrders.item(row, 0).text())
        status = self.comboStatus.currentText()
        set_order_status(order_id, status)
        self.load_orders()
        self.statusbar.showMessage(f'Заказ #{order_id} → {status}')
