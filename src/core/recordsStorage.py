# -*- coding:utf-8 -*-
# @module recordsStorage
# @desc Extendable (?) records storage engine
# @since 2022.02.15, 03:59
# @changed 2022.02.15, 04:16


import time

from src.lib.logger import DEBUG


#  class Test_recordsStorage(unittest.TestCase):
#
#      def empty_recordsData(self):
#          self.assertEqual(recordsStorage.recordsData, [])

recordsData = []


def addRecord(ownerId, data):
    timestamp = time.time()
    recordData = {
        'timestamp': timestamp,
        'ownerId': ownerId,
        'data': data,
    }
    fromId = '@:recordsStorage:addRecord'
    #  print(fromId, ownerId, data)
    DEBUG(fromId, recordData)
    recordsData.append(recordData)
    return True


def findRecord(ownerId, data):
    timestamp = time.time()
    recordData = {
        'timestamp': timestamp,
        'ownerId': ownerId,
        'data': data,
    }
    fromId = '@:recordsStorage:addRecord'
    #  print(fromId, ownerId, data)
    DEBUG(fromId, recordData)
    recordsData.append(recordData)
    return True


#  __all__ = [  # Exporting objects...
#      'addRecord',
#  ]

if __name__ == '__main__':
    print('@:recordsData: debug run')
