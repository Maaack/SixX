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

    def point_in_shape(self, (x,y)):
        return self.shape.point_query((x,y))

    def display(self, screen, offset = (0,0)):
        points = self.get_points()
        offset_points = []
        for point in points:
            offset_points.append((pymunk.Vec2d(point) + pymunk.Vec2d(offset)))
        pygame.draw.polygon(screen, self.color, offset_points, 0)

    def strobe(self, screen, offset = (0,0), level = 6):
        width = int(level)
        points = self.get_points()
        offset_points = []
        for point in points:
            offset_points.append((pymunk.Vec2d(point) + pymunk.Vec2d(offset)))
        pygame.draw.lines(screen, self.color, 1, offset_points, width)

    def get_points(self):
        shape_points = self.shape.get_points()
        points = []
        for (x, y) in shape_points:
            points.append((int(round(x)), int(round(y))))
        self.points = points
        return self.points

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

    # Just for debugging
    def __str__(self):
        return "( " + str(self.shape) + ", " + str(self.body) + " ), " + str(self.mass) + ", " + str(self.radius) + ", " + str(self.surface_area)
