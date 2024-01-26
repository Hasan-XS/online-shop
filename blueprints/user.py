from flask import Blueprint, render_template, request, session, redirect
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
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        if register != None:
            user = User(username=username, password=sha256_crypt.encrypt(password), email=email)
            db.session.add(user)
            db.session.commit()
            login_user(user)

            return redirect("user.dashboard")
        
        return "false"