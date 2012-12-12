import game
from game.classes.basics.Line import *
from game.classes.elements.Element import Element
__author__ = 'marek'

class Wall(Element):

    def __init__(self, GameObject, a = (0,0), b = (1,1), radius = 1):
        super(Wall, self).__init__()
        # Checking all inputs to be expected classes.
        if not isinstance(GameObject, game.Game):
            raise Exception("Not a valid type " + str(GameObject) +  " for a Game in " + str(self) + " !")
        self._Game = GameObject
        self._PhysicalWorld = GameObject.SpaceTime.PhysicalWorld
        self.BasicObject = self._Line = Line(self, a, b, radius)
        self._PhysicalWorld.add(self.BasicObject.shape)

