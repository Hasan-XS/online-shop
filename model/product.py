from sqlalchemy import *
from extention import db, get_current_time

class Product(db.Model):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=False, index=True)
    price = Column(Integer, nullable=False, index=True)
    active = Column(Integer, nullable=False, index=True)
    date_create = Column(String(12), default=get_current_time)