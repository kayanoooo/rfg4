from ui.guest_win import Ui_MainWindow
from users.base_window import BaseWindow


class guest_window(Ui_MainWindow, BaseWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_backlogin.clicked.connect(self.back_to_login)
        self.pushButton_refresh.clicked.connect(self.load_menu)

        self._setup_scroll_area(self.scrollArea_menu)
        self.load_menu()