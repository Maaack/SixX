#!/usr/bin/env python
# Hexagon Class
import pygame
import math
from game import pymunk
from game.libs import *


class ChargeLines(object):

    def __init__(self, color = (255, 255, 255), width = 2 , increments = 16):
        self.id = make_hash()
        self._points = []
        self._line_durations = []
        self._show_sides = 0
        self._width = width
        self._color = color
        self._increments = increments

    def show_sides(self, sides):
        if sides < 0:
            self._show_sides = 0
        if sides < len(self._points):
            self._show_sides = sides
        else:
            self._show_sides = len(self._points) - 1

    def display(self, screen):
        points = self._points
        line_max_opacity = 127
        line_opacity = []

        for i, duration in enumerate(self._line_durations):
            if i > self._show_sides:
                self._line_durations[i] = 0.0
            else:
                duration += 1.0
                self._line_durations[i] = duration

            if duration > self._increments:
                line_opacity.append(line_max_opacity)
            elif duration <= 0:
                line_opacity.append(0)
            else:
                opacity = line_max_opacity * ( duration / self._increments)
                line_opacity.append(opacity)

        end = start = 0
        for i, point in enumerate(points):
            end = start
            start = point
            r,g,b = self._color
            if i >= 1:
                opacity = line_opacity[i - 1]
            else:
                opacity = 0
            color = (r, g, b, opacity)
            if (start != 0 and end != 0):
                pygame.draw.line(screen, color, start, end, self._width)

    def get_display_object(self):
        return self

    def _get_points(self):
        return self._points

    def _set_points(self, points):
        while len(self._line_durations) != len(points):
            if len(self._line_durations) > len(points):
                self._line_durations.pop()
            elif len(self._line_durations) < len(points):
                self._line_durations.append(0)

        self._points = []
        for point in points:
            self._points.append(pymunk.Vec2d(point))

    points = property(_get_points, _set_points)
