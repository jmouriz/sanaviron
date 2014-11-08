#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo

from rectangle import Rectangle
from control import Control

class Margins(Rectangle):
    """This class represents the margins"""

    def __init__(self):
        Rectangle.__init__(self)
        self.active = True
        self.top = 0
        self.left = 0
        self.bottom = 0
        self.right = 0
        self.control = list()

        index = 0
        while index < 8:
            control = Control()
            self.control.append(control)
            index += 1

    def draw(self, context):
        if self.active:
            context.set_antialias(cairo.ANTIALIAS_NONE)
            context.set_source_rgb(0.3, 0.3, 0.3)
            dash = []
            context.set_dash(dash)

            context.set_line_width(1.0 / context.get_matrix()[0])
            context.rectangle(self.x + self.left, self.y + self.top, self.width - self.right - self.left,
                self.height - self.bottom - self.top)
            context.stroke()

            """self.control[NORTHWEST].x = self.x + self.left
          self.control[NORTHWEST].y = self.y + self.top
          self.control[NORTHEAST].x = self.x + self.width - self.right
          self.control[NORTHEAST].y = self.y + self.top
          self.control[SOUTHWEST].x = self.x + self.left
          self.control[SOUTHWEST].y = self.y + self.height - self.bottom
          self.control[SOUTHEAST].x = self.x + self.width - self.right
          self.control[SOUTHEAST].y = self.y + self.height - self.bottom
          self.control[NORTH].x = self.x + (self.width - self.right) / 2
          self.control[NORTH].y = self.y + self.top
          self.control[SOUTH].x = self.x + (self.width - self.right) / 2
          self.control[SOUTH].y = self.y + self.height - self.bottom
          self.control[WEST].x = self.x + self.left
          self.control[WEST].y = self.y + (self.height - self.bottom) / 2
          self.control[EAST].x = self.x + self.width - self.right
          self.control[EAST].y = self.y + (self.height - self.bottom) / 2

          for control in self.control:
            control.draw(context)"""
            context.set_antialias(cairo.ANTIALIAS_DEFAULT)