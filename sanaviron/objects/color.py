#!/usr/bin/python
# -*- coding: utf-8 -*-

from interfaces.serializable import Serializable

class Color(Serializable):
    """This class represents a color"""

    __name__ = "Color"

    def __init__(self, red=0.0, green=0.0, blue=0.0, alpha=1.0, string=None):
        Serializable.__init__(self)
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

        if string:
            self.set_color_as_hex(string)

    def get_properties(self):
        return ['red', 'green', 'blue', 'alpha']

    def __hex__(self):
        return self.serialize()

    def to_hex(self, number):   #number 0..1
        temp = hex(int(number * 255))[2:]
        if len(temp) != 2:
            temp = "0" + temp
        return temp

    def set_color_as_string(self, color="0 0 0 0"):
        self.red = float(color.split()[0])
        self.green = float(color.split()[1])
        self.blue = float(color.split()[2])
        self.alpha = float(color.split()[3])

    def set_color_as_hex(self, color="00000000"):
        self.red = float(int(color[0:2], 16)) / 255
        self.green = float(int(color[2:4], 16)) / 255
        self.blue = float(int(color[4:6], 16)) / 255
        self.alpha = float(int(color[6:], 16)) / 255 # TODO: May be optional?

    def serialize(self):
        return "".join(
            [self.to_hex(self.red), self.to_hex(self.green), self.to_hex(self.blue), self.to_hex(self.alpha)])
