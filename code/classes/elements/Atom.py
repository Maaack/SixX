#!/usr/bin/env python
# Atom Class
from classes.basics.Hexagon import Hexagon

class Atom:
    def __init__(self, (x, y), angle, color, skill = 'mimic'):
        radius = 16
        self.skill = skill
        self.hexagon = Hexagon(100, (x, y), radius, angle, color, width = 2)

    def get_display_object(self):
        return self.hexagon

    def get_clickable_object(self):
        return self.hexagon
