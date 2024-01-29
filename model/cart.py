from sqlalchemy import *
from extention import db

class Cart(db.Model):
    __tablename__ = "Carts"
    id = Column(Integer, primary_key=True)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    user = db.relationship("User", backref="Carts")