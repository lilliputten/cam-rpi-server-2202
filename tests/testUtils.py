# -*- coding:utf-8 -*-
# @module testUtils
# @since 2022.02.15, 05:02
# @changed 2022.02.15, 05:02

import traceback

def getTrace(str=None):
    # NOTE: Required to pass extracted traceback
    funcName = traceback.extract_stack(None, 2)[0][2]
    strList = [
        __name__,
        funcName,
        '',
    ]
    return ':'.join(strList)
