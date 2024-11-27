from flask import Blueprint, request, jsonify

from app.models import db, ProtectionSystem, Content
from app.encryptions import encrypt, decrypt, generate_encryption_key


bp = Blueprint('contents', __name__)


@bp.route('/contents', methods=['POST'])
def create_content():
    request_payload = request.get_json()
    protection_system_id = request_payload.get('protection_system_id', None)
    content_payload = request_payload.get('content_payload', None)

    error_message = None
    if protection_system_id is None and content_payload is None:
        error_message = '"protection_system_id" and "content_payload" are required fields.'
    elif protection_system_id is None:
        error_message = '"protection_system_id" is required field.'
    elif content_payload is None:
        error_message = '"content_payload" is required field.'

    encryption_mode_code = None
    if protection_system_id is not None:
        protection_system_id = int(protection_system_id)
        try:
            ps = ProtectionSystem.query.get_or_404(protection_system_id)
            encryption_mode_code = ps.encryption_mode_code
        except Exception as ex:
            error_message = 'No Protection System found for "protection_system_id"={}.'.format(protection_system_id)

    if error_message is not None:
        data = {
            'status': 'Error',
            'message': error_message
        }
        response = (jsonify(data), 400)
        return response

    encryption_key = generate_encryption_key()
    json_result = encrypt(content=content_payload, encryption_mode=encryption_mode_code, encryption_key=encryption_key)

    new_device = Content(protection_system=protection_system_id, encryption_key=encryption_key,
                         encrypted_payload=json_result)
    db.session.add(new_device)
    db.session.commit()

    data = {
        'status': 'OK',
        'message': 'Content created successfully.'
    }
    response = (jsonify(data), 201)
    return response


@bp.route('/contents/<int:id>', methods=['GET'])
def get_content(id):
    content = Content.query.get_or_404(id)
    data = {
        'id': content.id,
        'protection_system': content.protection_system,
        'encrypted_payload': content.encrypted_json
    }

    response = (jsonify(data), 200)
    return response


@bp.route('/contents', methods=['GET'])
def get_contents():
    contents = Content.query.all()
    data = []
    for content in contents:
        content_data = {
            'id': content.id,
            'protection_system': content.protection_system,
            'encrypted_payload': content.encrypted_json
        }

        data.append(content_data)

    response = (jsonify(data), 200)
    return response


@bp.route('/contents/<int:id>', methods=['DELETE'])
def delete_content(id):
    content = Content.query.get_or_404(id)
    db.session.delete(content)
    db.session.commit()
    data = {
        'status': 'OK',
        'message': 'Content deleted successfully.'
    }
    response = (jsonify(data), 200)
    return response
