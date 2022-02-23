# -*- coding:utf-8 -*-
# @module blueprintShot
# @desc Test camera shot api
# @since 2022.02.12, 01:46
# @changed 2022.02.12, 01:46

from flask import Blueprint
#  from flask import redirect
#  from flask import render_template
#  from flask import url_for
#  from flask import jsonify
#  from flask import request

from config import config

from src.core.lib.logger import DEBUG

from . import raspistillUtils

blueprintShot = Blueprint('blueprintShot', __name__)

#  # NOTE: Logged twice with `* Restarting with stat` in dev mode
#  DEBUG('@:blueprintShot: starting', {
#      'buildTag': config['buildTag'],
#  })

# Tests...


@blueprintShot.route('/shot/')
def route_shot():
    """
    Test make shot.
    """
    #  NOTE: Use command for server test reequests:
    # `wget -O- --progress=dot:default --no-check-certificate http://localhost:5000/shot/`
    debug = config['isDev']
    shotFileName = raspistillUtils.makeShot(debug=debug)
    return raspistillUtils.sendImageFile(shotFileName)


__all__ = [  # Exporting objects...
    'blueprintShot',
]

if __name__ == '__main__':
    DEBUG('@:blueprintShot: debug run')
