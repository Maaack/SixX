""" A window into the game world
Perhaps...

"""
__author__ = 'marek'

import pygame
import math
from game.libs import *
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
            'gray' : (127, 127, 127),
            'white' : (255, 255, 255),
            'red' : (255, 0, 0),
            'green' : (0, 255, 0),
            'blue' : (0, 0, 255),
            'yellow' : (255, 255, 0),
            'cyan' : (0, 255, 255),
            'magenta' : (255, 0, 255)
        }

        # Make a dictionary of player available colors
        self.player_color_dict = self.color_dict.copy()
        del self.player_color_dict['white']

        self.opacity_dict = {
            'opaque' : 255,
            'visible' : 255,
            'translucent' : 127,
            'semitransparent' : 127,
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
            'shell_opacity' : o_dict['translucent'],
            'shell_width' : 8,
            'selected_func' : self.strobe,
            'hover_func' : self.strobe,
        }

        self.energy_settings = {
            'border_width' : 0,
            'selected_func' : self.pulse
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


    def display_Circle(self, game, screen, offset = (0,0)):
        point = self.body.position
        point = point + offset
        point_x, point_y = point
        point = (int(round(point_x)), int(round(point_y)))
        radius = int(round(self.radius))
        pygame.draw.circle(screen, self.color, point, radius, int(self.width))
        x2 = math.cos(self.body.angle)*self.radius + point_x
        y2 = math.sin(self.body.angle)*self.radius + point_y
        line_color =  (255,255,255,63)
        point_2 = (int(round(x2)),int(round(y2)))
        pygame.draw.line(screen, line_color, point, point_2, 2)

    def display_Hexagon(self, game, screen, offset = (0,0)):
        angle = self.body.angle
        position = self.body.position
        points_floats = get_hex_points(self.radius,angle,position)
        points = []
        for point in points_floats:
            x, y = point
            points.append((round(x), round(y)))
        pygame.draw.polygon(screen, self.color, points, self.width)

    def display_Shell(self, game, screen, offset = (0,0)):
        points = self._Atom.get_points()
        points.append(points[0])
        # TODO: Move display information of Charge Lines into Shells
        # and pass all the data in on init, and let the object be
        # del between cycles.  Or somehow keep track of the Charge
        # Lines and other graphics in GameView or attached still to Shell
        # like it is now.  Not sure if I want GameView to rely on GameObjects
        # having references to other visual display objects, would rather
        # it all be handled in the GameView.
        self._ChargeLines.points = points
        return self._ChargeLines.display(game, screen, offset)


    def strobe(self, game, screen, offset = (0,0)):
        strobe_width = interval_triangle_wave(game.real_time, self.strobe_frequency, self.strobe_size)
        width = int(strobe_width)
        points = self.get_points()
        #offset_points = []
        #for point in points:
        #    offset_points.append((pymunk.Vec2d(point) + pymunk.Vec2d(offset)))
        pygame.draw.lines(screen, self.color, 1, points, width)


    def pulse(self, game, screen, offset = (0,0)):
        strobe_width = interval_triangle_wave(game.real_time, self.strobe_frequency, self.strobe_size)
        width = int(strobe_width)
        point = self.body.position
        point = point + offset
        point_x, point_y = point
        point = (int(round(point_x)), int(round(point_y)))
        radius = int(round(self.radius+width))
        pygame.draw.circle(screen, self.color, point, radius, int(self.width))
