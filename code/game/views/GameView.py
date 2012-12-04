""" A window into the game world
Perhaps...

"""
__author__ = 'marek'

import pygame
from game.views.View import View

class GameView(View):
    #TODO: All of this
    def __init__(self, GameObject):
        self._Game = GameObject
        PlaneObject = self._Game.Plane

        super(GameView, self).__init__(view_size, True)
        width, height = view_size
        self._width = width
        self._height = height
        self._position = position
        self.display_tick = 0

        self.atom_border_opacity = 255
        self.atom_shell_opacity = 255
        self.display_surface    = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.foreground_surface = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.background_surface = pygame.Surface(screen_size, pygame.SRCALPHA)


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