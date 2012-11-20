#!/usr/bin/env python
import pygame
import pymunk
import random
# Game Class
from libs import *
from classes import *

class Game:
    # Going to store just about everything in...
    all_objects = []

    # Anything added to this array means it needs to be cycled
    # through in the display section of the main loop
    display_objects = []
    selected_objects = []
    clickable_objects = []
    highlight_objects = []
    # Clocks
    game_time = 0
    real_time = 0
    # Display Variables
    display_tick = 0
    atom_strobe_frequency = 2.0
    atom_strobe_size = 5
    atom_radius = 10
    screen_edge_spawn_radius = 10
    # Game Variables
    number_of_hexes = 60

    def __init__(self, interface):
        self.interface = interface
        screen_width, screen_height = screen_size = interface.screen_size

        # Set up the physics and collision handling


        # Create the Plane that we are playing in.
        self.plane = Plane(self, interface.screen_size)
        # Add it to the objects that display
        self.display_objects.append(self.plane)

        self.display_surface    = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.foreground_surface = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.background_surface = pygame.Surface(screen_size, pygame.SRCALPHA)

        # Define the atom skills and colors
        self.skill_colors = {'basic': (0 , 0, 0),
             'align': (64, 255, 64),
             'attack': (255, 64, 64)}

        # Place the player's energy on the screen
        player_color = random.choice(interface.colors)
        self.player = Player('You', 1, 1, player_color)
        x = random.randint(self.screen_edge_spawn_radius, screen_width-self.screen_edge_spawn_radius)
        y = random.randint(self.screen_edge_spawn_radius, screen_height-self.screen_edge_spawn_radius)
        angle = get_random_angle()
        the_energy = Energy(self, self.player, (x,y))
        self.all_objects.append(the_energy.get_clickable_object())
        self.clickable_objects.append(the_energy.get_clickable_object())
        self.display_objects.append(the_energy.get_display_object())
        the_body, the_shape = the_energy.circle.get_body()
        self.plane.add(the_body, the_shape)

        # Make some atoms
        for n in range(self.number_of_hexes):
            x = random.randint(self.atom_radius, screen_width-self.atom_radius)
            y = random.randint(self.atom_radius, screen_height-self.atom_radius)
            angle = get_random_angle()
            color = (0, 0, 0)
            the_atom = Atom(self, (x, y), 0, 'basic')
            self.all_objects.append(the_atom)
            self.clickable_objects.append(the_atom.get_clickable_object())
            self.display_objects.append(the_atom.get_display_object())
            the_body, the_shape = the_atom.hexagon.get_body()
            self.plane.add(the_body, the_shape)

    def select_objects_at_point(self, point):
        action_taken = False
        deselected_objects = []
        for i, selected in enumerate(self.selected_objects):
            if (selected.point_in_shape(point)):
                action_taken = True
                self.selected_objects.pop(i)
                deselected_objects.append(selected)

        clickable_objects_r = list(self.clickable_objects)
        clickable_objects_r.reverse()
        for clickable in clickable_objects_r:
            deselected = 0
            for deselected in deselected_objects:
                if (clickable == deselected):
                    deselected = 1
                    break
            if (deselected):
                continue
            if (clickable.point_in_shape(point)):
                action_taken = True
                self.selected_objects.append(clickable)
        return action_taken


    def step(self, d_game_time, d_real_time):
        self.update_game_time(d_game_time)
        self.update_real_time(d_real_time)
        self.plane.step(d_game_time)


    def display(self, screen, offset = (0,0)):
        self.display_tick += 1
        self.display_surface.fill((255,255,255,0))
        self.background_surface.fill((255,255,255,0))
        self.foreground_surface.fill((255,255,255,0))

        # Display all the objects in the display
        # objects list.  Usually Hexagons.
        for display_object in self.display_objects:
            display_object.display(self, self.display_surface, offset)

        # Selected Objects will create a pulse in the background
        for selected_object in self.selected_objects:
            selected_object.display_selected(self, self.background_surface, offset)

        # Now begin with the foreground display
        # things like the commands that are being
        # currently executed.
        for highlighted_object in self.highlight_objects:
            highlighted_object.display(self, self.foreground_surface, offset)

        # Display background to surface first,
        # as other things drawn to the screen
        # will go above this surface graphics.
        screen.unlock()
        screen.blit(self.background_surface, (0,0))
        screen.blit(self.display_surface, (0,0))
        screen.blit(self.foreground_surface, (0,0))
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
            position = pymunk.Vec2d(selected.body.position)
            object_middle = position - offset
            # If the selected object is of type Hexagon
            # then we will try to apply force.
            # This will be replaced in the future with a
            # more generic solution.
            force_modifier = 30.0
            if (isinstance(selected, Hexagon)):
                force_vector = (offset_point - object_middle) * force_modifier
                selected.apply_impulse(force_vector)
            if (isinstance(selected, Circle)):
                force_vector = (offset_point - object_middle) * force_modifier
                selected.apply_impulse(force_vector)
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

    def default_collision_func(self, space, arbiter, *args):
        """For each contact, register the collision and figure
        out what to do. """
        game_objects = []
        energy_objects = []
        atom_objects = []
        print len(arbiter.shapes)
        for shape in arbiter.shapes:
            if hasattr(shape, 'game_object'):
                game_object = shape.game_object
                print game_object
                game_objects.append(game_object)
                if isinstance(game_object, Atom):
                    atom_objects.append(game_object)
                elif isinstance(game_object, Energy):
                    energy_objects.append(game_object)

        if len(energy_objects) == 1 and len(atom_objects) == 1:
            return energy_atom_collision_func(space, energy_objects[0], atom_objects[0])

        if len(atom_objects) == 2:
            return atom_atom_collision_func(space, atom_objects)

        return true