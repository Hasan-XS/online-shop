from flask import Blueprint, render_template
from model.product import Product

app = Blueprint("general", __name__)

@app.route("/")
def home():
    products = Product.query.all()
    return render_template("general/home.html", products=products)

@app.route("/details/<int:id>/<name>")
def details(id, name):
    details = Product.query.filter(Product.id == id).filter(Product.name == name).first_or_404()
    return render_template("general/details.html", details=details)

@app.route("/about")
def about():
    return render_template("general/about.html")