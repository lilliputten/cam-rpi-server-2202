# -*- coding:utf-8 -*-
# @module RecordOptions
# @since 2022.02.22, 01:47
# @changed 2022.02.24, 00:34


#  import time

from src.core.lib.logger import DEBUG
from src.core.lib import utils

from .Record import Record


class FindOptions():
    """
    Compare record parameters:
    - `ownerId`: string,
    - `recordId`: string,
    - `customFunc`: def or lambda with `record` parameter.
    """

    #  ownerId = None
    #  recordId = None
    #  customFunc = None

    def __init__(self, ownerId=None, recordId=None, customFunc=None):
        self.ownerId = ownerId
        self.recordId = recordId
        self.customFunc = customFunc

    def isRecordMatched(self, record: Record):
        """
        Compare record.
        Returns bool value: True if the record meets the specified conditions.
        """
        #  if customFunc:
        #      DEBUG(utils.getTrace(' customFunc specified'))
        ownerId = self.ownerId
        recordId = self.recordId
        customFunc = self.customFunc
        isFound = (bool(record) and (
            (not ownerId or record.ownerId == ownerId)
            and (not recordId or record.recordId == recordId)
            and (not customFunc or bool(customFunc(record)))
        )
        )
        #  DEBUG(utils.getTrace(' done'), {
        #      'isFound': isFound,
        #      'ownerId': ownerId,
        #      'recordId': recordId,
        #      'customFunc': customFunc,
        #      'record': record,
        #  })
        return isFound


class RemoveOptions():  # pylint: disable=too-few-public-methods

    #  removeFound = None
    #  removeOutdated = None

    def __init__(self, removeFound=False, removeOutdated=True):
        self.removeFound = removeFound
        self.removeOutdated = removeOutdated


__all__ = [  # Exporting objects...
    'FindOptions',
    'RemoveOptions',
]

if __name__ == '__main__':
    DEBUG(utils.getTrace(' debug run'))
