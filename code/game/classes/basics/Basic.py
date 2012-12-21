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
        if isinstance(self.shape, pymunk.Poly):
            return self.shape.get_points()
        elif isinstance(self.shape, pymunk.Segment):
            return (self.shape.a, self.shape.b)
        elif isinstance(self.shape, pymunk.Circle):
            if isinstance(self.body, pymunk.Body):
                return (self.body.position, self.shape.radius)

        else:
            return None