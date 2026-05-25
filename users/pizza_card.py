from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class pizzacard(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, item, images_dir):
        super().__init__()
        self.item_id = item['item_id']

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)
        self.setMinimumHeight(170)
        

        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        label_image = QLabel()
        label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_image.setScaledContents(True)
        label_image.setFixedSize(170, 140)

        image_path = images_dir / (item.get('image') or '')
        if image_path.exists():
            label_image.setPixmap(QPixmap(str(image_path)))
        else:
            label_image.setText('photo')

        price = float(item.get('price'))
        discount = item.get('discount_percentage')
        if discount:
            discount = float(discount)
            new_price = price * (1 - discount / 100)
            price_text = (f"price: <span style='color:red;text-decoration:line-through;'>"
                          f"{price:.2f}$ </span> <b> {new_price:.2f} </b>"
                          )
            discount_text = f"discount: <b> {discount:g}% </b>"
        else:
            price_text = f"price: <b> {price:.2f} </b>"
            discount_text = 'no\ndiscount'

        label_info = QLabel(
            f"<b> {item.get('category')} | {item.get('name')} </b> <br>"
            f"{item.get('description') or '-'} <br>"
            f"{price_text}"
            )
        label_info.setTextFormat(Qt.TextFormat.RichText)
        label_info.setWordWrap(True)

        label_discount = QLabel(discount_text)
        label_discount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_discount.setFrameShape(QFrame.Shape.Box)
        label_discount.setMinimumWidth(100)

        if discount and float(discount) > 20:
            label_discount.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        elif discount:
            label_discount.setStyleSheet("background-color: orange;")

        layout.addWidget(label_image)
        layout.addWidget(label_info)
        layout.addWidget(label_discount)

    def mousePressEvent(self, event):
        self.clicked.emit(self.item_id)
        super().mousePressEvent(event)

        


