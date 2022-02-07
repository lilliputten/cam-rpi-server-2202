# -*- coding:utf-8 -*-
# @module config
# @desc Universal server & client config
# @since 2022.02.06, 23:56
# @changed 2022.02.08, 02:09
# See:
#  - https://docs.python.org/3/library/configparser.html -- ???
#  - https://stackoverflow.com/questions/9590382/forcing-python-json-module-to-work-with-ascii
#  - https://flask.palletsprojects.com/en/2.0.x/config/

from os import path
import json
#  import yaml
import sys

from config_helpers import updateConfigWithYaml, readFiletoString

pythonVersion = sys.version

rootPath = path.dirname(path.abspath(__file__))  # Project root path

yamlConfigFilename = path.join(rootPath, 'config.yml')
yamlLocalConfigFilename = path.join(rootPath, 'config.local.yml')

uploadPath = path.join(rootPath, 'uploads')

#  Build params...
clientTemplatePath = path.join(rootPath, 'cam-client-app-build')
clientStaticPath = path.join(rootPath, 'static')
#  clientStaticPath = path.join(clientTemplatePath, 'static')

#  Generate/read build parameters (version, timetag etc)
#  Default values (empty)...
version = ''
timestamp = ''
timetag = ''
buildTag = ''
#  Filenames...
buildVersionFilename = path.join(rootPath, 'build-version.txt')
buildTagFilename = path.join(rootPath, 'build-tag.txt')
timestampFilename = path.join(rootPath, 'build-timestamp.txt')
timetagFilename = path.join(rootPath, 'build-timetag.txt')
packageFilename = path.join(rootPath, 'package.json')
#  Read version...
#  print('config: packageFilename', packageFilename  # DEBUG)
if path.isfile(buildVersionFilename):
    version = readFiletoString(buildVersionFilename)
elif path.isfile(packageFilename):
    pkgConfigFile = open(packageFilename)
    pkgConfig = json.load(pkgConfigFile)
    version = pkgConfig['version'].encode('ascii')
    pkgConfigFile.close()
# Read timestamp/timetag...
if path.isfile(timestampFilename):
    timestamp = readFiletoString(timestampFilename)
if path.isfile(timetagFilename):
    timetag = readFiletoString(timetagFilename)
# Read/generate buildTag...
if version and timetag:
    buildTag = 'v.' + version + '-' + timetag
elif path.isfile(buildTagFilename):
    buildTag = readFiletoString(buildTagFilename)

config = {  # Default config

    # Application parameters...

    'pythonVersion': pythonVersion,
    'version': version,
    'timestamp': timestamp,
    'timetag': timetag,
    'buildTag': buildTag,

    # Path parameters...

    'rootPath': rootPath,
    'uploadPath': uploadPath,

    # Generated client path (see `cam-client-app-build`, TODO?)

    'clientStaticPath': clientStaticPath,
    'clientTemplatePath': clientTemplatePath,

    # Image parameters...
    #
    #  - [Camera configuration - Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/configuration/camera.md)
    #
    #  Default dimensions: 2592x1944
    #  Half size: 1296x972
    #  Quarter size: 648x486

    'imageWidth': 648,
    'imageHeight': 486,

    # Client parameters... (UNUSED)

    'localImageFile': 'local-image.jpg',
    'remoteUrl': 'https://cam.lilliputten.ru/upload',

    # Image file paramaters...

    'imageExt': '.image',
    'imagesIndex': 'index.txt',

    # Logging...

    'outputLog': True,  # Print log to stdout
    'outputColoredLog': True,  # Use rich output log format with `termcolor`
    'writeLog': True,  # Write log to external file
    'clearLogFile': False,  # Clear log file at start
    'logFileName': 'log.txt',  # Log file name

    # Datetime formats...

    'dateTagFormat': '%y%m%d-%H%M',  # eg: '220208-0204'
    'dateTagPreciseFormat': '%y%m%d-%H%M%S',  # eg: '220208-020423'
    'shortDateFormat': '%Y.%m.%d-%H:%M',  # eg: '2022.02.08-02:04'
    'preciseDateFormat': '%Y.%m.%d-%H:%M:%S',  # eg: '2022.02.08-02:04:23'
    'logDateFormat': '%y%m%d-%H%M%S-%f',  # eg: '220208-020423-255157'
    'detailedDateFormat': '%Y.%m.%d-%H:%M:%S.%f',  # eg: '2022.02.08-02:04:23.255157'

}


updateConfigWithYaml(config, yamlConfigFilename)
updateConfigWithYaml(config, yamlLocalConfigFilename)

#  #  DEBUG
#  print('Config:', config)
#  print('Done')
