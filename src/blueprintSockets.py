# -*- coding:utf-8 -*-
# @module blueprintSockets
# @desc Test camera shot api
# @since 2022.02.12, 01:46
# @changed 2022.02.14, 00:58

# NOTE 2022.02.14, 00:57 -- Sockets is unused due to remote-server installation
# issues (gevent and eventlet cannot be correctly installed in shared apache
# hosting).

from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask_socketio import send
from flask_socketio import join_room
#  from flask import render_template
#  from flask import redirect
#  from flask import url_for
#  from flask import request

from config import config

from src.core.lib.logger import DEBUG

from .appSocketIO import appSocketIO


blueprintSockets = Blueprint('blueprintSockets', __name__)

# NOTE: Logged twice with `* Restarting with stat` in dev mode
DEBUG('@:blueprintSockets: starting', {
    'buildTag': config['buildTag'],
    #  'appSocketIO': appSocketIO,
})


useBroadcast = False


@appSocketIO.on('join')
def sockets_on_join(data):
    room = data['room']
    sendData = {'from': '@:blueprintSockets:sockets_on_join', 'data': data, 'room': room}
    DEBUG('@:blueprintSockets:sockets_on_join', sendData)
    join_room(room)
    send(sendData, room=room)


@blueprintSockets.route('/sockets/start')
@blueprintSockets.route('/sockets/start/<name>')
def sockets_start(name=None):
    data = {'from': '@:blueprintSockets:sockets_start', 'name': name}
    DEBUG('@:blueprintSockets:sockets_start', data)
    appSocketIO.emit('message', data, room='my_room', broadcast=useBroadcast)
    #  return jsonify(data)
    return render_template('sockets.html', name=name)


@blueprintSockets.route('/sockets/msg/')
@blueprintSockets.route('/sockets/msg/<msg>')
def sockets_msg(msg=None):
    data = {'from': '@:blueprintSockets:sockets_msg', 'msg': msg}
    DEBUG('@:blueprintSockets:sockets_msg: before emit', data)
    appSocketIO.emit('message', data, room='my_room', broadcast=useBroadcast)
    DEBUG('@:blueprintSockets:sockets_msg: after emit', data)
    return jsonify(data)


__all__ = [  # Exporting objects...
    'blueprintSockets',
]

if __name__ == '__main__':
    DEBUG('@:blueprintSockets: debug run')
