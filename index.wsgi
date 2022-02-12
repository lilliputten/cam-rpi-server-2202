# -*- coding: utf-8 -*-
# vim: ft=python:
# @module index.wsgi
# @desc Fullspace hosting server start script
# @since 2019.03.28, 21:32
# @changed 2022.02.07, 21:27

# NOTE: Try to fix genvent/greenlet bug
#  greenlet.error: cannot switch to a different thread
#  gevent.hub.LoopExit: ('This operation would block forever', <Hub at 0x7f7ed4449508 epoll default pending=0>)
#  @see [greenlet.error: cannot switch to a different thread · Issue #65 · miguelgrinberg/Flask-SocketIO](https://github.com/miguelgrinberg/Flask-SocketIO/issues/65)
#  from gevent import monkey
#  monkey.patch_all()

import sys  # noqa
import os  # noqa

venv = 'venv-py3-flask'  # Python 3.6
#  venv = 'virtualenv'  # Default
#  venv = 'venv-flask'  # Python 2.7

# Activate venv...
activate_this = '/home/g/goldenjeru/.' + venv + '/bin/activate_this.py'
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))

# TODO: Reuse `index.py`?

# Inject application path...
rootPath = os.path.dirname(os.path.abspath(__file__))  # From index.wsgi
sys.path.insert(1, rootPath)  # /home/g/goldenjeru/lilliputten.ru/cam-rpi-server/

# Start application...
from server.server import app as application  # noqa

__all__ = [  # Exporting objects...
    'application',
]
