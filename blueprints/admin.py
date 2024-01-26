from flask import Blueprint, abort, session, request, render_template, redirect, url_for
from extention import *
from model.product import Product

app = Blueprint("admin", __name__)

@app.before_request
def before_request():
    if session.get('admin_login', None) == None and request.endpoint != "admin.login":
        abort(403)

@app.route('/admin/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)

        if username == "admin" and password == "1234" :
            session['admin_login'] = username
            return redirect(url_for("admin.dashboard"))
        else:
            return redirect(url_for("admin.login"))
    else:
        return render_template("admin/login.html")
    

@app.route('/admin/dashboard/product', methods = ["POST", "GET"])
def products():
    if request.method == "GET":
        products = Product.query.all()
        return render_template("admin/product.html", products=products)
    else:
        name = request.form.get("name", None)
        price = request.form.get("price", None)
        description = request.form.get("description", None)
        file = request.files.get("cover", None)
        active = request.form.get("active", None)

        p = Product(name = name, description = description, price = price)
        if active == None:
            p.active = "not active"
        else:
            p.active = "active"

        db.session.add(p)
        db.session.commit()

        file.save(f"static/cover/{p.id}.jpg")
        return redirect(url_for("admin.dashboard"))
    

@app.route('/admin/dashboard/edit-product/<id>', methods = ["POST", "GET"])
def edit_product(id):
    products = Product.query.filter(Product.id == id).first_or_404()

    if request.method == "GET":
        return render_template("admin/edit-product.html", products=products)
    else:
        name = request.form.get("name", None)
        price = request.form.get("price", None)
        description = request.form.get("description", None)
        active = request.form.get("active", None)


        products.name = name
        products.price = price
        products.description = description
        if active == None:
            products.active = "not active"
        else:
            products.active = "active"

        db.session.commit()

        return redirect(url_for("admin.dashboard"))


@app.route('/admin/dashboard', methods = ["POST", "GET"])
def dashboard():
    products = Product.query.all()
    return render_template("admin/dashboard.html", products=products)