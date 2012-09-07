#!/usr/bin/env python
# MyCircle Class
# Experimenting with circles that rotate so that
# I may eventually get to hexagons.
import pymunk
import math
import libs
from libs import *

class Circle:
    def __init__(self, position, size, color = (255,255,255), width = 1, mass = 100):
        self.position = position
        self.size = size
        self.color = color
        self.width = width
        self.surface_area = 4 * math.pi * (self.size ** 2)
        self.mass = self.surface_area / 10
        self.inertia = pymunk.moment_for_circle(self.mass, 0, self.size)  # 1
        self.body = pymunk.Body(self.mass, self.inertia)  # 2
        self.body.position = position # 3
        self.shape = pymunk.Circle(self.body, self.size )  # 4
        self.shape.friction = 900.0
        self.shape.elasticity = 0.9

    def point_in_shape(self, (x,y)):
        return self.shape.point_query((x,y))

    def display(self, screen, offset = (0,0)):
        offset = pymunk.Vec2d(offset)
        x, y = self.shape.offset
        point = pymunk.Vec2d(int(x), int(y))
        point = point + offset
        x2 = math.cos(self.body.angle)*self.size + point.x
        y2 = math.sin(self.body.angle)*self.size + point.y
        pygame.draw.circle(screen, self.color, p, self.size, self.width)
        pygame.draw.line(screen, white, point, (x2,y2), 2)

    def get_display_object(self):
        return self

    def get_clickable_object(self):
        return self

    def apply_force(self, f, r = (0,0)):
        vector = pymunk.Vec2d(f)
        self.body.apply_force(vector, r)

    def apply_impulse(self, j, r=(0, 0)):
        vector = pymunk.Vec2d(j)
        self.body.apply_impulse(vector, r)

    def get_body(self):
        return self.body, self.shape
