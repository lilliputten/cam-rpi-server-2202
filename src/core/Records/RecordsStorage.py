# -*- coding:utf-8 -*-
# @module RecordsStorage
# @desc Extendable (?) records storage engine
# @since 2022.02.22, 01:47
# @changed 2022.02.26, 03:39


import time
#  import sys
#  import json
import traceback
from os import path

#  import sqlite3

# TinyDB. @see: https://tinydb.readthedocs.io/en/latest/usage.html
from tinydb import TinyDB
from tinydb import Query
#  from tinydb import where
from tinydb.storages import JSONStorage
from tinydb.storages import MemoryStorage
from tinydb.middlewares import CachingMiddleware

from config import config

from src.core.lib.logger import DEBUG
#  from src.core.lib import utils
from src.core.lib.utils import getTrace
#  from src.core.lib.utils import quoteStr
#  from src.core.lib import errors


#  #  Determine running under test suite...
#  isTest = 'unittest' in sys.modules

#  useMemoryStorage = isTest

defaultRelevanceTime = 10
dbName = 'RecordsStorage'

#  workPath = path.dirname(path.abspath(__file__))  # Module root path
#  dbFile = path.join(config['dbPath'], dbName + config['dbExt'])   # sqlite3
dbFile = path.join(config['dbPath'], dbName + '.json')


class RecordsStorage():

    useMemoryStorage = None
    relevanceTime = defaultRelevanceTime  # Relevance time parameter

    hasDbChanges = False
    db = None  # Database handler
    #  dbCur = None  # Sqlite db cursor
    recordsData = []

    def __init__(self, relevanceTime=None, useMemoryStorage=False):
        self.useMemoryStorage = useMemoryStorage
        if relevanceTime:
            self.relevanceTime = relevanceTime

    def __del__(self):
        self.dbClose()

    def dbOpen(self):
        #  self.db = sqlite3.connect(dbFile)  # sqlite3
        #  self.db = TinyDB(dbFile)
        try:
            if self.useMemoryStorage:
                # Use memory-based storage (basically during tests).
                db = TinyDB(storage=MemoryStorage)
            else:
                # Use real file-based storage.
                db = TinyDB(
                    dbFile,
                    storage=CachingMiddleware(JSONStorage),
                    sort_keys=True, indent=2,
                )
            self.db = db
            return db
        except Exception as err:
            #  sError = errors.toString(err, show_stacktrace=False)
            sTraceback = str(traceback.format_exc())
            DEBUG(getTrace('catched error'), {
                'err': err,
                'traceback': sTraceback,
            })
            raise err

    def getDbHandler(self):
        if self.db is not None:
            return self.db
        return self.dbOpen()

    def dbClose(self):
        if self.db is not None:
            self.dbSave()
            self.db.close()
            #  sqlite3...
            #  self.db.close()
            #  self.dbCur = None
            self.db = None

    def dbSave(self):
        if self.db is not None:
            # TODO: Force write (flush) tinydb?
            if hasattr(self.db, 'storage') and hasattr(self.db.storage, 'flush'):
                self.db.storage.flush()
            # self.db.commit()  # TODO: Check for hasDbChanges flag?
            self.hasDbChanges = False

    def dbSync(self):
        if self.db is not None:
            self.db.clear_cache()

    #  UNUSED: openDbCursor, closeDbCursor
    #  def openDbCursor(self):
    #      if not self.dbCur:
    #          try:
    #              self.dbOpen()
    #              # TODO: Check for successfull db opened?
    #              self.dbCur = self.db.cursor()
    #              # TODO: Check for successfull cursor created?
    #              # Ensure tabe is created
    #              dbCmd = (
    #                  'create table if not exists ' + dbName + ' ('
    #                  'timestamp real, '
    #                  'ownerId text, '
    #                  'recordId text, '
    #                  'jsonData text'
    #                  ')'
    #              )
    #              self.dbCur.execute(dbCmd)
    #              # TODO: Check for successfull table created?
    #          except Exception as err:
    #              #  sError = errors.toString(err, show_stacktrace=False)
    #              sTraceback = str(traceback.format_exc())
    #              DEBUG(getTrace('catched error'), {
    #                  'dbCmd': dbCmd,
    #                  'err': err,
    #                  #  'error': sError,
    #                  'traceback': sTraceback,
    #              })
    #              #  raise err
    #              errStr = 'Cannot open database with command: ' + dbCmd
    #              raise Exception(errStr) from err
    #      return self.dbCur
    #
    #  def closeDbCursor(self):
    #      return self.dbClose()  # ???

    def clearRecordsData(self):
        #  self.recordsData = []
        #  self.recordsData.clear()
        if self.db is not None:
            self.db.truncate()

    def getRecordsData(self):
        return self.recordsData

    def getRecordsCount(self):
        with self.getDbHandler() as db:
            return len(db)
        return 0
        #  return len(self.recordsData)

    def addRecord(self, timestamp=None, ownerId=None, recordId=None, data=None):
        """
        Add record with params:
        - timestamp (number)
        - ownerId (string)
        - recordId (string)
        - data (dict)
        """
        dbData = {
            'timestamp': timestamp,
            'ownerId': ownerId,
            'recordId': recordId,
            'data': data,
        }
        DEBUG(getTrace(), {
            'dbData': dbData,
        })
        try:
            with self.getDbHandler() as db:
                if db is not None:
                    db.insert(dbData)
        except Exception as err:
            sTraceback = str(traceback.format_exc())
            DEBUG(getTrace('catched error'), {
                'dbData': dbData,
                'err': err,
                'traceback': sTraceback,
            })
            #  #  errStr = 'Cannot execute db command: ' + dbCmd
            #  raise Exception(errStr) from err
            raise err
        return True

    def findOutdatedRecords(self):
        """
        Find outdated records.
        """
        with self.getDbHandler() as db:
            if db is not None:
                validTime = time.time() - self.relevanceTime
                Test = Query()
                result = db.search(Test.timestamp <= validTime)
                print(result)

    def removeOutdatedRecords(self):
        """
        Remove outdated records.
        Return removed records count.
        """
        with self.getDbHandler() as db:
            if db is not None:
                validTime = time.time() - self.relevanceTime
                Test = Query()
                result = db.remove(
                    # (Test.timestamp != None) & # pylint: disable=singleton-comparison
                    (Test.timestamp < validTime)
                )
                return len(result)
        return 0

    def findRecords(self, fragment):
        """
        `fragment`: data object with params:
        - `ownerId`: string,
        - `recordId`: string,
        Returns found records list.
        """
        with self.getDbHandler() as db:
            if fragment and db is not None:
                try:
                    return db.search(Query().fragment(fragment))
                except Exception as err:
                    sTraceback = str(traceback.format_exc())
                    DEBUG(getTrace('catched error'), {
                        'err': err,
                        'traceback': sTraceback,
                    })
                    raise err
        return []

    def extractRecords(self, fragment):
        """
        Find and remove records using fragment (all parameters are optional):
        - `ownerId`: string,
        - `recordId`: string,
        Returns found (and removed) records list.
        """
        records = self.findRecords(fragment)
        # Remove records
        if len(records):
            with self.getDbHandler() as db:
                if db is not None:
                    ids = list(map(lambda rec: rec.doc_id, records))
                    db.remove(doc_ids=ids)
        return records

    def removeRecords(self, fragment):
        """
        Remove records using fragment (all parameters are optional):
        - `ownerId`: string,
        - `recordId`: string,
        """
        self.extractRecords(fragment)

__all__ = [  # Exporting objects...
    'defaultRelevanceTime',
    'RecordsStorage',
]

if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
