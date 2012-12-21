#!/usr/bin/env python
# Interface Class
# Called by the SixX file to handle everything the player sees,
# hears, and does.  Not just the game, but also the menus, intro/credits,
# building, and scripting pages.
#
import pygame
import time
import random
import math
from . import *
from game.libs import *
from pygame.locals import *
from Game import Game

class Interface:

    real_time = 0
    fps_limit = 40
    time_mousebuttondown = 0
    button_mousebuttondown = ''
    pos_mousebuttondown = 0
    time_keydown = 0
    key_keydown = ''
    mod_keydown = ''
    game_offset = pymunk.Vec2d(0, 0)
    game_edge_scroll_size = 20
    game_edge_scroll_rate = 4
    game_edge_scroll_on = True
    game_zooming_rate = 1.1
    game_zooming_on = True

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
        self.screen_size = self.screen_width, self.screen_height = 900, 600

        # Setting the display and getting the Surface object
        self.screen = pygame.display.set_mode(self.screen_size)
        # Getting the Clock object
        self.clock = pygame.time.Clock()
        # Setting a title to the window
        pygame.display.set_caption('SixX')

        self.game = Game(self)

    def click(self, point):
        return self.game.select_objects_at_point(point)

    def command(self, point):
        return self.game.move_selected(point)

    def hover(self, point):
        return self.game.hover_over_point(point)

    def step(self):
        # Get any user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pos_mousebuttondown = event.pos
                self.button_mousebuttondown = event.button
                self.time_mousebuttondown = self.real_time

            if event.type == pygame.MOUSEBUTTONUP:
                self.pos_mousebuttondown = 0
                self.button_mousebuttondown = ''
                self.time_mousebuttondown = 0
                mouse_click = mouse_x, mouse_y = event.pos
                mouse_button = event.button

                if mouse_button == 1:
                    if (self.click(mouse_click) == 0):
                        self.command(mouse_click)
                        continue

                if mouse_button == 4:
                    self.game.zoom(self.game_zooming_rate, mouse_click)
                    continue

                if mouse_button == 5:
                    self.game.zoom((1/self.game_zooming_rate), mouse_click)
                    continue


            if event.type == pygame.MOUSEMOTION:
                mouse_pos = mouse_x, mouse_y = event.pos
                self.hover(mouse_pos)


        # No longer checking for pygame events.

        mouse_pos = mouse_x, mouse_y = pygame.mouse.get_pos()
        if (self.game_edge_scroll_on):
            if (mouse_x < self.screen_width and mouse_x > self.screen_width - self.game_edge_scroll_size):
                self.game.scroll(self.game_edge_scroll_rate, 0)
            elif (mouse_x > 0 and mouse_x < self.game_edge_scroll_size):
                self.game.scroll(-self.game_edge_scroll_rate, 0)
            if (mouse_y < self.screen_height and mouse_y > self.screen_height - self.game_edge_scroll_size):
                self.game.scroll(0, self.game_edge_scroll_rate)
            elif (mouse_y > 0 and mouse_y < self.game_edge_scroll_size):
                self.game.scroll(0, -self.game_edge_scroll_rate)

        # Limit the framerate
        dtime = self.clock.tick(self.fps_limit)
        self.real_time += dtime

        # Clear the screen
        self.screen.lock()
        self.screen.fill(self.white)

        # Make time go with gravity and display things
        self.game.step((1.0/self.fps_limit), dtime)
        self.game.display(self.screen)

        self.screen.unlock()
        # Display everything in the screen.
        pygame.display.flip()

        return True

    def get_real_time(self):
        return self.real_time



