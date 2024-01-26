from flask import Flask
from blueprints.admin import app as admin
import config
from extention import *

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
db.init_app(app)

app.register_blueprint(admin)

with app.app_context():
    db.create_all()
if __name__ == "__main__":
    app.run(debug=True)