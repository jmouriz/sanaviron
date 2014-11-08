#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import cairo
from object import Object
from scale import Scale
from objects import *

class Image(Object):
    """This class represents a image"""
    __name__ = "Image"

    def __init__(self, image=os.path.join("images", "logo.png")):
        Object.__init__(self)

        self.image = image

    def get_properties(self):
        return Object.get_properties(self) + ["image"]

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

    def draw(self, context):
        context.save()

        surface = cairo.ImageSurface.create_from_png(self.image)
        width = surface.get_width()
        height = surface.get_height()
        x, y = self.scale(context, width, height)
        context.set_source_surface(surface, self.x / x, self.y / y)

        context.paint()
        context.restore()
        Object.draw(self, context)

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
