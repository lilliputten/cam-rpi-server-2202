# -*- coding:utf-8 -*-
# @module serverUtils
# @desc Helper soutines for server.
# @since 2022.02.12, 02:41
# @changed 2022.02.12, 02:41

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
# from . import pathmagic  # noqa

import traceback

from flask import redirect
from flask import jsonify
#  from flask import render_template
#  from flask import request
#  from config import config
from src.lib.logger import DEBUG
from src.lib import errors


def server_handle_not_found(err):
    # TODO: Determine not found page url
    error = errors.toString(err)
    #  errorRepr = err.__repr__()
    code = getattr(err, 'code', 404)
    errorData = {
        'code': code,
        'error': error,
        #  'repr': errorRepr,
    }
    DEBUG('@:server:errorhandler(404):server_handle_not_found', errorData)
    return jsonify(errorData), code
    #  return render_template('error-not-found.html', error=error), code


def server_handle_exception(err):
    #  errorType, errorValue, errorTraceback = sys.exc_info()
    #  @see https://docs.python.org/2/library/traceback.html
    #  code = err.code if hasattr(err, 'code') else None  # http response code (if http error)
    code = getattr(err, 'code', 500)
    if code:  # Skip non-errors...
        if code == 308 and err.new_url:  # Skip redirect errors...
            new_url = err.new_url
            DEBUG('@:server:errorhandler(Exception):server_handle_exception: redirect', {
                'code': code,
                'new_url': new_url,
                'error': err,
            })
            return redirect(new_url)
        # TODO: Other non-errors?
        #  if code >= 200 and code < 400:
    errorTraceback = traceback.format_exc()
    error = errors.toString(err)
    #  errorRepr = err.__repr__()
    errorData = {
        'code': code,
        'error': error,
        #  'repr': errorRepr,
        'traceback': str(errorTraceback)
    }
    DEBUG('@:server:errorhandler(Exception):server_handle_exception', errorData)
    return jsonify(errorData), code
    #  return render_template('error.html', error=error), code


if __name__ == '__main__':
    DEBUG('@:serverUtils: debug run')
