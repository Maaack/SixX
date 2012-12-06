#!/usr/bin/env python
# SpaceTime Class
from game.libs import *
from game.pymunk import *
from game.classes import *

class SpaceTime:
    def __init__(self, GameObject, space_size):
        self.game = GameObject
        self.size = (width, height) = space_size
        self._Space = Space()
        self._Space.set_default_collision_handler( begin = GameObject.collision_begin_func, pre_solve = GameObject.collision_pre_solve_func )

        # Gravity vector
        self._Space.gravity = (0.0, 0.0)
        self.prev_step_time = 0
        self.next_step_time = 0

        self._all_objects = []
        self._display_objects = []
        self._skip_adding_objects = []

    def add(self, *args):
        for arg in args:
            self._Space.add_post_step_callback(self.add_to_space, arg)

    def remove(self, *args):
        for arg in args:
            self._Space.add_post_step_callback(self.remove_from_space, arg)

    def display(self, game, screen, offset = (0,0)):
        for wall in self.walls:
            wall.display(game, screen, offset)
        self._Space.step(self.next_step_time)
        self.prev_step_time = self.next_step_time

    def step(self, step):
        self.next_step_time = step
        self._Space.step(step)
        return self.prev_step_time

    def add_to_space(self, arg):
        if arg not in self._all_objects and arg not in self._skip_adding_objects:
            self._all_objects.append(arg)
            self._Space.add(arg)

    def remove_from_space(self, arg):
        if arg in self._all_objects:
            self._all_objects.remove(arg)
            self._Space.remove(arg)
        else:
            self._skip_adding_objects.append(arg)

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
                self.remove(shape)


        if len(EnergyObjects) == 1 and len(AtomObjects) == 1:
            if register:
                self.energy_atom_collision_func(EnergyObjects[0], AtomObjects[0])
            return False

        if len(AtomObjects) == 2:
            if register:
                self.atom_atom_collision_func(AtomObjects)
            return True

        return True

    def energy_atom_collision_func(self, EnergyObject, AtomObject):
        AtomObject.contact_Energy(EnergyObject)
        return False

    def atom_atom_collision_func(self, AtomObjects):
        return True
