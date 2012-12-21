#!/usr/bin/env python
# Line Class
import pygame
import math
from game.libs import *
from game.pymunk import *
from game.classes.basics.Basic import Basic

class Line(Basic):
    def __init__(self, ElementObject, a = (0,0), b = (1,1), radius = 1 ):
        self.a = Vec2d(a)
        self.b = Vec2d(b)
        self.radius = radius
        self.body = Body()
        self.body.game_object = ElementObject
        self.shape = Segment(self.body, a, b, radius)
        self.shape.friction = 100.0
        self.shape.collision_type = 0
        self.shape.elasticity = 0.9
        self.shape.game_object = ElementObject
