#!/usr/bin/env python
# Pin Class
import game
from game.libs import *
from game import pymunk

class Pin:
    def __init__(self, GameObject, GameElementA, GameElementB):
        # Checking all inputs to be expected classes.
        if not isinstance(GameObject, game.Game):
            raise Exception("Not a valid type " + str(GameObject) +  " for a Game in " + str(self) + " !")
        self._Game = GameObject
        self._Plane = GameObject.plane

        if hasattr(GameElementA, 'get_physical_object'):
            BodyA = GameElementA.get_physical_object()
        else:
            BodyA = GameElementA

        if hasattr(GameElementB, 'get_physical_object'):
            BodyB = GameElementB.get_physical_object()
        else:
            BodyB = GameElementB

        self.GameElementA = GameElementA
        self.GameElementB = GameElementB

        if isinstance(BodyA, pymunk.Body) and isinstance(BodyB, pymunk.Body):
            offset = pymunk.Vec2d(1,1)
            positionA = BodyA.position
            positionB = BodyB.position
            if get_distance_within(positionA, positionB , 0):
                constraint = pymunk.constraint.PivotJoint(BodyA, BodyB, positionA)
                #joint = pymunk.constraint.PivotJoint(self.body, body, position_self, position_other)
            else:
                constraint =  pymunk.constraint.PinJoint(BodyA, BodyB, positionA, positionB)
                #pymunk.constraint.PinJoint(self.body, body)
            self._Plane.add(constraint)
            self._Constraint = constraint
            constraint.game_object = self
        else:
            raise Exception("Not a valid type " + str(BodyA) +  " for a Body in " + str(self) + " !")

        if hasattr(GameElementA, 'add_Pin'):
            GameElementA.add_Pin(self)

        if hasattr(GameElementB, 'add_Pin'):
            GameElementB.add_Pin(self)

    def destroy(self):
        self._Plane.remove(self._Constraint)
        self._Constraint = None


