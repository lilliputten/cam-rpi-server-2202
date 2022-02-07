# -*- coding: utf-8 -*-
# vim: ft=python:
# @module index.wsgi
# @desc Local server start script
# @since 2022.02.07, 21:30
# @changed 2022.02.07, 21:30

import sys
import os

#  # Activate venv...
#  venv = 'venv-py3-flask'  # Python 3.6
#  #  venv = 'virtualenv'  # Default
#  #  venv = 'venv-flask'  # Python 2.7
#  activate_this = '/home/g/goldenjeru/.' + venv + '/bin/activate_this.py'
#  with open(activate_this) as f:
#      code = compile(f.read(), activate_this, 'exec')
#      exec(code, dict(__file__=activate_this))

# Add application path...
rootPath = os.path.dirname(os.path.abspath(__file__))  # From index.wsgi
sys.path.insert(1, rootPath)  # /home/g/goldenjeru/lilliputten.ru/cam-rpi-server/

# Start application...
from server.server import app as application  # noqa

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
