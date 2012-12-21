__author__ = 'marek'

import game
import pygame
from pygame.transform import scale
from pygame.transform import smoothscale
from pygame.locals import *
from game.views.View import View

class CameraView(View):
    def __init__(self, view_size):
        super(CameraView,self).__init__(view_size, True)
        self._Camera_Rect = self._View_Rect.copy()
        self._zoom = 1.0
        self._smooth_scale = True
        self._zoom_min = 1.
        self._zoom_max = 4.
        self._max_edge_zoom = .2
        self._zoom_in_scroll_modifier = .05
        self._zoom_out_scroll_modifier = .15

    def _get_zoom(self):
        return self._zoom

    def _set_zoom(self, zoom):
        if zoom < self._zoom_min:
            zoom = self._zoom_min
        if zoom > self._zoom_max:
            zoom = self._zoom_max
        self._zoom = zoom
        scale = 1.0/zoom
        RectObject = self._View_Rect
        width = RectObject.width * scale
        height = RectObject.height * scale
        old_center = self._Camera_Rect.center
        self._Camera_Rect.size = (width, height)
        self._Camera_Rect.normalize()
        self._Camera_Rect.center = old_center

    zoom = property(_get_zoom, _set_zoom)

    def zoom(self, dz, pos):
        """
        Zoom the Camera in or out of the View, and center around point.
        :param dz: The +/- difference to the 'z' coordinate (zoom).
          + to zoom in, - to zoom out
        :param pos: The position around which to zoom
        """
        old_Rect = self._Camera_Rect.copy()
        top = old_Rect.top
        left = old_Rect.left
        x, y = pos
        x, y = x / self._zoom + left, y / self._zoom + top
        zoom = self._zoom * dz
        self._set_zoom(zoom)
        # Copy the new size and old position of the Camera
        new_Rect = self._Camera_Rect.copy()
        # Set the Camera around the mouse position
        self._Camera_Rect.center = x, y
        # This next part requires different math depending on whether the view
        # is zooming in or out.  The purpose is to allow the player to zoom in or
        # or out around their mouse, without going too far and making it jarring.
        if dz > 1:
            width, height = old_Rect.size
            dx, dy = width * self._zoom_in_scroll_modifier, height * self._zoom_in_scroll_modifier
            old_Rect.inflate_ip(dx, dy)
            self._Camera_Rect.clamp_ip(old_Rect)
        if dz < 1:
            width, height = new_Rect.size
            dx, dy = width * self._zoom_out_scroll_modifier, height * self._zoom_out_scroll_modifier
            new_Rect.inflate_ip(dx, dy)
            self._Camera_Rect.clamp_ip(new_Rect)


    def scroll(self, dx, dy):
        """
        Scroll the Camera over the Views
        :param dx: The +/- difference to the x coordinate
        :param dy: The +/- difference to the y coordinate
        """
        self._Camera_Rect.move_ip(dx,dy)

        # Not updating the clipping position of the Views,
        # as multiple Cameras might point at the same View.


    def update_Views(self, area=None):
        if not isinstance(self._Surface, pygame.Surface):
            raise Exception("Trying to update Views on " + str(self._Surface) +  " in " + str(self) + " !")

        if isinstance(area, Rect):
            # Clipping the update area to the View Rect
            area_Rect = area.clip(self.Rect)
        else:
            # Updating the entire View
            area_Rect = self.Rect

        if area_Rect.size == 0:
            return

        area = area_Rect.size

        SurfaceObject = self._Surface
        # Clear the screen
        SurfaceObject.lock()
        SurfaceObject.fill(self._background_color)
        SurfaceObject.unlock()

        for ViewDict in self._Views.itervalues():
            View = ViewDict['View']
            position = ViewDict['position']
            View.update(self._Camera_Rect)

            if not View.Rect.contains(self._Camera_Rect):
                self._Camera_Rect.clamp_ip(View.Rect)

            CameraSurface = View.Surface.subsurface(self._Camera_Rect)
            if self._smooth_scale:
                ScaledSurface = smoothscale(CameraSurface, area)
            else:
                ScaledSurface = scale(CameraSurface, area)
            SurfaceObject.unlock()
            SurfaceObject.blit(ScaledSurface, position, area_Rect)
            del CameraSurface
            del ScaledSurface

