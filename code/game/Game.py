#!/usr/bin/env python
import pygame
import pymunk
import random
# Game Class
from game.libs import *
from game.classes import *

class Game:
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
    # Game Variables
    number_of_hexes = 60

    def __init__(self, interface):
        self.interface = interface
        self.screen_width, self.screen_height = screen_size = interface.screen_size

        # Set up the physics and collision handling


        # Create the Plane that we are playing in.
        self._Plane = Plane(self, interface.screen_size)
        # Add it to the objects that display
        self.display_objects.append(self._Plane)

        self.display_surface    = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.foreground_surface = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.background_surface = pygame.Surface(screen_size, pygame.SRCALPHA)

        # Define the atom skills and colors
        self.skills_list = ('basic', 'harvest', 'attack')

        self.skill_colors = {'basic': (0 , 0, 0),
             'align': (64, 255, 64),
             'attack': (255, 64, 64)}

        self.atom_mass = 100
        self.atom_max_charge = 100

        # Define the energy properties for the game
        self.energy_mass = 1
        self.energy_density = 5
        self.energy_transfer = 2
        self.energy_capacity = 1000

        # Place the player's energy on the screen
        player_color = random.choice(interface.colors)
        self.player = Player('You', 1, 1, player_color)
        self.player_characters.append(self.player)
        self.newEnergy(self.player, 100)

        # Make some atoms
        for n in range(self.number_of_hexes):
            self.newAtom('basic', False, 0)

    def _get_Plane(self):
        return self._Plane

    def _set_Plane(self, PlaneObject):
        if isinstance(PlaneObject, Plane):
            self._Plane = PlaneObject

    Plane = property(_get_Plane, _set_Plane)

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
        self._Plane.step(d_game_time)


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
                display_object.display(self, self.display_surface, offset)
            else:
                print str(display_object) + " has no method 'display'"

        # Selected Objects will create a pulse in the background
        for selected_object in self.selected_objects:
            if hasattr(selected_object, "get_display_object"):
                selected_object = selected_object.get_display_object()
            if hasattr(selected_object, "display_selected"):
                selected_object.display_selected(self, self.background_surface, offset)
            else:
                print str(selected_object) + " has no method 'display_selected'"

        for hovering_object in self.hovering_objects:
            if hasattr(hovering_object, "get_display_object"):
                hovering_object = hovering_object.get_display_object()
            if hasattr(hovering_object, "display_hovering"):
                hovering_object.display_hovering(self, self.background_surface, offset)
            else:
                print str(hovering_object) + " has no method 'display_hovering'"

        # Now begin with the foreground display
        # things like the commands that are being
        # currently executed.
        for highlighted_object in self.highlight_objects:
            if hasattr(highlighted_object, "display"):
                highlighted_object.display(self, self.foreground_surface, offset)
            else:
                print str(highlighted_object) + " has no method 'display'"

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

    def newEnergy(self, PlayerObject, amount = 100, position = False):
        if isinstance(PlayerObject, Player):
            if PlayerObject not in self.player_characters:
                self.player_characters.append(PlayerObject)
            """
            elif isinstance(player, NonPlayer):
                if player not in self.non_player_characters:
                    self.non_player_characters.append(player)
            """
        else:
            raise Exception("Not a valid type for a player!")

        if ( position == False or len(position) != 2 ):
            x = random.randint(self.screen_edge_spawn_radius, self.screen_width-self.screen_edge_spawn_radius)
            y = random.randint(self.screen_edge_spawn_radius, self.screen_height-self.screen_edge_spawn_radius)
            position = x,y


        the_energy = Energy(self, PlayerObject, position)
        return the_energy

    def newAtom(self, skill, position = False, angle = -1):
        if ( position == False or len(position) != 2 ):
            x = random.randint(self.screen_edge_spawn_radius, self.screen_width-self.screen_edge_spawn_radius)
            y = random.randint(self.screen_edge_spawn_radius, self.screen_height-self.screen_edge_spawn_radius)
            position = x,y

        if (angle < 0 or angle > math.pi*2):
            angle = get_random_angle()

        if (skill == False):
            skill = 'basic'

        the_atom = Atom(self, position, angle, skill)
        return the_atom

    def drop_object_from_space(self, bye_bye):
        self._Plane.remove(bye_bye)

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

    def collision_begin_func(self, space, arbiter, *args):
        # self.collision_pre_solve_func(space, arbiter, args, register=False)
        return True

    def collision_pre_solve_func(self, space, arbiter, *args, **kwargs):
        """For each contact, register the collision and figure
        out what to do. """
        GameObjects = []
        EnergyObjects = []
        ChargeObjects = []
        AtomObjects = []
        if 'register' in kwargs:
            register = kwargs['register']
        else:
            register = True
        for shape in arbiter.shapes:
            if hasattr(shape, 'game_object'):
                game_object = shape.game_object
                GameObjects.append(game_object)
                """
                if not hasattr(game_object, 'body'):
                    # Extra clean up catching just in case
                    # something has no body.  Should never
                    # happen... I think.
                    if hasattr(game_object, 'destroy'):
                        game_object.destroy()
                    self.drop_Object(game_object)
                el"""
                if isinstance(game_object, Atom):
                    AtomObjects.append(game_object)
                elif isinstance(game_object, Energy):
                    EnergyObjects.append(game_object)
                elif isinstance(game_object, Charge):
                    ChargeObjects.append(game_object)
            else:
                self._Plane.remove(shape)


        if len(EnergyObjects) == 1 and len(AtomObjects) == 1:
            if register:
                self.energy_atom_collision_func(EnergyObjects[0], AtomObjects[0])
            return False

        if len(AtomObjects) == 2:
            if register:
                self.atom_atom_collision_func(AtomObjects)
            return True

        return True

    def energy_atom_collision_func(self, EnergyObject, AtomObject):
        AtomObject.contact_Energy(EnergyObject)
        return False

    def atom_atom_collision_func(self, AtomObjects):
        return True


    def drop_Object(self, GameObject):
        if GameObject in self.all_objects:
            self.all_objects.remove(GameObject)
        if GameObject in self.hovering_objects:
            self.hovering_objects.remove(GameObject)
        if GameObject in self.selected_objects:
            self.selected_objects.remove(GameObject)
        if GameObject in self.display_objects:
            self.display_objects.remove(GameObject)
