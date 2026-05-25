from PyQt6.QtWidgets import QMessageBox, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer
from ui.admin_win import Ui_AdminWindow
from users.base_window import BaseWindow, _IMAGES_DIR
from users.pizza_card import pizzacard
from database.db import (
    all_users, all_roles, all_menu_items, all_orders,
    add_user, update_user, delete_user,
    add_menu_item, delete_menu_item,
)


class admin_window(BaseWindow, Ui_AdminWindow):
    def __init__(self, full_name=''):
        super().__init__()
        self.setupUi(self)
        self.labelCurrentUser.setText(full_name or 'admin')
        self._selected_item_id = None

        self.pushButtonLogout.clicked.connect(self.back_to_login)
        self.pushButtonRefreshUsers.clicked.connect(self.load_users)
        self.pushButtonRefreshRoles.clicked.connect(self.load_roles)
        self.pushButtonRefreshOrders.clicked.connect(self.load_orders)
        self.pushButtonRefreshItems.clicked.connect(self.load_items)
        self.pushButtonAddUser.clicked.connect(self.add_user_action)
        self.pushButtonEditUser.clicked.connect(self.edit_user_action)
        self.pushButtonDeleteUser.clicked.connect(self.delete_user_action)
        self.pushButtonAddItem.clicked.connect(self.add_item_action)
        self.pushButtonDeleteItem.clicked.connect(self.delete_item_action)

        self._items_widget = QWidget()
        self._items_layout = QVBoxLayout(self._items_widget)
        self._items_layout.setSpacing(8)
        self._items_layout.setContentsMargins(8, 8, 8, 8)
        self.scrollAreaItems.setWidget(self._items_widget)

        self.load_users()
        self.load_roles()
        self.load_orders()
        self.load_items()

    def load_users(self):
        self._fill_tables(self.tableWidgetUsers, all_users(),
                          ['id', 'username', 'password', 'full_name', 'contact_info', 'role'])

    def load_roles(self):
        self._fill_tables(self.tableWidgetRoles, all_roles(), ['id', 'role_name'])

    def load_orders(self):
        self._fill_tables(self.tableWidgetOrders, all_orders(),
                          ['order_id', 'full_name', 'order_date', 'order_type',
                           'delivery_address', 'customer_comment', 'total_amount', 'status'])

    def load_items(self):
        """Первоначальная загрузка (только один раз при запуске или по кнопке Обновить)"""
        # Очищаем layout
        self._clear_items_layout()
        
        self._selected_item_id = None
        items = all_menu_items()
        
        for item in items:
            card = pizzacard(item, _IMAGES_DIR)
            item_id = item['item_id']
            card.clicked.connect(lambda iid=item_id: self.on_item_clicked(iid))
            self._items_layout.addWidget(card)
        
        self._items_layout.addStretch()
        self.statusbar.showMessage(f'Загружено позиций: {len(items)}')

    def _clear_items_layout(self):
        """Безопасная очистка layout с карточками"""
        # Отключаем все сигналы
        for i in range(self._items_layout.count()):
            widget = self._items_layout.itemAt(i).widget()
            if widget and hasattr(widget, 'clicked'):
                try:
                    widget.clicked.disconnect()
                except:
                    pass
        
        # Очищаем layout
        while self._items_layout.count():
            item = self._items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def on_item_clicked(self, item_id):
        """Обработчик клика по товару"""
        self._selected_item_id = item_id
        self.statusbar.showMessage(f'Выбран товар #{item_id}')

    def _selected_id(self, table, label='строку'):
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self, '', f'Выберите {label}')
            return None
        return int(table.item(row, 0).text())

    def add_user_action(self):
        from ui.user_form import UserFormDialog
        dlg = UserFormDialog(self, all_roles())
        if dlg.exec() != dlg.DialogCode.Accepted:
            return
        ok, msg = dlg.validate()
        if not ok:
            QMessageBox.warning(self, 'Ошибка', msg)
            return
        if add_user(*dlg.get_data()):
            self.load_users()
        else:
            QMessageBox.critical(self, 'Ошибка', 'Не удалось добавить (логин занят?)')

    def edit_user_action(self):
        user_id = self._selected_id(self.tableWidgetUsers, 'пользователя')
        if user_id is None:
            return
        user = next((u for u in all_users() if u['id'] == user_id), None)
        if not user:
            return
        from ui.user_form import UserFormDialog
        dlg = UserFormDialog(self, all_roles(), user=user)
        if dlg.exec() != dlg.DialogCode.Accepted:
            return
        ok, msg = dlg.validate()
        if not ok:
            QMessageBox.warning(self, 'Ошибка', msg)
            return
        update_user(user_id, *dlg.get_data())
        self.load_users()

    def delete_user_action(self):
        user_id = self._selected_id(self.tableWidgetUsers, 'пользователя')
        if user_id is None:
            return
        if QMessageBox.question(self, '', f'Удалить пользователя #{user_id}?') == QMessageBox.StandardButton.Yes:
            delete_user(user_id)
            self.load_users()

    def add_item_action(self):
        from ui.item_form import ItemFormDialog
        dlg = ItemFormDialog(self)
        if dlg.exec() != dlg.DialogCode.Accepted:
            return
        ok, msg = dlg.validate()
        if not ok:
            QMessageBox.warning(self, 'Ошибка', msg)
            return
        name, desc, price, category = dlg.get_data()
        
        if add_menu_item(name, desc, float(price), category):
            # Получаем последний добавленный товар
            items = all_menu_items()
            if items:
                new_item = items[-1]
                card = pizzacard(new_item, _IMAGES_DIR)
                item_id = new_item['item_id']
                card.clicked.connect(lambda iid=item_id: self.on_item_clicked(iid))
                
                # Вставляем перед stretch (удаляем stretch, добавляем карточку, возвращаем stretch)
                stretch = self._items_layout.takeAt(self._items_layout.count() - 1)
                self._items_layout.addWidget(card)
                self._items_layout.addItem(stretch)
                
                self.statusbar.showMessage(f'Товар "{name}" добавлен')

    def delete_item_action(self):
        if not self._selected_item_id:
            QMessageBox.warning(self, '', 'Выберите товар, нажав на карточку')
            return
        
        # Проверяем, есть ли заказы с этим товаром
        from database.db import get_order_items_by_item
        order_items = get_order_items_by_item(self._selected_item_id)
        
        if order_items:
            QMessageBox.warning(
                self, 
                'Невозможно удалить', 
                f'Товар используется в {len(order_items)} заказах.\n\n'
                f'Удалите или измените заказы с этим товаром сначала.'
            )
            return
        
        reply = QMessageBox.question(self, 'Подтверждение', 
                                    f'Удалить товар #{self._selected_item_id}?',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            if delete_menu_item(self._selected_item_id):
                # Находим и удаляем карточку
                for i in range(self._items_layout.count()):
                    widget = self._items_layout.itemAt(i).widget()
                    if widget and hasattr(widget, 'item_id') and widget.item_id == self._selected_item_id:
                        # Отключаем сигнал
                        try:
                            widget.clicked.disconnect()
                        except:
                            pass
                        # Удаляем виджет
                        widget.setParent(None)
                        widget.deleteLater()
                        # Удаляем из layout
                        self._items_layout.takeAt(i)
                        break
                
                self._selected_item_id = None
                self.statusbar.showMessage('Товар удалён')
            else:
                QMessageBox.critical(self, 'Ошибка', 'Не удалось удалить товар')