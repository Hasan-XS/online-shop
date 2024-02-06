from sqlalchemy import *
from extention import db, get_current_time
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    date_create = Column(String(12), default=get_current_time)