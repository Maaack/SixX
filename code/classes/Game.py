#!/usr/bin/env python
# Atom Class
from classes import *
from libs import *
import random

class Game:
    # Going to store just about everything in...
    all_objects = []

    # Anything added to this array means it needs to be cycled
    # through in the display section of the main loop
    display_objects = []
    selected_objects = []
    clickable_objects = []
    game_time = 0
    real_time = 0


    def __init__(self, interface, number_of_hexes):
        self.interface = interface
        screen_width, screen_height = interface.screen_size
        # Create the Plane that we are playing in.
        self.plane = Plane(interface.screen_size)
        # Add it to the objects that display
        self.display_objects.append(self.plane)
        # Radius of all Atoms to start
        radius = 8
        for n in range(number_of_hexes):
            x = random.randint(radius, screen_width-radius)
            y = random.randint(radius, screen_height-radius)
            angle = get_random_angle()
            color = random.choice(interface.colors)
            the_atom = Atom((x, y), angle, color)
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


    def step(self, d_game_time, d_real_time, screen):
        self.update_game_time(d_game_time)
        self.update_real_time(d_real_time)
        atom_strobe_width = self.interface.real_time_tri_wave(2, 4)

        self.plane.step(d_game_time)
        for display_object in self.display_objects:
            display_object.display(screen)

        for selected_object in self.selected_objects:
            selected_object.strobe(screen, atom_strobe_width)

    def move_selected(self, point):
        if len(self.selected_objects) == 0:
            return False
        middle_points = []
        for i, selected in enumerate(self.selected_objects):
            middle_points.append(get_average_vector(selected.get_points()))
        average_vector = get_average_vector(middle_points)
        the_line = FadeInLine(average_vector, point)
        self.display_objects.append(the_line)


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

