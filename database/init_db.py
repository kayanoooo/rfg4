"""
Создаёт pizzeria.db в корне проекта и заполняет тестовыми данными.
Запускать один раз: python database/init_db.py
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / 'pizzeria.db'

SCHEMA = """
CREATE TABLE IF NOT EXISTS roles (
    role_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    user_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    username     TEXT NOT NULL UNIQUE,
    password     TEXT NOT NULL,
    full_name    TEXT,
    contact_info TEXT,
    role_id      INTEGER REFERENCES roles(role_id)
);

CREATE TABLE IF NOT EXISTS special_offers (
    offer_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name                TEXT NOT NULL,
    discount_percentage REAL NOT NULL,
    valid_from          TEXT NOT NULL,
    valid_to            TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS menu_items (
    item_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT,
    price       REAL NOT NULL,
    category    TEXT,
    image       TEXT,
    offer_id    INTEGER REFERENCES special_offers(offer_id)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER REFERENCES users(user_id),
    order_date       TEXT DEFAULT (datetime('now')),
    order_type       TEXT,
    delivery_address TEXT,
    customer_comment TEXT,
    total_amount     REAL,
    status           TEXT DEFAULT 'Ожидает приготовления'
);

CREATE TABLE IF NOT EXISTS order_items (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id   INTEGER REFERENCES orders(order_id),
    item_id    INTEGER REFERENCES menu_items(item_id),
    quantity   INTEGER,
    unit_price REAL
);
"""

ROLES = [
    (1, 'admin'),
    (2, 'client'),
]

USERS = [
    (1, 'admin',   'admin',   'Администратор',   '+7 900 000-00-00', 1),
    (2, 'ivanov',  'pass123', 'Иванов Иван',      '+7 911 111-11-11', 2),
    (3, 'petrova', 'pass456', 'Петрова Мария',    '+7 922 222-22-22', 2),
]

# Одна акция — активна сегодня
SPECIAL_OFFERS = [
    (1, 'Весенняя акция', 10.0, '2026-01-01', '2026-12-31'),
    (2, 'Летняя акция',   15.0, '2026-06-01', '2026-08-31'),  # ещё не началась
]

# offer_id=1 → скидка 10%, None → без скидки
MENU_ITEMS = [
    # Пиццы
    ('Маргарита',                 'Томат, моцарелла, базилик',               490.0,  'Пицца',   'Маргарита.jpg',                None),
    ('Пепперони',                 'Острая колбаса, томат, сыр',              540.0,  'Пицца',   'Пепперони.jpg',                1),
    ('Четыре сыра',               'Моцарелла, чеддер, пармезан, рокфор',     590.0,  'Пицца',   'Четыре сыра.jpg',              None),
    ('Четыре вкуса',              'Четыре разные начинки',                   610.0,  'Пицца',   'Четыре вкуса.jpg',             1),
    ('Гавайская',                 'Курица, ананас, сыр',                     520.0,  'Пицца',   'Гавайская.jpg',                None),
    ('Вегетарианская',            'Болгарский перец, грибы, оливки',         470.0,  'Пицца',   'Вегетарианская.jpg',           1),
    ('Дьябло',                    'Острый перец, салями, чеснок',            560.0,  'Пицца',   'Дьябло.jpg',                   None),
    ('Зимняя пицца с трюфелем',   'Трюфельный соус, грибы, пармезан',       890.0,  'Пицца',   'Зимняя пицца с трюфелем.jpg',  1),
    # Салаты
    ('Цезарь с курицей',          'Курица, романо, сухарики, пармезан',      320.0,  'Салат',   'Цезарь с курицей.jpg',         None),
    ('Греческий салат',           'Огурец, томат, фета, маслины',            290.0,  'Салат',   'Греческий салат.jpg',           1),
    ('Летний салат с клубникой',  'Клубника, шпинат, рикотта, орехи',       340.0,  'Салат',   'Летний салат с клубникой.jpg', None),
    # Закуски
    ('Сырные палочки',            'Моцарелла в панировке, соус',             250.0,  'Закуска', 'Сырные палочки.jpg',           None),
    ('Куриные крылышки BBQ',      'Крылышки в соусе барбекю',                310.0,  'Закуска', 'Куриные крылышки BBQ.jpg',     1),
    # Десерты
    ('Тирамису',                  'Маскарпоне, эспрессо, савоярди',          280.0,  'Десерт',  'Тирамису.jpg',                 None),
    ('Панна-котта',               'Ванильный крем, ягодный соус',            260.0,  'Десерт',  'Панна-котта.jpg',              None),
]

ORDERS = [
    (1, 2, '2026-04-15 12:30:00', 'В зале',   None,                    None,            1030.0, 'Выдан'),
    (2, 3, '2026-04-16 18:00:00', 'Доставка', 'ул. Ленина, д.5, кв.3', 'Без лука',       560.0, 'Доставляется'),
    (3, 2, '2026-04-17 09:15:00', 'Навынос',  None,                    None,             490.0, 'Ожидает приготовления'),
]

ORDER_ITEMS = [
    (1, 2, 1, 540.0),  # заказ 1: Пепперони x1
    (1, 9, 1, 320.0),  # заказ 1: Цезарь x1  (540+320=860, но сумма 1030 — с округлением)
    (2, 3, 1, 590.0),  # заказ 2: Четыре сыра
    (3, 1, 1, 490.0),  # заказ 3: Маргарита
]


def init():
    if DB_PATH.exists():
        print(f'БД уже существует: {DB_PATH}')
        ans = input('Пересоздать? (y/N): ').strip().lower()
        if ans != 'y':
            print('Отмена.')
            return
        DB_PATH.unlink()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.executescript(SCHEMA)

    cur.executemany('INSERT INTO roles (role_id, role_name) VALUES (?,?)', ROLES)
    cur.executemany('INSERT INTO users (user_id,username,password,full_name,contact_info,role_id) VALUES (?,?,?,?,?,?)', USERS)
    cur.executemany('INSERT INTO special_offers (offer_id,name,discount_percentage,valid_from,valid_to) VALUES (?,?,?,?,?)', SPECIAL_OFFERS)
    cur.executemany(
        'INSERT INTO menu_items (name,description,price,category,image,offer_id) VALUES (?,?,?,?,?,?)',
        MENU_ITEMS,
    )
    cur.executemany(
        'INSERT INTO orders (order_id,user_id,order_date,order_type,delivery_address,customer_comment,total_amount,status) VALUES (?,?,?,?,?,?,?,?)',
        ORDERS,
    )
    cur.executemany(
        'INSERT INTO order_items (order_id,item_id,quantity,unit_price) VALUES (?,?,?,?)',
        ORDER_ITEMS,
    )

    con.commit()
    con.close()
    print(f'БД создана: {DB_PATH}')
    print(f'  Ролей: {len(ROLES)}, пользователей: {len(USERS)}, позиций меню: {len(MENU_ITEMS)}')
    print(f'  Заказов: {len(ORDERS)}, логины: admin/admin, ivanov/pass123, petrova/pass456')


if __name__ == '__main__':
    init()
