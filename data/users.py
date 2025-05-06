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
    orders = orm.relationship("Orders", back_populates='user')
