#!/usr/bin/env python
# Basic Class
"""
All basic objects should inherit from this class
as it is a simple definition of an interface with
the physics engine.  Currently pymunk.

"""
import math
from game.libs import *
from game.classes import *
from game import pymunk

class Basic(object):
    """ Basic object.  Should not be created
    directly, but is inherited by the other
    classes.

    """

    def __init__(self, PlaneObject, ElementObject):
        """
        Basic init should never be called directly,
        this is mostly for class hinting
        :param PlaneObject: Plane
        :param ElementObject: Element
        :return:
        """
        self._Plane = PlaneObject
        self._Element = ElementObject
        self.body = None
        self.shape = None

    def destroy(self):
        if isinstance(self.shape, pymunk.Shape):
            self._Plane.remove(self.shape)
            self.shape.game_object = None
        self.shape = None

        if isinstance(self.body, pymunk.Body):
            self._Plane.remove(self.body)
            self.body.game_object = None
        self.body = None


    def get_points(self):
        """ Get the points of the object in any way feasible.

        :return: [points] for a polygon, (a,b) for lines, (position, radius) for circles
        """
        if isinstance(self.shape, pymunk.Poly):
            return self.shape.get_points()
        elif isinstance(self.shape, pymunk.Segment):
            return (self.shape.a, self.shape.b)
        elif isinstance(self.shape, pymunk.Circle):
            if isinstance(self.body, pymunk.Body):
                return (self.body.position, self.shape.radius)

        else:
            return None

    def get_position(self):
        """ Get the current object's position
        :return: Vec2d Object's position
        """
        return self.body.position

    def set_position(self, position):
        """ Set the position of the object
        :param position: Object will get set to this position
        :return: None
        """
        self.body.position = position

    position = property(get_position,set_position)

    def get_velocity(self):
        """ Get the current object's velocity
        :return: Vec2d Object's velocity
        """
        return self.body.velocity

    def set_velocity(self, velocity):
        """ Set the velocity of the object
        :param velocity: Object will get set to this velocity
        :return: None
        """
        self.body.velocity = velocity

    velocity = property(get_velocity,set_velocity)

    def get_relative_velocity(self, BasicObject):
        """ Get the relative velocity of this object with the other.
        Second object's velocity subtracted from the first object's velocity

        :param BasicObject: The Basic object to compare velocities with
        :return: velocity vector
        """
        if isinstance(BasicObject, Basic):
            return self.velocity - BasicObject.velocity

    def get_distance(self, BasicObject):
        if isinstance(BasicObject, Basic):
            position_vector = self.position
            return position_vector.get_distance(BasicObject.position)
