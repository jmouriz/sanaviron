#!/usr/bin/python
# -*- coding: utf-8 -*-

from control import Control
from object import Object
from objects import *
from math import pi
import sys
from gradient import Gradient

class Rounded(Object):
    """This class represents a rounded box"""
    __name__ = "Rounded"

    def __init__(self):
        Object.__init__(self)

        self.set_property("radius", 10)

        control = Control()
        self.handler.control.append(control)

    def post(self):
        self.handler.control[NORTHWEST].x = self.x
        self.handler.control[NORTHWEST].y = self.y
        #self.handler.control[NORTHWEST].active = False
        self.handler.control[NORTHEAST].x = self.x + self.width
        self.handler.control[NORTHEAST].y = self.y
        self.handler.control[SOUTHWEST].x = self.x
        self.handler.control[SOUTHWEST].y = self.y + self.height
        self.handler.control[SOUTHEAST].x = self.x + self.width
        self.handler.control[SOUTHEAST].y = self.y + self.height
        self.handler.control[NORTH].x = self.x + self.width / 2
        self.handler.control[NORTH].y = self.y
        self.handler.control[SOUTH].x = self.x + self.width / 2
        self.handler.control[SOUTH].y = self.y + self.height
        self.handler.control[WEST].x = self.x
        self.handler.control[WEST].y = self.y + self.height / 2
        self.handler.control[EAST].x = self.x + self.width
        self.handler.control[EAST].y = self.y + self.height / 2

        radius = float(self.get_property("radius"))
        self.handler.control[8].x = self.x + radius
        self.handler.control[8].y = self.y + radius
        self.handler.control[8].limbus = True

    def draw(self, context):
        ###context.save()
        radius = float(self.get_property("radius"))

        dash = list()
        context.set_dash(dash)
        context.set_line_width(1)

        if radius > (self.height / 2) or radius > (self.width / 2):
            if (self.height / 2) < (self.width / 2):
                radius = self.height / 2
            else:
                radius = self.width / 2

        context.move_to(self.x, self.y + radius)
        context.arc(self.x + radius, self.y + radius, radius, pi, -pi / 2)
        context.line_to(self.x + self.width - radius, self.y)
        context.arc(self.x + self.width - radius, self.y + radius, radius, -pi / 2, 0)
        context.line_to(self.x + self.width, self.y + self.height - radius)
        context.arc(self.x + self.width - radius, self.y + self.height - radius, radius, 0, pi / 2)
        context.line_to(self.x + radius, self.y + self.height)
        context.arc(self.x + radius, self.y + self.height - radius, radius, pi / 2, pi)
        context.close_path()

        self.fill_style = GRADIENT # DEBUG

        if self.fill_style == GRADIENT:
            self.set_gradient(Gradient(0, self.x, self.y, self.x + self.width, self.y))
            context.set_source(self.gradient.gradient)
        elif self.fill_style == COLOR:
            context.set_source_rgba(self.fill_color.red, self.fill_color.green,
                self.fill_color.blue, self.fill_color.alpha)
        context.fill_preserve()

        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)
        context.stroke()
        Object.draw(self, context)
        ###context.restore()

    def transform(self, x, y):
        radius = x - self.x
        if (radius > 0 and radius < self.height / 2 and radius < self.width / 2):
            self.set_property("radius", radius)
