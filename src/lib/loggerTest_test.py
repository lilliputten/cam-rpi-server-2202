# -*- coding:utf-8 -*-
# @module loggerTest_test
# @desc Sample test module
# @since 2022.02.15, 05:02
# @changed 2022.02.15, 05:02

# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `npm run -s python-tests -- -k loggerTest`
#  - `python -m unittest -f src/core/loggerTest_test.py`

import unittest
import traceback

from src.lib.loggerTest import test
#  from .loggerTest import test
#  test = True


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


class Test_loggerTest(unittest.TestCase):

    def test_case_1(self):
        print('\nRunning test', getTrace())
        self.assertEqual(test, True)


if __name__ == '__main__':
    unittest.main()
