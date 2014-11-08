#!/usr/bin/python
# -*- coding: utf-8 -*-

from object import Object
from separator import Separator
from size import Size
from objects import *

class Box(Object):
    """This class represents a box"""

    __name__ = "Box"

    def __init__(self):
        Object.__init__(self)

        self.separators = list()

    def get_properties(self):
        return Object.get_properties(self) + ["separators"]

    def post(self):
        self.handler.control[NORTHWEST].x = self.x
        self.handler.control[NORTHWEST].y = self.y
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

        self.magnetos[LEFT].x = self.handler.control[WEST].x
        self.magnetos[LEFT].y = self.handler.control[WEST].y
        self.magnetos[RIGHT].x = self.handler.control[EAST].x
        self.magnetos[RIGHT].y = self.handler.control[EAST].y
        self.magnetos[TOP].x = self.handler.control[NORTH].x
        self.magnetos[TOP].y = self.handler.control[NORTH].y
        self.magnetos[BOTTOM].x = self.handler.control[SOUTH].x
        self.magnetos[BOTTOM].y = self.handler.control[SOUTH].y

    def draw(self, context):
        dash = list()
        context.set_dash(dash)
        context.set_line_width(self.thickness)

        context.save()
        context.new_path()
        context.translate(self.x, self.y)
        if (self.width > 0) and (self.height > 0):
            context.scale(self.width,self.height)
        context.rectangle(0, 0, 1, 1)

        if self.fill_style == GRADIENT:
            context.set_source(self.gradient.gradient)
        elif self.fill_style == COLOR:
            context.set_source_rgba(self.fill_color.red, self.fill_color.green,
                self.fill_color.blue, self.fill_color.alpha)
        context.fill_preserve()
        context.restore()

        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)
        context.stroke()

        for i, separator in enumerate(self.separators):
            separator.synchronize(self)
            separator.draw(context)
            self.handler.control[ANONIMOUS+i] = separator.control

        Object.draw(self, context)
        ###context.restore()

    def transform(self, x, y):
        direction = self.direction
        if len(self.separators) > 0:
            if direction >= ANONIMOUS:
                separator = self.separators[direction - ANONIMOUS]
                if separator.direction == VERTICAL and x >= self.x and x - self.x <= self.width:
                    separator.position = x - self.x
                elif separator.direction == HORIZONTAL and y >= self.y and y - self.y <= self.height:
                    separator.position = y - self.y

    def add_separator_vertical(self, position):
        separator = Separator()
        separator.position = position
        separator.direction = VERTICAL
        self.separators.append(separator)
        self.handler.control.append(separator.control)

    def add_separator_horizontal(self, position):
        separator = Separator()
        separator.position = position
        separator.direction = HORIZONTAL
        self.separators.append(separator)
        self.handler.control.append(separator.control)

    def remove_separator(self):
        if self.separators.pop():
            self.handler.control.pop()

    def resize(self, x, y):
        source = Size()
        source.width = self.width
        source.height = self.height
        Object.resize(self, x, y)
        target = Size()
        target.width = self.width
        target.height = self.height

        if len(self.separators) > 0:
            for separator in self.separators:
                if separator.direction == HORIZONTAL and source.height and target.height:
                    separator.position = separator.position / source.height * target.height
                    separator.hidden = False
                elif separator.direction == VERTICAL and source.width and target.width:
                    separator.position = separator.position / source.width * target.width
                    separator.hidden = False
                else:
                    separator.hidden = True
