# -*- coding:utf-8 -*-
# @module recordsStorage
# @desc Extendable (?) records storage engine
# @since 2022.02.15, 03:59
# @changed 2022.02.15, 03:59


from src.lib.logger import DEBUG


recordsData = []


def addRecord(ownerId, data):
    recordData = {
        # timestamp
        'ownerId': ownerId,
        'data': data,
    }
    fromId = '@:recordsStorage:addRecord'
    print(fromId, ownerId, data)
    #  DEBUG(fromId, recordData)
    recordsData.append(recordData)
    return True


#  __all__ = [  # Exporting objects...
#      'addRecord',
#  ]

if __name__ == '__main__':
    print('@:recordsData: debug run')
