import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    grade = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    liter = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class Orders(SqlAlchemyBase):
    __tablename__ = 'today_orders'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String,
                                 sqlalchemy.ForeignKey("users.username"))
    order_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)



class Types(SqlAlchemyBase):
    __tablename__ = 'orders_types'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    order_type = sqlalchemy.Column(sqlalchemy.String)
