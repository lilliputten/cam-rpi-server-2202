# -*- coding:utf-8 -*-
# @module logger
# @since 2020.02.23, 02:18
# @changed 2020.04.23, 03:48


import yaml
import re


def dictFromClass(cls):
    return dict(
        (key, value)
        for (key, value) in cls.__dict__.items()
        #  if key not in _excluded_keys
    )


# Yaml extending (TODO: Extract to separated module)...
# See:
# - https://www.programcreek.com/python/example/104725/yaml.add_representer


def truncateLongString(s, maxLength=0):
    if maxLength and len(s) >= maxLength:
        s = s[0:maxLength-3] + '...'
    return s


def prepareLongString(s, maxLength=0):
    s = re.sub(r'\s+\n', '\n', s)
    return truncateLongString(s, maxLength)


class CustomYamlDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(CustomYamlDumper, self).increase_indent(flow, False)


def yamlReprStr(dumper, data):
    hasNewlines = '\n' in data or '\r' in data
    if (hasNewlines):  # Block style for long multiline strings...
        useStyle = '|' if len(data) > 30 else '"'
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style=useStyle)
    elif re.search(r'["\'\\ /]', data):
        #  style = '"' if "'" in data and '"' not in data else "'"
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='\'')
    else:
        return dumper.represent_str(data)
        #  return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='')


yaml.add_representer(str, yamlReprStr)


class BlockString:

    # default constructor
    def __init__(self, string, maxLength=0):
        self.string = string
        self.maxLength = maxLength

    def prepareString(self):
        return prepareLongString(self.string, self.maxLength)


def reprBlockString(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data.prepareString(), style='|')


yaml.add_representer(BlockString, reprBlockString)
