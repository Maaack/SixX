#!/usr/bin/env python
# Circle Class
import pygame
import math
from game.libs import *
from game import pymunk
from game.classes.basics.Basic import Basic

class Circle(Basic):
    strobe_frequency = 2.0
    strobe_size = 5

    def __init__(self, PlaneObject, ElementObject, mass, position, radius, color = (255,255,255), width = 0):
        self._Plane = PlaneObject
        self._Element = ElementObject
        self.radius = radius
        self.color = color
        self.width = width
        self.surface_area = 4 * math.pi * (self.radius ** 2)
        self.mass = self.surface_area / 10
        self.inertia = pymunk.moment_for_circle(self.mass, 0, self.radius)  # 1
        self.body = pymunk.Body(self.mass, self.inertia)  # 2
        self.position = position # 3
        self.body.velocity_limit = 600
        self.body.game_object = ElementObject

        self.shape = pymunk.Circle(self.body, self.radius)  # 4
        self.shape.collision_type = 2
        self.shape.friction = 900.0
        self.shape.elasticity = 0.9
        self.shape.game_object = ElementObject

    def destroy(self):
        if isinstance(self.shape, pymunk.Shape):
            self._Plane.remove(self.shape)
            self.shape.game_object = None
        self.shape = None

        if isinstance(self.body, pymunk.Body):
            self._Plane.remove(self.body)
            self.body.game_object = None
        self.body = None