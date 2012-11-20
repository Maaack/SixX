#!/usr/bin/env python
# Surface Class
import pygame
import math
from game.libs import *
import game.pymunk

class Surface:
    def __init__(self):
        self.space = pymunk.Space()
        # Gravity vector
        # self.space.gravity = (0.0, 300.0)
        self.space.set_default_collision_handler(default_collision_func)

    def display(self):
        return 0

    def add(self, *args):
        self.space.add(args)

    # Just for debugging
    def __str__(self):
        return "( " + str(self) + " ) "
