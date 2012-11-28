import sys
import pygame
from pygame.locals import *
from game import *

the_interface = Interface()

# Defining variables for fps and continued running

run_me = True
while run_me:
    run_me = the_interface.step()

# Quit the game
pygame.quit()
sys.exit()

