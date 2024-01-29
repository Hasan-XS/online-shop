from sqlalchemy import *
from extention import db

class Payment(db.Model):
    __tablename__ = "Payments"
    id = Column(Integer, primary_key=True)
    status = Column(String, default="pending")
    cart_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    cart = db.relationship("Cart", backref="Payments")