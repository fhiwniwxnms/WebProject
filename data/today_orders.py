import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


# class, liter, name, breakfast, lunch, snack

class Orders(SqlAlchemyBase):
    __tablename__ = 'today_orders'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    grade = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    liter = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String,
                             sqlalchemy.ForeignKey("users.name"))
    breakfast = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    lunch = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    snack = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user = orm.relationship('User')
