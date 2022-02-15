# -*- coding:utf-8 -*-
# @module pathmagic
# @desc Add parent path to python import paths for testing purposes (allows importing root config module)
# @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
# @since 2020.09.29, 22:35
# @changed 2022.02.15, 01:46

#  import sys
#  import os
#  import inspect


#  # NOTE: Add parent folder to imports list
#  currentFile = os.path.abspath(inspect.getfile(inspect.currentframe()))
#  currPath = os.path.dirname(currentFile)
#  parentPath = os.path.dirname(currPath)
#  sys.path.insert(0, parentPath)
#  rootPath = os.path.dirname(currPath)
#  sys.path.insert(0, rootPath)

# ALT:
# os.path.dirname(os.path.realpath(__file__))


__all__ = [  # Exporting objects...
    #  'rootPath',
]
