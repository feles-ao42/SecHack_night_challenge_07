from flask import request, Flask, jsonify
from flask_cors import CORS
import random
import requests

app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
CORS(app)

url = "http://127.0.0.1:5555/fizzbuzz/while"
payload = {"state": "false,false,false,784"}


@app.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


def fizzbuzz_number(number):
    number = int(number)
    if number % 73 == 0:
        return "365"
    elif number % 33 == 0:
        return "SEC"
    elif number % 13 == 0:
        return "HACK"
    else:
        return str(number)


def check_state(state, fiz_num_return):
    if fiz_num_return == "SEC":
        state[0] = True
    elif state[0] == True and fiz_num_return == "HACK":
        state[1] = True
    elif state[0] and state[1] and fiz_num_return == "365":
        state[2] = True
    else:
        state = [False, False, False, fiz_num_return]
    return state


@app.route("/")
def hello_mogunabi():
    return "<p>Hi I'm fizz buzz</p>"


@app.route("/fizzbuzz", methods=['GET'])
def fizzbuzz():
    # http://127.0.0.1:5555/fizzbuzz?number=37
    number = request.args.get('number')
    if number is None:
        return jsonify({'error': 'number is required'})
    try:
        number = int(number)
    except ValueError:
        return jsonify({'error': 'number is not integer'})
    if number < 1 or number > 1000:
        return jsonify({'error': 'number is out of range'})
    return jsonify({'result': fizzbuzz_number(number)})


@app.route("/fizzbuzz/test", methods=['GET'])
def test_fixxbuzz():
    # http://127.0.0.1:5555/fizzbuzz/random
    number = random.randint(1, 1000)
    old_num = number
    state = [False, False, False]
    while state[0] == False or state[1] == False or state[2] == False:
        fiz_num_return = fizzbuzz_number(number)
        state = check_state(state, fiz_num_return)
        number += 1
    return jsonify(old_num, number)


@app.route("/fizzbuzz/while", methods=['GET'])
def while_fizzbuzz():
    # http://127.0.0.1:5555/fizzbuzz/random
    state = request.args.get('state')
    state = state.split(",")
    fiz_num_return = fizzbuzz_number(state[3])
    state = check_state(state, fiz_num_return)
    return_number = int(state[3]) + 1
    return_state = [state[0], state[1], state[2], return_number]
    return jsonify(return_state)


@app.route("/fizzbuzz/start", methods=['GET'])
def start():
    # http://127.0.0.1:5555/fizzbuzz/random
    number = random.randint(1, 1000)
    state = [False, False, False, number]
    r = requests.get(url, params=payload)
    return r.text


if __name__ == '__main__':
    app.debug = True
    app.run()
