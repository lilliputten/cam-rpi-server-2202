# -*- coding:utf-8 -*-
# @module test-request.py
# @desc Test local/remote requests using session cookies.
# @since 2022.02.14, 06:07
# @changed 2022.02.14, 07:25

#  import traceback
import requests
import os
from os import path
import time
import sys
import inspect
import pickle

# Add parent dir to default exports...
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  # noqa
parentdir = os.path.dirname(currentdir)  # noqa
sys.path.insert(0, parentdir)  # noqa

from server.logger import DEBUG
import server.errors


cookiesFilename = 'log-cookies-py.data'  # File to save cookies between sessions

requestsSession = requests.Session()

#  testUrlPrefix = 'http://localhost:5000'
testUrlPrefix = 'https://cam-rpi-server.lilliputten.ru'


def convertCookiesToString(cookies):
    if not cookies:
        return ''
    return '; '.join([str(x)+'='+str(y) for x, y in cookies.items()])


def saveCookiesToFile(requestsSession):
    with open(cookiesFilename, 'wb') as f:
        cookies = requestsSession.cookies
        pickle.dump(cookies, f)


def loadCookiesFileFile(requestsSession):
    if path.isfile(cookiesFilename):
        with open(cookiesFilename, 'rb') as f:
            cookies = pickle.load(f)
            requestsSession.cookies.update(cookies)


def makeRequest(requestsSession, url):
    try:
        DEBUG('test-request:makeRequest: request starting', {
            'url': url,
            'requestsSession.cookies': convertCookiesToString(requestsSession.cookies),
        })
        # Make request...
        res = requestsSession.get(url)
        reason = res.reason
        headers = res.headers
        ok = res.ok
        status_code = res.status_code
        if not ok or status_code != 200:
            DEBUG('test-request:makeRequest: got invalid response', {
                'url': url,
                'headers': str(headers),
                'reason': reason,
                'ok': ok,
                'status_code': status_code,
            })
            raise Exception('Request "' + url + '" got error "' + reason + '" with code: ' + str(status_code))
        cookies = res.cookies
        contentLengthHeader = headers['Content-Length'] if 'Content-Length' in headers else ''
        contentTypeHeader = headers['Content-Type'] if 'Content-Type' in headers else ''
        isJson = 'application/json' in contentTypeHeader
        result = res.json() if isJson else res.text
        DEBUG('test-request:makeRequest: request done', {
            'url': url,
            'cookies': convertCookiesToString(cookies),
            'contentTypeHeader': contentTypeHeader,
            'contentLengthHeader': contentLengthHeader,
            'isJson': isJson,
            #  'headers': str(headers),
            #  'reason': reason,
            #  'ok': ok,
            #  'status_code': status_code,
            #  'result': result,
            #  'text': res.text,
            #  'res': res,
        })
        return result
    except Exception as err:
        sError = server.errors.toString(err, show_stacktrace=False)
        #  sError = str(err)
        #  sTraceback = str(traceback.format_exc())
        DEBUG('test-request:makeRequest: catched error', {
            'url': url,
            'error': sError,
            #  'traceback': sTraceback,
        })
        # return err
        raise err


def testRequest(requestsSession, url):
    try:
        DEBUG('test-request:testRequest: request starting', {
            'url': url,
        })
        data = makeRequest(requestsSession, url)
        DEBUG('test-request:testRequest: request done', {
            'url': url,
            'data': data,
        })
    except Exception as err:
        sError = server.errors.toString(err, show_stacktrace=False)
        #  sError = str(err)
        #  sTraceback = str(traceback.format_exc())
        DEBUG('test-request:testRequest: catched error', {
            'url': url,
            'error': sError,
            #  'traceback': sTraceback,
        })


def testRequests(requestsSession):
    loadCookiesFileFile(requestsSession)
    testRequest(requestsSession, testUrlPrefix + '/session/set_name/eee')
    time.sleep(3)
    testRequest(requestsSession, testUrlPrefix + '/session/get_name')
    saveCookiesToFile(requestsSession)


testRequests(requestsSession)
