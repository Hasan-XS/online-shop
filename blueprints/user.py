import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user
from passlib.hash import sha256_crypt

import config
from extention import *
from model.cart import Cart
from model.cart_item import CartItem
from model.payment import Payment
from model.product import Product
from model.user import User

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
    return render_template("general/dashboard.html")


@app.route("/user/dashboard/order/<id>", methods=["GET"])
@login_required
def order(id):
    cart = current_user.carts.filter(Cart.id == id).first_or_404()
    return render_template("general/order.html", cart=cart)


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
    id = request.args.get('id-rem')
    cart_item = CartItem.query.filter(CartItem.id == id).first_or_404()
    flash(f"Your cart item is {cart_item} removed!", "success")
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('user.cart'))


@app.route('/Increase-cart', methods=['GET'])
@login_required
def Increase_cart():
    id = request.args.get('id-inc')
    cart_item = CartItem.query.filter(CartItem.id == id).first_or_404()
    flash(f"Your cart item is {cart_item} Increase!", "success")
    if cart_item.quantity >= 1:
        cart_item.quantity += 1
    else:
        db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('user.cart'))


@app.route('/empty-cart', methods=['GET'])
@login_required
def empty_cart():
    id = request.args.get('id-empty')
    cart_item = CartItem.query.filter(CartItem.id == id).first_or_404()
    flash(f"Your cart item is {cart_item} removed!", "success")
    if cart_item.quantity >= 1:
        cart_item.quantity -= cart_item.quantity
        db.session.delete(cart_item)
    # else:
    #     db.session.delete(ct)
    db.session.commit()
    return redirect(url_for('user.cart'))


@app.route('/user/cart', methods=['GET'])
@login_required
def cart():
    cart = current_user.carts.filter(Cart.status == 'pending').first()
    return render_template("general/cart.html", cart=cart)


@app.route('/payment', methods=['GET'])
@login_required
def payment():
    cart = current_user.carts.filter(Cart.status == 'pending').first()
    r = requests.post(config.FIRST_REQUEST_PAYMENT,
                      data={"api": 'sandbox',
                            "amount": cart.total_price(),
                            "callback": config.REQUEST_PAYMENT_VERIFY_CALLBACK})
    token = r.json()['result']['token']
    url = r.json()['result']['url']
    pay = Payment(token=token, price=cart.total_price())
    pay.cart = cart
    db.session.add(pay)
    db.session.commit()
    return redirect(url)


@app.route('/verify', methods=['GET'])
@login_required
def verify():
    token = request.args.get("token")
    pay = Payment.query.filter(Payment.token == token).first_or_404()
    cart = current_user.carts.filter(Cart.status == 'pending').first()
    r = requests.post(config.REQUEST_PAYMENT_VERIFY,
                      data={"api": 'sandbox',
                            "amount": pay.price,
                            "token": token
                            })
    pay_status = bool(r.json()['success'])
    if pay_status:
        transaction_id = r.json()['result']['transaction_id']
        card_pan = r.json()['result']['card_pan']
        refid = r.json()['result']['refid']

        pay.card_pan = card_pan
        pay.refid = refid
        pay.transaction_id = transaction_id
        pay.status = "success"
        pay.cart.status = "paid"
        flash("Your cart (success)")
    else:
        pay.status = "Failed"

    db.session.commit()
    return redirect(url_for('user.dashboard'))
