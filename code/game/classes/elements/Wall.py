from game.classes.basics.Line import *
from game.classes.elements.Element import Element
__author__ = 'marek'

class Wall(Element):

    def __init__(self, GameObject, a = (0,0), b = (1,1), radius = 1):
        super(Wall, self).__init__()
        self._Game = GameObject
        self.BasicObject = self._Line = Line(a, b, radius)

