#!/usr/bin/env python
# Energy Class
import math
import game
from game.classes.elements.Player import Player
from game.libs import *
from game.classes.basics.Circle import Circle
from game.classes.elements.Element import Element

class Energy(Element):

    def __init__(self, GameObject, PlayerObject, position, energy = 1000):
        super(Energy, self).__init__()
        # Checking all inputs to be expected classes.
        if not isinstance(GameObject, game.Game):
            raise Exception("Not a valid type " + str(GameObject) +  " for a Game in " + str(self) + " !")

        if isinstance(PlayerObject, Player):
            self._ControllingPlayers = [PlayerObject]
            self._Player = PlayerObject
        elif len(PlayerObject) > 1:
            self._ControllingPlayers = PlayerObject
            self._Player = player = PlayerObject[0]
        else:
            print Player
            raise Exception("Not a valid type for a player!")

        if ( len(position) == 2 ):
            self._position = position
        else:
            print "Unworthy position " + str(position) + " was given to " + str(self) + " !"
            self._position = position = (0,0)

        self._Game = GameObject
        self._PhysicalWorld = GameObject.SpaceTime.PhysicalWorld

        GameObject.all_objects.append(self)
        GameObject.display_objects.append(self)

        self._energy_mass = GameObject.energy_mass
        self._energy_density = GameObject.energy_density
        self._energy_transfer = GameObject.energy_transfer
        self._color = PlayerObject.color
        self._energy_mass_modifier = 1.0
        self._energy_density_modifier = 1.0
        self._energy_transfer_modifier = 10.0
        self._energy = 0
        self._set_energy(energy)


    def display(self, game, screen, offset = (0,0)):
        self.BasicObject.display(game,screen,offset)

    def is_selected(self, position):
        return get_distance_within(position, self.BasicObject.body.position, self._radius)

    def is_deselected(self, position):
        return get_distance_within(position, self.BasicObject.body.position, self._radius)

    def destroy_Basics(self):
        self.destroy_Basic()
        self._Circle = None

    def get_physical_object(self):
        if self.BasicObject == None:
            print "get_phyiscal_body when none"
            return False
        return self.BasicObject.body

    def display_selected(self, game, screen, offset = (0,0)):
        if self.BasicObject == None:
            print "display_selected when none"
            return False
        self.BasicObject.pulse(game, screen, offset)

    def display_hovering(self, game, screen, offset = (0,0)):
        return True

    def _set_Circle(self, mass, position, radius, color):
        if isinstance(self.BasicObject, Circle):
            velocity = self.BasicObject.body.velocity
            self.destroy_Basic()
        else:
            velocity = (0,0)
        r,g,b = color
        color = r, g, b, 127
        self.BasicObject = self._Circle = Circle(self._PhysicalWorld, self, mass, position, radius, color)
        self._PhysicalWorld.add(self.BasicObject.body, self.BasicObject.shape)
        self.BasicObject.body.velocity = velocity

    def get_Player(self):
        return self._Player

    Player = property(get_Player)

    def _get_energy(self):
        return self._energy

    def _set_energy(self, energy):
        self._energy = energy
        if energy > 0:
            self._mass = mass = self._energy_mass * energy
            self._area = area = energy / self._energy_density
            self._radius = radius = math.sqrt(area / math.pi)
            color = self._Player.color
            if isinstance(self.BasicObject, Circle):
                self._position = position = self.BasicObject.body.position
            else:
                position = self._position
            self._set_Circle(mass, position, radius, color)
        else:
            self.destroy()

    energy = property(_get_energy, _set_energy)

    def _get_mass(self):
        return self._mass

    def _set_mass(self, mass):
        self._mass = mass

    mass = property(_get_mass, _set_mass)

    def transfer_energy(self, energy):
        max_transferable_energy = self._energy_transfer * self._energy_transfer_modifier
        energy = min(self._energy, max_transferable_energy)
        self._set_energy(self._energy - energy)
        # TODO indicate that the Energy lost energy
        return energy

    def create_impulse(self, force):
        max_force = self._energy_transfer
        # TODO: Visual indicator that the energy needs more of itself to perform
        # the desired task optimally.
        # force.length = min(force.length, max_force)
        # TODO: Make the energy split and push off it's smaller part to move
        self.BasicObject.body.apply_impulse(force)
