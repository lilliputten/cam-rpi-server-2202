# -*- coding:utf-8 -*-
# @module appSession
# @since 2022.02.07, 00:27
# @changed 2022.02.12, 06:11

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from . import pathmagic  # noqa
from config import config

import uuid
import random

#  from .app import app
import datetime
from .logger import (
    DEBUG,
    getMsDateTag,
    getMsTimeStamp,
)
from flask import session

useTimeStampInLastAccess = not config['isDev']
useSimplifiedSessionId = config['isDev']

#  DEBUG('@:appSession: starting', {
#  })


def getSessionId(callerId):
    sessionId = session.get('sessionId')
    now = datetime.datetime.now()  # Get current date object
    timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
    dateTag = getMsDateTag(now)
    if not sessionId:
        sesseionIdValue = random.randint(100000, 10000000) if useSimplifiedSessionId else uuid.uuid4()
        sessionId = dateTag + '-' + str(sesseionIdValue)
        DEBUG('@:appSession:getSessionId: new session id', {
            'callerId': callerId,
            'sessionId': sessionId,
            #  'sessionIdObj': sessionIdObj,
        })
        session['sessionId'] = sessionId
        session['sessionNew'] = True
    else:
        DEBUG('@:appSession:getSessionId: using exists session id', {
            'callerId': callerId,
            'sessionId': sessionId,
        })
        session['sessionNew'] = False
    #  sessionLastAccess = str(timestamp) + ' ' + dateTag
    sessionLastAccess = (str(timestamp) + ' ' if useTimeStampInLastAccess else '') + dateTag
    session['sessionLastAccess'] = sessionLastAccess
    return sessionId


def addExtendedSessionCookieToResponse(res):
    sessionId = session.get('sessionId')  # getSessionId('addExtendedSessionCookieToResponse')
    res.set_cookie('sessionId', sessionId)


__all__ = [  # Exporting objects...
    'session',
    'getSessionId',
]
