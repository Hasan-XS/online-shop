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
            return redirect("admin.login")
    else:
        return render_template("admin/login.html")
    

@app.route('/admin/dashboard/product', methods = ["POST", "GET"])
def product():
    if request.method == "GET":
        return render_template("admin/product.html")
    else:
        name = request.form.get("name", None)
        price = request.form.get("price", None)
        description = request.form.get("description", None)
        file = request.files.get("cover", None)
        active = request.form.get("active", None)

        p = Product(name = name, description = description, price = price)
        if active == None:
            p.active = 0
        else:
            p.active = 1

        db.session.add(p)
        db.session.commit()

        file.save(f"static/cover/{p.id}.jpg")
        return redirect("admin.dashboard")

@app.route('/admin/dashboard', methods = ["POST", "GET"])
def dashboard():
    return "dashboard"