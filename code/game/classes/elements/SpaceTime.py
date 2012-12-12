#!/usr/bin/env python
# SpaceTime Class
""" Each SpaceTime will be like an alternate timeline of the current
  running game.  Most of the time I'm guessing I'll handle one (or even none),
  but I want this to be the class responsible for handling the timeline, splitting,
  rewinding and all the events that occur in the world should probably be logged
  in the SpaceTime continuum.  Mmmm... continuum.

"""
from game.libs import *
from game.classes import *
import time
from game.classes.basics import PhysicalWorld
from game.classes.elements.Wall import Wall
from game.classes.elements.Atom import Atom
from game.classes.elements.Energy import Energy
from game.classes.elements.Charge import Charge
from game.classes.elements.Player import Player

class SpaceTime:
    def __init__(self, GameObject):
        self._Game = GameObject
        self._id = make_hash()
        self._PhysicalWorld = PhysicalWorld()
        self._PhysicalWorld.set_collision_handler(begin=self.collision_begin_func, pre_solve=self.collision_pre_solve_func)

        self._teams = {}
        self._players = {}
        self._objects = []
        self._visible_objects = []
        self._prev_step_time = 0
        self._curr_step_time = 0
        self._events_dict = {0:'init'}

    def _get_PhysicalWorld(self):
        return self._PhysicalWorld

    def _set_PhysicalWorld(self, PhysicalWorldObject):
        if isinstance(PhysicalWorldObject, PhysicalWorld):
            self._PhysicalWorld = PhysicalWorldObject

    PhysicalWorld = property(_get_PhysicalWorld, _set_PhysicalWorld)

    def get_teams(self):
        return self._teams

    def get_players(self):
        return self._players

    def get_visible_objects(self):
        return self._visible_objects

    def get_objects(self):
        return self._objects

    def step(self, step):
        self._prev_step_time = self._curr_step_time
        self._curr_step_time = step
        self._PhysicalWorld.step(step)
        return self._prev_step_time

    def collision_begin_func(self, space, arbiter, *args):
        # self.collision_pre_solve_func(space, arbiter, args, register=False)
        return True

    def collision_pre_solve_func(self, space, arbiter, *args, **kwargs):
        """For each contact, register the collision and figure
        out what to do. """
        GameObjects = []
        EnergyObjects = []
        ChargeObjects = []
        AtomObjects = []
        if 'register' in kwargs:
            register = kwargs['register']
        else:
            register = True
        for shape in arbiter.shapes:
            if hasattr(shape, 'game_object'):
                game_object = shape.game_object
                GameObjects.append(game_object)
                if isinstance(game_object, Atom):
                    AtomObjects.append(game_object)
                elif isinstance(game_object, Energy):
                    EnergyObjects.append(game_object)
                elif isinstance(game_object, Charge):
                    ChargeObjects.append(game_object)
            else:
                self._PhysicalWorld.remove(shape)


        if len(EnergyObjects) == 1 and len(AtomObjects) == 1:
            if register:
                self._Energy_Atom_collision_func(EnergyObjects[0], AtomObjects[0])
            return False

        if len(AtomObjects) == 2:
            if register:
                self._Atom_Atom_collision_func(AtomObjects)
            return True

        return True

    def _Energy_Atom_collision_func(self, EnergyObject, AtomObject):
        AtomObject.contact_Energy(EnergyObject)
        return False

    def _Atom_Atom_collision_func(self, AtomObjects):
        return True

    def new_Energy(self, PlayerObject, position, energy, **kwargs):
        EnergyObject = Energy(self._Game, PlayerObject, position, energy, **kwargs)
        self._objects.append(EnergyObject)
        self._visible_objects.append(EnergyObject)
        return EnergyObject

    def new_Atom(self, position, angle, skill, *args, **kwargs):
        AtomObject = Atom(self._Game, position, angle, skill, *args, **kwargs)
        self._objects.append(AtomObject)
        self._visible_objects.append(AtomObject)
        return AtomObject

    def new_Wall(self, a, b, thickness, **kwargs):
        WallObject = Wall(self._Game, a, b, thickness, **kwargs)
        self._objects.append(WallObject)
        self._visible_objects.append(WallObject)
        return WallObject

    def new_Player(self):
        PlayerObject = Player()
        id = PlayerObject.id
        self._players[ id ] = PlayerObject
        return PlayerObject

    def del_Element(self, ElementObject):
        if ElementObject in self._objects:
            self._objects.remove(ElementObject)
        if ElementObject in self._visible_objects:
            self._visible_objects.remove(ElementObject)