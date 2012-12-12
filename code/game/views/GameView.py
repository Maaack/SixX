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
                'color': c_dict['black'],
                'frequency': 2.0,
                'size': 5
            },
            'hover_func' : self.strobe,
            'hover_func_args' : {
                'color': c_dict['black'],
                'frequency': 2.0,
                'size': 5
            },
        }

        self.energy_settings = {
            'border_width' : 0,
            'selected_func' : self.pulse,
            'selected_func_args' : {
                'frequency': 2.0,
                'size': 5
            },
        }

        self.wall_settings = {
            'width' : 6,
            'color' : c_dict['black']
        }


        # Creating the list of layers as they will be displayed in order to the single
        # per pixel alpha Surface, along with any modifiers that may be attached to
        # the layer_settings dict.
        self.layer_list = [
            'barriers',
            'atom_border2',
            'atom_border',
            'atom_shell',
            'atom_charge',
            'energy_body',
            'selection',
            'mouse_hover',
            'mouse_splash',
            ]

        self.layer_settings = {
            'barriers':{
                },
            'atom_border2':{
                },
            'atom_border':{
                },
            'atom_shell':{
                },
            'atom_charge':{
                },
            'energy_body':{
                },
            'selection':{
                },
            'mouse_hover':{
                },
            'mouse_splash':{
                },
            }


        # Assign colors to each of the players
        self.player_colors_dict = {}

        for PlayerObject in self._players:
            self.get_Player_color(PlayerObject.id)

        self.display_objects = {}
        self._display_layer_callbacks = {}
        self._reset_display_callbacks()


    def update(self, area = None):

        self._reset_display_callbacks()
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
            if isinstance(selected_object, Atom):
                self.display_Atom_selected(selected_object)
            elif isinstance(selected_object, Energy):
                self.display_Energy_selected(selected_object)

        for hovering_object in self._Game.hovering_objects:
            if isinstance(hovering_object, Atom):
                self.display_Atom_selected(hovering_object)
            elif isinstance(hovering_object, Energy):
                self.display_Energy_selected(hovering_object)

        # Now begin with the foreground display
        # things like the commands that are being
        # currently executed.
        for highlighted_object in self._Game.highlight_objects:
            id = highlighted_object.id
            self._add_display_callback('selection', id, highlighted_object.display)

        SurfaceObject = self.Surface
        SurfaceObject.lock()
        # Clear the SurfaceObject
        SurfaceObject.fill(self.color_dict['white'])

        self._draw_display_callbacks()

        SurfaceObject.unlock()

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

    # Display methods for each type of game object
    def display_Energy(self, EnergyObject):
        position, radius = EnergyObject.get_points()
        PlayerObject = EnergyObject.get_Player()
        id = PlayerObject.id
        self.get_Player_color(id)
        color = self.player_colors_dict[id]

        width = self.energy_settings['border_width']
        position = int(position.x), int(position.y)
        radius = int(radius)
        width = int(width)
        self._add_display_callback('energy_body', id, pygame.draw.circle,
            color, position, radius, width)

    def display_Atom(self, AtomObject):
        id = AtomObject.id
        points = AtomObject.get_points()

        # The Display of the Shell is a bit special as it requires
        # an object to keep track of changes to make the UI act more
        # fluid than the data in the actual game may be.
        points_end = list(points)
        points_end.append(points_end[ 0 ])
        ShellObject = AtomObject.get_Shell()
        if isinstance(ShellObject, Shell):
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
            self._add_display_callback('atom_shell', id, ChargeLinesObject.display)

        # Displaying atom border
        color = self.atom_settings['border2_color']
        width = self.atom_settings['border2_width']
        self._add_display_callback('atom_border2', id, pygame.draw.polygon,
            color, points, width)
        color = self.atom_settings['border_color']
        width = self.atom_settings['border_width']
        self._add_display_callback('atom_border', id, pygame.draw.polygon,
            color, points, width)

    def display_Wall(self, WallObject):
        id = WallObject.id
        a, b = WallObject.get_points()
        color = self.wall_settings['color']
        width = self.wall_settings['width']
        self._add_display_callback('barriers', id, pygame.draw.line,
            color, a, b, width)

    def display_Atom_selected(self, AtomObject):
        id = AtomObject.id
        color = self.atom_settings['selected_func_args']['color']
        points = AtomObject.get_points()
        frequency = self.atom_settings['selected_func_args']['frequency']
        size = self.atom_settings['selected_func_args']['size']
        self._add_display_callback('selection', id, self.strobe,
            color, points, frequency, size)


    def display_Energy_selected(self, EnergyObject):
        id = EnergyObject.id
        color = self.get_Player_color(EnergyObject.Player.id)
        position, radius = EnergyObject.get_points()
        frequency = self.energy_settings['selected_func_args']['frequency']
        size = self.energy_settings['selected_func_args']['size']
        self._add_display_callback('selection', id, self.pulse,
            color, position, radius, frequency, size)


    def strobe(self, surface, color, points, strobe_frequency, strobe_size):
        strobe_width = interval_triangle_wave(self._Game.real_time, strobe_frequency, strobe_size)
        width = int(strobe_width)
        pygame.draw.lines(surface, color, 1, points, width)


    def pulse(self, surface, color, position, radius, strobe_frequency, strobe_size):
        strobe_width = interval_triangle_wave(self._Game.real_time, strobe_frequency, strobe_size)
        position = int(position.x), int(position.y)
        radius = int(radius)
        width = min(int(strobe_width), radius)
        pygame.draw.circle(surface, color, position, radius, width)

    def get_Player_color(self, id):
        if id in self.player_colors_dict:
            return self.player_colors_dict[id]
        else:
            color_options = self.player_color_options_dict.items()
            color_name, player_color = random.choice(color_options)
            self.player_colors_dict[ id ] = player_color
            return player_color

