#!/usr/bin/env python
# Wall Class
import pygame
from libs import *

class FadeInLine:

    display_ticks = 0
    delay = 0

    def __init__(self, a, b, radius = 2 , color = (0, 200, 0, 128), increments = 16, duration = 48):
        self.a = a
        self.b = b
        self.radius = radius
        self.color = color
        self.increments = increments
        self.duration = duration

    def display(self, screen):
        graphic_ticks = self.display_ticks - self.delay
        if (graphic_ticks > 0 and graphic_ticks < self.duration):
            end_p = get_segment_of_line(self.a,self.b,float(graphic_ticks)/self.increments)
            pygame.draw.line(screen, self.color, self.a, end_p, self.radius)
        self.display_ticks += 1

    def get_display_object(self):
        return self

    def set_display_delay(self, delay):
        self.delay = delay

    # Just for debugging
    def __str__(self):
        return "( " + str(self.a) + ", " + str(self.b) + " ) "
