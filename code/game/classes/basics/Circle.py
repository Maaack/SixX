#!/usr/bin/env python
# Circle Class
import pygame
import math
from game.libs import *
from game import pymunk

class Circle:
    strobe_frequency = 2.0
    strobe_size = 5

    def __init__(self, PlaneObject, ElementObject, mass, position, radius, color = (255,255,255), width = 0):
        self._Element = ElementObject
        self._Plane = PlaneObject
        self.position = position
        self.radius = radius
        self.color = color
        self.width = width
        self.surface_area = 4 * math.pi * (self.radius ** 2)
        self.mass = self.surface_area / 10
        self.inertia = pymunk.moment_for_circle(self.mass, 0, self.radius)  # 1
        self.body = pymunk.Body(self.mass, self.inertia)  # 2
        self.body.position = position # 3
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


    def display(self, game, screen, offset = (0,0)):
        point = pymunk.Vec2d(self.body.position)
        point = point + offset
        point_x, point_y = point
        point = (int(round(point_x)), int(round(point_y)))
        radius = int(round(self.radius))
        pygame.draw.circle(screen, self.color, point, radius, int(self.width))
        x2 = math.cos(self.body.angle)*self.radius + point_x
        y2 = math.sin(self.body.angle)*self.radius + point_y
        line_color =  (255,255,255)
        point_2 = (int(round(x2)),int(round(y2)))
        pygame.draw.line(screen, line_color, point, point_2, 2)

    def display_selected(self, game, screen, offset = (0,0)):
        self.pulse(game, screen, offset)

    def display_hovering(self, game, screen, offset = (0,0)):
        return True

    def pulse(self, game, screen, offset = (0,0)):
        strobe_width = interval_triangle_wave(game.real_time, self.strobe_frequency, self.strobe_size)
        width = int(strobe_width)
        point = pymunk.Vec2d(self.body.position)
        point = point + offset
        point_x, point_y = point
        point = (int(round(point_x)), int(round(point_y)))
        radius = int(round(self.radius+width))
        pygame.draw.circle(screen, self.color, point, radius, int(self.width))


    def get_display_object(self):
        return self
