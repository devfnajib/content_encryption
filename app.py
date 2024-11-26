from flask import Flask


app = Flask(__name__)


@app.route("/")
def index():
    data = {
        'status': 'OK'
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = (data, 200, headers)

    return response
