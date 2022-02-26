# -*- coding:utf-8 -*-
# @module RecordOptions
# @since 2022.02.22, 01:47
# @changed 2022.02.24, 00:34


#  import time

from src.core.lib.logger import DEBUG
from src.core.lib import utils


class FindOptions():
    """
    Compare record parameters:
    - `ownerId`: string,
    - `recordId`: string,
    """

    #  ownerId = None
    #  recordId = None

    def __init__(self, ownerId=None, recordId=None):
        self.ownerId = ownerId
        self.recordId = recordId

    #  UNUSED: isRecordMatched
    #  def isRecordMatched(self, record: Record):
    #      """
    #      Compare record.
    #      Returns bool value: True if the record meets the specified conditions.
    #      """
    #      ownerId = self.ownerId
    #      recordId = self.recordId
    #      isFound = (bool(record) and (
    #          (not ownerId or record.ownerId == ownerId)
    #          and (not recordId or record.recordId == recordId)
    #      )
    #      )
    #      #  DEBUG(utils.getTrace(' done'), {
    #      #      'isFound': isFound,
    #      #      'ownerId': ownerId,
    #      #      'recordId': recordId,
    #      #      'record': record,
    #      #  })
    #      return isFound

    def getQueryFragment(self):
        """
        Get fragment object for tinydb query search
        @see https://tinydb.readthedocs.io/en/latest/usage.html#advanced-queries
        """
        frag = {}
        if self.ownerId is not None:
            frag['ownerId'] = self.ownerId
        if self.recordId is not None:
            frag['recordId'] = self.recordId
        return frag


__all__ = [  # Exporting objects...
    'FindOptions',
]

if __name__ == '__main__':
    DEBUG(utils.getTrace(' debug run'))
