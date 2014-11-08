#!/usr/bin/python
# -*- coding: utf-8 -*-

import pango
import pangocairo
from object import Object
from objects import *
from control import Control

import gtk

class Table(Object):
    """This class represents a table"""
    __name__ = "Table"

    def __init__(self, rows=5, columns="0", titles=_("Column 1")):
        Object.__init__(self)
        self.vertical_spacing = 5
        self.horizontal_spacing = 5

        self.control = MANUAL

        self.rows = rows
        self.columns = columns
        self.titles = titles
        self.font = "Verdana"
        self.size = 16

    def get_properties(self):
        return Object.get_properties(self) + ["rows", "columns", "titles", "font", "size"]

    def post(self):
        controls = len(self.handler.control)
        while controls > ANONIMOUS:
            controls -= 1
            del self.handler.control[controls]

        columns = self.get_property("columns").split(':')

        offset = 0

        for i, column in enumerate(columns):
            offset += int(column)
            if i:
                offset += self.horizontal_spacing
            control = Control()
            self.handler.control.append(control)
            control.x = self.x + offset
            control.y = self.y + self.height / 2
            control.limbus = True

    def draw(self, context):
        ###context.save()

        rows = int(self.rows)
        columns = self.columns.split(':')
        n_columns = len(columns)

        titles = self.titles.split(':')

        self.width = 0
        self.height = 0

        context = pangocairo.CairoContext(context) # XXX
        total_width = 0

        for column in range(n_columns):
            for row in range(rows):
                layout = pangocairo.CairoContext.create_layout(context)
                fontname = self.font
                if fontname.endswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")): # XXX
                    description = fontname
                else:
                    size = int(self.size)
                    description = "%s %d" % (fontname, size)
                font = pango.FontDescription(description)
                layout.set_font_description(font)
                title = titles[column]
                layout.set_markup(title)

                if row == 0:
                    context.set_source_rgb(0.0, 0.0, 0.0)
                else:
                    context.set_source_rgb(0.75, 0.75, 0.75)

                width, height = layout.get_size()

                if columns[column] == '0':
                    width /= pango.SCALE
                    columns[column] = str(width)
                else:
                    width = int(columns[column])

                height /= pango.SCALE

                x = self.x + total_width + self.horizontal_spacing * column
                y = self.y + (self.vertical_spacing + height) * row

                context.move_to(x, y)
                context.show_layout(layout)

            self.height = (self.vertical_spacing + height) * rows

            total_width += width

        self.columns = ':'.join(columns)

        self.width = n_columns * self.horizontal_spacing - self.horizontal_spacing + total_width
        Object.draw(self, context)

    def get_cursor(self, direction):
        return gtk.gdk.Cursor(gtk.gdk.FLEUR)

    def transform(self, x, y):
        direction = self.direction - ANONIMOUS
        columns = self.columns.split(':')
        n_columns = len(columns)
        offset = self.x
        if direction < n_columns:
            for column in range(direction):
                offset += int(columns[column]) + self.horizontal_spacing
            columns[direction] = str(int(x - offset))
        self.columns = ':'.join(columns)
