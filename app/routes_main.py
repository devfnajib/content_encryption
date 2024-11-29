import logging
import traceback
from flask import Blueprint, request, jsonify
from loguru import logger
import shortuuid

from app.models import Content, Device, ProtectionSystem
from app.encryptions import decrypt


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    logger.info('Request received at "/"')
    data = {
        'status': 'OK'
    }

    response = (jsonify(data), 200)
    return response


@bp.route('/get_content')
def get_content():
    request_id = shortuuid.uuid()
    logger.info(f'[ReqID: "{request_id}"]: Request received at "/get_content"')
    request_payload = request.args
    logger.info(f'[ReqID: "{request_id}"]: Request payload: \n{request_payload}')
    content_id = request_payload.get('content_id', None)
    device_id = request_payload.get('device_id', None)
    content, device = None, None

    error_message, error_code = None, 400
    if content_id is None and device_id is None:
        error_message = '"content_id" and "device_id" are required fields.'
    elif content_id is None:
        error_message = '"content_id" is required field.'
    elif device_id is None:
        error_message = '"device_id" is required field.'

    if error_message is None:
        try:
            content = Content.query.get_or_404(content_id)
        except Exception as ex:
            error_message = 'No content found against "content_id": {}'.format(content_id)
            error_code = 404

        try:
            device = Device.query.get_or_404(device_id)
        except Exception as ex:
            error_message = 'No device found against "device_id": {}'.format(device_id)
            error_code = 404

        if error_message is None:
            if device.protection_system != content.protection_system:
                error_message = 'Device "{}" is not authorized to access this content.'.format(device.name)
                error_code = 401

    if error_message is not None:
        logger.warning(f'[ReqID: "{request_id}"]: {error_message}')
        data = {
            'status': 'Error',
            'error_message': error_message
        }

        response = (jsonify(data), error_code)
        return response

    ps = ProtectionSystem.query.get_or_404(content.protection_system)

    try:
        plain_content = decrypt(encryption_key=content.encryption_key, encryption_mode=ps.encryption_mode_code,
                                encryption_payload=content.encrypted_json)
    except Exception as ex:
        logger.error(f'[ReqID: "{request_id}"]: Error occurred: {ex.__str__()}')
        traceback.print_exc()
        data = {
            'status': 'Error',
            'error_message': ex.__str__()
        }

        response = (jsonify(data), 500)
        return response

    data = {
        'status': 'OK',
        'content': plain_content
    }

    response = (jsonify(data), 200)
    logger.success(f'[ReqID: "{request_id}"]: Request processed, returning response.')
    return response
