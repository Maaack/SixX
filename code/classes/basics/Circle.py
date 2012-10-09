#!/usr/bin/env python
# Circle Class
import pygame
import pymunk
import math
import libs
from libs import *

class Circle:
    strobe_frequency = 2.0
    strobe_size = 5

    def __init__(self, mass, position, radius, color = (255,255,255), width = 0):
        self.position = position
        self.radius = radius
        self.color = color
        self.width = width
        self.surface_area = 4 * math.pi * (self.radius ** 2)
        self.mass = self.surface_area / 10
        self.inertia = pymunk.moment_for_circle(self.mass, 0, self.radius)  # 1
        self.body = pymunk.Body(self.mass, self.inertia)  # 2
        self.body.position = position # 3
        self.shape = pymunk.Circle(self.body, self.radius)  # 4
        self.shape.friction = 900.0
        self.shape.elasticity = 0.9

    def point_in_shape(self, (x,y)):
        return get_distance_within((x,y), self.body.position, self.radius)

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
