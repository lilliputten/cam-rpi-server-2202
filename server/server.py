# -*- coding:utf-8 -*-
# @module server
# @since 2022.02.07, 00:27
# @changed 2022.02.08, 06:11

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from . import pathmagic  # noqa

import os
import traceback

#  from werkzeug import HTTP_STATUS_CODES
#  from werkzeug.exceptions import HTTPException

#  from flask import current_app as app
from .app import app

from flask import redirect
from flask import render_template
#  from flask import url_for
#  from flask import jsonify
#  from flask import request

from config import config

from .logger import DEBUG
from . import errors

from . import raspistillUtils

#  from .upload import uploadImage
#
#  import listImages
#  import imageUtils

#  from externalApi import externalApi


env = os.getenv('FLASK_ENV')
isDev = env == 'development'
run_main = os.environ.get('WERKZEUG_RUN_MAIN')
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
    #  'HTTP_STATUS_CODES': HTTP_STATUS_CODES,
})

if doInit:  # NOTE: Initializing only once...

    #  app.register_blueprint(externalApi)

    # Tests...

    @app.route('/')
    def route_root():
        #  return '<p>Hello, World!</p>'
        return 'route_root'
        #  name = 'guest'
        #  return render_template('hello.html', name=name)

    @app.route('/shot/')
    def route_shot():
        shotFileName = raspistillUtils.makeShot(debug=False)
        return raspistillUtils.sendImageFile(shotFileName)

    @app.route('/hello/')
    @app.route('/hello/<name>')
    def route_hello(name=None):
        return render_template('hello.html', name=name)

    @app.route('/user/<username>')
    def route_user(username):
        return 'Raw html: User: %s' % username

    # Errors processing...

    @app.errorhandler(404)
    def handle_not_found(err):
        # TODO: Determine not found page url
        error = errors.toString(err)
        errorRepr = err.__repr__()
        errorData = {
            'error': error,
            'repr': errorRepr,
        }
        DEBUG('server:errorhandler(404):handle_not_found', errorData)
        #  return jsonify(errorData), getattr(err, 'code', 500)
        return render_template('error-not-found.html', error=error), getattr(err, 'code', 404)

    @app.errorhandler(Exception)
    def handle_exception(err):
        #  errorType, errorValue, errorTraceback = sys.exc_info()
        #  @see https://docs.python.org/2/library/traceback.html
        code = err.code if hasattr(err, 'code') else None  # http response code (if http error)
        errorTraceback = traceback.format_exc()
        error = errors.toString(err)
        errorRepr = err.__repr__()
        errorData = {
            'code': code,
            'error': error,
            'repr': errorRepr,
            'traceback': str(errorTraceback)
        }
        if code:  # Skip non-errors...
            if code == 308 and err.new_url:  # Skip redirect errors...
                DEBUG('server:errorhandler(Exception):handle_exception: redirect', errorData)
                return redirect(err.new_url)
            # TODO: Other non-errors?
            #  if code >= 200 and code < 400:
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
