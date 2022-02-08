# -*- coding:utf-8 -*-
# @module raspistillUtils
# @since 2022.02.08, 04:10
# @changed 2022.02.08, 06:11

#  import os
#  import errno
import subprocess
import traceback

from os import path
from flask import send_file

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from . import pathmagic  # noqa

from config import config

#  from config import config

from .logger import DEBUG
#  from .errors import * as errors
from . import errors


def sendImageFile(imgPath, mimeType='image/jpeg'):
    DEBUG('sendImageFile: started', {
        'imgPath': imgPath,
        'mimeType': mimeType,
    })
    if not path.isfile(imgPath):
        #  return 'imageNotFound'
        #  return render_template('imageNotFound.html', id=id)
        errStr = 'No image file exists'
        DEBUG('raspistillUtils:sendImageFile: error: ' + errStr, {
            'imgPath': imgPath,
        })
        raise Exception(errStr)
    fileSize = path.getsize(imgPath)
    DEBUG('raspistillUtils:sendImageFile: image found', {
        'imgPath': imgPath,
        'fileSize': int(fileSize),
    })
    return send_file(imgPath, mimetype=mimeType)
    #  return render_template('viewImage.html', id=id, timestamp=timestamp, imageWidth=imageWidth, imageHeight=imageHeight, params=params)


def makeShot(debug=False):
    """
    Executes external shot command.
    Returns shot file name.
    """
    imgFile = 'test-image.jpg' if debug else config['localImageFile']
    imgPath = path.join(config['rootPath'], imgFile)
    realCmd = [
        'raspistill',
        '-w',
        str(config['imageWidth']),
        '-h',
        str(config['imageHeight']),
        '-o',
        imgPath,
        #  config['localImageFile'],
        #  'test-image.jpg',
    ]
    debugCmd = ['echo', 'Debug output']
    #  debugCmd = ['cat', imgPath]
    #  cmd = ['raspistill', '-w 648 -h 486 -o test-image.jpg']
    #  cmd = 'raspistill -w 648 -h 486 -o test-image.jpg'
    #  cmd = ['raspistill', '--help']
    cmd = debugCmd if debug else realCmd
    cmdStr = ' '.join(cmd)
    DEBUG('raspistillUtils:execCmd: Execution started', {
        #  'cmd': cmd,
        'imgPath': imgPath,
        'cmd': cmdStr,
    })
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        bStdout, bStderr = process.communicate()
        sStdout = bStdout.decode('utf-8').strip()
        sStderr = bStderr.decode('utf-8').strip()
        DEBUG('raspistillUtils:execCmd: Execution success', {
            'imgPath': imgPath,
            'cmd': cmdStr,
            #  'stdout': bStdout,
            'stdout': sStdout,
            'stderr': sStderr,
        })
        # Try to load image file...
        if not path.isfile(imgPath):
            errStr = 'No image file exists'
            DEBUG('raspistillUtils:execCmd: ' + errStr, {
                'imgPath': imgPath,
            })
            raise Exception(errStr)
        return imgPath
        #  with open(imgPath, 'rb') as fh:
        #      data = fh.read()
        #      DEBUG('raspistillUtils:execCmd: Image data loaded', {
        #          'imgPath': imgPath,
        #          'size': len(data),
        #      })
        #      return data
    except Exception as err:
        nErrno = err.errno if hasattr(err, 'errno') else None  # http response errno (if http error)
        sError = errors.toString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        DEBUG('raspistillUtils:execCmd: catched error', {
            'imgPath': imgPath,
            'cmd': cmdStr,
            'errno': nErrno,
            'error': sError,
            'traceback': sTraceback,
        })
        #  raise err
        detailsDebug = ': cmd=`' + cmdStr + '`, imgPath=`' + imgPath + '`, error: ' + sError
        detailsReal = '.'
        errStr = 'Cannot execute camera shot command' + (detailsDebug if debug else detailsReal)
        raise Exception(errStr)


__all__ = [  # Exporting objects...
    'makeShot',
]

if __name__ == '__main__':
    DEBUG('raspistillUtils test', {
    })