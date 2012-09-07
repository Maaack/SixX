#!/usr/bin/env python
# Plane Class
import pymunk
from classes.basics.Wall import *

class Plane:
    def __init__(self, (height, width), position = (0,0)):
        self.size = (height, width)
        self.position = position
        self.space = pymunk.Space()
        # Gravity vector
        self.space.gravity = (0.0, 0.0)
        self.prev_step_time = 0
        self.next_step_time = 0


        self.borders = [[(0,0), (0, width)],
            [(0, width), (height, width)],
            [(height, width), (height, 0)],
            [(height, 0), (0,0)]]

        self.walls = []

        for border in self.borders:
            a, b = border
            the_wall = Wall(a, b)
            self.walls.append(the_wall)
            self.space.add(the_wall.get_shape())

        # Add Walls to the Surface based on size.
        # The Walls should probably make a hexagon.
        # For fucks sake why not Gahh!?!

    def add(self, *args):
        for arg in args:
            self.space.add(arg)

    def display(self, screen, offset = (0,0)):
        for wall in self.walls:
            wall.display(screen, offset)
        self.space.step(self.next_step_time)
        self.prev_step_time = self.next_step_time

    def step(self, step):
        self.next_step_time = step
        return self.prev_step_time


    # Just for debugging
    def __str__(self):
        return "( " + str(self.position.x) + ", " + str(self.position.y) + " ) "
