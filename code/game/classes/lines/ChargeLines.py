#!/usr/bin/env python
# Hexagon Class
import pygame
import math
from game.libs import *
from game import pymunk


class ChargeLines:

    def __init__(self, points, color = (255, 255, 255), width = 2 , increments = 16):
        self._points = []
        self._line_durations = []
        self._show_sides = 0
        for point in points:
            self._points.append(pymunk.Vec2d(point))
            self._line_durations.append(0)
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

    def display(self, game, screen, offset = (0,0)):
        points = self._points
        offset_points = []
        line_max_opacity = 255
        line_opacity = []

        for point in points:
            offset_points.append((pymunk.Vec2d(point) + pymunk.Vec2d(offset)))

        for i, duration in enumerate(self._line_durations):
            if i > self._show_sides:
                self._line_durations[i] = 0
            else:
                duration += 1
                self._line_durations[i] = duration

            if duration > self._increments:
                line_opacity.append(line_max_opacity)
            elif duration <= 0:
                line_opacity.append(0)
            else:
                line_opacity.append(line_max_opacity * ( duration / self._increments))

        start = 0
        end = 0
        for i, point in enumerate(offset_points):
            end = start
            start = point
            r,g,b = self._color
            if i > 1:
                opacity = line_opacity[i - 1]
            else:
                opacity = 0
            color = (r, g, b, opacity)
            if (start != 0 and end != 0):
                pygame.draw.line(screen, color, start, end, self._width)

    def get_display_object(self):
        return self

