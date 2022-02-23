# -*- coding:utf-8 -*-
# @module RecordsStorageSingleton
# @since 2022.02.22, 01:47
# @changed 2022.02.22, 01:47


#  from src.core.lib.logger import DEBUG
from src.core.lib import utils

from .RecordsStorage import RecordsStorage


# Create singleton...
recordsStorage = RecordsStorage()


__all__ = [  # Exporting objects...
    'recordsStorage',
]


if __name__ == '__main__':
    print(utils.getTrace(), 'debug run')
