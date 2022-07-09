from flask import request, Flask, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
CORS(app)


@app.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/")
def hello_mogunabi():
    return "<p>Hello, Mogu nabi!</p>"


if __name__ == '__main__':
    app.debug = True
    app.run()
