from sqlalchemy import *
from extention import db, get_current_time

class Payment(db.Model):
    __tablename__ = "Payments"
    id = Column(Integer, primary_key=True)
    status = Column(String, default="pending")
    price = Column(Integer)
    cart_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    cart = db.relationship("Cart", backref="Payments")
    date_create = Column(String(12), default=get_current_time)