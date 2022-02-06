# -*- coding:utf-8 -*-
# @module server
# @since 2022.02.07, 00:27
# @changed 2022.02.07, 00:27

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
#  import .pathmagic  # noqa
#  from . import pathmagic  # noqa

import os
#  import traceback

#  from flask import current_app as app
from .app import app

#  from flask import redirect
from flask import render_template
#  from flask import url_for
#  from flask import jsonify
#  from flask import request

from config import config

from .logger import DEBUG

#  from .upload import uploadImage
#
#  import listImages
#  import imageUtils

#  from externalApi import externalApi


# NOTE: Logged twice with `* Restarting with stat`
DEBUG('Server started', {
    'FLASK_ENV': os.getenv('FLASK_ENV'),
    'buildTag': config['buildTag'],
})


#  app.register_blueprint(externalApi)


# Tests...


@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/user/<username>')
def profile(username):
    return 'User: %s' % username


# Errors processing...

@app.errorhandler(Exception)
def handle_error(e):
    #  errorType, errorValue, errorTraceback = sys.exc_info()
    #  @see https://docs.python.org/2/library/traceback.html
    #  errorTraceback = traceback.format_exc()
    error = str(e)
    #  errorRepr = e.__repr__()
    #  errorData = {
    #      'error': error,
    #      'repr': errorRepr,
    #      'traceback': str(errorTraceback)
    #  }
    #  DEBUG('server:Exception', errorData)
    #  return jsonify(errorData), getattr(e, 'code', 500)
    return render_template('error.html', error=error), getattr(e, 'code', 500)


if __name__ == '__main__':
    app.secret_key = 'hjAR5HUzijG04RJP3XIqUyy6M4IZhBrQ'
    app.logger.debug('test log')
    # app.debug = True
    app.run()
