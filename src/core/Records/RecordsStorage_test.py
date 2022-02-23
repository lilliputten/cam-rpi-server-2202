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

from src.core.lib import utils

from .RecordsStorage import RecordsStorage
from .RecordOptions import FindOptions
#  from .RecordOptions import RemoveOptions
#  from . import FindOptions


print('\nRunning tests for', utils.getTrace())


relevanceTime = 10

recordsStorage = RecordsStorage(relevanceTime)


class Test_recordsStorage(unittest.TestCase):

    #  def setUp(self):  # TODO: Initialisations before each test

    def tearDown(self):  # Made cleanups after each test
        """
        Made cleanups after each test
        """
        #  recordsStorage.recordsData = []
        recordsStorage.clearRecordsData()

    def test_emptyData(self):
        """
        Test initial (empty) state.
        """
        print('\nRunning test', utils.getTrace())
        #  self.assertEqual(recordsStorage.recordsData, [])
        self.assertEqual(recordsStorage.getRecordsCount(), 0)

    def test_addedRecord(self):
        """
        Test of data record adding.
        """
        print('\nRunning test', utils.getTrace())
        recordsStorage.addRecordFromData(ownerId='test', data={'value': 'new record'})
        #  self.assertEqual(len(recordsStorage.recordsData), 1)
        self.assertEqual(recordsStorage.getRecordsCount(), 1)

    def test_removeOutdated(self):
        """
        Test of explicitly removing outdated records.
        """
        print('\nRunning test', utils.getTrace())
        timestamp = time.time() - relevanceTime  # Add 'obsolete' record
        recordsStorage.addRecordFromData(timestamp=timestamp, ownerId='test', data={'value': 'must be removed'})
        recordsStorage.removeOutdatedRecords()  # Expilitly remove outdated records.
        recordsCount = recordsStorage.getRecordsCount()
        self.assertEqual(recordsCount, 0)

    def test_removeOutdatedDuringFind(self):
        """
        Test of implicitly (during find) removing outdated records.
        """
        print('\nRunning test', utils.getTrace())
        timestamp = time.time() - relevanceTime  # Add 'obsolete' record
        recordsStorage.addRecordFromData(timestamp=timestamp, ownerId='test', data={'value': 'must be removed'})
        # Try to find absent records. Outdated records must be removed.
        recordsStorage.findRecords(FindOptions(ownerId='ABSENT'))
        recordsCount = recordsStorage.getRecordsCount()
        self.assertEqual(recordsCount, 0)

    def test_getRecords(self):
        """
        Test of getting of records by parameter (`ownerId`).
        """
        print('\nRunning test', utils.getTrace())
        recordsStorage.addRecordFromData(ownerId='test', data={'value': 'must be found'})
        recordsStorage.addRecordFromData(ownerId='other', data={'value': 222})
        foundRecords = recordsStorage.findRecords(FindOptions(ownerId='test'))
        self.assertEqual(len(foundRecords), 1)

    def test_getRecordsWithCustomFunc(self):
        """
        Test of getting of records by custom comparator funciton.
        """
        print('\nRunning test', utils.getTrace())
        # NOTE: Compare function can be specified as lambda or def

        def customFunc(record):
            return record.data['value'] == 'must be found'  # noqa: E731  # use def instead lambda
        #  def customFunc(record):  # noqa: E306  # blank line
        #      isFound = record.data['value'] == 'must be found'
        #      return isFound
        recordsStorage.addRecordFromData(ownerId='test', data={'value': 'must be found'})
        recordsStorage.addRecordFromData(ownerId='other', data={'value': 222})
        foundRecords = recordsStorage.findRecords(FindOptions(customFunc=customFunc))
        self.assertEqual(len(foundRecords), 1)

    def test_removeRecords(self):
        """
        Test of removing of records by parameters (`ownerId`).
        """
        print('\nRunning test', utils.getTrace())
        recordsStorage.addRecordFromData(ownerId='test', data={'value': 'must be found and removed'})
        recordsStorage.addRecordFromData(ownerId='other', data={'value': 'must be remained'})
        recordsStorage.addRecordFromData(ownerId='test', data={'value': 'must be found and removed'})
        recordsStorage.addRecordFromData(ownerId='other', data={'value': 'must be remained'})
        recordsStorage.removeRecords(FindOptions(ownerId='test'))
        remainedRecordsCount = recordsStorage.getRecordsCount()
        self.assertEqual(remainedRecordsCount, 2)

    def test_extractRecords(self):
        """
        Test of extracing (finding & removing) of records by parameters (`ownerId`).
        """
        print('\nRunning test', utils.getTrace())
        recordsStorage.addRecordFromData(ownerId='test', data={'value': 'must be found and removed'})
        recordsStorage.addRecordFromData(ownerId='other', data={'value': 'must be remained'})
        recordsStorage.addRecordFromData(ownerId='test', data={'value': 'must be found and removed'})
        recordsStorage.addRecordFromData(ownerId='other', data={'value': 'must be remained'})
        removedRecords = recordsStorage.extractRecords(FindOptions(ownerId='test'))
        # Check removed records...
        # 2 records must be removed...
        self.assertEqual(len(removedRecords), 2)
        # Check which records was removed...
        removedRecordsValues = list(map(lambda record: record.data['value'], removedRecords))
        removedRecordsTest = functools.reduce(
            (lambda result, value: result and value == 'must be found and removed'), removedRecordsValues, True)
        self.assertEqual(removedRecordsTest, True)
        # Check removed records...
        # 2 records must be remained
        remainedRecordsCount = recordsStorage.getRecordsCount()
        self.assertEqual(remainedRecordsCount, 2)
        # Check which records was removed...
        remainedRecords = recordsStorage.getRecordsData()
        remainedRecordsValues = list(map(lambda record: record.data['value'], remainedRecords))
        remainedRecordsTest = functools.reduce(
            (lambda result, value: result and value == 'must be remained'), remainedRecordsValues, True)
        self.assertEqual(remainedRecordsTest, True)


if __name__ == '__main__':
    unittest.main()
