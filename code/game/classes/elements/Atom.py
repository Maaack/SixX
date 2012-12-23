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
import game
from game.classes.basics.Hexagon import Hexagon
from game.classes.basics.Pin import Pin
from game.classes.elements.Player import Player
from game.classes.elements.Charge import Charge
from game.classes.elements.Energy import Energy
from game.classes.elements.Shell import Shell
from game.classes.elements.Element import Element

class Atom(Element):

    def __init__(self, GameObject, position, angle, skill = 'basic', *args, **kwargs):
        """
        :param GameObject:Game
        :param position: (int, int)
        :param angle: float
        :param skill: str
        :param args:
        :param kwargs:
        :return:
        """
        super(Atom, self).__init__()
        # Checking all inputs to be expected classes.
        if not isinstance(GameObject, game.Game):
            raise Exception("Not a valid type " + str(GameObject) +  " for a Game in " + str(self) + " !")

        if ( len(position) == 2 ):
            self._position = position
        else:
            print "Unworthy position " + str(position) + " was given to " + str(self) + " !"
            self._position = position = (0,0)

        self._Game = GameObject
        self._PhysicalWorld = GameObject.SpaceTime.PhysicalWorld

        if skill in GameObject.skills_list:
            self._skill = skill
        else:
            self._skill = skill = 'basic'

        self._radius = radius = GameObject.atom_radius
        self._mass = mass = GameObject.atom_mass
        self._max_charge = GameObject.atom_max_charge

        GameObject.all_objects.append(self)
        GameObject.display_objects.append(self)

        self._angle = angle
        self._Player = None
        self._Shell = None
        self._Charge = None
        self._Charge_Pin = None

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

        self._energy_capacity = GameObject.energy_capacity
        self._energy_transfer = GameObject.energy_transfer
        self._energy_transfer_modifier = 10.0

        self._shell_charge_rate = GameObject.shell_charge_rate

        self.BasicObject = self._Hexagon = Hexagon(self._PhysicalWorld, self, mass, position, radius, angle, 2)
        self._PhysicalWorld.add(self.BasicObject.body, self.BasicObject.shape)

    def get_movable_object(self):
        if isinstance(self._Charge, Charge):
            return self._Charge.get_physical_object()

    def get_radius(self):
        return self._radius

    def destroy_Basics(self):
        self.destroy_Basic()
        self.destroy_Charge()

    def destroy_Charge(self):
        if hasattr(self._Charge, 'destroy'):
            self._Charge.destroy()
        self._Charge = None

    def destroy_Charge_Pin(self):
        if hasattr(self._Charge_Pin, 'destroy'):
            self._Charge_Pin.destroy()
        self._Charge_Pin = None

    def destroy_Shell(self):
        if hasattr(self._Shell, 'destroy'):
            self._Shell.destroy()
        self._Shell = None

    def contact_Energy(self, EnergyObject):
        if not isinstance(EnergyObject, Energy):
            raise Exception("Not a valid type " + str(EnergyObject) +  " for a Energy in " + str(self) + " !")

        player = EnergyObject.get_Player()

        physical_object = EnergyObject.get_physical_object()
        force = physical_object.force

        if isinstance(self._Charge, Charge):
            current_energy = self._Charge.energy
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
            self._set_Charge(player, total_energy)
            self._set_Shell(player, total_energy/self._energy_capacity)
#            energy_mass = self._Game.energy_mass
#            self.hexagon.body.apply_force(force)

    def _get_Charge(self):
        return self._Charge

    def _set_Charge(self, PlayerObject, energy):
        if not isinstance(PlayerObject, Player):
            raise Exception("Not a valid type " + str(PlayerObject) +  " for a Player in " + str(self) + " !")
        if energy > 0:
            self._Player = PlayerObject
            if hasattr(self._Charge, 'energy'):
                self._Charge.energy = energy
            else:
                self._Charge = Charge(self._Game, PlayerObject, self, energy)
        else:
            self.destroy_Charge()

    Charge = property(_get_Charge)

    def _get_Shell(self):
        return self._Shell

    def _set_Shell(self, PlayerObject, strength = 1.0):
        if not isinstance(PlayerObject, Player):
            raise Exception("Not a valid type " + str(PlayerObject) +  " for a Player in " + str(self) + " !")

        if strength > 0.0:
            if strength > 1.0:
                strength = 1.0
            self._Shell_strength = strength

            if not isinstance(self._Shell, Shell):
                self._Shell = Shell(self._Game, PlayerObject, self)
            elif self._Shell.get_Player() != PlayerObject:
                self._Shell.destroy()
                self._Shell = Shell(self._Game, PlayerObject, self)

            self._Shell.strength = strength
            return self._Shell

        else:
            strength = 0.0
            self._Shell_strength = strength
            self.destroy_Shell()

    Shell = property(_get_Shell)

    def add_Pin(self, PinObject):
        if isinstance(PinObject, Pin):
            self._Charge_Pin = Pin

    def create_impulse(self, force):
        max_force = self._energy_transfer
        # TODO: Visual indicator that the energy needs more of itself to perform
        # the desired task optimally.
        force.length = min(force.length, max_force)
        # TODO: Make the energy split and push off it's smaller part to move
        self.BasicObject.body.apply_impulse(force)
