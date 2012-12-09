#!/usr/bin/env python
# Plane Class
from game.libs import *
from game.pymunk import *
from game.classes.basics.Line import *

class Plane:
    def __init__(self, game, (height, width)):
        self.game = game
        self.size = (height, width)
        self.space = Space()
        self.space.set_default_collision_handler( begin = game.collision_begin_func, pre_solve = game.collision_pre_solve_func )

        # Gravity vector
        self.space.gravity = (0.0, 0.0)
        self.prev_step_time = 0
        self.next_step_time = 0

        self._all_objects = []
        self._skip_adding_objects = []

        self.borders = [[(0,0), (0, width)],
            [(0, width), (height, width)],
            [(height, width), (height, 0)],
            [(height, 0), (0,0)]]

        self.walls = []

        for border in self.borders:
            a, b = border
            the_wall = Line(a, b)
            self.walls.append(the_wall)
            self.space.add(the_wall.get_shape())

        # Add Walls to the Surface based on size.
        # The Walls should probably make a hexagon.

    def add(self, *args):
        for arg in args:
            self.space.add_post_step_callback(self.add_to_space, arg)

    def remove(self, *args):
        for arg in args:
            self.space.add_post_step_callback(self.remove_from_space, arg)

    def display(self, game, screen, offset = (0,0)):
        for wall in self.walls:
            wall.display(game, screen, offset)
        self.space.step(self.next_step_time)
        self.prev_step_time = self.next_step_time

    def step(self, step):
        self.next_step_time = step
        return self.prev_step_time

    def add_to_space(self, arg):
        if arg not in self._all_objects and arg not in self._skip_adding_objects:
            self._all_objects.append(arg)
            self.space.add(arg)

    def remove_from_space(self, arg):
        if arg in self._all_objects:
            self._all_objects.remove(arg)
            self.space.remove(arg)
        else:
            self._skip_adding_objects.append(arg)


