#!/usr/bin/env python
# Atom Class
"""
This object is the atom that energy can get
attached to to create a shell and a charge.

Atom's can have skills associated with them
that are then granted to a player when they
have created a aligned the atom to them.

Aligning an atom... hmmm...


"""
import math
from types import *
import game
from game.classes.basics.Hexagon import Hexagon
from game.classes.basics.Player import Player
from game.classes.elements.Charge import Charge
from game.classes.elements.Energy import Energy
from game.classes.elements.Shell import Shell

class Atom:

    def __init__(self, GameObject, position, angle, skill = 'basic', *args, **kwargs):
        # Checking all inputs to be expected classes.
        if not isinstance(GameObject, game.Game):
            raise Exception("Not a valid type " + str(GameObject) +  " for a Game in " + str(self) + " !")

        if ( len(position) == 2 ):
            self._position = position
        else:
            print "Unworthy position " + str(position) + " was given to " + str(self) + " !"
            self._position = position = (0,0)

        self._Game = GameObject
        self._Plane = GameObject.plane
        if skill in GameObject.skills_list:
            self._skill = skill
        else:
            self._skill = skill = 'basic'

        if skill in GameObject.skill_colors:
            self._color = color = GameObject.skill_colors[skill]
        else:
            self._color = color = ( 0, 0, 0 )

        self._radius = radius = GameObject.atom_radius
        self._mass = mass = GameObject.atom_mass
        self._max_charge = GameObject.atom_max_charge

        GameObject.all_objects.append(self)
        GameObject.display_objects.append(self)

        self._angle = angle
        self._Player = 0
        self._Shell = 0
        self._Charge = 0

        if 'PlayerObject' in kwargs:
            PlayerObject = kwargs['PlayerObject']
            if isinstance(PlayerObject, Player):
                self._Player = PlayerObject

        if 'ShellObject' in kwargs:
            ShellObject = kwargs['ShellObject']
            if isinstance(ShellObject, Shell):
                self._Shell = ShellObject

        if 'ChargeObject' in kwargs:
            ChargeObject = kwargs['ChargeObject']
            if isinstance(ChargeObject, Charge):
                self._Charge = ChargeObject

        self._energy_capacity = 100
        self._energy_transfer = 10
        self._energy_transfer_modifier = 1.0

        self.hexagon = Hexagon(self, mass, position, radius, angle, color, 2)
        self._Plane.add(self.hexagon.body, self.hexagon.shape)

    def get_physical_object(self):
        return self.circle.body

    def get_movable_object(self):
        if isinstance(self._Charge, Charge):
            return self._Charge.body

    def get_radius(self):
        return self._radius

    def get_angle(self):
        return self.hexagon.body.angle

    def get_position(self):
        return self.hexagon.body.position

    def is_hovering(self, position):
        return self.hexagon.shape.point_query(position)

    def is_selected(self, position):
        return False
        #return self.hexagon.shape.point_query(position)

    def is_deselected(self, position):
        return self.hexagon.shape.point_query(position)

    def destroy(self):
        self._Plane.remove(self.hexagon.body, self.hexagon.shape)

    def display(self, game, screen, offset = (0,0)):
        self.hexagon.display(game, screen, offset)
        if isinstance(self._Charge, Charge):
            self._Charge.display(game, screen, offset)

        if isinstance(self._Shell, Shell):
            self._Shell.display(game, screen, offset)

    def display_selected(self, game, screen, offset = (0,0)):
        self.hexagon.strobe(game, screen, offset)

    def display_hovering(self, game, screen, offset = (0,0)):
        self.hexagon.strobe(game, screen, offset)

    def add_charge(self, EnergyObject):
        if not isinstance(EnergyObject, Energy):
            raise Exception("Not a valid type " + str(EnergyObject) +  " for a Energy in " + str(self) + " !")

        player = EnergyObject.get_Player()
        energy = EnergyObject.get_energy()


        if isinstance(self._Charge, Charge):
            current_energy = self._Charge.get_charge()
            if self._Charge.get_Player() != player:
                current_energy = -(current_energy)
                is_opposing = True
            else:
                is_opposing = False

        else:
            current_energy = 0

        if current_energy <= self._energy_capacity:
            max_additional_energy = self._energy_capacity - current_energy
            max_transferable_energy = self._energy_transfer * self._energy_transfer_modifier
            max_transferable_energy = min(max_transferable_energy, max_additional_energy)
            energy = EnergyObject.transfer_energy(max_transferable_energy)
            total_energy = energy + current_energy
            self._set_charge(player, total_energy)


    def _set_charge(self, player, energy):
        if energy < 0:
            self.destroy_Charge()
            return True

        if isinstance(player, Player):
            self._Player = player
        else:
            raise Exception("Not a valid type " + str(player) +  " for a Player in " + str(self) + " !")

        # Destroy the charge before as it may have a new mass
        # now depending on the amount of energy.
        self.destroy_Charge()
        scale = energy / self._energy_capacity
        self._Charge = Charge(self._Game, player, self, energy, scale)
        return self._Charge

    def _create_Shell(self, PlayerObject):
        if isinstance(PlayerObject, Player):
            self._Player = PlayerObject
        else:
            raise Exception("Not a valid type " + str(PlayerObject) +  " for a Player in " + str(self) + " !")

        self._Shell = Shell(self._Game, PlayerObject, self)
        return self._Shell

    def set_Shell(self, PlayerObject, strength = 1.0):
        if strength > 1.0:
            strength = 1.0
        elif strength < 0.0:
            strength = 0.0
            self.destroy_Shell()

        self._shell_strength = strength
        self._update_Shell(PlayerObject, strength)


    def _update_Shell(self, PlayerObject, strength):
        if isinstance(self._Shell, Shell):
            self._Shell.update_strength(strength)

        elif isinstance(PlayerObject, Player):
            self._Player = PlayerObject
            shell = self._create_Shell(self._Player)
            shell.update_strength(strength)
        else:
            raise Exception("Not a valid type " + str(PlayerObject) +  " for a Player in " + str(self) + " !")


    def destroy_Shell(self):
        if isinstance(self._Shell, Shell):
            self._Shell = 0


    def destroy_Charge(self):
        if isinstance(self._Charge, Charge):
            self._Charge.destroy()
            self._Charge = 0

    def contact_energy(self, energy):
        if self._Player == 0:
            self._Player = energy.get_Player()
            self.add_charge(energy)

        elif self._Player == energy.get_Player():
            self.add_charge(energy)
