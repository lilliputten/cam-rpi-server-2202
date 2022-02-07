# -*- coding: utf-8 -*-
# vim: ft=python:
# @module index.wsgi
# @since 2019.03.28, 21:32
# @changed 2022.02.07, 05:22

import sys
import os

venv = 'venv-py3-flask'  # Python 3.6
#  venv = 'virtualenv'  # Default
#  venv = 'venv-flask'  # Python 2.7

# Activate venv...
activate_this = '/home/g/goldenjeru/.' + venv + '/bin/activate_this.py'
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))

# Add application path...
rootPath = os.path.dirname(os.path.abspath(__file__))  # From index.wsgi
sys.path.insert(1, rootPath)  # /home/g/goldenjeru/lilliputten.ru/cam-rpi-server/

# Start application...
from server.server import app as application  # noqa
