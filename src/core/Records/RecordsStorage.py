# -*- coding:utf-8 -*-
# @module RecordsStorage
# @desc Extendable (?) records storage engine
# @since 2022.02.22, 01:47
# @changed 2022.02.22, 02:25


from src.lib.logger import DEBUG
from src.lib import utils

from .Record import Record


class RecordsStorage():

    recordsData = []

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

    def testRecord(self, record, ownerId=None, recordId=None, customFunc=None):
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

    def removeRecordsByPos(self, posList):
        """
        Remove records specified by their positions in list.
        Nothing returned.
        """
        # Iterate upside-down and remove records by positions from tail...
        sortedPos = sorted(posList, reverse=True)
        #  DEBUG(utils.getTrace(' start'), {
        #      'sortedPos': sortedPos,
        #      'posList': posList,
        #      'recordsData': self.recordsData,
        #  })
        for pos in sortedPos:
            del self.recordsData[pos]
        #  DEBUG(utils.getTrace(' done'), {
        #      'sortedPos': sortedPos,
        #      'posList': posList,
        #      'recordsData': self.recordsData,
        #  })

    def findRecordsWithPositions(self, ownerId=None, recordId=None, customFunc=None):
        """
        Low-level method for records finding.
        Found conditions specified with parameters (see `testRecord`, all of them are optional):
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        Returns tuple of `records`, `positions`: crsp found records and their positions in list.
        """
        #  DEBUG(utils.getTrace(' start'), {
        #      'recordsData': self.recordsData,
        #      'ownerId': ownerId,
        #      'recordId': recordId,
        #      'customFunc': customFunc,
        #  })
        records = []
        positions = []
        for pos in range(len(self.recordsData)):
            record = self.recordsData[pos]
            isFound = self.testRecord(record, ownerId=ownerId, recordId=recordId, customFunc=customFunc)
            if isFound:
                #  DEBUG(utils.getTrace(' record found'), {
                #      'pos': pos,
                #      'record': record,
                #  })
                positions.append(pos)
                records.append(record)
        #  DEBUG(utils.getTrace(' done'), {
        #      'positions': positions,
        #      'records': records,
        #  })
        return records, positions

    def findRecords(self, ownerId=None, recordId=None, customFunc=None, removeFound=False):
        """
        Core method for records fetching an removing.
        Found conditions specified with parameters (all of them are optional):
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        Compare function (`customFunc`) can be specified as lambda or def
        If `removeFound` flag is specified, then found records are removed from storage.
        Returns list of found records.
        """
        #  DEBUG(utils.getTrace('start'), {
        #      'removeFound': removeFound,
        #      'recordsData': self.recordsData,
        #      'ownerId': ownerId,
        #      'recordId': recordId,
        #  })
        # Find records and their positions...
        records, positions = self.findRecordsWithPositions(ownerId=ownerId, recordId=recordId, customFunc=customFunc)
        # Remove found records if `removeFound` flag specified...
        if removeFound and positions and len(positions):
            self.removeRecordsByPos(positions)
        #  DEBUG(utils.getTrace('done'), {
        #      'removeFound': removeFound,
        #      'recordsData': self.recordsData,
        #      'positions': positions,
        #      'records': records,
        #  })
        return records

    def getRecords(self, ownerId=None, recordId=None, customFunc=None):
        """
        Find-only records with conditions (all parameters are optional):
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        Returns found records list.
        """
        return self.findRecords(ownerId=ownerId, recordId=recordId, customFunc=customFunc, removeFound=False)

    def extractRecords(self, ownerId=None, recordId=None, customFunc=None):
        """
        Find and remove records with conditions (all parameters are optional):
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        Returns found (and removed) records list.
        """
        return self.findRecords(ownerId=ownerId, recordId=recordId, customFunc=customFunc, removeFound=True)

    def removeRecords(self, ownerId=None, recordId=None, customFunc=None):
        """
        Remove records with conditions (all parameters are optional):
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        Returns removed records list.
        """
        return self.extractRecords(ownerId=ownerId, recordId=recordId, customFunc=customFunc)


__all__ = [  # Exporting objects...
    'RecordsStorage',
]

if __name__ == '__main__':
    DEBUG(utils.getTrace(' debug run'))
