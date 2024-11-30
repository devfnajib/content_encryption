from flask import Blueprint, request, jsonify
from loguru import logger
import shortuuid

from app.models import db, Device, ProtectionSystem


bp = Blueprint('devices', __name__)


@bp.route('/devices', methods=['POST'])
def create_device():
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: POST Request received at "/devices"')
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
        logger.info(f'[ReqID: "{request_id}"]: Validating protection_system_id.')
        protection_system_id = int(protection_system_id)
        ps = db.session.get(ProtectionSystem, protection_system_id)
        if ps is None:
            error_message = f'No Protection System found for "protection_system_id"={protection_system_id}.'
        else:
            logger.info(f'[ReqID: "{request_id}"]: protection_system_id validated.')

    if error_message is not None:
        logger.error(f'[ReqID: "{request_id}"]: {error_message}')
        data = {
            'status': 'Error',
            'message': error_message
        }
        response = (jsonify(data), 400)
        return response

    logger.info(f'[ReqID: "{request_id}"]: Creating new Device.')
    new_device = Device(name=name, protection_system=protection_system_id)
    db.session.add(new_device)
    db.session.commit()

    data = {
        'status': 'OK',
        'message': 'Device created successfully.'
    }
    response = (jsonify(data), 201)
    logger.success(f'[ReqID: "{request_id}"]: Device created successfully.')
    return response


@bp.route('/devices/<int:id>', methods=['GET'])
def get_device(id):
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: GET Request received at "/devices/{id}"')
    device = db.session.get(Device, id)
    if device is None:
        logger.error(f'[ReqID: "{request_id}"]: No such Device found with id="{id}".')
        data = {
            'status': 'Error',
            'message': f'No such Device found with id="{id}".'
        }
        response = (jsonify(data), 404)
        return response

    data = {
        'id': device.id,
        'name': device.name,
        'protection_system': device.protection_system
    }

    response = (jsonify(data), 200)
    logger.success(f'[ReqID: "{request_id}"]: Returning Device details.')
    return response


@bp.route('/devices', methods=['GET'])
def get_devices():
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: GET Request received at "/devices"')
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
    logger.success(f'[ReqID: "{request_id}"]: Returning all Devices.')
    return response


@bp.route('/devices/<int:id>', methods=['PUT'])
def update_device(id):
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: PUT Request received at "/devices/{id}"')
    device = db.session.get(Device, id)
    if device is None:
        logger.error(f'[ReqID: "{request_id}"]: No such Device found with id="{id}".')
        data = {
            'status': 'Error',
            'message': f'No such Device found with id="{id}".'
        }
        response = (jsonify(data), 404)
        return response

    request_payload = request.get_json()
    name = request_payload.get('name', None)
    protection_system_id = request_payload.get('protection_system_id', None)

    error_message = None
    if name is None and protection_system_id is None:
        error_message = 'At least one of the following parameters is reqwuired to update: "name" and "protection_system_id"'

    if protection_system_id is not None:
        logger.info(f'[ReqID: "{request_id}"]: Validating protection_system_id.')
        protection_system_id = int(protection_system_id)
        ps = db.session.get(ProtectionSystem, protection_system_id)
        if ps is None:
            error_message = f'No Protection System found for "protection_system_id"={protection_system_id}.'
        else:
            logger.info(f'[ReqID: "{request_id}"]: protection_system_id validated.')

    if error_message is not None:
        logger.error(f'[ReqID: "{request_id}"]: {error_message}.')
        data = {
            'status': 'Error',
            'message': error_message
        }
        response = (jsonify(data), 400)
        return response

    logger.info(f'[ReqID: "{request_id}"]: Updating device.')
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
    logger.success(f'[ReqID: "{request_id}"]: Device updated successfully.')
    return response


@bp.route('/devices/<int:id>', methods=['DELETE'])
def delete_device(id):
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: DELETE Request received at "/devices/{id}"')
    device = db.session.get(Device, id)
    if device is None:
        logger.error(f'[ReqID: "{request_id}"]: No such Device found with id="{id}".')
        data = {
            'status': 'Error',
            'message': f'No such Device found with id="{id}".'
        }
        response = (jsonify(data), 404)
        return response

    db.session.delete(device)
    db.session.commit()
    data = {
        'status': 'OK',
        'message': 'Device deleted successfully.'
    }
    response = (jsonify(data), 200)
    logger.success(f'[ReqID: "{request_id}"]: Device deleted successfully.')
    return response
