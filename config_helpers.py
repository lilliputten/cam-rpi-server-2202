# -*- coding:utf-8 -*-
# @module config_helpers
# @since 2022.02.07, 00:04
# @changed 2022.02.07, 00:04

from os import path
import yaml
#  import json
#  import sys


def updateConfigWithYaml(config, file):
    """
    Extend config from file
    """
    if path.isfile(file):
        with open(file) as file:
            #  print 'Extending config with', file
            yamlConfigData = yaml.load(file, Loader=yaml.FullLoader)
            #  print 'yamlConfigData:', yamlConfigData
            config.update(yamlConfigData)


def readFiletoString(file):
    """
    Read text string from file
    """
    if path.isfile(file):
        with open(file) as fh:
            #  print 'Extending config with', file
            data = fh.read().strip()
            fh.close()
            return data
