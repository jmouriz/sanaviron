#!/usr/bin/python
# -*- coding: utf-8 -*-

from point import Point

class Position(Point):
    """This class represents a position"""

    __name__ = "Position"

    def __init__(self):
        Point.__init__(self)

    def move(self, x, y):
        self.x = x
        self.y = y
