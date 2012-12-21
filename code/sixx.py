"""
SixX
Game Engine

Run with Python 2.7.3

"""
import sys
import pygame
from pygame.locals import *
from game import *


# Open the Interface, which is everything right now.
# Then loops until the interface says to stop on a step.
the_interface = Interface()
run_me = True
while run_me:
    run_me = the_interface.step()

# Quit the game
pygame.quit()
sys.exit()

