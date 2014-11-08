#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import sin, cos

from control import Control
from object import Object
from objects import *

class Arc(Object):
    """This class represents an arc"""

    __name__ = "Arc"

    def __init__(self):
        Object.__init__(self)
        self.angle_start = 0.0
        self.angle_stop = 360.0
        self.radius_horizontal = 0
        self.radius_vertical = 0
        self.centre_x = 0
        self.centre_y = 0
        self.closed = False
        self.closed_at_centre = False

        self.handler.control.append(Control())
        self.handler.control.append(Control())

        #self.block = False

    def get_properties(self):
        return Object.get_properties(self) + ["angle_start", "angle_stop", "closed", "closed_at_centre"]

    def set_angle_start(self, ang):
        self.angle_start = ang

    def set_angle_stop(self, ang):
        self.angle_stop = ang

    def post(self):
        self.handler.control[NORTHWEST].x = self.x
        self.handler.control[NORTHWEST].y = self.y
        self.handler.control[NORTHEAST].x = self.x + self.width
        self.handler.control[NORTHEAST].y = self.y
        self.handler.control[SOUTHWEST].x = self.x
        self.handler.control[SOUTHWEST].y = self.y + self.height
        self.handler.control[SOUTHEAST].x = self.x + self.width
        self.handler.control[SOUTHEAST].y = self.y + self.height

        self.handler.control[8].x = self.centre_x + self.radius_horizontal * cos(grad2rad(self.angle_start))
        self.handler.control[8].y = self.centre_y + self.radius_vertical * sin(grad2rad(self.angle_start))
        self.handler.control[8].limbus = True

        self.handler.control[9].x = self.centre_x + self.radius_horizontal * cos(grad2rad(self.angle_stop))
        self.handler.control[9].y = self.centre_y + self.radius_vertical * sin(grad2rad(self.angle_stop))
        self.handler.control[9].limbus = True

        #self.height = self.width

    def draw(self, context):
        context.set_dash(self.dash)
        context.set_line_width(self.thickness)

        self.radius_horizontal = self.width / 2.0
        self.radius_vertical = self.height / 2.0
        self.centre_x = self.x + self.radius_horizontal
        self.centre_y = self.y + self.radius_vertical

        context.save()
        context.new_path()
        context.translate(self.x, self.y)
        if (self.width) and (self.height > 0):
            context.scale(self.width, self.height)
        context.arc(0.5, 0.5, 0.5, grad2rad(self.angle_start), grad2rad(self.angle_stop))

        if (self.angle_start == self.angle_stop) or (self.angle_start == 0.0 and self.angle_stop == 360.0) or\
           (self.angle_start == 360.0 and self.angle_stop == 0.0):
            closed = False
        else:
            closed = self.closed

        if closed:
            if self.closed_at_centre:
                context.line_to(0.5, 0.5)
            context.close_path()

        if self.fill_style == GRADIENT:
            self.set_gradient(self.gradient)
        elif self.fill_style == COLOR:
            context.set_source_rgba(self.fill_color.red, self.fill_color.green,
                self.fill_color.blue, self.fill_color.alpha)
        context.fill_preserve()
        context.restore()

        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)
        context.stroke()
        Object.draw(self, context)

    def transform(self, x, y):
        if self.direction == 8:
            x0 = self.x + self.radius_horizontal
            y0 = self.y + self.radius_vertical

            self.closed_at_centre = not((x < self.x) or (y < self.y))

            if (x > (self.width + self.x)) or (y > (self.height + self.y)):
                self.closed_at_centre = False

            if (self.radius_horizontal > 0) and (self.radius_vertical > 0):
                ang = angle_from_coordinates(x, y, x0, y0, self.radius_horizontal,
                    self.radius_vertical)
                self.set_angle_start(ang)
        else:
            x0 = self.x + self.radius_horizontal
            y0 = self.y + self.radius_vertical

            self.closed_at_centre = not ((x < self.x) or (y < self.y))

            if (x > (self.width + self.x)) or (y > (self.height + self.y)):
                self.closed_at_centre = False

            if (self.radius_horizontal > 0) and (self.radius_vertical > 0):
                ang = angle_from_coordinates(x, y, x0, y0, self.radius_horizontal,
                    self.radius_vertical)
                self.set_angle_stop(ang)
