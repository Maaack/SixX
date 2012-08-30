import math
import random
from pymunk.vec2d import Vec2d

def get_hex_points(size, angle):
    sides = 6
    points = range(1,sides+1)
    for i, value in enumerate(points):
         p_angle = (2 * math.pi * value / sides) + angle
         x = math.cos(p_angle) * size
         y = math.sin(p_angle) * size
         points[i] = x, y
    return points

def get_hex_area(radius):
    area = ( 3 * math.sqrt( 3 ) / 2 ) * ( radius ** 2 )
    return area

def get_random_vector():
    the_angle = get_random_angle()
    the_x = math.sin(the_angle)
    the_y = math.cos(the_angle)
    the_vector = Vec2d(the_x, the_y)
    the_vector.normalize_return_length()
    return the_vector

def get_random_angle():
    return random.uniform(0, math.pi*2)

def get_distance_within((x1,y1), (x2, y2), max_distance):
    # Avoid doing any square roots by checking the points
    # distance squared against the max distance squared
    return ((x2-x1)**2 + (y2-y1)**2) < (max_distance**2)
