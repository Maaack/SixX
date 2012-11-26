import math
import random
from ..pymunk.vec2d import Vec2d

def get_hex_points(size, angle, offset = (0,0)):
    sides = 6
    points = range(1,sides+1)
    offset_x, offset_y = offset
    for i, value in enumerate(points):
         p_angle = (2 * math.pi * value / sides) + angle
         x = (math.cos(p_angle) * size) + offset_x
         y = (math.sin(p_angle) * size) + offset_y
         points[i] = x, y
    return points

def get_hex_area(radius):
    area = ( 3 * math.sqrt( 3 ) / 2 ) * ( radius ** 2 )
    return area

def get_circle_surface_area_diff(radius_1, radius_2):
    area_1 = math.pi * (radius_1 ** 2)
    area_2 = math.pi * (radius_2 ** 2)
    return area_1 - area_2

def get_random_vector():
    the_angle = get_random_angle()
    the_x = math.sin(the_angle)
    the_y = math.cos(the_angle)
    the_vector = Vec2d(the_x, the_y)
    the_vector.normalize_return_length()
    return the_vector

def get_random_angle():
    # In radians
    return random.uniform(0, math.pi*2)

def get_distance_within((x1,y1), (x2, y2), max_distance):
    # Avoid doing any square roots by checking the points
    # distance squared against the max distance squared
    return ((x2-x1)**2 + (y2-y1)**2) < (max_distance**2)

def get_average_vector(vectors):
    if len(vectors) == 0:
        return Vec2d(0,0)
    total_vector = Vec2d(0,0)
    count_vectors = 0
    for the_vector in vectors:
        count_vectors += 1
        total_vector += Vec2d(the_vector)
    avg_vector = total_vector/count_vectors
    return avg_vector

def get_segment_of_line(a, b, total = 1.0):
    if (total >= 1.0):
        total = 1.0
    ab = b - a
    return a + ab * total

def interval_triangle_wave(time, frequency, max_height = 1.0):
    wavelength_ms = 1000.0 / frequency
    level_2 = 2 * math.fmod(time, wavelength_ms) / wavelength_ms
    if level_2 > 1:
        return (1 - (level_2 - 1)) * max_height
    else:
        return level_2 * max_height
