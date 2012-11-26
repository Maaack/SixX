#!/usr/bin/env python
# Player Class
import pygame

class Player:
    def __init__(self, name, number, team_number = 0, color = (255, 255, 255), color2= (196,0,64)):
        self.name = name
        self.number = number
        self.team_number = team_number
        self.color = color
        self.color2 = color2

    def __eq__(self, other):
        return self.number == other.number

    def __ne__(self, other):
        return self.number != other.number
