from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

from data import get_jobs

import time
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socket_io = SocketIO(app)

# TODO: replace with a queue
# TODO: use AIML to overhaul the logic
ASK = [("What job role are you looking for?", 'q'),
       ("What is you level of experience? (entry, mid or senior)", 'explvl'),
       ("Are you looking for a full time, part time or an internship position?", 'jt'),
       ("With a salary expectation of..?", 'q2'),
       ("Which city would you like to work at?", 'l'),
       ("Any other relevant keywords that you would want me to keep in mind?", 'keywords')]

DATA = {}


@app.route('/')
def index():
    return render_template('index.html')


def parse_data():
    query = DATA['keywords'] + DATA['l'] + ' ' + DATA['q']

    DATA['q2'] = '$' + DATA['q2'] if '$' not in DATA['q2'] else DATA['q2']
    DATA['q'] = DATA['q'].replace(' ', '+').lower()
    DATA['explvl'] = f"{DATA['explvl'].lower()}_level"
    DATA['jt'] = DATA['jt'].replace(' ', '').lower()
    DATA['l'] = DATA['l'].replace(' ', '+').lower()
    DATA['keywords'] = DATA['keywords'].lower()

    if DATA['keywords'].lower() == 'no':
        del DATA['keywords']

    res = get_jobs(query, DATA)

    if not res:
        emit('result', json.dumps({'text': f"Your job query dint throw up anything, check another time"}))
    else:
        emit('result', json.dumps({'text': f"Relevant jobs - {' '.join(res)}"}))


@socket_io.on('init')
def handle_my_custom_event(jval):

    if jval['connected']:
        emit('hey', 'Hi, my name is Cecil')

        time.sleep(1)

        sdata = json.dumps({'question': ["What job role are you looking for?", 'q']})

        emit('message', sdata)


@socket_io.on('message')
def handle_conversation(msg):
    DATA.update(msg)

    for idx, val in enumerate(ASK):

        if val[-1] not in DATA:
            sdata = json.dumps({'question': list(val)})

            time.sleep(2)

            emit('message', sdata)
            break
    else:
        emit('get relevant', 'Hold on, searching appropriate job roles that would be a great fit for you, '
                             'this might about 10 seconds though')
        parse_data()


if __name__ == '__main__':
    socket_io.run(app)

