# -*- coding:utf-8 -*-
# @module RecordsStorage
# @desc Extendable (?) records storage engine
# @since 2022.02.22, 01:47
# @changed 2022.02.26, 02:35


import time
import sqlite3
import json
import traceback
from os import path

from config import config

from src.core.lib.logger import DEBUG
#  from src.core.lib import utils
from src.core.lib.utils import quoteStr, getTrace
#  from src.core.lib import errors

from .Record import Record
from .RecordOptions import FindOptions, RemoveOptions
#  from . import RecordOptions


defaultRelevanceTime = 10
dbName = 'RecordsStorage'

#  workPath = path.dirname(path.abspath(__file__))  # Module root path
dbFile = path.join(config['dbPath'], dbName + config['dbExt'])


class RecordsStorage():

    relevanceTime = defaultRelevanceTime  # Relevance time parameter

    hasDbChanges = False
    db = None  # Sqlite db connection
    dbCur = None  # Sqlite db cursor
    recordsData = []

    def __init__(self, relevanceTime=None):
        if relevanceTime:
            self.relevanceTime = relevanceTime

    def __del__(self):
        self.closeDb()

    def dbOpen(self):
        if not self.db:
            self.db = sqlite3.connect(dbFile)
            # TODO: Check for successfull db opened?
        return self.db

    def closeDb(self):
        if self.db:
            self.saveDb()
            self.db.close()
            self.db = None
            self.dbCur = None

    def saveDb(self):
        if self.db:
            self.db.commit()  # TODO: Check for hasDbChanges flag?
            # TODO: Check for successfull operation result?
            self.hasDbChanges = False

    def openDbCursor(self):
        if not self.dbCur:
            try:
                self.dbOpen()
                # TODO: Check for successfull db opened?
                self.dbCur = self.db.cursor()
                # TODO: Check for successfull cursor created?
                # Ensure tabe is created
                dbCmd = (
                    'create table if not exists ' + dbName + ' ('
                    'timestamp real, '
                    'ownerId text, '
                    'recordId text, '
                    'jsonData text'
                    ')'
                )
                self.dbCur.execute(dbCmd)
                # TODO: Check for successfull table created?
            except Exception as err:
                #  sError = errors.toString(err, show_stacktrace=False)
                sTraceback = str(traceback.format_exc())
                DEBUG(getTrace('catched error'), {
                    'dbCmd': dbCmd,
                    'err': err,
                    #  'error': sError,
                    'traceback': sTraceback,
                })
                #  raise err
                errStr = 'Cannot open database with command: ' + dbCmd
                raise Exception(errStr) from err
        return self.dbCur

    def closeDbCursor(self):
        return self.closeDb()  # ???


    def clearRecordsData(self):
        #  self.recordsData = []
        self.recordsData.clear()

    def getRecordsData(self):
        return self.recordsData

    def getRecordsCount(self):
        return len(self.recordsData)

    def addRecordObject(self, record: Record):
        """
        Add record with `Record` object instance.
        """
        #  DEBUG(getTrace(), {
        #      'record': record,
        #  })
        try:
            self.recordsData.append(record)
            dbCur = self.openDbCursor()
            # TODO: Check for cursor successfully created
            jsonData = json.dumps(record.data) if record.data else '{}'
            dbCmd = (
                'insert into ' + dbName + ' values ('
                + quoteStr(record.timestamp) + ', '
                + quoteStr(record.ownerId, addQuotes=True) + ', '
                + quoteStr(record.recordId, addQuotes=True) + ', '
                + quoteStr(jsonData, addQuotes=True)
                + ')'
            )
            DEBUG(getTrace(), {
                'dbCmd': dbCmd,
                'jsonData': jsonData,
                'record': record,
            })
            dbCur.execute(dbCmd)
        except Exception as err:
            #  sError = errors.toString(err, show_stacktrace=False)
            sTraceback = str(traceback.format_exc())
            DEBUG(getTrace('catched error'), {
                'dbCmd': dbCmd,
                'err': err,
                #  'error': sError,
                'traceback': sTraceback,
            })
            #  raise err
            errStr = 'Cannot execute db command: ' + dbCmd
            raise Exception(errStr) from err
        return True

    def addRecordFromData(self, timestamp=None, ownerId=None, recordId=None, data=None):
        """
        Add record with raw data (all parameters are optional).
        The data converting to `Record` object instance (see `addRecordObject` above):
        - timestamp (number)
        - ownerId (string)
        - recordId (string)
        - data (dict)
        """
        record = Record(timestamp=timestamp, ownerId=ownerId, recordId=recordId, data=data)
        #  DEBUG(getTrace(), {
        #      #  'timestamp': timestamp,
        #      #  'ownerId': ownerId,
        #      #  'recordId': recordId,
        #      #  'data': data,
        #      'record': record,
        #  })
        return self.addRecordObject(record)

    def isRecordOutdated(self, record: Record):
        """
        Test record outdated.
        Returns bool value: True if record is outdated (can be removed).
        TODO: To use `Record.isOutdated`?
        """
        if not record or not record.timestamp or (time.time() - record.timestamp) >= self.relevanceTime:
            return True
        return False

    def processRecords(self, findOptions: FindOptions = None, removeOptions: RemoveOptions = None):
        """
        Main low-level method for records finding and processing.
        Found conditions specified with parameters
        (see `FindOptions`, `FindOptions.isRecordMatched`,
        all of them are optional):
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        Remove parameters (see `RemoveOptions`):
        - `removeFound` -- Remove found records (default is False).
        - `removeOutdated` -- Remove outdated records (default is True).
        Returns tuple of `records`, `positions`: crsp found records and their positions in list.
        """
        #  DEBUG(getTrace(' start'), {
        #      'recordsData': self.recordsData,
        #      'ownerId': findOptions.ownerId,
        #      'recordId': findOptions.recordId,
        #      'customFunc': findOptions.customFunc,
        #      'removeFound': removeOptions.removeFound,
        #      'removeOutdated': removeOptions.removeOutdated,
        #  })
        records = []
        # Scan records in reversed order (removing records from list's tail)
        pos = len(self.recordsData) - 1
        while pos >= 0:
            record = self.recordsData[pos]
            isFound = bool(findOptions) and findOptions.isRecordMatched(record)
            if isFound:
                #  DEBUG(getTrace(' record found'), {
                #      'pos': pos,
                #      'record': record,
                #  })
                records.insert(0, record)  # Insert at begining of list ('coz scanning in reverse order)
            # Remove record if neede...
            if removeOptions:
                if ((isFound and removeOptions.removeFound)
                        or (removeOptions.removeOutdated and self.isRecordOutdated(record))
                        ):
                    #  DEBUG(getTrace(' record removing'), {
                    #      'pos': pos,
                    #      'record': record,
                    #      'isFound': isFound,
                    #  })
                    del self.recordsData[pos]
            pos = pos - 1
        #  DEBUG(getTrace(' done'), {
        #      'records': records,
        #  })
        return records

    def findRecords(self, findOptions: FindOptions):
        """
        Find-only records with conditions (all parameters are optional):
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        Returns found records list.
        """
        return self.processRecords(findOptions, RemoveOptions(removeFound=False))

    def extractRecords(self, findOptions: FindOptions):
        """
        Find and remove records with conditions (all parameters are optional):
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        Returns found (and removed) records list.
        """
        return self.processRecords(findOptions, RemoveOptions(removeFound=True))

    def removeRecords(self, findOptions: FindOptions):
        """
        Remove records with conditions (all parameters are optional):
        - `ownerId`: string,
        - `recordId`: string,
        - `customFunc`: def or lambda with `record` parameter.
        """
        self.extractRecords(findOptions)

    def removeOutdatedRecords(self):
        """
        Remove outdated records.
        """
        self.processRecords(removeOptions=RemoveOptions(removeOutdated=True))


__all__ = [  # Exporting objects...
    'defaultRelevanceTime',
    'RecordsStorage',
]

if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
