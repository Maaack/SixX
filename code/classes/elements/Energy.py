#!/usr/bin/env python
# Energy Class
import math
from classes.basics.Circle import Circle

class Energy:
    def __init__(self, (x, y), angle, color = (255,0,0), mass = 100):
        areabymass = 2
        area = mass * areabymass
        radius = math.sqrt(area / math.pi)
        self.circle = Circle( mass, (x, y), radius, color)

    def get_display_object(self):
        return self.circle

    def get_clickable_object(self):
        return self.circle
