# -*- coding:utf-8 -*-
# @module blueprintTest
# @desc Test camera shot api
# @since 2022.02.12, 01:46
# @changed 2022.02.12, 01:46

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from . import pathmagic  # noqa

from flask import Blueprint
from flask import render_template
#  from flask import redirect
#  from flask import render_template
#  from flask import url_for
#  from flask import jsonify
#  from flask import request

from config import config

from .logger import DEBUG


blueprintTest = Blueprint('blueprintTest', __name__)


# NOTE: Logged twice with `* Restarting with stat` in dev mode
DEBUG('@:blueprintTest: starting', {
    'buildTag': config['buildTag'],
})

# Tests...


@blueprintTest.route('/')
def route_root():
    #  return '<p>Hello, World!</p>'
    return 'route_root'
    #  name = 'guest'
    #  return render_template('hello.html', name=name)


@blueprintTest.route('/hello/')
@blueprintTest.route('/hello/<name>')
def route_hello(name=None):
    return render_template('hello.html', name=name)


@blueprintTest.route('/user/<username>')
def route_user(username):
    return 'Raw html: User: %s' % username


__all__ = [  # Exporting objects...
    'blueprintTest',
]

if __name__ == '__main__':
    DEBUG('@:blueprintTest: debug run')
