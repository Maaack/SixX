import os
import sys
import pygame
import pygame.mixer
import pymunk
import classes
import libs
import random
from pygame.locals import *
from libs import *
from classes import *

the_interface = Interface()


# Defining variables for fps and continued running

run_me = True
while run_me:
    run_me = the_interface.step()

# Quit the game
pygame.quit()
sys.exit()
