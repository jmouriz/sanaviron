#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from object import Object
from point import Point
from objects import *


class Line(Object):
    """This class represents a line"""
    __name__ = "Line"

    def __init__(self):
        Object.__init__(self)
        self.handler.line = True
        self.dash = list()

        self.start = Point()
        self.end = Point()

        self.set_property("arrow-tip-length", 4 * 4)
        self.set_property("arrow-length", 8 * 4)
        self.set_property("arrow-width", 3 * 4)

    def post(self):
        self.handler.control[NORTHWEST].x = self.start.x
        self.handler.control[NORTHWEST].y = self.start.y
        self.handler.control[SOUTHEAST].x = self.end.x
        self.handler.control[SOUTHEAST].y = self.end.y

    def draw(self, context):
        context.set_dash(self.dash)
        context.set_line_width(self.thickness)

        # arrow config
        #arrow_tip_length = self.get_property("arrow-tip-length")
        arrow_length = self.get_property("arrow-length")
        arrow_width = self.get_property("arrow-width")

        width = arrow_width / 2
        length = math.sqrt(width * width + arrow_length * arrow_length)
        degrees = math.tan(width / length)
        angle = math.atan2(abs(self.end.y - self.start.y), abs(self.end.x - self.start.x)) + math.pi
        a = Point()
        b = Point()
        a.x = self.end.x + length * math.cos(angle - degrees)
        a.y = self.end.y + length * math.sin(angle - degrees)
        b.x = self.end.x + length * math.cos(angle + degrees)
        b.y = self.end.y + length * math.sin(angle + degrees)

        # line
        context.move_to(self.start.x, self.start.y)
        context.line_to(self.end.x, self.end.y)

        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)
        context.stroke()

        # arrow
        if 0:
            context.move_to(self.end.x, self.end.y)
            context.line_to(a.x, a.y)
            context.line_to(b.x, b.y)
            context.line_to(self.end.x, self.end.y)

            context.fill_preserve()
            context.stroke()

        Object.draw(self, context)

    def resize(self, x, y):
        Object.resize(self, x, y)
        self.start.x = self.handler.pivot.x
        self.start.y = self.handler.pivot.y
        self.end.x = x
        self.end.y = y