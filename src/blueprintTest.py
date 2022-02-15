# -*- coding:utf-8 -*-
# @module blueprintTest
# @desc Test camera shot api
# @since 2022.02.12, 01:46
# @changed 2022.02.12, 01:46

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
# from . import pathmagic  # noqa

#  from flask import Blueprint
#  from flask import render_template
#  from flask import session
from flask import Blueprint
#  from flask import redirect
from flask import render_template
#  from flask import url_for
#  from flask import jsonify
#  from flask import request

#  from config import config

from .lib.logger import DEBUG
#  from .app import app

#  from flask import session

#  session.init_app(app)

blueprintTest = Blueprint('blueprintTest', __name__)

#  # NOTE: Logged twice with `* Restarting with stat` in dev mode
#  DEBUG('@:blueprintTest: starting', {
#      'buildTag': config['buildTag'],
#  })


# Tests...


sharedVars = {
    'name': None,
}


@blueprintTest.route('/<name>')
def route_root(name=None):
    #  return '<p>Hello, World!</p>'
    fromId = '@:blueprintTest:route_root'
    data = {
        'fromId': fromId,
        'name': name,
    }
    DEBUG(fromId, data)
    #  return 'blueprintTest:route_root: ' + session.get('name', '')
    return render_template('hello.html', name=name)


@blueprintTest.route('/user/<name>')
def route_user(name):
    return 'blueprintTest: Raw html: User: %s' % name
    #  res = jsonify(data)
    #  return res


__all__ = [  # Exporting objects...
    'blueprintTest',
]

if __name__ == '__main__':
    DEBUG('@:blueprintTest: debug run')
