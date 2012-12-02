#!/usr/bin/env python
# Shell Class
"""
This object gets attached to an atom to
indicate that the Atom has shell around it.
A shell is associated with a particular Player
and protects that player's energy from evaporating
inside the protection of the shell.

Shell can be easily attached to the charge inside an atom.

Does not add mass (yet) to the rest so therefore doesn't need
a physical component, just needs to display.
"""
from game.libs.math_is_fun import *
import math
import game
import Atom
from game.classes.basics.Player import Player
from game.classes.lines.ChargeLines import ChargeLines
from game.classes.elements.Element import Element

class Shell(Element):

    def __init__(self, GameObject, PlayerObject, AtomObject):
        """
        :param GameObject:GameObject.Game
        :param PlayerObject: Player
        :param AtomObject: Atom
        :return:
        """
        # Checking all inputs to be expected classes.
        if not isinstance(GameObject, game.Game):
            raise Exception("Not a valid type " + str(GameObject) +  " for a Game in " + str(self) + " !")

        if not isinstance(PlayerObject, Player):
            raise Exception("Not a valid type " + str(PlayerObject) +  " for a Player in " + str(self) + " !")

        if not isinstance(AtomObject, Atom.Atom):
            raise Exception("Not a valid type " + str(AtomObject) +  " for an Atom in " + str(self) + " !")

        self._Game = GameObject
        self._Player = PlayerObject
        self._Atom = AtomObject

        self._color = color = PlayerObject.color
        self._points = points = AtomObject.get_points()
        first_point = points[0]
        self._point_count = len(points)
        points.append(first_point)
        self._strength = 0.0

        self._ChargeLines = ChargeLines(points, color, 5, 80)

    def get_display_object(self):
        return self._ChargeLines

    def display(self, game, screen, offset = (0,0)):
        points = self._Atom.get_points()
        points.append(points[0])
        self._ChargeLines.points = points
        return self._ChargeLines.display(game, screen, offset)

    def get_Player(self):
        return self._Player

    def _set_strength(self, strength):
        self._strength = strength
        points = self._Atom.get_points()
        self._point_count = point_count = len(points)
        self._sides = sides = math.floor(strength * point_count)
        self._ChargeLines.show_sides(sides)

    def _get_strength(self):
        return self._strength

    strength = property(_get_strength, _set_strength)

    def _get_points(self):
        return self._points

    def _set_points(self, points):
        self._points = points

    points = property(_get_points, _set_points)


