#!/usr/bin/env python
# Energy Class
import math
from types import *
from game.classes.basics.Circle import Circle
from game.classes.basics.Player import Player

class Energy:

    def __init__(self, game, player, (x, y), size = 100):
        self.game = game
        if isinstance(player, Player):
            self.controllers = [player]
            self.player = player
        elif isinstance(player, ListType):
            self.controllers = player
            self.player = player[0]
        else:
            print Player
            raise Exception("Not a valid type for a player!")
        self.size = size
        areabymass = 2
        area = size * areabymass
        radius = math.sqrt(area / math.pi)
        color = self.player.color
        self.circle = Circle(self, size, (x, y), radius, color)

    def get_display_object(self):
        return self.circle

    def get_clickable_object(self):
        return self.circle

    def lose_charge(self, amount):
        self.size -= min(self.size, amount)
        if self.size < 0:
            shape = self.circle.shape
            body = self.circle.body
            space.add_post_step_callback(space.remove, shape, body)
