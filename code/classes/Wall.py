#!/usr/bin/env python
# Wall Class
import pymunk
import pygame

class Wall:
    def __init__(self, a = (0,0), b = (10,10), radius = 0 ):
        self.a = a
        self.b = b
        self.radius = radius
        self.body = pymunk.Body()
        self.shape = pymunk.Segment(self.body, a, b, radius)
        self.shape.friction = 100.0
        self.shape.collision_type = 0
        self.shape.elasticity = 0.9

    def display(self, screen):
        pygame.draw.line(screen, (0,0,0), self.a, self.b, 6)

    def get_shape(self):
        return self.shape

    # Just for debugging
    def __str__(self):
        return "( " + str(self.a) + ", " + str(self.b) + " ) "
