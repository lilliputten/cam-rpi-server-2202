# -*- coding: utf-8 -*-
# vim: ft=python:
# @module index.wsgi
# @since 2019.03.28, 21:32
# @changed 2020.07.04, 01:47

import sys
#  impor os

activate_this = '/home/g/goldenjeru/.venv-flask/bin/activate_this.py'
#  activate_this = '/home/g/goldenjeru/.venv-py3-flask/bin/activate_this.py'
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))

sys.path.insert(1, '/home/g/goldenjeru/lilliputten.ru/cam-rpi-server/')

#  # Modified code
#  activate_this = '/home/g/goldenjeru/.venv-py3-flask/bin/activate_this.py'
#  with open(activate_this) as f:
#      code = compile(f.read(), activate_this, 'exec')
#      exec(code, dict(__file__=activate_this))
#
#  rootPath = os.path.dirname(os.path.abspath(__file__))  # From index.wsgi
#
#  sys.path.insert(1, rootPath)

from server.server import app as application  # noqa
