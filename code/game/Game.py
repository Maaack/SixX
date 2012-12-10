#!/usr/bin/env python
# Game Class
import pygame
import pymunk
import random
from game.views import *
from game.libs import *
from game.classes import *

class Game:
    """Responsible for opening up a game and displaying to the interface"""
    # Going to store just about everything in...
    all_objects = []

    # Anything added to this array means it needs to be cycled
    # through in the display section of the main loop
    display_objects = []
    selected_objects = []
    highlight_objects = []
    hoverable_objects = []
    hovering_objects = []
    player_characters = []
    non_player_characters = []
    # Clocks
    game_time = 0
    real_time = 0
    # Display Variables
    display_tick = 0
    atom_strobe_frequency = 2.0
    atom_strobe_size = 5
    atom_radius = 10
    screen_edge_spawn_radius = 10

    def __init__(self, InterfaceObject):
        self._Interface = InterfaceObject
        self.screen_width, self.screen_height = screen_size = InterfaceObject.screen_size

        # Create the first SpaceTime that will hold the world and elements in play
        self._SpaceTime = st = SpaceTime(self)

        # Create the main display
        self._MainView = MainView(screen_size)
        self._GameView = GameView(screen_size, self, self._SpaceTime)
        self._MainView.attach_View(self._GameView)

        # Create the main Player, and Neutral Player (for later)
        self._Player = PlayerObject =  Player('You', 1, 1)
        self._Neutral_Player = Player('Neutral')

        # Create the Level
        self._Level = RandomLevel(PlayerObject, screen_size)
        LevelContents = self._Level.get_Elements()

        # Define the atom skills and colors
        self.skills_list = ('basic', 'harvest', 'attack')
        self.atom_mass = 100
        self.atom_max_charge = 100

        self.shell_charge_rate = 0.2

        # Define the energy properties for the game
        self.energy_mass = 1
        self.energy_density = 5
        self.energy_transfer = 2
        self.energy_capacity = 1000

        self.load_Level()


    def _set_SpaceTime(self):
        return self._SpaceTime

    def _set_SpaceTime(self, SpaceTimeObject):
        if isinstance(SpaceTimeObject, SpaceTime):
            self._SpaceTime = SpaceTimeObject

    SpaceTime = property(_set_SpaceTime, _set_SpaceTime)

    def load_Level(self, LevelObject = None, SpaceTime = None):
        if LevelObject == None:
            LevelObject = self._Level
        if SpaceTime == None:
            SpaceTime = self._SpaceTime

        ElementsList = LevelObject.get_Elements()

        for ElementDict in ElementsList:
            if ElementDict['type'] == 'Atom':
                position = ElementDict['position']
                angle = ElementDict['angle']
                skill = ElementDict['skill']
                SpaceTime.new_Atom(position, angle, skill)
            elif ElementDict['type'] == 'Energy':
                PlayerObject = ElementDict['player']
                position = ElementDict['position']
                energy = ElementDict['energy']
                SpaceTime.new_Energy(PlayerObject, position, energy)
            elif ElementDict['type'] == 'Wall':
                a = ElementDict['a']
                b = ElementDict['b']
                thickness = ElementDict['thickness']
                SpaceTime.new_Wall(a, b, thickness)

    def select_objects_at_point(self, point):
        action_taken = False
        deselected_objects = []
        for i, selected in enumerate(self.selected_objects):
            if (hasattr(selected, 'is_deselected') and selected.is_deselected(point)):
                action_taken = True
                self.selected_objects.pop(i)
                deselected_objects.append(selected)

        all_objects_r = list(self.all_objects)
        all_objects_r.reverse()
        if not action_taken:
            for object in all_objects_r:
                if object in deselected_objects:
                    continue

                if (hasattr(object, 'is_selected') and object.is_selected(point)):
                    action_taken = True
                    self.selected_objects.append(object)
        return action_taken

    def hover_over_point(self, point, offset = (0,0)):
        self.hovering_objects = []
        for i, object in enumerate(self.all_objects):
            if hasattr(object, 'is_hovering'):
                if (object.is_hovering(point)):
                    object.display_selected(self, self.background_surface, offset)
                    self.hovering_objects.append(object)



    def step(self, d_game_time, d_real_time):
        self.update_game_time(d_game_time)
        self.update_real_time(d_real_time)
        self._SpaceTime.step(d_game_time)


    def display(self, screen, offset = (0,0)):
        self.display_tick += 1
        self.display_surface.fill((255,255,255,0))
        self.background_surface.fill((255,255,255,0))
        self.foreground_surface.fill((255,255,255,0))

        # Display all the objects in the display
        # objects list.  Usually Hexagons.
        for display_object in self.display_objects:
            if hasattr(display_object, "get_display_object"):
                display_object = display_object.get_display_object()
            if hasattr(display_object, "display"):
                display_object.display(self, self.display_surface)
            else:
                print str(display_object) + " has no method 'display'"

        # Selected Objects will create a pulse in the background
        for selected_object in self.selected_objects:
            if hasattr(selected_object, "get_display_object"):
                selected_object = selected_object.get_display_object()
            if hasattr(selected_object, "display_selected"):
                selected_object.display_selected(self, self.background_surface)
            else:
                print str(selected_object) + " has no method 'display_selected'"

        for hovering_object in self.hovering_objects:
            if hasattr(hovering_object, "get_display_object"):
                hovering_object = hovering_object.get_display_object()
            if hasattr(hovering_object, "display_hovering"):
                hovering_object.display_hovering(self, self.background_surface)
            else:
                print str(hovering_object) + " has no method 'display_hovering'"

        # Now begin with the foreground display
        # things like the commands that are being
        # currently executed.
        for highlighted_object in self.highlight_objects:
            if hasattr(highlighted_object, "display"):
                highlighted_object.display(self, self.foreground_surface)
            else:
                print str(highlighted_object) + " has no method 'display'"

        # Display background to surface first,
        # as other things drawn to the screen
        # will go above this surface graphics.
        screen.unlock()
        screen.blit(self.background_surface, offset)
        screen.blit(self.display_surface, offset)
        screen.blit(self.foreground_surface, offset)
        screen.lock()


    def move_selected(self, point, offset = (0,0)):
        if len(self.selected_objects) == 0:
            return False
        offset = pymunk.Vec2d(offset)
        point = pymunk.Vec2d(point)
        offset_point = point - offset
        main_line_delay = 8
        middle_points = []
        for selected in self.selected_objects:
            if hasattr(selected, "get_movable_object"):
                movable = selected.get_movable_object()
                if isinstance(movable, pymunk.Body):
                    position = pymunk.Vec2d(movable.position)
                    object_middle = position - offset
                    # If the selected object is of type Hexagon
                    # then we will try to apply force.
                    # This will be replaced in the future with a
                    # more generic solution.
                    force_modifier = 2.0 / (1 / movable.mass)
                    force_vector = (offset_point - object_middle) * force_modifier
                    force_vector = force_vector
                    movable.apply_impulse(pymunk.Vec2d(force_vector))
                    middle_points.append(object_middle)

        # Get the average vector of all the objects selected
        # or in other words, the groups most middle point.
        average_vector = get_average_vector(middle_points)
        # Create a line from the average of selected objects to the point
        the_line = FadeInLine(average_vector, offset_point)

        # If the number of selected objects is greater than 1,
        # draw lines from their middle's to the average, and
        # put a delay on the display of the main line.
        if len(middle_points) > 1:
            for middle_point in middle_points:
                to_middle_line = FadeInLine(middle_point, average_vector, 2, (127,255,127,64), main_line_delay, 48)
                self.highlight_objects.append(to_middle_line)
            the_line.set_display_delay(main_line_delay)

        self.highlight_objects.append(the_line)

    def drop_object_from_space(self, bye_bye):
        self._SpaceTime.remove(bye_bye)

    def drop_highlights(self):
        self.highlight_objects = []

    def get_game_time(self):
        return self.game_time

    def get_real_time(self):
        return self.real_time

    def update_game_time(self, d_game_time):
        self.game_time += d_game_time

    def update_real_time(self, d_real_time):
        self.real_time += d_real_time

    def reset_real_time(self):
        self.real_time = 0

    def reset_game_time(self):
        self.game_time = 0

    def reset_times(self):
        self.reset_real_time()
        self.reset_game_time()

    def get_time_difference(self):
        return self.real_time - self.game_time

    def drop_Object(self, GameObject):
        if GameObject in self.all_objects:
            self.all_objects.remove(GameObject)
        if GameObject in self.hovering_objects:
            self.hovering_objects.remove(GameObject)
        if GameObject in self.selected_objects:
            self.selected_objects.remove(GameObject)
        if GameObject in self.display_objects:
            self.display_objects.remove(GameObject)
