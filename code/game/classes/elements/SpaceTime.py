#!/usr/bin/env python
# SpaceTime Class
""" Each SpaceTime will be like an alternate timeline of the current
  running game.  Most of the time I'm guessing I'll handle one (or even none),
  but I want this to be the class responsible for handling the timeline, splitting,
  rewinding and all the events that occur in the world should probably be logged
  in the SpaceTime continuum.  Mmmm... continuum.

"""
from game.libs import *
from game.pymunk import *
from game.classes import *
import time
from game.classes.basics import PhysicalWorld

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

    def create_Energy(self, PlayerObject, **kwargs):
        the_energy = Energy(self._Game, PlayerObject, **kwargs)
        self._objects.append(the_energy)
        self._visible_objects.append(the_energy)
        return the_energy

    def create_Atom(self, ElementData, **kwargs):
        the_atom = Atom(self._Game, ElementData, **kwargs)
        self._objects.append(the_atom)
        self._visible_objects.append(the_atom)
        return the_atom

    def new_Player(self):
        the_player = Player()
        the_player_id = the_player.id
        self._players[the_player_id] = the_player

        return Player()