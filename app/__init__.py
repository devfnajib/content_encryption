from flask import Flask
from flask_migrate import Migrate
from loguru import logger

from configs import DB_CONNECTION_STRING
from app.models import db
from app.routes_protection_systems import bp as protection_systems_bp
from app.routes_devices import bp as devices_bp
from app.routes_contents import bp as contents_bp
from app.routes_main import bp as main_bp


def create_application():
    logger.info('Creating Flask App.')
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECTION_STRING
    db.init_app(app)
    migrate = Migrate(app, db)
    logger.success('DB connection setup.')

    app.register_blueprint(protection_systems_bp)
    app.register_blueprint(devices_bp)
    app.register_blueprint(contents_bp)
    app.register_blueprint(main_bp)
    logger.success('All routes registered.')

    return app
