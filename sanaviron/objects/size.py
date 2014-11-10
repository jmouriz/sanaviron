#!/usr/bin/python
# -*- coding: utf-8 -*-

from interfaces.serializable import Serializable

class Size(Serializable):
    """This class represents a size"""

    __name__ = "Size"

    def __init__(self):
        Serializable.__init__(self)
        self.width = 0
        self.height = 0

    def get_properties(self):
        return ["width", "height"]

    def set_size(self, size):
        (self.width, self.height) = (abs(size.width), abs(size.height))
