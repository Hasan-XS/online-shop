from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from passlib.hash import sha256_crypt
from model.user import User
from extention import *
from flask_login import login_user

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

@app.route("/user/dashboard")
def dashboard():
    return "dashboard"