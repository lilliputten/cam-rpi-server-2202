# -*- coding:utf-8 -*-
# @module blueprintSession
# @desc Test camera shot api
# @since 2022.02.14, 03:01
# @changed 2022.02.14, 03:01

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
# from . import pathmagic  # noqa

from flask import jsonify
#  from flask import session
from flask import Blueprint
from flask import render_template
from flask import make_response
from . import appSession
#  from flask import redirect
#  from flask import url_for
#  from flask import request

#  from config import config

from .lib.logger import DEBUG

blueprintSession = Blueprint('blueprintSession', __name__)

#  # NOTE: Logged twice with `* Restarting with stat` in dev mode
#  DEBUG('@:blueprintSession: starting', {
#      #  'buildTag': config['buildTag'],
#      'appSession': str(appSession),
#  })


# Tests...

#  session.set('id', 123)

sharedVars = {
    'name': None,
}


@blueprintSession.route('/session/start')
def route_start():
    #  return '<p>Hello, World!</p>'
    #  return 'blueprintSession:route_root'
    #  name = 'guest'
    fromId = '@:blueprintSession:route_start'
    sessionId = appSession.getSessionId('route_start')
    name = appSession.session.get('name')
    data = {
        'fromId': fromId,
        'sessionId': sessionId,
        #  'name': name,
        'sharedVars.name': sharedVars['name'],
        'session:name': appSession.session.get('name'),
    }
    DEBUG(fromId, data)
    #  sharedVars['name'] = name
    #  appSession.session['name'] = name
    res = make_response(render_template('hello.html', name=name))
    appSession.addExtendedSessionCookieToResponse(res)
    return res


# Test cookies:
# wget -T 30 -t 1 -O- --save-headers --keep-session-cookies --save-cookies log-cookies-local.txt --load-cookies log-cookies-local.txt --progress=dot:default --no-check-certificate http://localhost:5000/session/set_name/aaa
# wget -T 30 -t 1 -O- --save-headers --keep-session-cookies --save-cookies log-cookies-remote.txt --load-cookies log-cookies-remote.txt --progress=dot:default --no-check-certificate https://cam-rpi-server.lilliputten.ru/session/set_name/aaa


@blueprintSession.route('/session/set_name/<name>')
def route_set_name(name=None):
    fromId = '@:blueprintSession:route_set_name'
    dataPre = {
        'pre:name': appSession.session.get('name'),
        'pre:sessionId': appSession.session.get('sessionId'),
        'pre:sessionNew': appSession.session.get('sessionNew'),
        'pre:sessionLastAccess': appSession.session.get('sessionLastAccess'),
    }
    sessionId = appSession.getSessionId('route_set_name')
    sessionNew = appSession.session.get('sessionNew')
    sessionLastAccess = appSession.session.get('sessionLastAccess')
    dataNew = {
        'fromId': fromId,
        'new:name': name,
        'new:sessionId': sessionId,
        'new:sessionNew': sessionNew,
        'new:sessionLastAccess': sessionLastAccess,
        #  'old sharedVars.name': sharedVars['name'],
        'old session:name': appSession.session.get('name'),
    }
    sharedVars['name'] = name
    appSession.session['name'] = name
    #  dataNew['newName'] = appSession.session.get('name')
    data = {**dataPre, **dataNew}
    DEBUG(fromId, data)
    res = jsonify(data)
    appSession.addExtendedSessionCookieToResponse(res)
    return res


@blueprintSession.route('/session/get_name')
def route_get_name():
    fromId = '@:blueprintSession:route_get_name'
    dataPre = {
        #  'pre:name': appSession.session.get('name'),
        'pre:sessionId': appSession.session.get('sessionId'),
        'pre:sessionNew': appSession.session.get('sessionNew'),
        'pre:sessionLastAccess': appSession.session.get('sessionLastAccess'),
    }
    name = appSession.session.get('name')
    sessionId = appSession.getSessionId('route_get_name')
    sessionNew = appSession.session.get('sessionNew')
    sessionLastAccess = appSession.session.get('sessionLastAccess')
    dataNew = {
        'fromId': fromId,
        'name': name,
        'new:sessionId': sessionId,
        'new:sessionNew': sessionNew,
        'new:sessionLastAccess': sessionLastAccess,
        #  'old sharedVars.name': sharedVars['name'],
        #  'old session:name': appSession.session.get('name'),
    }
    data = {**dataPre, **dataNew}
    DEBUG(fromId, data)
    res = jsonify(data)
    appSession.addExtendedSessionCookieToResponse(res)
    return res


__all__ = [  # Exporting objects...
    'blueprintSession',
]

if __name__ == '__main__':
    DEBUG('@:blueprintSession: debug run')
