from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from passlib.hash import sha256_crypt
from model.cart import Cart
from model.cart_item import CartItem
from model.product import Product
from model.user import User
from extention import *
from flask_login import login_user, login_required, current_user

app = Blueprint("user", __name__)


@app.route("/user/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("general/user-login.html")
    else:
        register = request.form.get("regis", None)
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        email = request.form.get("email", None)

        if register != None:
            user = User.query.filter(User.username == username).first()
            if user != None:
                flash("Choose another username!")
                return redirect(url_for("user.login"))
            user = User(username=username, password=sha256_crypt.encrypt(password), email=email)
            db.session.add(user)
            db.session.commit()
            login_user(user)

            return redirect(url_for("user.dashboard"))

        else:
            user = User.query.filter(User.username == username).first()
            if user == None:
                flash("The username or password is wrong!")
                return redirect(url_for("user.login"))
            if sha256_crypt.verify(password, user.password):
                login_user(user)
                return redirect(url_for("user.dashboard"))
            else:
                flash("The username or password is wrong!")
                return redirect(url_for("user.login"))


@app.route("/user/dashboard", methods=["GET"])
@login_required
def dashboard():
    return "dashboard"


@app.route('/add-to-cart', methods=['GET'])
@login_required
def add_to_cart():
    id = request.args.get('id')
    product = Product.query.filter(Product.id == id).first_or_404()

    cart = current_user.carts.filter(Cart.status == 'pending').first()
    if cart == None:
        cart = Cart()
        current_user.carts.append(cart)
        db.session.add(cart)

    cart_item = cart.cart_items.filter(CartItem.product == product).first()
    if cart_item == None:
        item = CartItem(quantity=1)
        item.price = product.price
        item.cart = cart
        item.product = product
        db.session.add(item)
    else:
        cart_item.quantity += 1

    db.session.commit()

    return redirect(url_for('user.cart'))


@app.route('/remove-cart', methods=['GET'])
@login_required
def remove_cart():
    id = request.args.get('id')
    cart_item = CartItem.query.filter(CartItem.id == id).first_or_404()
    flash(f"Your cart item is {cart_item} removed!", "success")
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('user.cart'))

@app.route('/user/cart', methods=['GET'])
@login_required
def cart():
    cart = current_user.carts.filter(Cart.status == 'pending').first()
    return render_template("general/cart.html", cart=cart)