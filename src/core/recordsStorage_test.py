# -*- coding:utf-8 -*-
# @module recordsStorage_test
# @since 2022.02.15, 05:02
# @changed 2022.02.21, 22:32

# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `npm run -s python-tests -- -k recordsStorage`
#  - `python -m unittest -f src/core/recordsStorage_test.py`

import unittest

from . import recordsStorage

#  from tests.testUtils import getTrace
from src.lib import utils


print('\nRunning tests for', utils.getTrace())


class Test_recordsStorage(unittest.TestCase):

    #  def setUp(self):  # Initialisations before each test

    def tearDown(self):  # Cleanups after each test
        recordsStorage.recordsData = []

    def test_emptyData(self):
        print('\nRunning test', utils.getTrace())
        self.assertEqual(recordsStorage.recordsData, [])

    def test_addedRecord(self):
        print('\nRunning test', utils.getTrace())
        recordsStorage.addRecord(ownerId='test', data={'test': 1})
        self.assertEqual(len(recordsStorage.recordsData), 1)


if __name__ == '__main__':
    unittest.main()
