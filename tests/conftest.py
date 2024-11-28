import pytest
from app import create_application, db


@pytest.fixture(scope='session')
def app():
    app = create_application()

    # Connect with an empty Test DB to run tests.
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()
