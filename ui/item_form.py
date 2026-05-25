from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton
)


class ItemFormDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Новый товар')
        self.resize(320, 180)

        main = QVBoxLayout(self)
        grid = QGridLayout()

        self.lineName     = QLineEdit()
        self.lineDesc     = QLineEdit()
        self.linePrice    = QLineEdit()
        self.lineCategory = QLineEdit()

        for i, (lbl, w) in enumerate([
            ('Название *', self.lineName),
            ('Описание',   self.lineDesc),
            ('Цена *',     self.linePrice),
            ('Категория',  self.lineCategory),
        ]):
            grid.addWidget(QLabel(lbl), i, 0)
            grid.addWidget(w, i, 1)
        main.addLayout(grid)

        btns = QHBoxLayout()
        btns.addStretch()
        self.pushButtonSave   = QPushButton('Сохранить')
        self.pushButtonCancel = QPushButton('Отмена')
        btns.addWidget(self.pushButtonSave)
        btns.addWidget(self.pushButtonCancel)
        main.addLayout(btns)

        self.pushButtonSave.clicked.connect(self.accept)
        self.pushButtonCancel.clicked.connect(self.reject)

    def get_data(self):
        return (
            self.lineName.text().strip(),
            self.lineDesc.text().strip(),
            self.linePrice.text().strip(),
            self.lineCategory.text().strip(),
        )

    def validate(self):
        name, _, price, _ = self.get_data()
        if not name:
            return False, 'Введите название'
        try:
            float(price)
        except ValueError:
            return False, 'Цена должна быть числом'
        return True, ''
