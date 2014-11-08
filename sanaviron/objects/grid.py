#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo

from rectangle import Rectangle

#from size import Size

class Grid(Rectangle):
    """This class represents a grid"""

    def __init__(self):
        Rectangle.__init__(self)
        self.active = True
        self.size = 15.0
        self.snap = True

    def draw(self, context):
        ###context.save()
        context.set_antialias(cairo.ANTIALIAS_NONE)
        context.set_line_width(1.0 / context.get_matrix()[0])
        context.set_source_rgba(0.0, 0.0, 0.0, 0.3)
        dash = [2.0 / context.get_matrix()[0], 2.0 / context.get_matrix()[0]]
        context.set_dash(dash)

        x, y = self.x, self.y

        while x <= self.x + self.width:
            context.move_to(x, self.y)
            context.line_to(x, self.y + self.height)
            x += self.size

        while y <= self.y + self.height:
            context.move_to(self.x, y)
            context.line_to(self.x + self.width, y)
            y += self.size

        context.stroke()
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ###context.restore()

    def nearest(self, value):
        if self.snap:
            lower = self.size * int(value / self.size)
            upper = self.size * int(value / self.size) + self.size
            middle = (lower + upper) / 2.0
            if value > middle:
                return float(upper)
            else:
                return float(lower)
        else:
            return value
