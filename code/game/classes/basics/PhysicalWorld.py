#!/usr/bin/env python
# PhysicalWorld Class
import pygame
import math
from game.libs import *
from game.pymunk import *


class PhysicalWorld(object):
    def __init__(self, BasicsList = []):
        self._Space = Space()
        # Gravity vector
        self._Space.gravity = (0.0, 0.0)

        self._all_objects = []
        self._skip_adding_objects = []

        for BasicObject in BasicsList:
            self._add_to_space(BasicObject)

    def step(self, step):
        self._Space.step(step)

    def add(self, *args):
        for arg in args:
            self._Space.add_post_step_callback(self._add_to_space, arg)

    def remove(self, *args):
        for arg in args:
            self._Space.add_post_step_callback(self._remove_from_space, arg)

    def _add_to_space(self, arg):
        if arg not in self._all_objects and arg not in self._skip_adding_objects:
            self._all_objects.append(arg)
            self._Space.add(arg)

    def _remove_from_space(self, arg):
        """ Checks that an object is in the PhysicalWorld before removing it
        because PyMunk doesn't do this and will throws ValueErrors when trying
        to remove the same object multiple times.
        :param arg: Basic
        :return:
        """
        if arg in self._all_objects:
            self._all_objects.remove(arg)
            self._Space.remove(arg)
        else:
            self._skip_adding_objects.append(arg)

    def set_collision_handler(self, **kwargs):
        """ Custom collision detection functions passed directly into PyMunk Space.
        begin : func(space, arbiter, *args, **kwargs) -> bool
        pre_solve : func(space, arbiter, *args, **kwargs) -> bool
        post_solve : func(space, arbiter, *args, **kwargs)
        separate : func(space, arbiter, *args, **kwargs)
        """
        self._Space.set_default_collision_handler(**kwargs)
