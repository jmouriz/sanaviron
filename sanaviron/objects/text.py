#!/usr/bin/python
# -*- coding: utf-8 -*-
from .__init__ import *

from gi.repository import Pango
from gi.repository import PangoCairo
from .object import Object
from .scale import Scale
from .position import Position
from gi.repository import Gtk
from gi.repository import GObject
import os
import platform
from ctypes import c_char_p, c_int, CDLL

if platform.system() == "Windows":
    extension = "dll"
else:
    extension = "so"

if platform.machine() == "x86_64":
    suffix = platform.machine() + "."
else:
    suffix = ""

WSIface = CDLL(os.path.join(os.path.dirname(__file__), "wide-string", "wide-string." + suffix + extension))

WSIface.get_cursor_position.restype = c_int

#class Text(Object, Gtk.Editable):
class Text(Object):
    """This class represents a text"""
    __name__ = "Text"

    def __init__(self, text = _("enter text here")):
        Object.__init__(self)

        self.layout = None

        class Cursor:
            pass

        self.cursor = Cursor()
        self.cursor.visible = True
        self.cursor.index = (0, 0)

        self.timer_id = GObject.timeout_add(500, self.timer)

        self.font = "Verdana"
        self.size = 32
        self.preserve = False
        self.text = text
        self.foreground = "#000" # TODO

    def get_properties(self):
        return Object.get_properties(self) + ["font", "size", "preserve", "text", "foreground"]

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

        #_context = PangoCairo.create_context(context) # XXX
        #self.layout = PangoCairo.create_layout(_context)
        self.layout = PangoCairo.create_layout(context)
        fontname = self.font
        if fontname.endswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")): # XXX
            description = fontname
        else:
            size = int(self.size)
            description = "%s %d" % (fontname, size)
        font = Pango.FontDescription(description)
        self.layout.set_justify(True)
        self.layout.set_font_description(font)
        text = self.get_property('text')
        self.layout.set_markup(text)

        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)
        #context.set_source_rgb(1.0, 0.0, 0.0)
        context.move_to(self.x, self.y)

        if bool(self.preserve):
            self.layout.set_width(int(self.width) * Pango.SCALE)
            width, height = self.layout.get_size()
            height /= Pango.SCALE
            self.height = height
        else:
            width, height = self.layout.get_size()
            width /= Pango.SCALE
            height /= Pango.SCALE
            self.scale(context, width, height)

        PangoCairo.show_layout(context, self.layout)
        context.restore()

        if self.selected and self.cursor.visible:
            self.draw_cursor(context)

        Object.draw(self, context)

    def timer(self, *args):
        self.cursor.visible ^= 1
        self.canvas.update()
        return self.timer_id > 0

    def delete(self):
        self.timer_id = 0
        Object.delete(self)

    def draw_cursor(self, context):
        bounds = self.get_cursor_bounds()
        context.new_path()
        context.set_source_rgba(0.0, 0.0, 0.0, 1.0)
        context.set_line_width(2.0)
        context.move_to(self.x + bounds.x - bounds.width / 2, self.y + bounds.y)
        context.line_to(self.x + bounds.x + bounds.width / 2, self.y + bounds.y)
        context.move_to(self.x + bounds.x, self.y + bounds.y)
        context.line_to(self.x + bounds.x, self.y + bounds.y + bounds.height)
        context.move_to(self.x + bounds.x - bounds.width / 2, self.y + bounds.y + bounds.height)
        context.line_to(self.x + bounds.x + bounds.width / 2, self.y + bounds.y + bounds.height)
        context.stroke()

    def scale(self, context, width, height):
        if not self.width:
            self.width = width

        if not self.height:
            self.height = height

        scale = Scale()

        if width:
            scale.horizontal = self.width / width

        if height:
            scale.vertical = self.height / height

        if scale.horizontal:
            context.scale(scale.horizontal, 1.0)

        if scale.vertical:
            context.scale(1.0, scale.vertical)

    def get_aspect(self):
        if bool(self.preserve):
            return (1, 1)

        width, height = self.layout.get_size()

        if width:
            horizontal = self.width / (width / Pango.SCALE)
        else:
            horizontal = 1

        if height:
            vertical = self.height / (height / Pango.SCALE)
        else:
            vertical = 1

        return (horizontal, vertical)

    def get_index_from_x_y(self, x, y):
        (horizontal, vertical) = self.get_aspect()
        position = Position()
        position.x = int((x - self.x) * Pango.SCALE / horizontal)
        position.y = int((y - self.y) * Pango.SCALE / vertical)
        return self.layout.xy_to_index(position.x, position.y)

    def get_cursor_position(self):
        return self.cursor.index[0]

    def set_cursor_position(self, position):
        real = WSIface.get_cursor_position(self.text, position)
        self.cursor.index = (real, 0)

    def get_cursor_bounds(self):
        (strong, weak) = self.layout.get_cursor_pos(self.get_cursor_position())
        (horizontal, vertical) = self.get_aspect()

        class Bounds:
            pass

        bounds = Bounds()
        bounds.x = (strong.x / Pango.SCALE) * horizontal
        bounds.y = (strong.y / Pango.SCALE) * vertical
        bounds.width = strong.width / Pango.SCALE + 15
        bounds.height = strong.height / Pango.SCALE * vertical

        return bounds

    def press(self, x, y):
        self.cursor.visible = True
        self.cursor.index = self.get_index_from_x_y(x, y)

    def resize(self, x, y):
        self.cursor.visible = False
        Object.resize(self, x, y)

    def move(self, x, y):
        self.cursor.visible = False
        Position.move(self, x, y)
