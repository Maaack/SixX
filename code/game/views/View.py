__author__ = 'marek'

import game
import pygame
import time
from pygame.transform import scale
from pygame.locals import *

class View(object):
    def __init__(self, view_size, name = '', per_pixel_alpha = True):
        self._view_size = view_size
        self.name = name
        self._per_pixel_alpha = per_pixel_alpha
        if per_pixel_alpha:
            self._Surface   = pygame.Surface(view_size, pygame.SRCALPHA)
        else:
            self._Surface   = pygame.Surface(view_size)
        self._Views = {}
        self._View_Rect = self._Surface.get_clip()
        self._background_color = (0,0,0)
        self._last_update_time = time.time()
        # TODO: Set fps from the Interface or MainView
        self._frames_per_second = 40.0
        self._update_interval = 1/self._frames_per_second

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

    def _get_fps(self):
        return self._frames_per_second

    def _set_fps(self, fps):
        self._frames_per_second = fps
        if fps > 0:
            self._update_interval = 1.0/self._frames_per_second
        else:
            # Passing in fps < 0 means you don't want the surface to update unless forced.
            # This sets the update interval to zero, effectively skipping its updates per call to update.
            # Good for menus or other things that only update on player interaction.
            self._update_interval = 0

    fps = property(_get_fps, _set_fps)



    def attach_View(self, ViewObject, position = (0,0), area = None):
        """

        :param ViewObject:View
        :return:
        """
        if isinstance(ViewObject, game.views.View) and ViewObject.name not in self._Views:
            # TODO: Doing this by name is not going to work, need a globally unique id for each View
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

    def update(self):
        # Check that we should be running updates at all.
        if self._update_interval > 0:
            # Check that one does not update the view more than the frame rate
            # This can happen in the case of multiple cameras pointing at a Surface
            # asking the View to update before getting the Surface area.
            current_time = time.time()
            if current_time > self._last_update_time + self._update_interval:
                self.update_forced()

    def update_forced(self):
        self._last_update_time = time.time()
        self.update_Views()

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

