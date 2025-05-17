from datetime import datetime

from sqlalchemy import case

from db_work import db_session
from db_work.create_tables import User, Orders, Types
from keyboards.inline_kbs import admins


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
    db_sess = db_session.create_session()
    order = Orders()
    order.date = datetime.now()
    order.username = user_telegram_id
    order.order_id = ords
    db_sess.add(order)
    db_sess.commit()


def cancel_order(user_telegram_id: str):
    db_sess = db_session.create_session()
    db_sess.query(Orders).filter(Orders.username == user_telegram_id).delete()
    db_sess.commit()


def get_active_orders(user_telegram_id: str):
    db_sess = db_session.create_session()
    orders = db_sess.query(
        Orders,Types.order_type).filter(
        Orders.username == user_telegram_id, Orders.order_id == Types.id
    ).all()
    if not orders:
        return 'У вас нет активных заказов! 🍽'
    return orders

def ex_classes():
    db_sess = db_session.create_session()
    grade_order = [
        '11А', '11Б', '11В',
        '10А', '10Б', '10В',
        '9А', '9Б', '9В',
        '8А', '8Б', '8В',
        '7А', '7Б', '7В',
        '6А', '6Б', '6В',
        '5А', '5Б', '5В',
        '4А', '4Б', '4В',
        '3А', '3Б', '3В',
        '2А', '2Б', '2В',
        '1А', '1Б', '1В'
    ]
    data = []
    date = str(datetime.now())[:10]
    order_case = case(
        {grade: i for i, grade in enumerate(grade_order)},
        value=User.grade.concat(User.liter)
    )
    results = (db_sess.query(
        User.name,
        User.grade,
        User.liter,
        Orders.date,
        Types.order_type
    ).join(
        Orders, User.username == Orders.username
    ).join(
        Types, Orders.order_id == Types.id
    ).order_by(
        order_case,
        User.name
    ).all())
    if not results:
        return 'Нет текущих заказов ❌'
    for result in results:
        full_grade = f"{result.grade}{result.liter}"
        data.append("{:<5}{:<20} \n{:<10}".format(full_grade, result.name, result.order_type))

    return data