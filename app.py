from flask import Flask
from flask_migrate import Migrate

from configs import DB_CONNECTION_STRING
from content_management.models import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECTION_STRING
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    data = {
        'status': 'OK'
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = (data, 200, headers)

    return response
