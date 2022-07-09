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


def fizzbuzz_number(number):
    if number % 73 == 0:
        return "365"
    elif number % 33 == 0:
        return "SEC"
    elif number % 13 == 0:
        return "HACK"
    else:
        return str(number)


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


@app.route("/fizzbuzz/random", methods=['GET'])
def make_random_int():
    # http://127.0.0.1:5555/fizzbuzz/random
    import random
    number = random.randint(1, 1000)
    old_num = number
    state = [False, False, False]
    while state[0] == False or state[1] == False or state[2] == False:
        fiz_num_return = fizzbuzz_number(number)
        if fiz_num_return == "SEC":
            state[0] = True
        elif state[0] == True and fiz_num_return == "HACK":
            state[1] = True
        elif state[0] and state[1] and fiz_num_return == "365":
            state[2] = True
        else:
            state = [False, False, False]
        number += 1
    return jsonify(old_num,number)


if __name__ == '__main__':
    app.debug = True
    app.run()
