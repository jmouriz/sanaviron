#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo
from objects import *
from gradientcolor import GradientColor
from interfaces.serializable import Serializable


class Gradient(Serializable):
    """This class represents a gradient"""

    __name__ = "Gradient"

    def __init__(self, type=LINEAR, x=0, y=0, width=1, height=1, string=None):
        Serializable.__init__(self)
        self.type = type
        self.colors = [GradientColor(1, 1, 1, 1, 0), GradientColor(0, 0, 0, 1, 1)]
        self.x, self.y = x, y
        self.width, self.height = width, height
        if type == LINEAR:
            self.gradient = cairo.LinearGradient(x, y, width, height)
        elif type == RADIAL:
            self.gradient = cairo.RadialGradient(x, y, width, height, 10, 100)

        if string:
            self.colors = []
            data = string.split('|')
            area = data.pop().split(':')
            self.x = float(area[0])
            self.y = float(area[1])
            self.width = float(area[2])
            self.height = float(area[3])
            map(lambda color: self.colors.append(GradientColor(string=color)), data)

        self.update()

    def get_properties(self):
        return ['type', 'colors']

    def change_size(self, x, y, x1, y1):
        self.x, self.y = x, y
        self.width, self.height = x1, y1
        self.update()

    def clear(self):
        self.colors = []
        self.update()

    def set_position(self, index, position):
        self.colors[index].position = position
        self.update()

    def set_color(self, index, color):
        self.colors[index] = color
        self.update()

    def add_new_color(self, gradient_color):
        self.colors.append(gradient_color)
        self.update()


    def delete_color(self, position):
        if len(self.colors) > 1:
            self.colors[position] = []
            self.update()


    def insert_color(self, gradient_color, position):
        self.colors.insert(position, gradient_color)
        self.update()

    def change_type(self, type):
        self.type = type
        self.update()

    def update(self):
        if self.gradient is cairo.Gradient:
            del(self.gradient)
        if self.type == LINEAR: ###ToDo two type!!!
            self.gradient = cairo.LinearGradient(self.x, self.y, self.width, self.height)
        elif self.type == RADIAL:
            self.gradient = cairo.RadialGradient(self.x, self.y, self.width, self.height, 10, 100)
        else: raise BaseException

        for color in self.colors:
            self.gradient.add_color_stop_rgba(float(color.position), color.red, color.green, color.blue, color.alpha)

    def serialize(self):
        colors = list()
        map(lambda color: colors.append(color.serialize()), self.colors)
        return "|".join(colors) + "|%.02f:%.02f:%.02f:%.02f" % (self.x, self.y, self.width, self.height)
