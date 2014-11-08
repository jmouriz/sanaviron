#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo
from rectangle import Rectangle

from objects import HORIZONTAL, VERTICAL

class Guides(Rectangle):
    """This class represets the auxiliary guides"""

    def __init__(self):
        Rectangle.__init__(self)
        self.active = True
        self.tags = list()
        self.magnetism = 32

    def draw(self, context):
        if not self.active:
            return
        ###context.save()
        context.set_antialias(cairo.ANTIALIAS_NONE)

        for tag in self.tags:
            tag.draw_guide(context)

        context.stroke()
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ###context.restore()

    def add_tag(self, tag):
        tag.synchronize(self)
        self.tags.append(tag)

    def nearest(self, position):
        target = position
        for tag in self.tags:
            lower = tag.position - self.magnetism
            upper = tag.position + self.magnetism

            if tag.orientation == HORIZONTAL:
                if position.x > lower and position.x < upper:
                    target.x = tag.position
            elif tag.orientation == VERTICAL:
                if position.y > lower and position.y < upper:
                    target.y = tag.position
        return target