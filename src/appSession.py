# -*- coding:utf-8 -*-
# @module appSession
# @since 2022.02.07, 00:27
# @changed 2022.02.15, 04:17

import uuid
import random
import datetime

from flask import session

from config import config

from src.core.lib.logger import DEBUG
from src.core.lib.logger import (
    getMsDateTag,
    getMsTimeStamp,
)

#  from src.core import RecordsStorage

useTimeStampInLastAccess = not config['isDev']
useSimplifiedSessionId = config['isDev']

#  # Test RecordsStorage...
#  recordsStorage = RecordsStorage()
#  DEBUG('@:appSession: starting', {
#      'addRecord': recordsStorage.addRecord,
#  })
#  recordsStorage.addRecord('test', {'test': 1})


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
    sessionId = session.get('sessionId', '')  # getSessionId('addExtendedSessionCookieToResponse')
    if sessionId:
        res.set_cookie('sessionId', sessionId)


__all__ = [  # Exporting objects...
    'session',
    'getSessionId',
]

if __name__ == '__main__':
    print('@:appSession: debug run')
