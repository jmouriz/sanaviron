#!/usr/bin/python
# -*- coding: utf-8 -*-

from handler import Handler
from magnetos import Magnetos
from rectangle import Rectangle
from color import Color
from gradient import Gradient
from position import Position
from point import Point
from size import Size
from objects import get_side
from objects import *

import gtk
import cairo
import pango
import pangocairo
import platform

class Object(Rectangle):
    """This class represents the parent of all draweable objects"""

    def __init__(self):
        #self.id = random.uniform(0, 999999999)
        Rectangle.__init__(self)
        self.handler = Handler()
        self.magnetos = Magnetos()
        self.offset = Point()
        self.pivot = Point()
        self.selected = False
        self.resizing = False
        self.direction = NONE
        self.control = AUTOMATIC
        self.z = 0

        self.hints = False
        from ui.canvas import Canvas
        self.canvas = Canvas()
        self.handler.is_testing = self.canvas.is_testing

        self.dash = []
        self.thickness = 1.0

        self.fill_style = COLOR
        self.fill_color = Color(0.25, 0.25, 0.25, 0.25)
        self.stroke_color = Color(0.25, 0.25, 0.25, 1.0)
        self.gradient = Gradient()

    def get_properties(self):
        return Rectangle.get_properties(self) + ["z", "fill_style", "fill_color", "stroke_color", "gradient"]

    def post(self):
        pass

    def delete(self):
        self.canvas.document.pages[0].children.remove(self)

    def set_fill_style(self, fill_style):
        self.fill_style = fill_style
        #self.set_property("fill_style", fill_style)
        if fill_style == COLOR:
            self.set_fill_color()
        elif fill_style == GRADIENT:
            self.set_gradient()

    def set_gradient(self, gradient=Gradient()): #ToDo: by name and from Canvas!
        self.fill_style = GRADIENT
        self.gradient = gradient

    def set_fill_color(self, color=Color()):
        self.fill_style = COLOR
        self.fill_color = color

    def set_stroke_color(self, color=Color()):
        self.stroke_color = color

    def draw_hints(self, context):
        extent = 25.0

        context.save()
        context.new_path()
        context.rectangle(self.x - extent, self.y - extent, extent, extent)
        context.set_source_rgba(130 / 255.0, 130 / 255.0, 250 / 255.0, 0.25)
        context.fill_preserve()
        context.set_line_width(1)
        context.set_source_rgb(130 / 255.0, 130 / 255.0, 250 / 255.0)
        context.stroke()

        context = pangocairo.CairoContext(context)
        layout = pangocairo.CairoContext.create_layout(context)
        if platform.system() == 'Windows':
            fontname = 'Sans'
        else:
            fontname = 'Ubuntu'
        text = str(int(self.z))
        length = len(text)
        if length > 3:
            size = 6
            text = "..." + text[length-1:4]
        elif length > 2:
            size = 8
        elif length > 1:
            size = 10
        else:
            size = 12
        description = '%s Bold %d' % (fontname, size)
        font = pango.FontDescription(description)
        layout.set_justify(True)
        layout.set_font_description(font)
        layout.set_text(text)
        context.set_source_rgb(0, 0, 0)
        width, height = layout.get_size()
        width /= pango.SCALE
        height /= pango.SCALE
        context.move_to(self.x - (extent + width) / 2, self.y - (extent + height) / 2)
        context.show_layout(layout)
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        context.restore()

    def draw(self, context):
        if self.hints:
            self.draw_hints(context)

        ###context.save()
        if self.selected:
            self.handler.x = self.x
            self.handler.y = self.y
            self.handler.width = self.width
            self.handler.height = self.height
            self.post()
            self.handler.draw(context)

        if self.magnetos.magnetized:
            self.magnetos.draw(context)
        ###context.restore()

    def at_position(self, x, y):
        if not len(self.handler.control):
            return False
        return (x >= (self.x - self.handler.control[0].size / 2.0)) and\
               (x <= (self.x + self.width + self.handler.control[0].size / 2.0)) and\
               (y >= (self.y - self.handler.control[0].size / 2.0)) and\
               (y <= (self.y + self.height + self.handler.control[0].size / 2.0))

    def in_region(self, x, y, width, height):
        if width < 0:
            x += width
            width *= -1
        if height < 0:
            y += height
            height *= -1
        return (x + width) > self.x and (y + height) > self.y and\
               x < (self.x + self.width) and y < (self.y + self.height)

    def in_selection(self, selection):
        return self.in_region(selection.x, selection.y, selection.width, selection.height)

    def transform(self, x, y):
        pass

    def get_cursor(self, direction):
        if direction == NORTHWEST:
            cursor = gtk.gdk.TOP_LEFT_CORNER
        elif direction == NORTH:
            cursor = gtk.gdk.TOP_SIDE
        elif direction == NORTHEAST:
            cursor = gtk.gdk.TOP_RIGHT_CORNER
        elif direction == WEST:
            cursor = gtk.gdk.LEFT_SIDE
        elif direction == EAST:
            cursor = gtk.gdk.RIGHT_SIDE
        elif direction == SOUTHWEST:
            cursor = gtk.gdk.BOTTOM_LEFT_CORNER
        elif direction == SOUTH:
            cursor = gtk.gdk.BOTTOM_SIDE
        elif direction == SOUTHEAST:
            cursor = gtk.gdk.BOTTOM_RIGHT_CORNER
        elif direction >= ANONIMOUS:
            cursor = gtk.gdk.CROSSHAIR
        else:
            cursor = gtk.gdk.ARROW

        return gtk.gdk.Cursor(cursor)

    def resize(self, x, y):
        direction = self.direction

        position = Position()
        position.x = self.x
        position.y = self.y

        size = Size()
        size.width = self.width
        size.height = self.height

        side = get_side(direction)

        if side is not VERTICAL:
            size.width = x - self.pivot.x
            if size.width < 0:
                position.x = x
            else:
                position.x = self.pivot.x

        if side is not HORIZONTAL:
            size.height = y - self.pivot.y
            if size.height < 0:
                position.y = y
            else:
                position.y = self.pivot.y

        self.set_position(position)
        self.set_size(size)

    def press(self, x, y):
        pass
