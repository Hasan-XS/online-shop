from flask import Blueprint, render_template
from model.product import Product

app = Blueprint("general", __name__)

@app.route("/")
def home():
    products = Product.query.all()
    return render_template("general/home.html", products=products)

@app.route("/about")
def about():
    return render_template("general/about.html")