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
from types import *
from game.Game import *
from game.classes.basics.Player import Player
from game.classes.lines.ChargeLines import ChargeLines

class Shell:

    def __init__(self, GameObject, PlayerObject, AtomObject):
        # Checking all inputs to be expected classes.
        if not isinstance(GameObject, GameObject.Game):
            raise Exception("Not a valid type " + str(GameObject) +  " for a Game in " + str(self) + " !")

        if not isinstance(PlayerObject, Player):
            raise Exception("Not a valid type " + str(PlayerObject) +  " for a Player in " + str(self) + " !")

        if not isinstance(AtomObject, Atom):
            raise Exception("Not a valid type " + str(AtomObject) +  " for an Atom in " + str(self) + " !")


        self._Game = GameObject
        self._Player = PlayerObject
        self._Atom = AtomObject
        self._angle = angle = AtomObject.get_angle()
        self._color = color = PlayerObject.color
        self._radius = radius = GameObject.atom_radius
        self._points  = points = get_hex_points(radius, angle)
        self._strength = 0.0

        self.chargeLines = ChargeLines(self, points, color)

    def get_display_object(self):
        return self.chargeLines

    def get_player(self):
        return self._Player

    def update_strength(self, strength):
        self._strength = strength
        self._sides = sides = math.floor(strength * 6.0)
        self.chargeLines.show_sides(sides)



