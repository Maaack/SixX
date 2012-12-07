#!/usr/bin/env python
# Player Class
import pygame
from game.libs import make_hash

class Player:
    def __init__(self, name, number, team_number = 0, color = (255, 255, 255), color2= (196,0,64)):
        self._id = make_hash()
        self.name = name
        self.number = number
        self.team_number = team_number
        self.color = color
        self.color2 = color2


    def get_id(self):
        return self._id

    id = property(get_id)

    def __eq__(self, other):
        return self._id == other._id

    def __ne__(self, other):
        return self._id != other._id
