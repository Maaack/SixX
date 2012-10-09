#!/usr/bin/env python
# Wall Class
import pygame
import pymunk
from libs import *

class OutwardPulseLine:

    display_ticks = 0
    delay = 0
    size = 1.0

    def __init__(self, position, points, color = (0, 200, 0, 128), width = 2, scale = 1.1, duration = 48):
        self.position = pymunk.Vec2d(position)
        self.points = points
        self.color = color
        self.width = width
        self.scale = scale
        self.duration = duration

    def display(self, game, screen, offset = (0,0)):
        offset = pymunk.Vec2d(offset)
        graphic_ticks = self.display_ticks - self.delay
        if (graphic_ticks > 0 and graphic_ticks < self.duration):
            self.size *= self.scale
            offset_points = []
            for point in self.points:
                point *= self.size
                offset_point = point + offset + self.position
                offset_x, offset_y = int(offset_point.x), int(offset_point.y)
                offset_vector = pymunk.Vec2d(offset_x, offset_y)
                offset_points.append(offset_vector)
            pygame.draw.lines(screen, self.color, 1, offset_points, self.width)
        self.display_ticks += 1

    def get_display_object(self):
        return self

    def set_display_delay(self, delay):
        self.delay = delay

    def set_line_spread(self, spread):
        self.spread = spread
    # Just for debugging
    def __str__(self):
        return "( " + str(self.a) + ", " + str(self.b) + " ) "
