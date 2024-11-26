from flask import Flask
from flask_migrate import Migrate

from configs import DB_CONNECTION_STRING
from app.models import db
from app.routes_protection_systems import bp as protection_systems_bp


def create_application():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECTION_STRING
    db.init_app(app)
    migrate = Migrate(app, db)
    app.register_blueprint(protection_systems_bp)

    return app
