#!/usr/bin/env python
# Level Class
from game.libs import *
from game.pymunk import *
from game.classes import *
__author__ = 'marek'

class Level(object):
    _contents = []
    _players = []

    def add_Element(self, ElementData):
        if isinstance(ElementData, ElementData):
            self._contents.append(ElementData)

    def add_Player(self, GameElement):
        if isinstance(GameElement, elements.Element):
            self._contents.append(GameElement)

