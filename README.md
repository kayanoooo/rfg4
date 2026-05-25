# rfg4 — Пиццерия (PyQt6 + MySQL)

Проект системы управления пиццерией с разделением ролей. Окна создаются в Qt Designer как `.ui`, конвертируются в `.py` через `pyuic6` и подключаются через `Ui_*` + `setupUi(self)`.

## Логины

text
admin / admin
ivanov / pass123
petrova / pass456


## Как запустить

1. Создать базу данных MySQL:

CREATE DATABASE pizzeria_pm02;

2. Настроить подключение в database/db.py:

_CONFIG = dict(
    host='localhost',
    user='root',
    password='ваш_пароль',
    database='pizzeria_pm02',
    ...
)

3. Инициализировать БД:

database/init_db.py

4. Установить зависимости:

pip install -r requirements.txt

5. Запустить:

python main.py


## Подключение к БД

Настройки в database/db.py:

host='localhost'
user='root'
password='aboba'
database='pizzeria_pm02'

## UI

В папке ui лежат .ui файлы и сгенерированные .py:

login_win.ui       -> login_win.py
client_win.ui      -> client_win.py
guest_win.ui       -> guest_win.py
manager_win.ui     -> manager_win.py
admin_win.ui       -> admin_win.py
order_form.ui      -> order_form.py
user_form.ui       -> user_form.py
item_form.ui       -> item_form.py

Пример команды:

pyuic6 ui/login_win.ui -o ui/login_win.py
pyuic6 ui/client_win.ui -o ui/client_win.py
pyuic6 ui/guest_win.ui -o ui/guest_win.py
pyuic6 ui/manager_win.ui -o ui/manager_win.py
pyuic6 ui/admin_win.ui -o ui/admin_win.py
pyuic6 ui/order_form.ui -o ui/order_form.py
pyuic6 ui/user_form.ui -o ui/user_form.py
pyuic6 ui/item_form.ui -o ui/item_form.py

В Python-файлах окна подключаются так:

from ui.client_win import Ui_MainWindow

class client_window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


## Карточка товара

Карточка в users/pizza_card.py:


картинка слева | информация по центру | скидка/цена справа

Путь до картинок:

_IMAGES_DIR = Path(__file__).resolve().parent.parent / 'resources' / 'photos'

Особенность: скидка >20% выделяется красной рамкой и фоном 🔥

## Функционал

Клиент:

    просмотр меню карточками;

    оформление заказа (в зале/доставка/навынос);

    просмотр и отмена своих заказов.

Гость:

    просмотр меню без авторизации.

Менеджер:

    просмотр всех заказов;

    изменение статуса выбранного заказа.

Администратор:

    управление пользователями (CRUD);

    управление товарами (добавление/удаление);

    просмотр и изменение заказов;

    аналитика по продажам.

## Сборка EXE

На Windows:

pyinstaller --onefile --windowed --add-data "resources;resources" --add-data "ui;ui" --hidden-import=PyQt6 main.py

python -m pyinstaller --onefile --windowed --name "Пиццерия" --icon="resources/icon.ico" --add-data "resources;resources" --add-data "ui;ui" --hidden-import=PyQt6 main.py

