#!/usr/bin/env python
# Atom Class
from Hexagon import Hexagon

class Atom:
    def __init__(self, (x, y), angle, color, skill = 'mimic'):
        radius = 8
        self.skill = skill
        self.hexagon = Hexagon(100, (x, y), radius, angle, color)

    def get_display_object(self):
        return self.hexagon

    def get_clickable_object(self):
        return self.hexagon

    # Just for debugging
    def __str__(self):
        return "( " + str(self.position.x) + ", " + str(self.position.y) + " ) "
