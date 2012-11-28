#!/usr/bin/env python
# Charge Class
"""
This object gets attached to an atom to
indicate that the Atom has charge built inside
of it.  This object can be used to maintain
a shield or charge of the whole atom.  It should
be attached to the Atom hexagon object with a
pinJoint so that it's mass gets calculated in
the physics of the containing Hexagon.

Needs to be removed every time it changes size
because of the limitation of Chipmunk not handling
objects changing mass spontaneously. :-(

"""
import game
import Atom
from game.classes.basics.Pin import Pin
from game.classes.basics.Hexagon import Hexagon
from game.classes.basics.Player import Player
from game.classes.elements.Element import Element

class Charge(Element):

    def __init__(self, GameObject, PlayerObject, AtomObject, charge, scale = 1.0):
        # Checking all inputs to be expected classes.
        if isinstance(GameObject, game.Game):
            self._Game = GameObject
            self._Plane = GameObject.plane
        else:
            raise Exception("Not a valid type " + str(GameObject) +  " for a Game in " + str(self) + " !")

        if isinstance(PlayerObject, Player):
            self._Player = PlayerObject
            self._color = color = PlayerObject.color
        else:
            raise Exception("Not a valid type " + str(PlayerObject) +  " for a Player in " + str(self) + " !")

        if isinstance(AtomObject, Atom.Atom):
            self._Atom = AtomObject
            self._position = position = AtomObject.get_position()
            self._angle = angle = AtomObject.get_angle()
            atom_radius = AtomObject.get_radius()
        else:
            raise Exception("Not a valid type " + str(AtomObject) +  " for a Atom in " + str(self) + " !")

        if ( len(position) == 2 ):
            self._position = position
        else:
            self._position = position = (0,0)
            print "Unworthy position " + str(position) + " was given to " + str(self) + " !"

        if scale > 1.0:
            scale = 1.0
        elif scale < 0.0:
            scale = 0.0

        self._Atom_Pin = None
        self._charge = charge
        self._radius = radius = scale * atom_radius
        self.BasicObject = self._Hexagon = Hexagon(self._Plane, self, charge, position, radius, angle, color, 0, False)
        self._Plane.add(self.BasicObject.body)

    def get_display_object(self):
        return self

    def destroy_Basic(self):
        if hasattr(self._Atom_Pin, 'destroy'):
            self._Atom_Pin.destroy()
        self._Atom_Pin = None

        if hasattr(self.BasicObject, 'destroy'):
            self.BasicObject.destroy()
        self.BasicObject = None

    def display(self, game, screen, offset = (0,0)):
        self.BasicObject.display(game, screen, offset)

    def get_charge(self):
        return self._charge

    def _set_charge(self):
        return self._charge


    def get_Player(self):
        return self._Player

    def add_Pin(self, PinObject):
        if isinstance(PinObject, Pin):
            self._Atom_Pin = PinObject