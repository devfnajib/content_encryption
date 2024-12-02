import pytest
from app import create_application, db


@pytest.fixture(scope='session')
def app():
    app = create_application(test_run=True)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()
