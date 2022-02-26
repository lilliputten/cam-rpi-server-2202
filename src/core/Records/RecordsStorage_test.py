# -*- coding:utf-8 -*-
# @module RecordsStorage_test
# @since 2022.02.22, 01:47
# @changed 2022.02.24, 00:34

# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `npm run -s python-tests -- -k RecordsStorage`
#  - `python -m unittest -f src/core/Records/RecordsStorage_test.py`

import time
import unittest
import functools

from tinydb import Query

from src.core.lib import utils

from .RecordsStorage import RecordsStorage


print('\nRunning tests for', utils.getTrace())


relevanceTime = 10

recordsStorage = RecordsStorage(relevanceTime, useMemoryStorage=True)


class Test_recordsStorage(unittest.TestCase):

    #  def setUp(self):  # TODO: Initialisations before each test

    def tearDown(self):  # Made cleanups after each test
        """
        Made cleanups after each test
        """
        recordsStorage.clearRecordsData()

    #  def test_openDb(self):
    #      """
    #      Test open db.
    #      """
    #      print('\nRunning test', utils.getTrace())
    #      dbCur = recordsStorage.openDbCursor()
    #      self.assertTrue(bool(dbCur))

    def test_emptyData(self):
        """
        Test initial (empty) state.
        """
        print('\nRunning test', utils.getTrace())
        self.assertEqual(recordsStorage.getRecordsCount(), 0)

    def test_addedRecord(self):
        """
        Test of data record adding.
        """
        print('\nRunning test', utils.getTrace())
        recordsStorage.addRecord(ownerId='test', data={'value': 'new record'})
        recordsStorage.dbSave()
        recordsCount = recordsStorage.getRecordsCount()
        self.assertEqual(recordsCount, 1)

    def test_removeOutdated(self):
        """
        Test of explicitly removing outdated records.
        """
        print('\nRunning test', utils.getTrace())
        timestamp = time.time() - relevanceTime  # Add 'obsolete' record
        recordsStorage.addRecord(timestamp=timestamp, ownerId='test', data={'value': 'must be removed'})
        removedRecorsCount = recordsStorage.removeOutdatedRecords()  # Expilitly remove outdated records.
        self.assertEqual(removedRecorsCount, 1)
        recordsCount = recordsStorage.getRecordsCount()
        self.assertEqual(recordsCount, 0)

    def test_findRecords(self):
        """
        Test of getting of records by parameter (`ownerId`).
        """
        print('\nRunning test', utils.getTrace())
        recordsStorage.addRecord(ownerId='test', data={'value': 'must be found'})
        recordsStorage.addRecord(ownerId='other', data={'value': 222})
        foundRecords = recordsStorage.findRecords({'ownerId': 'test'})
        self.assertEqual(len(foundRecords), 1)

    def test_findRecordsWithCustomFunc(self):
        """
        Test of getting of records by custom comparator funciton.
        """
        print('\nRunning test', utils.getTrace())
        recordsStorage.addRecord(ownerId='test', data={'value': 'must be found'})
        recordsStorage.addRecord(ownerId='other', data={'value': 222})
        def customFunc(data, value):
            return data['value'] == value  # noqa: E731  # use def instead lambda
        with recordsStorage.getDbHandler() as db:
            if db is not None:
                Test = Query()
                foundRecords = db.search(Test.data.test(customFunc, 'must be found'))
                foundRecordsCount = len(foundRecords)
                self.assertEqual(foundRecordsCount, 1)

    def test_removeRecords(self):
        """
        Test of removing of records by parameters (`ownerId`).
        """
        print('\nRunning test', utils.getTrace())
        recordsStorage.addRecord(ownerId='test', data={'value': 'must be found and removed'})
        recordsStorage.addRecord(ownerId='other', data={'value': 'must be remained'})
        recordsStorage.addRecord(ownerId='test', data={'value': 'must be found and removed'})
        recordsStorage.addRecord(ownerId='other', data={'value': 'must be remained'})
        recordsStorage.removeRecords({'ownerId': 'test'})
        remainedRecordsCount = recordsStorage.getRecordsCount()
        self.assertEqual(remainedRecordsCount, 2)

    def test_extractRecords(self):
        """
        Test of extracing (finding & removing) of records by parameters (`ownerId`).
        """
        print('\nRunning test', utils.getTrace())
        recordsStorage.addRecord(ownerId='test', data={'value': 'must be found and removed'})
        recordsStorage.addRecord(ownerId='other', data={'value': 'must be remained'})
        recordsStorage.addRecord(ownerId='test', data={'value': 'must be found and removed'})
        recordsStorage.addRecord(ownerId='other', data={'value': 'must be remained'})
        removedRecords = recordsStorage.extractRecords({'ownerId': 'test'})
        # Check removed records...
        # 2 records must be removed...
        self.assertEqual(len(removedRecords), 2)
        # Check which records was removed...
        removedRecordsValues = list(map(lambda record: record['data']['value'], removedRecords))
        removedRecordsTest = functools.reduce(
            (lambda result, value: result and value == 'must be found and removed'), removedRecordsValues, True)
        self.assertEqual(removedRecordsTest, True)
        # Check removed records...
        # 2 records must be remained
        remainedRecordsCount = recordsStorage.getRecordsCount()
        self.assertEqual(remainedRecordsCount, 2)
        # Check which records was removed...
        remainedRecords = recordsStorage.getRecordsData()
        remainedRecordsValues = list(map(lambda record: record['data']['value'], remainedRecords))
        remainedRecordsTest = functools.reduce(
            (lambda result, value: result and value == 'must be remained'), remainedRecordsValues, True)
        self.assertEqual(remainedRecordsTest, True)


if __name__ == '__main__':
    unittest.main()
