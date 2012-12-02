__author__ = 'marek'

import game
import pygame
from pygame.transform import scale
from pygame.locals import *
from game.views.View import View

class CameraView(View):
    def __init__(self, view_size, name):
        super(CameraView,self).__init__(view_size, name)
        self._Camera_Rect = self._View_Rect
        self._zoom = 1.0

    def _get_zoom(self):
        return self._zoom

    def _set_zoom(self, zoom):
        self._zoom = zoom
        scale = 1.0/zoom
        RectObject = self._View_Rect
        d_width = (RectObject.width * scale) - RectObject.width
        d_height = (RectObject.height * scale) - RectObject.height
        RectObject.inflate_ip(d_width, d_height)
        #RectObject.width = RectObject.width * scale
        #RectObject.height = RectObject.height * scale
        self._Camera_Rect = RectObject

    zoom = property(_get_zoom, _set_zoom)


    def update_Views(self):
        if not isinstance(self._Surface, pygame.Surface):
            raise Exception("Trying to update Views on " + str(self._Surface) +  " in " + str(self) + " !")

        screen = self._Surface
        # Clear the screen
        screen.lock()
        screen.fill(self._background_color)

        for ViewDict in self._Views:
            View = ViewDict['View']
            position = ViewDict['position']
            area = ViewDict['area']
            View.update()
            CameraSurface = View.Surface.subsurface(self._Camera_Rect)
            ScaledSurface = scale(CameraSurface, self.Rect)
            screen.blit(ScaledSurface, position, area)
            del CameraSurface
            del ScaledSurface

        screen.unlock()

    #TODO: Scrolling the camera
    def scroll(self, dx, dy):
        pass