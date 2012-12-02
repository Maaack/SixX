__author__ = 'marek'

import game
import pygame
from pygame.transform import scale
from pygame.locals import *

class View(object):
    def __init__(self, view_size, name = ''):
        self._view_size = view_size
        self._Surface   = pygame.Surface(view_size, pygame.SRCALPHA)
        self._Views = {}
        self._View_Rect = self._Surface.get_clip()
        self._background_color = (0,0,0)
        self.name = name

    def _get_Surface(self):
        return self._Surface

    def _set_Surface(self, SurfaceObject):
        if not isinstance(SurfaceObject, pygame.Surface):
            raise Exception("Not a valid type " + str(SurfaceObject) +  " for a Surface in " + str(self) + " !")
        self._Surface = SurfaceObject

    Surface = property(_get_Surface, _set_Surface)

    def _get_size(self):
        RectObject = self.Surface.get_clip()
        return RectObject.size

    def _set_size(self, (width, height)):
        RectObject = self.Surface.get_clip()
        RectObject.width = width
        RectObject.height = height
        self._View_Rect = RectObject
        self.Surface.set_clip(RectObject)

    size = property(_get_size, _set_size)

    def _get_position(self):
        RectObject = self.Surface.get_clip()
        return RectObject.left, RectObject.top

    def _set_position(self, (x,y)):
        RectObject = self.Surface.get_clip()
        RectObject.left = x
        RectObject.top = y
        self._View_Rect = RectObject
        self.Surface.set_clip(RectObject)

    position = property(_get_position, _set_position)

    def _get_center_position(self):
        RectObject = self.Surface.get_clip()
        return RectObject.center

    def _set_center_position(self, (x,y)):
        RectObject = self.Surface.get_clip()
        RectObject.centerx = x
        RectObject.centery = y
        self._View_Rect = RectObject
        self.Surface.set_clip(RectObject)

    center_position = property(_get_center_position, _set_center_position)

    def _get_Rect(self):
        return self._View_Rect

    Rect = property(_get_Rect)


    def attach_View(self, ViewObject, position = (0,0), area = None):
        """

        :param ViewObject:View
        :return:
        """
        if isinstance(ViewObject, game.views.View) and ViewObject.name not in self._Views:
            self._Views[ViewObject.name] = {'View':ViewObject,
                                            'position':position,
                                            'area':area}

    def remove_View(self, ViewObject):
        """

        :param ViewObject:View
        :return:
        """
        if isinstance(ViewObject, game.views.View) and ViewObject.name in self._Views:
            del self._Views[ViewObject.name]

    def update_Views(self):
        if not isinstance(self._Surface, pygame.Surface):
            raise Exception("Trying to Display on " + str(self._Surface) +  " in " + str(self) + " !")

        screen = self._Surface
        # Clear the screen
        screen.lock()
        screen.fill(self._background_color)

        for ViewDict in self._Views:
            View = ViewDict['View']
            position = ViewDict['position']
            area = ViewDict['area']
            View.update()
            screen.blit(View.Surface, position, area)

        screen.unlock()


    def update(self, SurfaceObject, position = (0,0), mask = None):
        self.update_Views()