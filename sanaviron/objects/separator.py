#!/usr/bin/python
# -*- coding: utf-8 -*-

from control import Control
from rectangle import Rectangle
from objects import NONE, HORIZONTAL, VERTICAL

class Separator(Rectangle):
    """This class represents a box separator"""

    def __init__(self):
        Rectangle.__init__(self)
        self.hidden = False
        self.position = 0.0
        self.direction = NONE

        self.control = Control()
        self.control.limbus = True

    def draw(self, context):
        self.control.active = not self.hidden
        if not self.hidden:
            if self.direction == VERTICAL:
                context.move_to(self.x + self.position, self.y)
                context.line_to(self.x + self.position, self.y + self.height)
                self.control.x = self.x + self.position
                self.control.y = self.y + self.height / 2
            elif self.direction == HORIZONTAL:
                context.move_to(self.x, self.y + self.position)
                context.line_to(self.x + self.width, self.y + self.position)
                self.control.x = self.x + self.width / 2
                self.control.y = self.y + self.position
            context.stroke()

    def serialize(self):
        return "%.02f:%d" % (self.position, self.direction)