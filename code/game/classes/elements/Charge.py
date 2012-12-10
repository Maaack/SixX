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
from game.classes.elements import Player
from game.classes.elements.Element import Element

class Charge(Element):

    def __init__(self, GameObject, PlayerObject, AtomObject, energy):
        # Checking all inputs to be expected classes.
        if not isinstance(GameObject, game.Game):
            raise Exception("Not a valid type " + str(GameObject) +  " for a Game in " + str(self) + " !")

        if not isinstance(PlayerObject, Player):
            raise Exception("Not a valid type " + str(PlayerObject) +  " for a Player in " + str(self) + " !")

        if not isinstance(AtomObject, Atom.Atom):
            raise Exception("Not a valid type " + str(AtomObject) +  " for a Atom in " + str(self) + " !")

        self._Game = GameObject
        self._Plane = GameObject.Plane
        self._energy_mass = GameObject.energy_mass
        self._energy_capacity = GameObject.energy_capacity
        self._energy_density = GameObject.energy_density
        self._energy_transfer = GameObject.energy_transfer
        self._Player = PlayerObject
        self._color = PlayerObject.color
        self._Atom = AtomObject
        self._position  = AtomObject.get_position()
        self._angle = AtomObject.get_angle()
        self._atom_radius = radius = GameObject.atom_radius


        self._Atom_Pin = None
        self._set_energy(energy)

    def get_display_object(self):
        return self

    def destroy_Basics(self):
        self.destroy_Basic()
        self._Hexagon = None
        self.destroy_Pin()

    def destroy_Pin(self):
        if hasattr(self._Atom_Pin, 'destroy'):
            self._Atom_Pin.destroy()
        self._Atom_Pin = None

    def _set_Hexagon(self, mass, position, radius, angle, color):
        if isinstance(self.BasicObject, Hexagon):
            velocity = self.BasicObject.body.velocity
            self.destroy_Basics()
        else:
            velocity = (0,0)
        self.BasicObject = self._Hexagon = Hexagon(self._Plane, self, mass, position, radius, angle, color, 0, False)
        self._Plane.add(self.BasicObject.body)
        self.BasicObject.body.velocity = velocity
        Pin(self._Game, self, self._Atom)

    def display(self, game, screen, offset = (0,0)):
        self.BasicObject.display(game, screen, offset)

    def _get_energy(self):
        return self._energy

    def _set_energy(self, energy):
        self._energy = energy
        if energy > 0:
            self._mass = mass = self._energy_mass * energy
            self._radius = radius = ( energy / self._energy_capacity ) * self._atom_radius
            self._color = color = self._Player.color
            self._position = position = self._Atom.get_position()
            self._angle = angle = self._Atom.get_angle()
            self._set_Hexagon(mass, position, radius, angle, color)
        else:
            self.destroy()

    energy = property(_get_energy, _set_energy)

    def get_Player(self):
        return self._Player

    def add_Pin(self, PinObject):
        if isinstance(PinObject, Pin):
            self._Atom_Pin = PinObject