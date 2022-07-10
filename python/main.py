from flask import request, Flask, jsonify
from flask_cors import CORS
import random
import requests

app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
CORS(app)

url1 = "http://192.168.51.141:5555/fizzbuzz/while"  # 古本
url2 = "http://192.168.51.168:5555/fizzbuzz/while"  # 武藤さん
url3 = "http://192.168.51.169:5555/fizzbuzz/while"  # 田村さん
url4 = "http://127.0.0.1:5000/fizzbuzz/while"  # さきさん


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
        state[0] = "True"
    elif state[0] == "True" and fiz_num_return == "HACK":
        state[1] = "True"
    elif state[0] == "True" and state[1] == "True" and fiz_num_return == "365":
        state[2] = "True"
    else:
        state = ["False", "False", "False"]
    return state


def check_state_list(state, number):
    fiz_num_return = fizzbuzz_number(number)
    state = check_state(state, fiz_num_return)
    sec_state = state[0]
    hack_state = state[1]
    sanrokugo_state = state[2]
    return_number = int(number) + 1
    return sec_state, hack_state, sanrokugo_state, return_number


@app.route("/fizzbuzz/while", methods=['GET'])
def while_fizzbuzz():
    # http://127.0.0.1:5555/fizzbuzz/random
    sec_state = request.args.get('sec_state')
    hack_state = request.args.get('hack_state')
    sanrokugo_state = request.args.get('sanrokugo_state')
    number = request.args.get('number')
    state = [sec_state, hack_state, sanrokugo_state]
    sec_state, hack_state, sanrokugo_state, return_number = check_state_list(state, number)
    return jsonify(
        {"sec_state": sec_state, "hack_state": hack_state, "sanrokugo_state": sanrokugo_state,
         "number": return_number})


@app.route("/fizzbuzz/start", methods=['GET'])
def start():
    # http://127.0.0.1:5555/fizzbuzz/random
    number = random.randint(0, 1000)
    start_number = number
    sec_state = "False"
    hack_state = "False"
    sanrokugo_state = "False"
    urllist = [url4, url4, url4, url4]
    urlnum = 0
    payload = {"hack_state": hack_state, "sec_state": sec_state, "sanrokugo_state": sanrokugo_state, "number": number}

    while sec_state == "False" or hack_state == "False" or sanrokugo_state == "False":
        r = requests.get(urllist[urlnum], params=payload).json()
        sec_state = r["sec_state"]
        hack_state = r["hack_state"]
        sanrokugo_state = r["sanrokugo_state"]
        number = int(r["number"])
        payload = {"hack_state": hack_state, "sec_state": sec_state, "sanrokugo_state": sanrokugo_state,
                   "number": number}
        if urlnum == 3:
            urlnum = 0
        else:
            urlnum += 1
    return "success!!! \nstart number is " + str(start_number) + "\nfinish number is " + str(
        int(number) - 1) + "\nfinished by " + str(urllist[urlnum])


if __name__ == '__main__':
    app.debug = True
    app.run()
