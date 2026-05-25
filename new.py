#количество и ед изм

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox
)


class ItemFormDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Новый товар')
        self.resize(320, 260)

        main = QVBoxLayout(self)
        grid = QGridLayout()

        self.lineName     = QLineEdit()
        self.lineDesc     = QLineEdit()
        self.linePrice    = QLineEdit()
        self.lineCategory = QLineEdit()
        
        self.spinQuantity = QSpinBox()
        self.spinQuantity.setRange(0, 9999)
        self.spinQuantity.setValue(0)
        
        self.lineUnit = QLineEdit()
        self.lineUnit.setPlaceholderText('шт')
        self.lineUnit.setText('шт')

        fields = [
            ('Название *', self.lineName),
            ('Описание',   self.lineDesc),
            ('Цена *',     self.linePrice),
            ('Категория',  self.lineCategory),
            ('Количество:', self.spinQuantity),
            ('Ед. изм.:',  self.lineUnit),
        ]
        
        for i, (lbl, w) in enumerate(fields):
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


# Строка с остатком с цветовой индикацией
    if quantity == 0:
        stock_text = f"<span style='color:#C0392B; font-weight:bold;'>❌ НЕТ В НАЛИЧИИ</span>"
    elif quantity < 5:
        stock_text = f"<span style='color:#E67E22;'>⚠️ Остаток: {quantity} {unit} (мало)</span>"
    else:
        stock_text = f"<span style='color:#27AE60;'>✅ В наличии: {quantity} {unit}</span>"
