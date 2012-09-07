#!/usr/bin/env python
# Wall Class
import pymunk
import pygame

class Wall:
    def __init__(self, a = (0,0), b = (1,1), radius = 1 ):
        self.a = pymunk.Vec2d(a)
        self.b = pymunk.Vec2d(b)
        self.radius = radius
        self.body = pymunk.Body()
        self.shape = pymunk.Segment(self.body, a, b, radius)
        self.shape.friction = 100.0
        self.shape.collision_type = 0
        self.shape.elasticity = 0.9

    def display(self, screen, offset = (0,0)):
        offset_a = self.a + pymunk.Vec2d(offset)
        offset_b = self.b + pymunk.Vec2d(offset)
        pygame.draw.line(screen, (0,0,0), offset_a, offset_b, 6)

    def get_shape(self):
        return self.shape

    # Just for debugging
    def __str__(self):
        return "( " + str(self.a) + ", " + str(self.b) + " ) "
