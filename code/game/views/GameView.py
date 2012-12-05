""" A window into the game world
Perhaps...

"""
__author__ = 'marek'

import pygame
from game.views.View import View

class GameView(View):
    #TODO: All of this

    def __init__(self, view_size, GameObject):
        self._Game = GameObject
        PlaneObject = GameObject.Plane
        super(GameView, self).__init__(view_size, True)
        self.display_tick = 0

        # Defining some basic colors
        self.color_dict = {
            'black' : (0, 0, 0),
            'white' : (255, 255, 255),
            'red' : (255, 0, 0),
            'green' : (0, 255, 0),
            'blue' : (0, 0, 255),
            'yellow' : (255, 255, 0),
            'cyan' : (0, 255, 255),
            'magenta' : (255, 0, 255)
        }
        self.player_color_dict = self.color_dict.copy()
        del self.player_color_dict['white']

        self.opacity_dict = {
            'opaque' : 255,
            'visible' : 255,
            'transparent' : 0,
            'hidden' : 0,
            'invisible' : 0
        }

        c_dict = self.color_dict
        o_dict = self.opacity_dict

        self.atom_settings = {
            'border_opacity' : o_dict['visible'],
            'border_color' : c_dict['black'],
            'border_width' : 2,
            'border2_opacity' : o_dict['visible'],
            'border2_color' : c_dict['white'],
            'border2_width' : 4,
            'shell_opacity' : o_dict['visible'],
        }

        self.display_surface    = pygame.Surface(view_size, pygame.SRCALPHA)
        self.foreground_surface = pygame.Surface(view_size, pygame.SRCALPHA)
        self.background_surface = pygame.Surface(view_size, pygame.SRCALPHA)
        # TODO: Define a surface for each of the graphical elements that can be assumed
        # to have all the same transparency

    def display(self, screen, position = (0,0)):
        self.display_tick += 1
        self.display_surface.fill((255,255,255,0))
        self.background_surface.fill((255,255,255,0))
        self.foreground_surface.fill((255,255,255,0))

        # Display all the objects in the display
        # objects list.  Usually Hexagons.
        for display_object in self._Game.display_objects:
            if hasattr(display_object, "get_display_object"):
                display_object = display_object.get_display_object()
            if hasattr(display_object, "display"):
                display_object.display(self, self._Game.display_surface)
            else:
                print str(display_object) + " has no method 'display'"

        # Selected Objects will create a pulse in the background
        for selected_object in self._Game.selected_objects:
            if hasattr(selected_object, "get_display_object"):
                selected_object = selected_object.get_display_object()
            if hasattr(selected_object, "display_selected"):
                selected_object.display_selected(self, self._Game.background_surface)
            else:
                print str(selected_object) + " has no method 'display_selected'"

        for hovering_object in self._Game.hovering_objects:
            if hasattr(hovering_object, "get_display_object"):
                hovering_object = hovering_object.get_display_object()
            if hasattr(hovering_object, "display_hovering"):
                hovering_object.display_hovering(self, self._Game.background_surface)
            else:
                print str(hovering_object) + " has no method 'display_hovering'"

        # Now begin with the foreground display
        # things like the commands that are being
        # currently executed.
        for highlighted_object in self._Game.highlight_objects:
            if hasattr(highlighted_object, "display"):
                highlighted_object.display(self, self._Game.foreground_surface)
            else:
                print str(highlighted_object) + " has no method 'display'"

        # Display background to surface first,
        # as other things drawn to the screen
        # will go above this surface graphics.
        screen.unlock()
        screen.blit(self.background_surface, position)
        screen.blit(self.display_surface, position)
        screen.blit(self.foreground_surface, position)
        screen.lock()