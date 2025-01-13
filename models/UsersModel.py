from sqlalchemy import Column, BigInteger, String
from utils.Database import db


class UsersModel(db.Model):
    __tablename__ = 'user'

    class User(db.Model):
        __tablename__ = 'user'

        user_id = Column(BigInteger, primary_key=True, autoincrement=True)
        user_name = Column(String(255), nullable=False, unique=True)
        password = Column(String(255), nullable=False)
