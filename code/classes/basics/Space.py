#!/usr/bin/env python
# Atom Class
import pymunk

class Surface:
    def __init__(self):
        self.space = pymunk.Space()
        # Gravity vector
        # self.space.gravity = (0.0, 300.0)

    def display(self):
        return 0

    def add(self, *args):
        self.space.add(args)

    # Just for debugging
    def __str__(self):
        return "( " + str(self) + " ) "
