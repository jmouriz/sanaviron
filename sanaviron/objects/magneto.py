#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk.gdk

from point import Point
from objects import NONE, HORIZONTAL, VERTICAL, BOTH

class Magneto(Point):
    """This class represents a object magnetic line"""

    __name__ = "Magneto"

    def __init__(self):
        Point.__init__(self)
        self.orientation = NONE

    def draw(self, context):
        context.set_line_width(1.0 / context.get_matrix()[0])

        if self.orientation in [ VERTICAL, BOTH ]:
            context.move_to(0, self.y)
            context.line_to(500, self.y)
        if self.orientation in [ HORIZONTAL, BOTH ]:
            context.move_to(self.x, 0)
            context.line_to(self.x, 500)

        context.set_source_rgba(0.0, 0.0, 0.75, 1.0)
        context.stroke()
