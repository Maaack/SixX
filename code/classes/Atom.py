#!/usr/bin/env python
# Atom Class
from Hexagon import Hexagon

class Atom:
    def __init__(self, (x, y), angle, color, skill = 'mimic'):
        radius = 8
        self.skill = skill
        self.hexagon = Hexagon(100, (x, y), radius, angle, color)

    def display(self, screen):
        self.hexagon.display(screen)

    def highlight(self, screen):
        self.hexagon.highlight(screen)

    def point_in_shape(self, (x,y)):
        return self.hexagon.shape.point_query((x,y))

    # Just for debugging
    def __str__(self):
        return "( " + str(self.position.x) + ", " + str(self.position.y) + " ) "
