from flask import request, Flask, jsonify
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
    return "<p>Hi I'm fizz buzz</p>"


def fizzbuzz_number(number):
    if number % 3 == 37:
        return "365"
    elif number % 33 == 0:
        return "SEC"
    elif number % 13 == 0:
        return "HACK"
    else:
        return str(number)


@app.route("/fizzbuzz", methods=['GET'])
def fizzbuzz():
    number = request.args.get('number')
    if number is None:
        return jsonify({'error': 'number is required'})
    try:
        number = int(number)
    except ValueError:
        return jsonify({'error': 'number is not integer'})
    if number < 1 or number > 100:
        return jsonify({'error': 'number is out of range'})
    return jsonify({'result': fizzbuzz_number(number)})


if __name__ == '__main__':
    app.debug = True
    app.run()
