#!/usr/bin/env python
# Level Class
from game.libs import *
from game.pymunk import *
from game.classes import *
__author__ = 'marek'

class ElementData(object):
    _data = {}
    def __init__(self, ElementData = None):
        if isinstance(ElementData, DictType):
            self._data = ElementData