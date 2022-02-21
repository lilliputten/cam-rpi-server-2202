# -*- coding:utf-8 -*-
# @module testUtils
# @since 2022.02.15, 05:02
# @changed 2022.02.21, 22:15

#  import traceback
#  import re
#  from src.lib import utils


#  def getTrace(str=None):
#      # NOTE: Required to pass extracted traceback
#      traces = traceback.extract_stack(None, 2)
#      lastTrace = traces[0]
#      modPath = lastTrace[0]
#      modNameMatch = re.search(r'([^\\/]*).py$', modPath)
#      modName = modNameMatch.group(1) if modNameMatch else modPath
#      funcName = lastTrace[2]
#      strList = [
#          #  __name__,
#          modName,
#          funcName,
#          str,
#      ]
#      filteredList = list(filter(None, strList))
#      traceResult = ':'.join(filteredList)
#      print('@:testUtils:getTrace', {
#          'traceResult': traceResult,
#          'traces': traces,
#          'lastTrace': lastTrace,
#          #  'modPath': modPath,
#          'modName': modName,
#          'funcName': funcName,
#      })
#      return traceResult


__all__ = [  # Exporting objects...
    #  'getTrace',
]
