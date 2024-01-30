from sqlalchemy import *
from extention import db

class CartItem(db.Model):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("Products.id"), nullable=False)
    cart_id = Column(Integer, ForeignKey("Carts.id"), nullable=False)
    quantity = Column(Integer)
    product =  db.relationship("Product", backref="Cart_Items")
    cart =  db.relationship("Cart", backref="Cart_Items")