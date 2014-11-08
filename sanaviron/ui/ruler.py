#!/usr/bin/python
# -*- coding: utf-8 -*-
import platform
import gtk

from interfaces.signalizable import Signalizable
from objects.tag import Tag
from objects import HORIZONTAL, VERTICAL

if platform.system() != 'Windows':
    gtk.threads_init()

import cairo
import pango
import pangocairo

class Ruler(gtk.Viewport, Signalizable):
    """This class represents a non-orientated ruler interface"""

    def __init__(self, orientation=VERTICAL):
        gtk.Viewport.__init__(self)
        Signalizable.__init__(self)

        self.orientation = orientation
        self.x = 0
        self.y = 0
        self.offset = 0
        self.tags = list()
        self.zoom = 1.0
        self.show_position = True
        self.layout = gtk.Layout()
        self.add(self.layout)

        size = 25
        if self.orientation == HORIZONTAL:
            self.set_size_request(-1, size)
        elif self.orientation == VERTICAL:
            self.set_size_request(size, -1)

        self.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.layout.add_events(gtk.gdk.EXPOSURE_MASK)
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)

        self.connect("motion-notify-event", self.motion, False)
        self.connect("button-release-event", self.release)
        self.connect("button-press-event", self.press)
        self.layout.connect("expose-event", self.expose)

        self.install_signal("append-tag")
        self.install_signal("move-tag")

    def motion(self, widget, event, external):
        if self.orientation == HORIZONTAL:
            self.x = event.x - self.offset * external
            for tag in self.tags:
                if tag.selected and event.state & gtk.gdk.BUTTON1_MASK:
                    tag.move(self.x)
                    self.emit("move-tag", tag)
                elif tag.at_position(self.x):
                    widget.window.set_cursor(gtk.gdk.Cursor(tag.get_cursor()))
                    self.show_position = False
                    break
                else:
                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW))
                    self.show_position = True
        elif self.orientation == VERTICAL:
            self.y = event.y - self.offset * external
            for tag in self.tags:
                if tag.selected and event.state & gtk.gdk.BUTTON1_MASK:
                    tag.move(self.y)
                    self.emit("move-tag", tag)
                elif tag.at_position(self.y):
                    widget.window.set_cursor(gtk.gdk.Cursor(tag.get_cursor()))
                    self.show_position = False
                    break
                else:
                    widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW))
                    self.show_position = True
        self.queue_draw()
        return True

    def press(self, widget, event):
        position = 0
        if self.orientation == HORIZONTAL:
            position = event.x
        if self.orientation == VERTICAL:
            position = event.y
        for tag in self.tags:
            if tag.at_position(position):
                tag.selected = True
                break

    def release(self, widget, event):
        select = False
        for tag in self.tags:
            if tag.selected:
                select = True
                tag.selected = False
        if not select:
            tag = Tag()
            tag.orientation = self.orientation
            if self.orientation == HORIZONTAL:
                tag.position = event.x
            elif self.orientation == VERTICAL:
                tag.position = event.y
            self.tags.append(tag)
            self.emit("append-tag", tag)
        return True

    def expose(self, widget, event):
        context = widget.bin_window.cairo_create()
        context.set_antialias(cairo.ANTIALIAS_NONE)
        width, height = widget.window.get_size()
        size = width if self.orientation == HORIZONTAL else height
        context.set_dash([])

        def draw_lines(context, position, margin, size, unit, zoom):
            while position <= size:
                if self.orientation == HORIZONTAL:
                    context.move_to(position * zoom, margin)
                    context.line_to(position * zoom, size)
                elif self.orientation == VERTICAL:
                    context.move_to(margin, position * zoom)
                    context.line_to(size, position * zoom)
                position += unit

        context.set_line_width(1)
        draw_lines(context, 25, 18, size, 10, self.zoom)
        draw_lines(context, 25, 10, size, 50, self.zoom)
        context.stroke()

        context.set_line_width(2)
        draw_lines(context, 25, 8, size, 100, self.zoom)
        context.stroke()

        context.set_line_width(3)
        for tag in self.tags:
            tag.draw_tag(context)
        context.stroke()

        if self.show_position:
            context.set_line_width(1)
            context.set_source_rgb(0.0, 0.0, 0.75)
            border = 2
            if self.orientation == HORIZONTAL and self.x:
                context.move_to(self.x, border)
                context.line_to(self.x, size)
            elif self.orientation == VERTICAL and self.y:
                context.move_to(border, self.y)
                context.line_to(size - border, self.y)
            context.stroke()


            context = pangocairo.CairoContext(context)
            layout = pangocairo.CairoContext.create_layout(context)
            fontname = 'Sans' if platform.system() == 'Windows' else 'Ubuntu'
            size = 8
            description = '%s %d' % (fontname, size)
            font = pango.FontDescription(description)
            layout.set_justify(True)
            layout.set_font_description(font)
            text = None
            if self.orientation == HORIZONTAL:
                context.move_to(self.x + 2, 0)
                text = str(int(self.x))
            elif self.orientation == VERTICAL:
                context.move_to(2, self.y)
                text = str(int(self.y))
            layout.set_text(text)
            context.set_antialias(cairo.ANTIALIAS_DEFAULT)
            context.set_source_rgb(0.0, 0.0, 0.0)
            context.show_layout(layout)
        return True


class HorizontalRuler(Ruler):
    """This class represents a horizontal ruler"""

    def __init__(self):
        Ruler.__init__(self, HORIZONTAL)


class VerticalRuler(Ruler):
    """This class represents a vertical ruler"""

    def __init__(self):
        Ruler.__init__(self)


if __name__ == '__main__':
    horizontal_window = gtk.Window()
    horizontal_window.connect("delete-event", gtk.main_quit)
    horizontal_ruler = HorizontalRuler()
    horizontal_window.add(horizontal_ruler)
    horizontal_window.show_all()
    vertical_window = gtk.Window()
    vertical_window.connect("delete-event", gtk.main_quit)
    vertical_ruler = VerticalRuler()
    vertical_window.add(vertical_ruler)
    vertical_window.show_all()
    gtk.main()
