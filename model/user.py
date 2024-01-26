from sqlalchemy import *
from extention import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)