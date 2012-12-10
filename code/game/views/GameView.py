""" A window into the game world
Perhaps...

"""
__author__ = 'marek'

import pygame
import math
from game.libs import *
from game.classes import *
from game.views.View import View

class GameView(View):
    #TODO: All of this

    def __init__(self, view_size, GameObject, SpaceTimeObject):
        super(GameView, self).__init__(view_size, True)
        self._Game = GameObject
        self._SpaceTime = SpaceTimeObject
        self.display_tick = 0
        self._players = SpaceTimeObject.get_players()
        self._teams = SpaceTimeObject.get_teams()
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
        self.player_color_options_dict = self.color_dict.copy()
        del self.player_color_options_dict['white']

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
            'selected_func_args' : {
                'strobe_frequency': 2.0,
                'strobe_size': 5
            },
            'hover_func' : self.strobe,
            'hover_func_args' : {
                'strobe_frequency': 2.0,
                'strobe_size': 5
            },
        }

        self.energy_settings = {
            'border_width' : 0,
            'selected_func' : self.pulse,
            'selected_func_args' : {
                'strobe_frequency': 2.0,
                'strobe_size': 5
            },
        }

        self.wall_settings = {
            'width' : 6,
            'color' : c_dict['black']
        }

        # TODO: Define a surface for each of the graphical elements that can be assumed
        # to have all the same transparency
        self.surfaces_dict = {
            'barriers' : pygame.Surface(view_size),
            'energy_body' : pygame.Surface(view_size),
            'atom_charge' : pygame.Surface(view_size),
            'atom_border' : pygame.Surface(view_size),
            'atom_border2' : pygame.Surface(view_size),
            'atom_shell' : pygame.Surface(view_size, pygame.SRCALPHA),
            'selection' : pygame.Surface(view_size, pygame.SRCALPHA),
            'mouse_hover' : pygame.Surface(view_size, pygame.SRCALPHA),
            'mouse_splash' : pygame.Surface(view_size, pygame.SRCALPHA),
        }

        # Assign colors to each of the players
        self.player_colors_dict = {}

        for PlayerObject in self._players:
            player_color = random.choice(self.player_color_options_dict)
            id = PlayerObject.id
            self.player_colors_dict[ id ] = player_color

        self.display_objects = {}


    def update(self, area = None):

        for key, SurfaceObject2 in self.surfaces_dict.iteritems():
            SurfaceObject2.fill((255,255,255,0))

        display_objects = self._SpaceTime.get_visible_objects()

        # TODO: Only update objects that are in the area given.
        for object in display_objects:
            if isinstance(object, Atom):
                self.display_Atom(object)
            elif isinstance(object, Energy):
                self.display_Energy(object)
            elif isinstance(object, Wall):
                self.display_Wall(object)


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

        SurfaceObject = self.Surface
        SurfaceObject.lock()
        # Clear the SurfaceObject
        SurfaceObject.fill(self._background_color)

        SurfaceObject.unlock()
        for SurfaceObject2 in self.surfaces_dict:
            SurfaceObject.blit(SurfaceObject2)
        SurfaceObject.lock()

    # Display methods for each type of game object
    def display_Energy(self, EnergyObject):
        position, radius = EnergyObject.get_points()
        PlayerObject = EnergyObject.get_Player()
        id = PlayerObject.id
        color = self.player_colors_dict[id]

        width = self.energy_settings['border_width']
        surface = self.surfaces_dict['energy_body']
        pygame.draw.circle(surface, color, position, radius, width)

    def display_Atom(self, AtomObject):
        id = AtomObject.id
        points = AtomObject.get_points()

        # The Display of the Shell is a bit special as it requires
        # an object to keep track of changes to make the UI act more
        # fluid than the data in the actual game may be.
        points_end = points.copy()
        points_end.append(points_end[ 0 ])
        ShellObject = AtomObject.get_Shell()
        PlayerObject = ShellObject.get_Player()
        player_id = PlayerObject.id
        color_shell = self.player_colors_dict[ player_id ]
        width = self.atom_settings['shell_width']
        if id not in self.display_objects:
            self.display_objects[ id ] = {
                'shell' : ChargeLines(color_shell, width)
            }
        ChargeLinesObject = self.display_objects[ id ][ 'shell' ]
        ChargeLinesObject.points = points_end
        surface = self.surfaces_dict['atom_shell']
        ChargeLinesObject.display( surface )

        # Displaying atom border
        color = self.atom_settings['border2_color']
        width = self.atom_settings['border2_width']
        surface = self.surfaces_dict['atom_border2']
        pygame.draw.polygon(surface, color, points, width)
        color = self.atom_settings['border_color']
        width = self.atom_settings['border_width']
        surface = self.surfaces_dict['atom_border']
        pygame.draw.polygon(surface, color, points, width)

    def display_Wall(self, WallObject):
        surface = self.surfaces_dict['barriers']
        a, b = WallObject.get_points()
        color = self.wall_settings['color']
        width = self.wall_settings['width']
        pygame.draw.line(surface, color, a, b, width)

    def strobe(self, surface, color, points, strobe_frequency, strobe_size):
        strobe_width = interval_triangle_wave(self._Game.real_time, strobe_frequency, strobe_size)
        width = int(strobe_width)
        pygame.draw.lines(surface, color, 1, points, width)


    def pulse(self, surface, color, position, radius, strobe_frequency, strobe_size, width):
        strobe_width = interval_triangle_wave(self._Game.real_time, strobe_frequency, strobe_size)
        width = int(strobe_width)
        pygame.draw.circle(surface, color, position, radius, int(width))
