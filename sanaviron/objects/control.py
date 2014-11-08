#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo

from objects import set_as_point
from math import pi

class Control:#(Rectangle):
    """This class represents a control point"""

    def __init__(self):
        set_as_point(self)
        self.size = 5.0
        self.active = True
        self.limbus = False
        self.pivot = False

    def draw(self, context):
        if not self.active:
            return

        ###context.save()
        context.set_antialias(cairo.ANTIALIAS_NONE)
        self.width = self.size / context.get_matrix()[0]
        self.height = self.size / context.get_matrix()[0]
        dash = list()
        context.set_dash(dash)
        context.set_line_width(1.0 / context.get_matrix()[0])

        if self.limbus:
            context.set_source_rgba(1.0, 0.5, 0.5, 1.0)
            context.arc(self.x, self.y, 3 / context.get_matrix()[0], 0, 2.0 * pi)
        elif self.pivot:
            size = self.size * 4.0
            self.width = size / context.get_matrix()[0]
            self.height = size / context.get_matrix()[0]
            context.set_source_rgba(0.0, 0.25, 0.0, 0.5)
            context.set_line_width(2.0 / context.get_matrix()[0])
            context.move_to(self.x, self.y - self.height / 2.0)
            context.line_to(self.x, self.y + self.height / 2.0)
            context.move_to(self.x - self.width / 2.0, self.y)
            context.line_to(self.x + self.width / 2.0, self.y)
        else:
            context.set_source_rgba(0.3, 1.0, 0.3, 1.0)
            context.rectangle(self.x - self.width / 2.0, self.y - self.height / 2.0, self.width, self.height)

        context.fill_preserve()

        if self.limbus:
            context.set_source_rgba(0.25, 0.0, 0.0, 0.5)
        else:
            context.set_source_rgba(0.0, 0.25, 0.0, 0.5)

        context.stroke()
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ###context.restore()

    def at_position(self, x, y):
        return x >= (self.x - self.size / 2.0) and x <= (self.x + self.size) and\
               y >= (self.y - self.size / 2.0) and y <= (self.y + self.size)
