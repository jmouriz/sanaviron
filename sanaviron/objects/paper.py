#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo

from margins import Margins
from scale import Scale

class Paper(Margins):
    """This class represents a paper"""

    def __init__(self):
        Margins.__init__(self)

        self.background = None

    def draw(self, context):
        context.save()
        context.set_antialias(cairo.ANTIALIAS_NONE)
        shadow = 5.0 / context.get_matrix()[0]
        context.set_line_width(1.0 / context.get_matrix()[0])
        context.rectangle(self.x, self.y, self.width, self.height)

        context.set_source_rgb(1.0, 1.0, 1.0)
        context.fill_preserve()

        if self.background:
            surface = cairo.ImageSurface.create_from_png(self.background)
            width = surface.get_width()
            height = surface.get_height()
            context.save()
            x, y = self.scale(context, width, height)
            context.set_source_surface(surface, self.x / x, self.y / y)
            context.paint()
            context.restore()
            context.set_source_rgba(1.0, 1.0, 1.0, 0.5)
            context.paint()

        context.set_source_rgb(0.0, 0.0, 0.0)
        dash = list()
        context.set_dash(dash)
        context.stroke()

        Margins.draw(self, context)

        context.set_source_rgba(0.0, 0.0, 0.0, 0.25)
        dash = list()
        context.set_dash(dash)

        context.set_line_width(shadow)
        context.move_to(self.x + self.width + shadow / 2.0, self.y + shadow)
        context.line_to(self.x + self.width + shadow / 2.0, self.y + self.height + shadow / 2.0)
        context.line_to(self.x + shadow, self.y + self.height + shadow / 2.0)
        context.stroke()

        context.restore()

    def scale(self, context, width, height):
        if not self.width:
            self.width = width

        if not self.height:
            self.height = height

        scale = Scale()
        scale.horizontal = self.width / float(width)
        scale.vertical = self.height / float(height)

        if scale.horizontal:
            context.scale(scale.horizontal, 1.0)
        else:
            scale.horizontal = 1

        if scale.vertical:
            context.scale(1.0, scale.vertical)
        else:
            scale.vertical = 1

        return (scale.horizontal, scale.vertical)
