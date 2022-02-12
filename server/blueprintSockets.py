# -*- coding:utf-8 -*-
# @module blueprintSockets
# @desc Test camera shot api
# @since 2022.02.12, 01:46
# @changed 2022.02.12, 01:46

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from . import pathmagic  # noqa

from .app import app
from flask import Blueprint
#  from flask import render_template
from flask import jsonify
#  from flask import redirect
from flask import render_template
#  from flask import url_for
#  from flask import request
from flask_socketio import send, SocketIO, emit, join_room
from config import config

from .logger import DEBUG


blueprintSockets = Blueprint('blueprintSockets', __name__)

socketio = SocketIO(app, cors_allowed_origins="*")

# NOTE: Logged twice with `* Restarting with stat` in dev mode
DEBUG('@:blueprintSockets: starting', {
    'buildTag': config['buildTag'],
    #  'socketio': socketio,
})


# Tests...


@socketio.on('join')
def client_join_room(data):
    print(type(data))
    DEBUG('@:blueprintSockets:client_join_room', {
        'data': data,
    })
    room = data['room']
    join_room(room)
    send('you have entered the room.', room=room)


@blueprintSockets.route('/sockets/start')
@blueprintSockets.route('/sockets/start/<name>')
def sockets_test(name=None):
    #  socketio.emit('message', 'Message: name: ' + str(name), room='my_room', broadcast=True)
    #  data = {'name': name}
    #  return jsonify(data)
    return render_template('sockets.html', name=name)


@blueprintSockets.route('/sockets/msg/')
@blueprintSockets.route('/sockets/msg/<name>')
def send_message(name=None):
    socketio.emit('message', 'Server: name: ' + name, room='my_room', broadcast=True)
    data = {'name': name}
    return jsonify(data)


__all__ = [  # Exporting objects...
    'blueprintSockets',
]

if __name__ == '__main__':
    DEBUG('@:blueprintSockets: debug run')
