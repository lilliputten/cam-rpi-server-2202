# -*- coding:utf-8 -*-
# @module appSocketIO
# @since 2022.02.07, 00:27
# @changed 2022.02.07, 00:27

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from . import pathmagic  # noqa

from .app import app
#  import os
#  from flask import Flask
#  from config import config
#  from werkzeug.routing import BaseConverter
from .logger import DEBUG
#  from flask_socketio import send
from flask_socketio import SocketIO
#  from flask_socketio import emit
#  from flask_socketio import join_room


appSocketIO = SocketIO(app, cors_allowed_origins="*")

DEBUG('@:appSocketIO: starting', {
})


__all__ = [  # Exporting objects...
    'appSocketIO',
]
