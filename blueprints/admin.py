from flask import Blueprint, abort, session, request, render_template, redirect, url_for

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
    
@app.route('/admin/dashboard', methods = ["POST", "GET"])
def dashboard():
    return "dashboard"