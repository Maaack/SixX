#!/usr/bin/env python
# Hexagon Class
import pygame
import math
from game.libs import *
from game import pymunk
from game.classes.basics.Basic import Basic


class Hexagon(Basic):
    strobe_frequency = 2.0
    strobe_size = 5
    game = 0

    def __init__(self, PlaneObject, ElementObject, mass, position, radius, angle = 0, width = 1, shape = True):
        self._Plane = PlaneObject
        self._Element = ElementObject
        self.mass = mass
        self.position = position
        self.radius = radius
        # So simple that the perimeter is just 6x the radius.
        self.perimeter = 6 * radius
        # Set surface area to ( 3 * sqrt(3) / 2 ) r ^ 2
        self.surface_area = ( 3 * math.sqrt( 3 ) / 2 ) * ( radius ** 2 )
        self.width = width
        self.points = get_hex_points(radius, angle)

        self.inertia = pymunk.moment_for_poly(self.mass, self.points)  # 1
        self.body = pymunk.Body(self.mass, self.inertia)  # 2
        self.body.position = position # 3
        self.body.velocity_limit = 600
        self.body.game_object = ElementObject

        if shape:
            friction = 900.0
            elasticity = 0.9
            self.shape = pymunk.Poly(self.body, self.points)  # 4
            self.shape.collision_type = 1
            self.shape.friction = friction
            self.shape.elasticity = elasticity
            # Adding my custom game_object to shape for collision detection
            self.shape.game_object = ElementObject
        else:
            self.shape = None

    def destroy(self):
        if isinstance(self.shape, pymunk.Shape):
            self._Plane.remove(self.shape)
            self.shape.game_object = None
        self.shape = None

        if isinstance(self.body, pymunk.Body):
            self._Plane.remove(self.body)
            self.body.game_object = None
        self.body = None


    def display(self, game, screen, offset = (0,0)):
        angle = self.body.angle
        position = self.body.position
        points_floats = get_hex_points(self.radius,angle,position)
        points = []
        for point in points_floats:
            x, y = point
            points.append((round(x), round(y)))
        pygame.draw.polygon(screen, self.color, points, self.width)


    def strobe(self, game, screen, offset = (0,0)):
        strobe_width = interval_triangle_wave(game.real_time, self.strobe_frequency, self.strobe_size)
        width = int(strobe_width)
        points = self.get_points()
        offset_points = []
        for point in points:
            offset_points.append((pymunk.Vec2d(point) + pymunk.Vec2d(offset)))
        pygame.draw.lines(screen, self.color, 1, offset_points, width)

    def get_points(self):
        if self.shape is not None:
            shape_points = self.shape.get_points()
            points = []
            for (x, y) in shape_points:
                points.append((int(round(x)), int(round(y))))
            self.points = points
            return self.points
        else:
            return False

    def get_display_object(self):
        return self

    # Just for debugging
    def __str__(self):
        return "( " + str(self.shape) + ", " + str(self.body) + " ), " + str(self.mass) + ", " + str(self.radius) + ", " + str(self.surface_area)
