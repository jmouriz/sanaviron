#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo

from rectangle import Rectangle

class Selection(Rectangle):
    """This class represents a selection rectangle"""

    def __init__(self):
        Rectangle.__init__(self)
        self.active = False

    def draw(self, context):
        ###context.save()
        context.set_antialias(cairo.ANTIALIAS_NONE)
        dash = list()
        context.set_dash(dash)
        context.set_line_width(1.0 / context.get_matrix()[0])
        context.rectangle(self.x, self.y, self.width, self.height)
        context.set_source_rgba(0.0, 0.0, 0.5, 0.15)
        context.fill_preserve()
        context.set_source_rgba(0.0, 0.0, 0.25, 0.5)
        context.stroke()
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ###context.restore()
