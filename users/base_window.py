from PyQt6.QtWidgets import *
from pathlib import Path
from database.db import all_menu_items, one_menu_item
from users.pizza_card import pizzacard

_IMAGES_DIR = Path(__file__).resolve().parent.parent / 'resources' / 'photos'

class BaseWindow(QMainWindow):
    def back_to_login(self):
        from auth.auth import login_window
        self.win = login_window()
        self.win.show()
        self.close()

    def _setup_scroll_area(self, scroll_area):
        self.card_widget = QWidget()
        self.card_layout = QVBoxLayout(self.card_widget)
        self.card_layout.setSpacing(8)
        self.card_layout.setContentsMargins(8, 8, 8, 8)
        scroll_area.setWidget(self.card_widget)
        scroll_area.setWidgetResizable(True)

    def clear_card(self):
        while self.card_layout.count():
            if w := self.card_layout.itemAt(0).widget():
                w.deleteLater()

    def load_menu(self):
        self.clear_card()
        items = all_menu_items()
        for item in items:
            card = pizzacard(item, _IMAGES_DIR)
            card.clicked.connect(self.show_menu_item)
            self.card_layout.addWidget(card)
        self.card_layout.addStretch()
        self.statusbar.showMessage(f'load positions: {len(items)}')

    def show_menu_item(self, item_id):
        item = one_menu_item(item_id)
        if item:
            text = (f"category: {item.get('category')}"
                    f"name: {item.get('name')}"
                    f"price: {float(item.get('price')):.2f} $"
                    f"description {item.get('description') or ''}"
                    )
            if item.get('discount_percentage'):
                text += f"discount: {item.get('discount_percentage'):g}"
            QMessageBox.information(self, item['name'], text)
    
    def _fill_tables(self, widget, rows, keys):
        widget.setRowCount(0)
        widget.setColumnCount(len(keys))
        widget.setHorizontalHeaderLabels(keys)
        widget.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, key in enumerate(keys):
                widget.setItem(i, j, QTableWidgetItem(str(row.get(key) or '')))

