from app import db
from app.models import ProtectionSystem, Device, Content

from app.encryptions import generate_encryption_key, encrypt


def test_create_ps(app):
    with app.app_context():
        ps = ProtectionSystem(name='AES 1', encryption_mode='AES + ECB', encryption_mode_code=1)
        db.session.add(ps)
        db.session.commit()
        assert ProtectionSystem.query.count() == 1


def test_get_ps(app):
    with app.app_context():
        ps = db.session.get(ProtectionSystem, 1)
        assert ps.id == 1


def test_create_device(app):
    with app.app_context():
        device = Device(name='Android', protection_system=1)
        db.session.add(device)
        db.session.commit()
        assert device.query.count() == 1


def test_get_device(app):
    with app.app_context():
        device = db.session.get(Device, 1)
        assert device.id == 1


def test_create_content(app):
    with app.app_context():
        encryption_key = generate_encryption_key()
        ps = db.session.get(ProtectionSystem, 1)
        encryption_mode_code = ps.encryption_mode_code
        json_result = encrypt(content='This is the text to be encrypted.', encryption_mode=encryption_mode_code,
                              encryption_key=encryption_key)

        content = Content(protection_system=ps.id, encryption_key=encryption_key, encrypted_payload=json_result)
        db.session.add(content)
        db.session.commit()
        assert content.query.count() == 1


def test_get_content(app):
    with app.app_context():
        content = db.session.get(Content, 1)
        assert content.id == 1
