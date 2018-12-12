from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

from data import run

import time
import json


query_param = {
                       'explvl': 'entry_level',
                       'l': 'new+york',
                       'q': 'python+software+engineer',
                       'jt': 'fulltime'
                    }


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socket_io = SocketIO(app)

ASK = [("What job role are you looking for?", 'q'),
       ("What is you level of experience? (entry, mid or senior)", 'explvl'),
       ("Are you looking for a full time, part time or an internship position", 'jt'),
       ("Which city would you like to work at?", 'l')]

DATA = {}


def parse_data():
    DATA['q'] = DATA['q'].replace(' ', '+').lower()
    DATA['explvl'] = f"{DATA['explvl'].lower()}_level"
    DATA['jt'] = DATA['jt'].replace(' ', '').lower()
    DATA['l'] = DATA['l'].replace(' ', '+').lower()

    print('hey yo!')


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
            emit('message', sdata)
            break
    else:
        emit('over', 'Hold on, searching appropriate job roles that you could apply to')
        parse_data()


if __name__ == '__main__':
    socket_io.run(app)

