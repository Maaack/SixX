#!/usr/bin/env python
# Wall Class
import pygame
from libs import *

class FadeInLine:

    display_ticks = 0

    def __init__(self, a, b, radius = 1 , color = (0,0,0), increments = 20, duration = 60):
        self.a = a
        self.b = b
        self.radius = radius
        self.color = color
        self.increments = increments
        self.duration = duration

    def display(self, screen):
        if (self.display_ticks < self.duration):
            end_p = get_segment_of_line(self.a,self.b,float(self.display_ticks)/self.increments)
            pygame.draw.line(screen, self.color, self.a, end_p, self.radius)
        self.display_ticks += 1

    def get_display_object(self):
        return self

    # Just for debugging
    def __str__(self):
        return "( " + str(self.a) + ", " + str(self.b) + " ) "
