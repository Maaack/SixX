#!/usr/bin/env python
# Energy Class
import math
import game
from game.libs import *
from game.classes.basics.Circle import Circle
from game.classes.basics.Player import Player

class Energy:
    circle = 0

    def __init__(self, GameObject, PlayerObject, position, energy = 100):
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
        self._Plane = GameObject.plane

        GameObject.all_objects.append(self)
        GameObject.display_objects.append(self)

        self._energy_mass = GameObject.energy_mass
        self._energy_density = GameObject.energy_density
        self._color = PlayerObject.color
        self._energy = energy
        self._reset_energy(energy)

        self._energy_transfer = 1
        self._energy_transfer_modifier = 1.0

    def get_physical_object(self):
        return self.circle.body

    def get_movable_object(self):
        return self.get_physical_object()

    def display(self, game, screen, offset = (0,0)):
        self.circle.display(game,screen,offset)

    def is_selected(self, position):
        return get_distance_within(position, self.circle.body.position, self._radius)

    def is_deselected(self, position):
        return get_distance_within(position, self.circle.body.position, self._radius)

    def display_selected(self, game, screen, offset = (0,0)):
        if self.circle == None:
            print "Display_selected when none"
            return False
        self.circle.pulse(game, screen, offset)

    def display_hovering(self, game, screen, offset = (0,0)):
        return True

    def destroy(self):
        self.destroyCircle()
        self._Game.drop_Object(self)


    def destroyCircle(self):
        if isinstance(self.circle, Circle):
            self._Plane.remove(self.circle.body, self.circle.shape)
            self.circle = None


    def _set_energy(self, energy):
        if self._energy != energy:
            self._reset_energy(energy)

    def _reset_energy(self, energy = 0):
        old_energy = self._energy
        self._energy = energy
        if energy > 0:
            self._mass = mass = self._energy_mass * energy
            self._area = area = energy / self._energy_density
            self._radius = radius = math.sqrt(area / math.pi)
            color = self._Player.color
            if isinstance(self.circle, Circle):
                self._position = position = self.circle.body.position
            else:
                position = self._position
            self._makeCircle(mass, position, radius, color)
        else:
            self.destroy()


    def _makeCircle(self, mass, position, radius, color):
        if isinstance(self.circle, Circle):
            force = self.circle.body.force
        else:
            force = (0,0)
        self.destroyCircle()
        self.circle = Circle(self, mass, position, radius, color)
        self._Plane.add(self.circle.body, self.circle.shape)
        self.circle.body.apply_force(force)


    def get_Player(self):
        return self._Player

    def get_energy(self):
        return self._energy

    def transfer_energy(self, energy):
        max_transferable_energy = self._energy_transfer * self._energy_transfer_modifier
        energy = min(self._energy, max_transferable_energy)
        self._set_energy(self._energy - energy)
        # TODO indicate that the Energy lost energy
        return energy