__author__ = 'marek'
#!/usr/bin/env python
# Level Class
from game.libs import *
from game.pymunk import *
from game.classes import *
from game.classes.Level import Level

class RandomLevel(Level):
    screen_edge_spawn_radius = 10

    def __init__(self, level_size, number_of_hexes):
        self._contents = []

        height, width = level_size
        # Add Walls to the Surface based on size.
        # The Walls should probably make a hexagon.
        borders = [
            [(0,0), (0, width)],
            [(0, width), (height, width)],
            [(height, width), (height, 0)],
            [(height, 0), (0,0)]
        ]

        self.walls = []

        for border in borders:
            a, b = border
            the_wall = Wall(a, b)
            self._contents.append(the_wall)

        self._players = []

        # Place the player's energy on the screen
        self._player = Player('You', 1, 1)
        self._players.append(self._player)
        self.newEnergy(self.player, 100)

        # Make some atoms
        for n in range(self.number_of_hexes):
            self.newAtom('basic', False, 0)


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