# -*- coding:utf-8 -*-
# @module RecordsStorage
# @desc Extendable (?) records storage engine
# @since 2022.02.22, 01:47
# @changed 2022.02.23, 00:01


import time

from src.lib.logger import DEBUG
from src.lib import utils

from .Record import Record


defaultRelevanceTime = 10


class RecordsStorage():

    relevanceTime = defaultRelevanceTime
    recordsData = []

    def __init__(self, relevanceTime=None):
        if relevanceTime:
            self.relevanceTime = relevanceTime

    def clearRecordsData(self):
        #  self.recordsData = []
        self.recordsData.clear()

    def getRecordsData(self):
        return self.recordsData

    def getRecordsCount(self):
        return len(self.recordsData)

    def addRecordObject(self, record):
        """
        Add record with `Record` object instance:
        - timestamp (number)
        - ownerId (string)
        - recordId (string)
        - data (dict)
        """
        #  DEBUG(utils.getTrace(), {
        #      'record': record,
        #  })
        self.recordsData.append(record)
        return True

    def addRecord(self, timestamp=None, ownerId=None, recordId=None, data=None):
        """
        Add record with raw data (all parameters are optional).
        The data converting to `Record` object instance (see `addRecordObject` above):
        - timestamp (number)
        - ownerId (string)
        - recordId (string)
        - data (dict)
        """
        record = Record(timestamp=timestamp, ownerId=ownerId, recordId=recordId, data=data)
        #  DEBUG(utils.getTrace(), {
        #      #  'timestamp': timestamp,
        #      #  'ownerId': ownerId,
        #      #  'recordId': recordId,
        #      #  'data': data,
        #      'record': record,
        #  })
        return self.addRecordObject(record)

    def isRecordOutdated(self, record):
        """
        Test record outdated.
        Returns bool value: True if record is outdated (can be removed).
        TODO: To use `Record.isOutdated`?
        """
        if not record or not record.timestamp or (time.time() - record.timestamp) >= self.relevanceTime:
            return True
        return False

    def isRecordMatched(self, record, ownerId=None, recordId=None, customFunc=None):
        """
        Compare record with parameters:
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        Returns bool value: True if the record meets the specified conditions.
        """
        #  if customFunc:
        #      DEBUG(utils.getTrace(' customFunc specified'))
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

    def processRecords(self, ownerId=None, recordId=None, customFunc=None, removeFound=False, removeOutdated=True):
        """
        Main low-level method for records finding and processing.
        Found conditions specified with parameters (see `isRecordMatched`, all of them are optional):
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        Remove parameters:
        - `removeFound` -- Remove found records (default is False).
        - `removeOutdated` -- Remove outdated records (default is True).
        Returns tuple of `records`, `positions`: crsp found records and their positions in list.
        """
        #  DEBUG(utils.getTrace(' start'), {
        #      'recordsData': self.recordsData,
        #      'ownerId': ownerId,
        #      'recordId': recordId,
        #      'customFunc': customFunc,
        #      'removeFound': removeFound,
        #      'removeOutdated': removeOutdated,
        #  })
        records = []
        # Scan records in reversed order (removing records from list's tail)
        pos = len(self.recordsData) - 1
        while pos >= 0:
            record = self.recordsData[pos]
            isFound = self.isRecordMatched(record, ownerId=ownerId, recordId=recordId, customFunc=customFunc)
            if isFound:
                #  DEBUG(utils.getTrace(' record found'), {
                #      'pos': pos,
                #      'record': record,
                #  })
                records.insert(0, record)  # Insert at begining of list ('coz scanning in reverse order)
            # Remove record if neede...
            if (isFound and removeFound) or (removeOutdated and self.isRecordOutdated(record)):
                #  DEBUG(utils.getTrace(' record removing'), {
                #      'pos': pos,
                #      'record': record,
                #      'isFound': isFound,
                #  })
                del self.recordsData[pos]
            pos = pos - 1
        #  DEBUG(utils.getTrace(' done'), {
        #      'records': records,
        #  })
        return records

    def findRecords(self, ownerId=None, recordId=None, customFunc=None):
        """
        Find-only records with conditions (all parameters are optional):
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        Returns found records list.
        """
        return self.processRecords(ownerId=ownerId, recordId=recordId, customFunc=customFunc, removeFound=False)

    def extractRecords(self, ownerId=None, recordId=None, customFunc=None):
        """
        Find and remove records with conditions (all parameters are optional):
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        Returns found (and removed) records list.
        """
        return self.processRecords(ownerId=ownerId, recordId=recordId, customFunc=customFunc, removeFound=True)

    def removeRecords(self, ownerId=None, recordId=None, customFunc=None):
        """
        Remove records with conditions (all parameters are optional):
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        """
        self.extractRecords(ownerId=ownerId, recordId=recordId, customFunc=customFunc)

    def removeOutdatedRecords(self):
        """
        Remove outdated records.
        """
        self.processRecords(removeOutdated=True)


__all__ = [  # Exporting objects...
    'defaultRelevanceTime',
    'RecordsStorage',
]

if __name__ == '__main__':
    DEBUG(utils.getTrace(' debug run'))
