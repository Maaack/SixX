
__author__ = 'marek'

import game
import pygame
import time
from game.libs import make_hash
import random
from pygame.transform import scale
from pygame.locals import *

class View(object):
    def __init__(self, view_size, per_pixel_alpha = True):
        self._view_size = view_size
        self._id = make_hash()
        self._per_pixel_alpha = per_pixel_alpha
        if per_pixel_alpha:
            self._Surface   = pygame.Surface(view_size, pygame.SRCALPHA)
        else:
            self._Surface   = pygame.Surface(view_size)
        self._Views = {}
        self._View_Rect = self._Surface.get_clip()
        self._background_color = (255,255,255,0)
        self._last_update_time = time.time()
        # TODO: Set fps from the Interface or MainView
        self._frames_per_second = 40.0
        self._update_interval = 1/self._frames_per_second
        self._force_next_update = True

        self.layer_list = []

    def _get_id(self):
        return self._id

    id = property(_get_id)

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

    def force_next_update(self):
        """  Force the View to update even if the update interval is zero.
        :return:
        """
        self._force_next_update = True

    def attach_View(self, ViewObject, position = (0,0), area = None):
        """
        :param ViewObject:View
        """
        if isinstance(ViewObject, game.views.View) and ViewObject.id not in self._Views:
            # TODO: Doing this by name is not going to work, need a globally unique id for each View
            self._Views[ViewObject.id] = {'View':ViewObject,
                                            'position':position,
                                            'area':area}

    def remove_View(self, ViewObject):
        """
        :param ViewObject:View
        """
        if isinstance(ViewObject, game.views.View) and ViewObject.name in self._Views:
            del self._Views[ViewObject.id]

    def update(self, area=None):
        # Check that we should be running updates at all.
        if self._update_interval > 0 or self._force_next_update:
            if isinstance(area, Rect):
                # Clipping the update area to the View Rect
                area = area.clip(self.Rect)
            else:
                # Updating the entire View
                area = self.Rect

            if area.size == 0:
                return

            # Check that one does not update the view more than the frame rate
            # This can happen in the case of multiple cameras pointing at a Surface
            # asking the View to update before getting the Surface area.
            current_time = time.time()
            if current_time > self._last_update_time + self._update_interval:
                if area.size == self._View_Rect.size:
                    self._last_update_time = time.time()
                self.update_forced(area)

    def update_forced(self, area=None):
        self._force_next_update = False
        self.update_Views(area)

    def update_Views(self, area=None):
        """
        Update the contents of the specified area.  If no area is provided then
        update the entire view
        :param area: pygame.Rect
        """
        if not isinstance(self.Surface, pygame.Surface):
            raise Exception("Trying to Display on " + str(self.Surface) +  " in " + str(self) + " !")

        SurfaceObject = self.Surface
        # Clear the SurfaceObject
        SurfaceObject.lock()
        SurfaceObject.fill(self._background_color)

        SurfaceObject.unlock()
        for key, ViewDict in self._Views.iteritems():
            View = ViewDict['View']
            position = ViewDict['position']
            if ViewDict['area'] != None:
                area = ViewDict['area']
            View.update(area)
            SurfaceObject.unlock()
            View_Surface = View.Surface
            # View_Surface = View_Surface.convert_alpha()
            SurfaceObject.blit(View_Surface, position, area)

    def _reset_display_callbacks(self):
        """ Resets the display dict to its original format.

        :return:
        """
        self._display_layer_callbacks = {}

    def _draw_display_callbacks(self):
        for key in self.layer_list:
            if key not in self._display_layer_callbacks:
                continue
            callback_dict = self._display_layer_callbacks[key]
            layer_settings = self.layer_settings[key]
            # If there were any settings for the layer we'd do something with them now.
            if 'opacity' in layer_settings:
                # ToDo: Something about it.
                pass

            for key2, callback_data in callback_dict.iteritems():
                if 'func' in callback_data and 'args' in callback_data:
                    display_function = callback_data['func']
                    args = callback_data['args']
                    display_function(self.Surface, *args)

    def _add_display_callback(self, layer, key, func, *args, **kwargs):
        if layer not in self._display_layer_callbacks:
            self._display_layer_callbacks[ layer ] = {}

        self._display_layer_callbacks[layer][key] = {
            'func': func,
            'args': args,
            'kwargs': kwargs,
            }
