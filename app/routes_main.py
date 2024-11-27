import os
from flask import Blueprint, jsonify


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    data = {
        'status': 'OK'
    }

    response = (jsonify(data), 200)
    return response
