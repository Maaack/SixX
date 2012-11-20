#!/usr/bin/env python
# Wall Class
import pygame
import math
from game.libs import *
from game.pymunk import *

class Wall:
    def __init__(self, a = (0,0), b = (1,1), radius = 1 ):
        self.a = Vec2d(a)
        self.b = Vec2d(b)
        self.radius = radius
        self.body = Body()
        self.shape = Segment(self.body, a, b, radius)
        self.shape.friction = 100.0
        self.shape.collision_type = 0
        self.shape.elasticity = 0.9

    def display(self, game, screen, offset = (0,0)):
        offset_a = self.a + Vec2d(offset)
        offset_b = self.b + Vec2d(offset)
        pygame.draw.line(screen, (0,0,0), offset_a, offset_b, 6)

    def get_shape(self):
        return self.shape

    # Just for debugging
    def __str__(self):
        return "( " + str(self.a) + ", " + str(self.b) + " ) "
