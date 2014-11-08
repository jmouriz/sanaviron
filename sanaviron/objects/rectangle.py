#!/usr/bin/python
# -*- coding: utf-8 -*-

from position import Position
from size import Size


class Rectangle(Position, Size):
    """This class represents a rectangle"""

    __name__ = "Rectangle"

    def __init__(self):
        Position.__init__(self)
        Size.__init__(self)

    def get_properties(self):
        return Position.get_properties(self) + Size.get_properties(self)

    def synchronize(self, rectangle):
        self.x = rectangle.x
        self.y = rectangle.y
        self.width =  rectangle.width
        self.height = rectangle.height