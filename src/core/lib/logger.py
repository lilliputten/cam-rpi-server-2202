# -*- coding:utf-8 -*-
# @module logger
# @since 2020.02.23, 02:18
# @changed 2022.02.24, 00:49

#  import pathmagic  # noqa # Add parent path to import paths for import config in debug mode
# from . import pathmagic  # noqa

import math
from os import path
import datetime
import yaml
from termcolor import colored

from config import config

# from . import utils
from . import yamlSupport


def getMsDateTag(now=None, isDetailed=False):
    if not now:
        now = datetime.datetime.now()  # Get current date object
    #  Format date like '2022.02.08-02:04:23.255157' or '220208-020423-255157'
    formatStr = config['detailedDateFormat'] if isDetailed else config['logDateFormat']
    dateTag = now.strftime(formatStr)
    dateTag = dateTag[:-3]  # Convert microseconds (.NNNNNN) to milliseconds (.NNN)
    return dateTag


def getMsTimeStamp(now=None):
    if not now:
        now = datetime.datetime.now()  # Get current date object
    timestamp = math.floor(now.timestamp() * 1000)  # Get milliseconds timestamp (for technical usage)
    return timestamp


def createHeader():
    now = datetime.datetime.now()  # Get current date object
    #  timestamp = math.floor(now.timestamp() * 1000)  # Get milliseconds timestamp (for technical usage)
    timestamp = getMsTimeStamp(now)  # Get milliseconds timestamp (for technical usage)
    #  #  dateTag = now.strftime(config['logDateFormat'])  # Format date like '220208-020423-255157'
    #  dateTag = now.strftime(config['detailedDateFormat'])  # Format date like 2022.02.08-02:04:23.255157
    #  #  if dateTag.endswith('000'):  # Remove extra finsishing '000'
    #  dateTag = dateTag[:-3]  # Convert microseconds (.NNNNNN) to milliseconds (.NNN)
    dateTag = getMsDateTag(now, True)
    header = '[' + str(timestamp) + ' ' + dateTag + ']'
    return header


def createLogData(_title, data=None):
    logData = ''
    if data is not None:
        logData = yaml.dump(data, Dumper=yamlSupport.CustomYamlDumper, default_flow_style=False, indent=2)
        logData = logData.replace('!!python/unicode ', '')
        logData = '  ' + logData.replace('\n', '\n  ').rstrip()  # Indent data
        if not logData.endswith('\n'):
            logData += '\n'
        #  if 'test' in data:
        #      print('Test data:', data)
        #      print('Test yaml:', logData)
    return logData


hasLoggedEntries = False


def DEBUG(title, data=None):
    global hasLoggedEntries  # pylint: disable=global-statement
    header = createHeader()
    logData = createLogData(title, data)  # Ensure trailing newline for record delimiting
    fileMode = 'a'  # Default file mode: append (ab)
    if not hasLoggedEntries:
        #  print('[Log started]\n'  # Insert empty line to stdout)
        if config['clearLogFile']:
            fileMode = 'w'  # Clear file on first entry (wb)
        hasLoggedEntries = True
    if config['writeLog']:
        rootPath = config['rootPath']
        logFile = path.join(rootPath, config['logFileName'])
        with open(logFile, fileMode, encoding='utf-8') as file:
            file.write(header + '\n')
            file.write(title + '\n')
            file.write(logData + '\n')
    if config['outputLog']:
        if config['outputColoredLog']:
            header = colored(header, 'green')
            title = colored(title, 'red')
        print(header + "\n" + title + "\n" + logData)
        #  print(header)
        #  print(title)
        #  print(logData)


__all__ = [  # Exporting objects...
    'DEBUG',
]

if __name__ == '__main__':  # Test
    DEBUG('Test')
