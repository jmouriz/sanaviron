#!/usr/bin/python
# -*- coding: utf-8 -*-

from color import Color

class GradientColor(Color):
    """This class represents a gradient color"""

    __name__ = "GradientColor"

    def __init__(self, red=0.0, green=0.0, blue=0.0, alpha=1.0, position=0, string=None):
        Color.__init__(self, red, green, blue, alpha)
        self.position = position

        if string:
            array = string.split(':')
            #Color.set_color_as_hex(self, array[0])
            self.set_color_as_hex(array[0])
            self.position = array[1]

    def get_properties(self):
        return Color.get_properties(self) + ['position']

    def serialize(self):
        return Color.serialize(self) + ":%d" % int(self.position)