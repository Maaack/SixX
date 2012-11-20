#!/usr/bin/env python
# Atom Class
import math
from game.classes.basics.Hexagon import Hexagon

class Atom:
    charge = 0
    alignment = 0
    aligning_player = 0
    alignment_max = 100
    player = 0
    controller = []

    def __init__(self, game, (x, y), angle, skill = 'basic'):
        self.game = game
        self.skill = skill
        self.color = game.skill_colors[skill]
        self.radius = game.atom_radius
        self.hexagon = Hexagon(self, 100, (x, y), self.radius, angle, self.color, width = 2)

    def get_display_object(self):
        return self.hexagon

    def get_clickable_object(self):
        return self.hexagon

    def contact_energy(self, energy):
        if self.alignment == 0 and self.aligning_player != energy.player:
            self.aligning_player = energy.player

        if self.aligning_player == energy.player:
            charge = min(self.alignment_max, energy.size)
            self.alignment += charge
            energy.lose_charge(charge)
        else:
            charge = max(self.alignment + self.alignment_max, energy.size)
            self.alignment -= charge
            if self.alignment < 0:
                self.aligning_player = energy.player
                self.alignment = -(self.alignment)
            elif self.alignment == 0:
                self.aligning_player = 0


