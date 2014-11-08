#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo

from point import Point
from magneto import Magneto
from objects import NONE, CENTER, HORIZONTAL, VERTICAL, BOTH

class Magnetos(list):
    """This class represents the object magnetos"""

    def __init__(self):
        list.__init__(self)

        self.magnetism = 48
        self.magnetized = False

        index = 0
        while index < CENTER:
            magneto = Magneto()
            magneto.orientation = BOTH
            self.append(magneto)
            index += 1

    def __getitem__(self, key):
        return list.__getitem__(self, key)

    def __setitem__(self, key, item):
        list.__setitem__(self, key, item)

    def draw(self, context):
        for magneto in self:
            magneto.draw(context)

    def get_magnetized(self, point):
        target = point
        orientation = NONE
        for magneto in self:
            magneto.orientation = NONE
            if not orientation == HORIZONTAL and abs(target.x - magneto.x) < self.magnetism:
                magneto.orientation = HORIZONTAL
                target.x = magneto.x
            if not orientation == VERTICAL and abs(target.y - magneto.y) < self.magnetism:
                magneto.orientation = BOTH if magneto.orientation == HORIZONTAL else VERTICAL
                target.y = magneto.y
            if not orientation:
                orientation = magneto.orientation
        return target

    def is_magnetized(self, point):
        self.magnetized = False
        for magneto in self:
            if abs(point.x - magneto.x) < self.magnetism or abs(point.y - magneto.y) < self.magnetism:
               self.magnetized = True
               return True
        return False
