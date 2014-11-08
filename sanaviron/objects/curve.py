#!/usr/bin/python
# -*- coding: utf-8 -*-

from object import Object
from objects import *
from control import Control

class Curve(Object):
    """This class represents a curve"""
    __name__ = "Curve"

    def __init__(self):
        Object.__init__(self)
        #self.handler.line = True
        self.dash = list()
        self.radius = 20

        self.control = MANUAL

        control = Control()
        self.handler.control.append(control)

        self.block = False

    def post(self):
        self.handler.control[NORTHWEST].x = self.x
        self.handler.control[NORTHWEST].y = self.y
        self.handler.control[SOUTHEAST].x = self.x + self.width
        self.handler.control[SOUTHEAST].y = self.y + self.height

        if not self.block:
            self.handler.control[8].x = self.x + self.width
            self.handler.control[8].y = self.y
            self.handler.control[8].limbus = True
            self.block ^= 1

    def draw(self, context):
        ###context.save()
        context.set_dash(self.dash)
        context.set_line_width(self.thickness)
        context.move_to(self.x, self.y)
        context.curve_to(self.x, self.y, self.handler.control[8].x, self.handler.control[8].y, self.x + self.width,
            self.y + self.height)
        #context.curve_to(self.x, self.y, self.x + self.width, self.y, self.x + self.width, self.y + self.height)
        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)
        context.stroke()
        Object.draw(self, context)
        ###context.restore()

    def transform(self, x, y):
        self.handler.control[8].x = x
        self.handler.control[8].y = y
