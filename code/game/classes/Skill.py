#!/usr/bin/env python
# Atom Class

class Skill:
    def __init__(self, position):
        self.position = position

    def display(self):
        pygame.draw.circle(screen, self.color, p, self.size, self.width)

    # Just for debugging
    def __str__(self):
        return "( " + str(self.position.x) + ", " + str(self.position.y) + " ) "
