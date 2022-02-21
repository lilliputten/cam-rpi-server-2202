# -*- coding:utf-8 -*-
# @module recordsStorage
# @desc Extendable (?) records storage engine
# @since 2022.02.15, 03:59
# @changed 2022.02.15, 04:16


import time

from src.lib.logger import DEBUG
from src.lib import utils


#  class Test_recordsStorage(unittest.TestCase):
#
#      def empty_recordsData(self):
#          self.assertEqual(recordsStorage.recordsData, [])

recordsData = []


def addRecord(ownerId='', recordId='', data={}):
    timestamp = time.time()
    recordData = {
        'timestamp': timestamp,
        'ownerId': ownerId,
        'recordId': recordId,
        'data': data,
    }
    #  fromId = '@:recordsStorage:addRecord'
    #  print(fromId, ownerId, data)
    DEBUG(utils.getTrace(), recordData)
    recordsData.append(recordData)
    return True


def findRecords(ownerId='', recordId=''):
    #  funcName = traceback.extract_stack(None, 2)[0][2]
    #  fromId = '@:recordsStorage:addRecord'
    #  print(fromId, ownerId, data)
    DEBUG(utils.getTrace(), {
        'ownerId': ownerId,
        'recordId': recordId,
    })
    #  recordsData.append(recordData)
    #  return True


__all__ = [  # Exporting objects...
    'addRecord',
]

if __name__ == '__main__':
    print(utils.getTrace(), 'debug run')
