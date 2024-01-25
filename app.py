from flask import Flask
from blueprints.admin import app as admin
from config import *
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

app.register_blueprint(admin)

if __name__ == "__main__":
    app.run(debug=True)