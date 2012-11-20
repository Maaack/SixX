from types import *

def energy_atom_collision_func(space, energy, atom):
    atom.contact_energy(energy)
    return False

def atom_atom_collision_func(space, atom_objects):
    return True
