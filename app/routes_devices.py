from flask import Blueprint, request, jsonify

from app.models import db, Device, ProtectionSystem


bp = Blueprint('devices', __name__)


@bp.route('/devices', methods=['POST'])
def create_device():
    request_payload = request.get_json()
    name = request_payload.get('name', None)
    protection_system_id = request_payload.get('protection_system_id', None)

    error_message = None
    if name is None and protection_system_id is None:
        error_message = '"name" and "protection_system_id" are required fields.'
    elif name is None:
        error_message = '"name" is required field.'
    elif protection_system_id is None:
        error_message = '"protection_system_id" is required field.'

    if protection_system_id is not None:
        protection_system_id = int(protection_system_id)
        try:
            ProtectionSystem.query.get_or_404(protection_system_id)
        except Exception as ex:
            error_message = 'No Protection System found for "protection_system_id"={}.'.format(protection_system_id)

    if error_message is not None:
        data = {
            'status': 'Error',
            'message': error_message
        }
        response = (jsonify(data), 400)
        return response

    new_device = Device(name=name, protection_system=protection_system_id)
    db.session.add(new_device)
    db.session.commit()

    data = {
        'status': 'OK',
        'message': 'Device created successfully.'
    }
    response = (jsonify(data), 201)
    return response


@bp.route('/devices/<int:id>', methods=['GET'])
def get_device(id):
    device = Device.query.get_or_404(id)
    data = {
        'id': device.id,
        'name': device.name,
        'protection_system': device.protection_system
    }

    response = (jsonify(data), 200)
    return response


@bp.route('/devices', methods=['GET'])
def get_devices():
    devices = Device.query.all()
    data = []
    for device in devices:
        device_data = {
            'id': device.id,
            'name': device.name,
            'protection_system': device.protection_system
        }

        data.append(device_data)

    response = (jsonify(data), 200)
    return response


@bp.route('/devices/<int:id>', methods=['PUT'])
def update_device(id):
    device = Device.query.get_or_404(id)

    request_payload = request.get_json()
    name = request_payload.get('name', None)
    protection_system_id = request_payload.get('protection_system_id', None)

    error_message = None
    if name is None and protection_system_id is None:
        error_message = 'At least one of the following parameters is reqwuired to update: "name" and "protection_system_id"'

    if protection_system_id is not None:
        protection_system_id = int(protection_system_id)
        try:
            ProtectionSystem.query.get_or_404(protection_system_id)
        except Exception as ex:
            error_message = 'No Protection System found for "protection_system_id"={}.'.format(protection_system_id)

    if error_message is not None:
        data = {
            'status': 'Error',
            'message': error_message
        }
        response = (jsonify(data), 400)
        return response

    if name is not None:
        device.name = name
    if protection_system_id is not None:
        device.protection_system = protection_system_id

    db.session.commit()
    data = {
        'status': 'OK',
        'message': 'Device updated successfully.'
    }
    response = (jsonify(data), 200)
    return response


@bp.route('/devices/<int:id>', methods=['DELETE'])
def delete_device(id):
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    db.session.commit()
    data = {
        'status': 'OK',
        'message': 'Device deleted successfully.'
    }
    response = (jsonify(data), 200)
    return response
