#!/usr/bin/env python
# Interface Class
# Called by the SixX file to handle everything the player sees,
# hears, and does.  Not just the game, but also the menus, intro/credits,
# building, and scripting pages.
#
import pygame
import pygame.mixer
import random
from pygame.locals import *
from libs import *
from classes import *

class Interface:

    real_time = 0
    fps_limit = 60

    def __init__(self):
        # Defining some basic colors
        self.black = 0, 0, 0
        self.white = 255, 255, 255
        red = 255, 0, 0
        green = 0, 255, 0
        blue = 0, 0, 255
        yellow = 255, 255, 0
        cyan = 0, 255, 255
        magenta = 255, 0, 255

        self.colors = [self.black, red, green, blue, yellow, cyan, magenta]

        # Defining the screen size
        self.screen_size = self.screen_width, self.screen_height = 600, 400

        # Setting the display and getting the Surface object
        self.screen = pygame.display.set_mode(self.screen_size)
        # Getting the Clock object
        self.clock = pygame.time.Clock()
        # Setting a title to the window
        pygame.display.set_caption('SixX')

        number_of_hexes = 100
        self.game = Game(self, number_of_hexes)

    def click(self, point):
        self.game.select_objects(point)


    def step(self):
        # Get any user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = mouse_x, mouse_y = pygame.mouse.get_pos()
                self.click(mouse_click)


        # Limit the framerate
        dtime = self.clock.tick(self.fps_limit)
        self.real_time += dtime

        # Clear the screen
        self.screen.lock()
        self.screen.fill(self.white)

        # Make time go with gravity and display things
        self.game.step((1.0/self.fps_limit), dtime, self.screen)


        self.screen.unlock()
        # Display everything in the screen.
        pygame.display.flip()

        return True

    def real_time_tri_wave(self, frequency, max_height = 1.0):
        wavelength_ms = 1000.0 / frequency
        level_2 = 2 * (self.real_time % wavelength_ms) / wavelength_ms
        if level_2 > 1:
            return (1 - (level_2 - 1)) * max_height
        else:
            return level_2 * max_height
