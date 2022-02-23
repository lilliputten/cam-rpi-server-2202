# -*- coding:utf-8 -*-
# @module Record
# @desc Extendable (?) records storage engine
# @since 2022.02.22, 01:47
# @changed 2022.02.24, 00:34


import time

from src.core.lib.logger import DEBUG
from src.core.lib import utils


class Record():

    timestamp: None
    ownerId = None
    recordId = None
    data = None

    def __init__(self, timestamp=None, ownerId=None, recordId=None, data=None):
        if not timestamp:
            timestamp = time.time()
        self.timestamp = timestamp
        self.ownerId = ownerId
        self.recordId = recordId
        self.data = data
        #  DEBUG(utils.getTrace(), {
        #      'timestamp': timestamp,
        #      'ownerId': ownerId,
        #      'recordId': recordId,
        #      'data': data,
        #  })


__all__ = [  # Exporting objects...
    'Record',
]


if __name__ == '__main__':
    DEBUG(utils.getTrace(' debug run'))
