import os
import sys
import pygame
import pygame.mixer
import pymunk
import classes
import libs
import random
from pygame.locals import *
from libs import *
from classes import *

# Defining some basic colors
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0
cyan = 0, 255, 255
magenta = 255, 0, 255


colors = [black, red, green, blue, yellow, cyan, magenta]

# Going to store just about everything in...
all_objects = []

# Anything added to this array means it needs to be cycled
# through in the display section of the main loop
display_objects = []
selected_objects = []
clickable_objects = []

# Defining the screen size
screen_size = screen_width, screen_height = 600, 400

# Setting the display and getting the Surface object
screen = pygame.display.set_mode(screen_size)
# Getting the Clock object
clock = pygame.time.Clock()
# Setting a title to the window
pygame.display.set_caption('SixX')

number_of_hexes = 100

the_plane = Plane(screen_size)
display_objects.append(the_plane)

for n in range(number_of_hexes):
    radius = 8
    x = random.randint(radius, screen_width-radius)
    y = random.randint(radius, screen_height-radius)
    angle = get_random_angle()
    color = random.choice(colors)
    the_atom = Atom((x, y), angle, color)
    all_objects.append(the_atom)
    clickable_objects.append(the_atom)
    display_objects.append(the_atom)
    the_body, the_shape = the_atom.hexagon.get_body()
    the_plane.add(the_body, the_shape)


# Defining variables for fps and continued running
fps_limit = 60.0
run_me = True
while run_me:

    # Get any user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_me = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            deselected_objects = []
            for i, selected_object in enumerate(selected_objects):
                if (selected_object.point_in_shape((mouse_x, mouse_y))):
                    selected_objects.pop(i)
                    deselected_objects.append(selected_object)

            clickable_objects_r = list(clickable_objects)
            clickable_objects_r.reverse()
            for clickable_object in clickable_objects_r:
                deselected = 0
                for deselected_object in deselected_objects:
                    if (clickable_object == deselected_object):
                        deselected = 1
                        break
                if (deselected):
                    continue
                if (clickable_object.point_in_shape((mouse_x, mouse_y))):
                    selected_objects.append(clickable_object)


    # Limit the framerate
    dtime_ms = clock.tick(fps_limit)
    dtime = dtime_ms/1000.0

    update_game_time(dtime_ms)


    # Clear the screen
    screen.lock()
    screen.fill(white)

    # Make time go with gravity and stuff
    the_plane.step(1.0/fps_limit)

    for display_object in display_objects:
        display_object.display(screen)

    for selected_object in selected_objects:
        selected_object.highlight(screen)

    screen.unlock()
    # Display everything in the screen.
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
