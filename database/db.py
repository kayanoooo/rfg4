import pymysql
from contextlib import contextmanager

_CONFIG = dict(host='localhost', user='root', password='aboba', database='pizzeria_pm02', cursorclass=pymysql.cursors.DictCursor, autocommit=True)

@contextmanager
def _cursor():
    try:
        db = pymysql.connect(**_CONFIG)
        with db.cursor() as cur:
            yield cur
    finally:
        db.close()

def _fetchall(sql, params=()):
    with _cursor() as c:
        c.execute(sql, params)
        return c.fetchall()
    
def _fetchone(sql, params=()):
    with _cursor() as c:
        c.execute(sql, params)
        return c.fetchone()
    
def _exec(sql, params=()):
    try:
        with _cursor() as c:
            c.execute(sql, params)
            return c.lastrowid
    except Exception as e:
        print(e, 'db error') or False











def check_login(username, password):
    return _fetchone("""
select u.user_id as id, u.full_name, r.role_name as role
from users u
join roles r on r.role_id = u.role_id
where username = %s and password = %s
""", (username, password))

_MENU_SQL = """
select mi.item_id, mi.name, mi.description, mi.price, mi.category, mi.image, mi.offer_id, so.name as offer_name, so.discount_percentage
from menu_items mi
left join special_offers so on so.offer_id = mi.offer_id
and curdate() between so.valid_from and so.valid_to
"""

_USER_SQL = """
select u.user_id as id, u.username, u.password, u.full_name, u.contact_info, u.role_id, r.role_name as role
from users u
join roles r on r.role_id = u.role_id
"""

def all_users():
    return _fetchall(_USER_SQL + 'order by u.user_id')

def all_roles():
    return _fetchall('select role_id as id, role_name from roles order by role_id')

def all_menu_items():
    return _fetchall(_MENU_SQL + 'order by mi.item_id')

def one_menu_item(item_id):
    return _fetchone(_MENU_SQL + 'where mi.item_id = %s', (item_id,))

def add_menu_item(name, description, price, category):
    """Добавляет товар, возвращает True если успешно"""
    try:
        _exec(
            'insert into menu_items (name, description, price, category) values (%s,%s,%s,%s)',
            (name, description or None, price, category or None)
        )
        return True
    except Exception as e:
        print(e, 'db error')
        return False
    
def delete_menu_item(item_id):
    """Удаляет товар, возвращает True если успешно, False если ошибка"""
    try:
        _exec('delete from menu_items where item_id=%s', (item_id,))
        return True  # Если дошли сюда - удаление успешно
    except Exception as e:
        print(e, 'db error')
        return False
        
def add_order(user_id, order_type, delivery_address, comment, total_amount):
    return _exec(
        'insert into orders (user_id, order_type, delivery_address, customer_comment, total_amount) '
        'values (%s,%s,%s,%s,%s)',
        (user_id or None, order_type, delivery_address or None, comment or None, total_amount)
    )

def add_order_item(order_id, item_id, quantity, unit_price):
    return _exec(
        'insert into order_items (order_id, item_id, quantity, unit_price) values (%s,%s,%s,%s)',
        (order_id, item_id, quantity, unit_price)
    )


_ORDER_SQL = """
select o.order_id, o.user_id, u.full_name, o.order_date, o.order_type,
       o.delivery_address, o.customer_comment, o.total_amount, o.status
from orders o
join users u on u.user_id = o.user_id
"""

def all_orders(user_id=None):
    if user_id:
        return _fetchall(_ORDER_SQL + 'where o.user_id = %s order by o.order_id desc', (user_id,))
    return _fetchall(_ORDER_SQL + 'order by o.order_id desc')

def one_order(order_id):
    return _fetchone(_ORDER_SQL + 'where o.order_id = %s', (order_id,))

def order_items_for_order(order_id):
    return _fetchall("""
select oi.id, oi.item_id, mi.name, oi.quantity, oi.unit_price
from order_items oi
join menu_items mi on mi.item_id = oi.item_id
where oi.order_id = %s
""", (order_id,))


def set_order_status(order_id, status):
    return _exec('update orders set status=%s where order_id=%s', (status, order_id))

def delete_order(order_id):
    _exec('delete from order_items where order_id=%s', (order_id,))
    return _exec('delete from orders where order_id=%s', (order_id,))


def add_user(username, password, full_name, contact_info, role_id):
    return _exec(
        'insert into users (username, password, full_name, contact_info, role_id) values (%s,%s,%s,%s,%s)',
        (username, password, full_name, contact_info or None, role_id)
    )

def update_user(user_id, username, password, full_name, contact_info, role_id):
    return _exec(
        'update users set username=%s, password=%s, full_name=%s, contact_info=%s, role_id=%s where user_id=%s',
        (username, password, full_name, contact_info or None, role_id, user_id)
    )

def delete_user(user_id):
    return _exec('delete from users where user_id=%s', (user_id,))

def get_order_items_by_item(item_id):
    """Проверяет, есть ли заказы с этим товаром"""
    return _fetchall(
        'SELECT * FROM order_items WHERE item_id = %s LIMIT 1',
        (item_id,)
    )

