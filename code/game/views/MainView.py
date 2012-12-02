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

        # Dict of Views by View.name
        self._Views = {}
        self._background_color = (0,0,0)
        self.name = 'SixX'
        # Setting a title to the window
        pygame.display.set_caption(self.name)

    def update(self):
        self.update_Views()
        pygame.display.flip()