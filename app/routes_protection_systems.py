from flask import Blueprint, request, jsonify
from loguru import logger
import shortuuid

from app.exceptions import InvalidEncryptionMode
from app.encryptions import validate_input
from app.models import db, ProtectionSystem


bp = Blueprint('protection_systems', __name__)


@bp.route('/protection_systems', methods=['POST'])
def create_protection_system():
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: POST Request received at "/protection_systems"')
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
        logger.warning(f'[ReqID: "{request_id}"]: {error_message}')
        data = {
            'status': 'Error',
            'message': error_message
        }
        response = (jsonify(data), 400)
        return response

    encryption_mode_code = 1
    try:
        logger.info(f'[ReqID: "{request_id}"]: Validating encryption_mode.')
        encryption_mode_code = validate_input(encryption_mode=encryption_mode)
        logger.info(f'[ReqID: "{request_id}"]: encryption_mode validated.')
    except InvalidEncryptionMode as ex:
        logger.error(f'[ReqID: "{request_id}"]: Invalid encryption_mode: {ex.get_error()}')
        response = (jsonify(ex.get_error()), 400)
        return response
    except Exception as ex:
        logger.error(f'[ReqID: "{request_id}"]: Invalid value for "encryption_mode" parameter.')
        data = {
            'status': 'Error',
            'message': 'Invalid value for "encryption_mode" parameter.'
        }
        response = (jsonify(data), 400)
        return response

    logger.info(f'[ReqID: "{request_id}"]: Creating new Protection System.')
    new_ps = ProtectionSystem(name=name, encryption_mode=encryption_mode, encryption_mode_code=encryption_mode_code)
    db.session.add(new_ps)
    db.session.commit()

    data = {
        'status': 'OK',
        'message': 'Protection System created successfully.'
    }
    response = (jsonify(data), 201)
    logger.success(f'[ReqID: "{request_id}"]: Protection System created successfully.')
    return response


@bp.route('/protection_systems/<int:id>', methods=['GET'])
def get_protection_system(id):
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: GET Request received at "/protection_systems/{id}"')
    ps = ProtectionSystem.query.get_or_404(id)
    data = {
        'id': ps.id,
        'name': ps.name,
        'encryption_mode': ps.encryption_mode
    }

    response = (jsonify(data), 200)
    logger.success(f'[ReqID: "{request_id}"]: Returning Protection System details.')
    return response


@bp.route('/protection_systems', methods=['GET'])
def get_protection_systems():
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: GET Request received at "/protection_systems"')
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
    logger.success(f'[ReqID: "{request_id}"]: Returning all Protection Systems.')
    return response


@bp.route('/protection_systems/<int:id>', methods=['PUT'])
def update_protection_system(id):
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: PUT Request received at "/protection_systems/{id}"')
    ps = ProtectionSystem.query.get_or_404(id)
    request_payload = request.get_json()
    name = request_payload.get('name', None)
    encryption_mode = request_payload.get('encryption_mode', None)

    if name is not None:
        ps.name = name

    if encryption_mode is not None:
        try:
            logger.info(f'[ReqID: "{request_id}"]: Validating encryption_mode.')
            encryption_mode_code = validate_input(encryption_mode=encryption_mode)
            logger.info(f'[ReqID: "{request_id}"]: encryption_mode validated.')
            ps.encryption_mode = encryption_mode
            ps.encryption_mode_code = encryption_mode_code
        except InvalidEncryptionMode as ex:
            logger.error(f'[ReqID: "{request_id}"]: Invalid encryption_mode: {ex.get_error()}')
            response = (jsonify(ex.get_error()), 400)
            return response
        except Exception as ex:
            logger.error(f'[ReqID: "{request_id}"]: Invalid value for "encryption_mode" parameter.')
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
    logger.success(f'[ReqID: "{request_id}"]: Protection System updated successfully.')
    return response


@bp.route('/protection_systems/<int:id>', methods=['DELETE'])
def delete_protection_system(id):
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: DELETE Request received at "/protection_systems/{id}"')
    ps = ProtectionSystem.query.get_or_404(id)
    db.session.delete(ps)
    db.session.commit()
    data = {
        'status': 'OK',
        'message': 'Protection System deleted successfully.'
    }
    response = (jsonify(data), 200)
    logger.success(f'[ReqID: "{request_id}"]: Protection System deleted successfully.')
    return response
