# -*- coding:utf-8 -*-
# @module appSocketIO
# @since 2022.02.07, 00:27
# @changed 2022.02.12, 06:11

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from . import pathmagic  # noqa

from .app import app
from .logger import DEBUG
from flask_socketio import SocketIO


appSocketIO = SocketIO(app, cors_allowed_origins="*")

#  appSocketIO sample data:
#
#  async_mode: 'threading'
#  default_exception_handler: None
#  exception_handlers: {}
#  handlers: []
#  manage_session: True
#  namespace_handlers: []
#  server: <socketio.server.Server object at 0x052D37A8>
#  server_options: {'cors_allowed_origins': '*', 'async_mode': 'threading'}
#  sockio_mw: <flask_socketio._SocketIOMiddleware object at 0x056148F8>
#  wsgi_server: None
#  _handle_event: <bound method SocketIO._handle_event...>
#
#  function variables
#
#  - close_room
#  - emit
#  - event
#  - init_app
#  - on
#  - on_error
#  - on_error_default
#  - on_event
#  - on_namespace
#  - run
#  - send
#  - sleep
#  - start_background_task
#  - stop
#  - test_client

DEBUG('@:appSocketIO: starting', {
    'async_mode': appSocketIO.async_mode,
    'manage_session': appSocketIO.manage_session,
    'wsgi_server': appSocketIO.wsgi_server,
})

#  Log output from remote server:
#
#  [1644635348832 2022.02.12-06:09:08.832]
#  @:appSocketIO: starting
#    async_mode: gevent
#    manage_session: true
#    wsgi_server: null

__all__ = [  # Exporting objects...
    'appSocketIO',
]
