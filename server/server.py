# -*- coding:utf-8 -*-
# @module server
# @since 2022.02.07, 00:27
# @changed 2022.02.08, 01:50

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from . import pathmagic  # noqa

import os
import traceback

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


env = os.getenv('FLASK_ENV')
isDev = env == 'development'
run_main = os.environ.get("WERKZEUG_RUN_MAIN")
isMain = run_main == 'true'
doInit = not isDev or isMain
#  run_main = False
#  if env == 'development' and os.environ.get("WERKZEUG_RUN_MAIN") == "true":
#      run_main = True


# NOTE: Logged twice with `* Restarting with stat`
DEBUG('Server started', {
    'doInit': doInit,
    'isDev': isDev,
    'isMain': isMain,
    'env': env,
    'run_main': run_main,
    #  'FLASK_ENV': os.getenv('FLASK_ENV'),
    'buildTag': config['buildTag'],
})


if doInit:  # NOTE: Initializing only once...

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

    @app.errorhandler(404)
    def handle_not_found(err):
        #  return render_template('404.html'), 404
        #  errorTraceback = traceback.format_exc()
        error = str(err)
        errorRepr = err.__repr__()
        errorData = {
            'error': error,
            'repr': errorRepr,
            #  'traceback': str(errorTraceback)
        }
        DEBUG('server:errorhandler(404):handle_not_found', errorData)
        #  return jsonify(errorData), getattr(err, 'code', 500)
        return render_template('error-not-found.html', error=error), getattr(err, 'code', 404)

    @app.errorhandler(Exception)
    def handle_exception(err):
        #  errorType, errorValue, errorTraceback = sys.exc_info()
        #  @see https://docs.python.org/2/library/traceback.html
        errorTraceback = traceback.format_exc()
        error = str(err)
        errorRepr = err.__repr__()
        errorData = {
            'error': error,
            'repr': errorRepr,
            'traceback': str(errorTraceback)
        }
        DEBUG('server:errorhandler(Exception):handle_exception', errorData)
        #  return jsonify(errorData), getattr(err, 'code', 500)
        return render_template('error.html', error=error), getattr(err, 'code', 500)


if __name__ == '__main__':
    app.secret_key = 'hjAR5HUzijG04RJP3XIqUyy6M4IZhBrQ'
    #  print('server:__main__')
    #  app.logger.debug('test log')
    # app.debug = True
    #  if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    app.run()
