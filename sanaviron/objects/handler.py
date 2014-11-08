#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo

from control import Control
from objects import NONE, CENTER, ANONIMOUS

class Handler:
    """This class represents a rectangular control points handler"""

    def __init__(self):
        self.control = list()
        self.can_pivot = True
        self.center_pivot = False
        self.pivot = Control()
        self.pivot.pivot = True

        self.line = False

        self.is_testing = False

        index = 0
        while index < ANONIMOUS:
            control = Control()
            self.control.append(control)
            index += 1

    def draw_handler(self, context):
        if not self.line:
            context.set_antialias(cairo.ANTIALIAS_NONE)
            context.set_line_width(1.0 / context.get_matrix()[0])
            context.set_source_rgb(0.5, 0.5, 1.0)
            dash = []
            context.set_dash(dash)
            context.rectangle(self.x, self.y, self.width, self.height)
            context.stroke()
            context.set_antialias(cairo.ANTIALIAS_DEFAULT)

    def draw_controls(self, context):
        for control in self.control:
            control.draw(context)

    def draw_pivot(self, context):
        self.pivot.draw(context)

    def draw(self, context):
        self.draw_handler(context)
        self.draw_controls(context)
        if self.can_pivot:
            self.draw_pivot(context)

    def at_position(self, x, y):
        return self.get_direction(x, y) is not NONE

    def get_direction(self, x, y):
        for direction, control in enumerate(self.control):
            if control.at_position(x, y):
                return direction
        return NONE
