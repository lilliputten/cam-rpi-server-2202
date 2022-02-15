# -*- coding:utf-8 -*-
# @module recordsStorage_test
# @since 2022.02.15, 05:02
# @changed 2022.02.15, 05:02

# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `npm run -s python-tests -- -k recordsStorage`
#  - `python -m unittest -f src/core/recordsStorage_test.py`

import unittest
import traceback

from . import recordsStorage
#  from src.core.recordsStorage import test

#  from tests.testUtils import getTrace


def getTrace(str=None):
    funcName = traceback.extract_stack(None, 2)[0][2]
    strList = [
        __name__,
        funcName,
        str,
    ]
    filteredList = list(filter(None, strList))
    return ':'.join(filteredList)


print('\nRunning tests for', getTrace())


class Test_recordsStorage(unittest.TestCase):

    #  def setUp  # ...

    def tearDown(self):
        # Clean records after each test
        recordsStorage.recordsData = []

    def test_emptyData(self):
        print('\nRunning test', getTrace())
        self.assertEqual(recordsStorage.recordsData, [])

    def test_addedRecord(self):
        print('\nRunning test', getTrace())
        recordsStorage.addRecord('test', {'test': 1})
        self.assertEqual(len(recordsStorage.recordsData), 1)


if __name__ == '__main__':
    unittest.main()
