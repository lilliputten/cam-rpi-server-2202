# -*- coding:utf-8 -*-
# @module RecordsStorage_test
# @since 2022.02.22, 01:47
# @changed 2022.02.22, 02:03

# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `npm run -s python-tests -- -k RecordsStorage`
#  - `python -m unittest -f src/core/Records/RecordsStorage_test.py`

import unittest
import functools

#  from . import recordsStorage
from .RecordsStorage import RecordsStorage

from src.lib import utils


print('\nRunning tests for', utils.getTrace())


recordsStorage = RecordsStorage()


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
        recordsStorage.addRecord(ownerId='test', data={'value': 'new record'})
        #  self.assertEqual(len(recordsStorage.recordsData), 1)
        self.assertEqual(recordsStorage.getRecordsCount(), 1)

    def test_getRecords(self):
        """
        Test of getting of records by parameter (`ownerId`).
        """
        print('\nRunning test', utils.getTrace())
        recordsStorage.addRecord(ownerId='test', data={'value': 'must be found'})
        recordsStorage.addRecord(ownerId='other', data={'value': 222})
        foundRecords = recordsStorage.getRecords(ownerId='test')
        self.assertEqual(len(foundRecords), 1)

    def test_getRecordsWithCustomFunc(self):
        """
        Test of getting of records by custom comparator funciton.
        """
        print('\nRunning test', utils.getTrace())
        # NOTE: Compare function can be specified as lambda or def
        customFunc = lambda record: record.data['value'] == 'must be found'  # noqa: E731  # use def instead lambda
        #  def customFunc(record):  # noqa: E306  # blank line
        #      isFound = record.data['value'] == 'must be found'
        #      return isFound
        recordsStorage.addRecord(ownerId='test', data={'value': 'must be found'})
        recordsStorage.addRecord(ownerId='other', data={'value': 222})
        foundRecords = recordsStorage.getRecords(customFunc=customFunc)
        self.assertEqual(len(foundRecords), 1)

    def test_extractRecords(self):
        """
        Test finding and removeing (extracting) of records by parameters (`ownerId`).
        """
        print('\nRunning test', utils.getTrace())
        recordsStorage.addRecord(ownerId='test', data={'value': 'must be found and removed'})
        recordsStorage.addRecord(ownerId='other', data={'value': 'must be remained'})
        recordsStorage.addRecord(ownerId='test', data={'value': 'must be found and removed'})
        recordsStorage.addRecord(ownerId='other', data={'value': 'must be remained'})
        foundRecords = recordsStorage.extractRecords(ownerId='test')
        self.assertEqual(len(foundRecords), 2)
        remainedRecordsCount = recordsStorage.getRecordsCount()
        self.assertEqual(remainedRecordsCount, 2)

    def test_removeRecords(self):
        """
        Test of removeing of records by parameters (`ownerId`).
        """
        print('\nRunning test', utils.getTrace())
        recordsStorage.addRecord(ownerId='test', data={'value': 'must be found and removed'})
        recordsStorage.addRecord(ownerId='other', data={'value': 'must be remained'})
        recordsStorage.addRecord(ownerId='test', data={'value': 'must be found and removed'})
        recordsStorage.addRecord(ownerId='other', data={'value': 'must be remained'})
        removedRecords = recordsStorage.removeRecords(ownerId='test')
        # Check removed records...
        # 2 records must be removed...
        self.assertEqual(len(removedRecords), 2)
        # Check which records was removed...
        removedRecordsValues = list(map(lambda record: record.data['value'], removedRecords))
        removedRecordsTest = functools.reduce((lambda result, value: result and value == 'must be found and removed'), removedRecordsValues, True)
        self.assertEqual(removedRecordsTest, True)
        # Check removed records...
        # 2 records must be remained
        remainedRecordsCount = recordsStorage.getRecordsCount()
        self.assertEqual(remainedRecordsCount, 2)
        # Check which records was removed...
        remainedRecords = recordsStorage.getRecordsData()
        remainedRecordsValues = list(map(lambda record: record.data['value'], remainedRecords))
        remainedRecordsTest = functools.reduce((lambda result, value: result and value == 'must be remained'), remainedRecordsValues, True)
        self.assertEqual(remainedRecordsTest, True)


if __name__ == '__main__':
    unittest.main()
