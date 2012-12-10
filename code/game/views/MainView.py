__author__ = 'marek'

import game
import pygame
from pygame.transform import scale
from pygame.locals import *
from game.views.View import View

class MainView(View):
    def __init__(self, screen_size):
        """

        :param SurfaceObject: pygame.Surface
        :return:
        """
        # Setting the display and getting the Surface object
        self._screen_size = screen_size
        self._Screen = self._Surface = pygame.display.set_mode(screen_size)

        # Getting the Clock object
        self._Clock = pygame.time.Clock()
        # TODO: Set FPS from outside source
        self._display_time = 0
        self._frames_per_second = 40.0
        self._update_interval = 1/self._frames_per_second

        # Dict of Views by View.name
        self._Views = {}
        self._background_color = (0,0,0)

        # Setting a title to the window
        self.name = window_caption = 'SixX'
        pygame.display.set_caption(window_caption)


    def update(self, area = None):
        dtime = self._Clock.tick(self._frames_per_second)
        self._display_time += dtime
        self.update_Views(area)
        pygame.display.flip()

