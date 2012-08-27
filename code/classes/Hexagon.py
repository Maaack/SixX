#!/usr/bin/env python
# Hexagon Class
import pygame
import pymunk
import math
import libs
from libs import *


class Hexagon:
    def __init__(self, mass, position, radius, angle = 0, color = ( 0, 0, 0 ), width = 1, friction = 900.0, elasticity = 0.9 ):
        self.mass = mass
        self.position = position
        self.radius = radius
        # So simple that the perimeter is just 6x the radius.
        self.perimeter = 6 * radius
        # Set surface area to ( 3 * sqrt(3) / 2 ) r ^ 2
        self.surface_area = ( 3 * math.sqrt( 3 ) / 2 ) * ( radius ** 2 )
        self.color = color
        self.width = width
        self.points = get_hex_points(radius, angle)
        self.inertia = pymunk.moment_for_poly(self.mass, self.points)  # 1
        self.body = pymunk.Body(self.mass, self.inertia)  # 2
        self.body.position = position # 3
        self.shape = pymunk.Poly(self.body, self.points)  # 4
        self.shape.friction = friction
        self.shape.elasticity = elasticity

    def display(self, screen):
        points = self.get_points()
        pygame.draw.polygon(screen, self.color, points, 0)

    def highlight(self, screen):
        max_width = 4
        frequency = 2
        points = self.get_points()
        pulse_time = get_game_time() % (1000 / frequency)
        interval = pulse_time * max_width / (1000 / (frequency * 2))
        if ( interval > max_width ):
            width = max_width - (interval - max_width)
        else:
            width = interval
        pygame.draw.lines(screen, self.color, 1, points, width)

    def get_points(self):
        shape_points = self.shape.get_points()
        points = range(6)
        for i , (x, y) in enumerate(shape_points):
            points[i] = int(x), int(y)
        self.points = points
        return self.points

    def apply_force(self, vector = (0,0), offset  = (0,0)):
        vector.normalize_return_length()
        self.body.apply_force(vector, offset)

    def get_body(self):
        return self.body, self.shape

    # Just for debugging
    def __str__(self):
        return "( " + str(self.shape) + ", " + str(self.body) + " ), " + str(self.mass) + ", " + str(self.radius) + ", " + str(self.surface_area)
