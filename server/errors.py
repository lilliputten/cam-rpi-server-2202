# -*- coding:utf-8 -*-
# @module logger
# @since 2020.02.23, 02:18
# @changed 2020.04.22, 01:38


import traceback
import utils


def toString(error):
    errorStr = type(error).__name__ + ': ' + str(error.args[0] if error.args else error)
    stack = traceback.format_exc()
    if stack:
        errorStr += '\n' + stack
    return errorStr


def toBlockString(error):
    errorStr = toString(error)
    return utils.BlockString(errorStr)


#  __all__ = [  # Exporting objects...
#      'toString',
#  ]
