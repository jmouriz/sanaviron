#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk.gdk

from rectangle import Rectangle
from objects import NONE, HORIZONTAL, VERTICAL

class Tag(Rectangle):
    """This class represents a ruler tag"""

    __name__ = "Tag"

    def __init__(self):
        Rectangle.__init__(self)
        self.position = 0
        self.selected = False
        self.size = 25
        self.orientation = NONE

    def get_properties(self):
        return ["position", "orientation"]

    def draw_tag(self, context):
        position = self.position
        size = self.size
        if self.orientation == HORIZONTAL:
            border = 5
            context.move_to(position, border)
            context.line_to(position, size - border)
        elif self.orientation == VERTICAL:
            border = 4
            context.move_to(border, position)
            context.line_to(size - border, position)
        context.set_source_rgb(0.75, 0.0, 0.0)
        #context.stroke()

    def draw_guide(self, context):
        position = self.position
        dash = [2.0 / context.get_matrix()[0], 4.0 / context.get_matrix()[0],
                24.0 / context.get_matrix()[0], 4.0 / context.get_matrix()[0]]
        context.set_line_width(1.0 / context.get_matrix()[0])
        context.set_dash(dash)
        if self.orientation == VERTICAL:
            context.move_to(self.x, position)
            context.line_to(self.x + self.width, position)
        elif self.orientation == HORIZONTAL:
            context.move_to(position, self.y)
            context.line_to(position, self.y + self.height)
        context.set_source_rgb(0.75, 0.0, 0.0)
        #context.stroke()

    def at_position(self, position):
        return position > self.position - 5 and position < self.position + 5

    def get_cursor(self):
        return gtk.gdk.SB_H_DOUBLE_ARROW if self.orientation == HORIZONTAL else gtk.gdk.SB_V_DOUBLE_ARROW

    def move(self, position):
        self.position = position
