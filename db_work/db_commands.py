import sqlalchemy

from data import db_session
from data.db_session import SqlAlchemyBase
from data.create_tables import User, Orders, Types
from keyboards.all_kb import admins
from datetime import datetime


def insert_orders_types():
    db_sess = db_session.create_session()
    data = [
        Types(order_type='Завтрак'),
        Types(order_type='Обед'),
        Types(order_type='Полдник'),
        Types(order_type='Завтрак + обед'),
        Types(order_type='Завтрак + полдник'),
        Types(order_type='Обед + полдник'),
        Types(order_type='Завтрак + обед + полдник')
    ]
    existing_types = {u[0] for u in db_sess.query(Types.order_type).filter(
        Types.order_type.in_([u.order_type for u in data])
    ).all()}
    types_to_add = [u for u in data if u.order_type not in existing_types]

    if types_to_add:
        db_sess.add_all(types_to_add)
        db_sess.commit()

def insert_info_users(user_telegram_id: str, name, grade, liter):
    user = User()
    user.username = user_telegram_id
    user.name = name
    user.grade = grade
    user.liter = liter
    if user_telegram_id in admins:
        user.status = '2'
    else:
        user.status = '1'
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def insert_info_orders(user_telegram_id: str, ords=0):
    order = Orders()
    order.date = datetime.now()
    order.username = user_telegram_id
    order.order_id = ords
    db_sess = db_session.create_session()
    db_sess.add(order)
    db_sess.commit()
