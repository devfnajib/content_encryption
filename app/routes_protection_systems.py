from flask import Blueprint, request, jsonify

bp = Blueprint('main', __name__)


@bp.route("/")
def index():
    data = {
        'status': 'OK'
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = (data, 200, headers)

    return response
