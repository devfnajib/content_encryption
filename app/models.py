from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class ProtectionSystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    encryption_mode = db.Column(db.String(100), nullable=False)
    encryption_mode_code = db.Column(db.Integer, nullable=False)
    devices = db.relationship('Device', backref='devices_protection_system', lazy=True)
    contents = db.relationship('Content', backref='contents_protection_system', lazy=True)

    def __init__(self, name, encryption_mode, encryption_mode_code):
        self.name = name
        self.encryption_mode = encryption_mode
        self.encryption_mode_code = encryption_mode_code


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    protection_system = db.Column(db.Integer, db.ForeignKey('protection_system.id'), nullable=False)

    def __init__(self, name, protection_system):
        self.name = name
        self.protection_system = protection_system


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    protection_system = db.Column(db.Integer, db.ForeignKey('protection_system.id'), nullable=False)
    encryption_key = db.Column(db.String(100), nullable=False)
    encrypted_payload = db.Column(db.String(10000), nullable=False)  # no char limit

    def __init__(self, protection_system, encryption_key, encrypted_payload):
        self.protection_system = protection_system
        self.encryption_key = encryption_key
        self.encrypted_payload = encrypted_payload
