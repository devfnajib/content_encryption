from flask import Blueprint, request, jsonify

from app.exceptions import InvalidEncryptionMode
from app.encryptions import validate_input
from app.models import db, ProtectionSystem


bp = Blueprint('protection_systems', __name__)


@bp.route('/protection_systems', methods=['POST'])
def create_protection_system():
    request_payload = request.get_json()
    name = request_payload.get('name', None)
    encryption_mode = request_payload.get('encryption_mode', None)

    error_message = None
    if name is None and encryption_mode is None:
        error_message = '"name" and "encryption_mode" are required fields.'
    elif name is None:
        error_message = '"name" is required field.'
    elif encryption_mode is None:
        error_message = '"encryption_mode" is required field.'

    if error_message is not None:
        data = {
            'status': 'Error',
            'message': error_message
        }
        response = (jsonify(data), 400)
        return response

    encryption_mode_code = 1
    try:
        encryption_mode_code = validate_input(encryption_mode=encryption_mode)
    except InvalidEncryptionMode as ex:
        response = (jsonify(ex.get_error()), 400)
        return response
    except Exception as ex:
        data = {
            'status': 'Error',
            'message': 'Invalid value for "encryption_mode" parameter.'
        }
        response = (jsonify(data), 400)
        return response

    new_ps = ProtectionSystem(name=name, encryption_mode=encryption_mode, encryption_mode_code=encryption_mode_code)
    db.session.add(new_ps)
    db.session.commit()

    data = {
        'status': 'OK',
        'message': 'Protection System created successfully.'
    }
    response = (jsonify(data), 201)
    return response


@bp.route('/protection_systems/<int:id>', methods=['GET'])
def get_protection_system(id):
    ps = ProtectionSystem.query.get_or_404(id)
    data = {
        'id': ps.id,
        'name': ps.name,
        'encryption_mode': ps.encryption_mode
    }

    response = (jsonify(data), 200)
    return response


@bp.route('/protection_systems', methods=['GET'])
def get_protection_systems():
    pss = ProtectionSystem.query.all()
    data = []
    for ps in pss:
        ps_data = {
            'id': ps.id,
            'name': ps.name,
            'encryption_mode': ps.encryption_mode
        }

        data.append(ps_data)

    response = (jsonify(data), 200)
    return response


@bp.route('/protection_systems/<int:id>', methods=['PUT'])
def update_protection_system(id):
    ps = ProtectionSystem.query.get_or_404(id)
    request_payload = request.get_json()
    name = request_payload.get('name', None)
    encryption_mode = request_payload.get('encryption_mode', None)

    if name is not None:
        ps.name = name

    if encryption_mode is not None:
        try:
            encryption_mode_code = validate_input(encryption_mode=encryption_mode)
            ps.encryption_mode = encryption_mode
            ps.encryption_mode_code = encryption_mode_code
        except InvalidEncryptionMode as ex:
            response = (jsonify(ex.get_error()), 400)
            return response
        except Exception as ex:
            data = {
                'status': 'Error',
                'message': 'Invalid value for "encryption_mode" parameter.'
            }
            response = (jsonify(data), 400)
            return response

    db.session.commit()
    data = {
        'status': 'OK',
        'message': 'Protection System updated successfully.'
    }
    response = (jsonify(data), 200)
    return response


@bp.route('/protection_systems/<int:id>', methods=['DELETE'])
def delete_protection_system(id):
    ps = ProtectionSystem.query.get_or_404(id)
    db.session.delete(ps)
    db.session.commit()
    data = {
        'status': 'OK',
        'message': 'Protection System deleted successfully.'
    }
    response = (jsonify(data), 200)
    return response
