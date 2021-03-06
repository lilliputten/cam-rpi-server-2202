# -*- coding:utf-8 -*-
# @module test-local-command
# @since 2022.02.08, 03:15
# @changed 2022.02.14, 06:07

#  import os
#  import errno
import subprocess
import traceback
import os
import sys
import inspect

# Add parent dir to default exports...
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  # noqa
parentdir = os.path.dirname(currentdir)  # noqa
sys.path.insert(0, parentdir)  # noqa

from server.logger import DEBUG
import server.errors


def execCmd():
    #  cmd = ['echox', 'More output']
    #  cmd = ['raspistill', '-w 648 -h 486 -o temp/test-image.jpg']
    #  cmd = 'raspistill -w 648 -h 486 -o temp/test-image.jpg'
    cmd = [
        'raspistill',
        '-w',
        '648',
        '-h',
        '486',
        '-o',
        'temp/test-image.jpg',
    ]
    #  cmd = ['raspistill', '--help']
    DEBUG('test-local-command:execCmd: Execution started', {
        'cmd': cmd,
    })
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        bStdout, bStderr = process.communicate()
        stdout = bStdout.decode('utf-8').strip()
        stderr = bStderr.decode('utf-8').strip()
        DEBUG('test-local-command:execCmd: Execution success', {
            'stdout': stdout,
            'stderr': stderr,
        })
    except Exception as err:
        errno = err.errno
        sError = server.errors.toString(err, show_stacktrace=False)
        #  sError = str(err)
        sTraceback = str(traceback.format_exc())
        DEBUG('test-local-command:execCmd: catched error', {
            'cmd': cmd,
            'errno': errno,
            'error': sError,
            'traceback': sTraceback,
        })


execCmd()
