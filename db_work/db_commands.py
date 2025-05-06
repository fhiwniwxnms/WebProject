import sqlalchemy

from data import db_session
from data.db_session import SqlAlchemyBase
from data.today_orders import Orders
from data.users import User
from keyboards.all_kb import admins


def insert_info_users(user_telegram_id: str, name, grade, liter):
    user = User()
    if user_telegram_id in admins:
        user.status = '2'
        user.username = user_telegram_id
        user.name = name
        user.grade = grade
        user.liter = liter
    else:
        user.status = '1'
        user.username = user_telegram_id
        user.name = name
        user.grade = grade
        user.liter = liter
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def insert_info_orders(user_telegram_id: str, ords=0):
    pass
    # db_sess = db_session.create_session()
    # user = db_sess.query(User).filter(User.username == user_telegram_id)
    # order = Orders(name=)
    # users_row = db_sess.query(User).filter(User.username == user_telegram_id)
    # for user in users_row:
    #     order_row = Orders(
    #         name=user.name,
    #         grade=user.grade,
    #         liter=user.liter
    #     )
    #     db_sess.add(order_row)
    # order.breakfast = br
    # order.lunch = la
    # order.snack = af
    # db_sess.add(order)
    # db_sess.commit()
