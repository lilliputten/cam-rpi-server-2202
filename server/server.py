# -*- coding:utf-8 -*-
# @module server
# @since 2022.02.07, 00:27
# @changed 2022.02.12, 02:57

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from . import pathmagic  # noqa

import os

#  from externalApi import externalApi
#  from flask import jsonify
#  from flask import redirect
#  from flask import render_template
#  from flask import request
#  from flask import url_for
#  import imageUtils
#  import listImages
from config import config
from .app import app
from .logger import DEBUG
from . import serverUtils
from .blueprintTest import blueprintTest
from .blueprintShot import blueprintShot


run_main = os.environ.get('WERKZEUG_RUN_MAIN')
isMain = run_main == 'true'
doInit = not config['isDev'] or isMain

if doInit:  # NOTE: Initializing only once (avoiding double initialization with `* Restarting with stat`...)

    DEBUG('@:server: starting', {
        'doInit': doInit,
        'isDev': config['isDev'],
        'isMain': isMain,
        'env': config['env'],
        'run_main': run_main,
        #  'FLASK_ENV': os.getenv('FLASK_ENV'),
        'buildTag': config['buildTag'],
        #  'HTTP_STATUS_CODES': HTTP_STATUS_CODES,
    })

    #  Register blueprint apis...

    app.register_blueprint(blueprintTest)
    app.register_blueprint(blueprintShot)

    # Errors handling...

    @app.errorhandler(404)
    def handle_not_found(err):
        return serverUtils.server_handle_not_found(err)

    @app.errorhandler(Exception)
    def handle_exception(err):
        return serverUtils.server_handle_exception(err)


if __name__ == '__main__':
    app.secret_key = 'hjAR5HUzijG04RJP3XIqUyy6M4IZhBrQ'
    #  print('server:__main__')
    #  app.logger.debug('test log')
    # app.debug = True
    #  if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    app.run()
