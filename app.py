from flask import Flask
from blueprints.admin import app as admin
from blueprints.general import app as general
from blueprints.user import app as user
from flask_login import LoginManager
import config
from model.user import User
from extention import *

app = Flask(__name__)
login_manager = LoginManager()
# Secret key
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
db.init_app(app)
login_manager.init_app(app)

# register blueprint
app.register_blueprint(admin)
app.register_blueprint(general)
app.register_blueprint(user)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first_or_404()

with app.app_context():
    db.create_all()
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")