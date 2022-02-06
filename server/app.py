# -*- coding:utf-8 -*-
# @module app
# @since 2022.02.07, 00:27
# @changed 2022.02.07, 00:27

#  Local imports workaround, @see https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
#  import pathmagic  # noqa

import os

from flask import Flask

from config import config

from werkzeug.routing import BaseConverter


#  rootPath = config['rootPath']
#  clientStaticPath = config['clientStaticPath']
clientTemplatePath = config['clientTemplatePath']

app = Flask(__name__,
            static_url_path='',
            static_folder=clientTemplatePath)


@app.template_filter()
def getenv(key):
    return os.getenv(key)


class ListConverter(BaseConverter):
    regex = r'\S+(?:,\d+)*,?'

    def to_python(self, value):
        return [str(x) for x in value.split(',')]

    def to_url(self, value):
        return ','.join(str(x) for x in value)


app.url_map.converters['list'] = ListConverter

__all__ = [  # Exporting objects...
    'app',
]
