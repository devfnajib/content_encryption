from flask import Blueprint, request, jsonify
from loguru import logger
import shortuuid

from app.models import db, ProtectionSystem, Content
from app.encryptions import encrypt, decrypt, generate_encryption_key


bp = Blueprint('contents', __name__)


@bp.route('/contents', methods=['POST'])
def create_content():
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: POST Request received at "/contents"')
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
        logger.info(f'[ReqID: "{request_id}"]: Validating protection_system_id.')
        protection_system_id = int(protection_system_id)
        try:
            ps = ProtectionSystem.query.get_or_404(protection_system_id)
            logger.info(f'[ReqID: "{request_id}"]: protection_system_id validated.')
            encryption_mode_code = ps.encryption_mode_code
        except Exception as ex:
            error_message = 'No Protection System found for "protection_system_id"={}.'.format(protection_system_id)

    if error_message is not None:
        logger.error(f'[ReqID: "{request_id}"]: {error_message}')
        data = {
            'status': 'Error',
            'message': error_message
        }
        response = (jsonify(data), 400)
        return response

    encryption_key = generate_encryption_key()
    logger.info(f'[ReqID: "{request_id}"]: Encrypting content.')
    json_result = encrypt(content=content_payload, encryption_mode=encryption_mode_code, encryption_key=encryption_key)

    logger.info(f'[ReqID: "{request_id}"]: Content encrypted. Creating new content record in DB.')
    new_content = Content(protection_system=protection_system_id, encryption_key=encryption_key,
                          encrypted_payload=json_result)
    db.session.add(new_content)
    db.session.commit()

    data = {
        'status': 'OK',
        'message': 'Content created successfully.'
    }
    response = (jsonify(data), 201)
    logger.success(f'[ReqID: "{request_id}"]: Content created successfully.')
    return response


@bp.route('/contents/<int:id>', methods=['GET'])
def get_content(id):
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: GET Request received at "/contents/{id}"')
    content = Content.query.get_or_404(id)
    data = {
        'id': content.id,
        'protection_system': content.protection_system,
        'encrypted_payload': content.encrypted_json
    }

    response = (jsonify(data), 200)
    logger.success(f'[ReqID: "{request_id}"]: Returning Content details.')
    return response


@bp.route('/contents', methods=['GET'])
def get_contents():
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: GET Request received at "/contents"')
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
    logger.success(f'[ReqID: "{request_id}"]: Returning all Contents.')
    return response


@bp.route('/contents/<int:id>', methods=['PUT'])
def update_content(id):
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: PUT Request received at "/contents/{id}"')
    content = Content.query.get_or_404(id)

    request_payload = request.get_json()
    protection_system_id = request_payload.get('protection_system_id', None)
    content_payload = request_payload.get('content_payload', None)

    if protection_system_id is None and content_payload is None:
        error_message = 'At least one of "protection_system_id" or "content_payload" is required.'
        logger.error(f'[ReqID: "{request_id}"]: {error_message}')
        data = {
            'status': 'Error',
            'message': error_message
        }
        response = (jsonify(data), 400)
        return response
    elif protection_system_id == content.protection_system and content_payload is None:
        message = ('Content not provided and "protection_system_id" is not changed. '
                   'Not making any change in the content.')
        data = {
            'status': 'OK',
            'message': message
        }
        response = (jsonify(data), 200)
        logger.success(f'[ReqID: "{request_id}"]: {message}')
        return response

    encryption_mode_code = None
    if protection_system_id is not None:
        logger.info(f'[ReqID: "{request_id}"]: Validating protection_system_id.')
        protection_system_id = int(protection_system_id)
        try:
            ps = ProtectionSystem.query.get_or_404(protection_system_id)
            logger.info(f'[ReqID: "{request_id}"]: protection_system_id validated.')
            encryption_mode_code = ps.encryption_mode_code
        except Exception as ex:
            error_message = 'No Protection System found for "protection_system_id"={}.'.format(protection_system_id)
            logger.error(f'[ReqID: "{request_id}"]: {error_message}')
            data = {
                'status': 'Error',
                'message': error_message
            }
            response = (jsonify(data), 400)
            return response
    else:
        logger.info(f'[ReqID: "{request_id}"]: protection_system_id not provided, updating content only.')

    if content_payload is None:
        logger.info(f'[ReqID: "{request_id}"]: Decrypting current content to encrypt it again using new Protection System.')
        ps = ProtectionSystem.query.get_or_404(content.protection_system)
        content_payload = decrypt(encryption_key=content.encryption_key, encryption_mode=ps.encryption_mode_code,
                                  encryption_payload=content.encrypted_json)

    encryption_key = generate_encryption_key()
    logger.info(f'[ReqID: "{request_id}"]: Encrypting content.')
    json_result = encrypt(content=content_payload, encryption_mode=encryption_mode_code, encryption_key=encryption_key)

    logger.info(f'[ReqID: "{request_id}"]: Content encrypted. Updating content record in DB.')
    content.protection_system = protection_system_id
    content.encrypted_json = json_result
    content.encryption_key = encryption_key
    db.session.commit()

    data = {
        'status': 'OK',
        'message': 'Content updated successfully.'
    }
    response = (jsonify(data), 201)
    logger.success(f'[ReqID: "{request_id}"]: Content updated successfully.')
    return response


@bp.route('/contents/<int:id>', methods=['DELETE'])
def delete_content(id):
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: DELETE Request received at "/contents/{id}"')
    content = Content.query.get_or_404(id)
    db.session.delete(content)
    db.session.commit()
    data = {
        'status': 'OK',
        'message': 'Content deleted successfully.'
    }
    response = (jsonify(data), 200)
    logger.success(f'[ReqID: "{request_id}"]: Content deleted successfully.')
    return response
