__author__ = 'marek'
#!/usr/bin/env python
# Level Class
from game.libs import *
from game.pymunk import *
from game.classes import *
from game.classes.elements.Player import Player
from game.classes.data import Level

class RandomLevel(Level):
    screen_edge_spawn_radius = 10

    def __init__(self, PlayerObject, level_size = (800,600), number_of_hexes = 60):
        self._contents = []
        self._players = []
        self._players.append(PlayerObject)
        self._level_size = level_size
        self._level_width, self._level_height = width, height = level_size
        # Add Walls to the Surface based on size.
        # The Walls should probably make a hexagon.
        borders = [
            [(0,0), (width, 0)],
            [(width, 0), (width, height)],
            [(width, height), (0, height)],
            [(0, height), (0,0)]
        ]

        for border in borders:
            a, b = border
            self.new_Wall(a, b)

        # Position the Player's energy randomly
        self.new_Energy(PlayerObject)

        # Make some atoms, positioned randomly!
        for n in range(number_of_hexes):
            self.new_Atom('basic', False, 0)

    def new_Wall(self, a, b, thickness = 4):
        wall_data = {
            'type':'Wall',
            'a':a,
            'b':b,
            'thickness':thickness,
            }
        self._contents.append(wall_data)
        return wall_data

    def new_Energy(self, PlayerObject, energy = 1000, position = False):
        if isinstance(PlayerObject, Player):
            if PlayerObject not in self._players:
                self._players.append(PlayerObject)
        else:
            raise Exception("Not a valid type for a player!")

        if ( position == False or len(position) != 2 ):
            x = random.randint(self.screen_edge_spawn_radius, self._level_width - self.screen_edge_spawn_radius)
            y = random.randint(self.screen_edge_spawn_radius, self._level_height - self.screen_edge_spawn_radius)
            position = x,y

        energy_data = {
            'type':'Energy',
            'player':PlayerObject,
            'position':position,
            'energy':energy,
        }
        self._contents.append(energy_data)
        return energy_data

    def new_Atom(self, skill, position = False, angle = -1):
        if ( position == False or len(position) != 2 ):
            x = random.randint(self.screen_edge_spawn_radius, self._level_width - self.screen_edge_spawn_radius)
            y = random.randint(self.screen_edge_spawn_radius, self._level_height - self.screen_edge_spawn_radius)
            position = x,y

        if (angle < 0 or angle > math.pi*2):
            angle = get_random_angle()

        if (skill == False):
            skill = 'basic'

        atom_data = {
            'type':'Atom',
            'position':position,
            'angle':angle,
            'skill':skill,
            }
        self._contents.append(atom_data)
        return atom_data