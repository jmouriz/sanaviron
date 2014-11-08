#!/usr/bin/python
# -*- coding: utf-8 -*-

"""A canvas for drawing things on it"""

import platform
import sys
import gtk


if platform.system() != 'Windows':
    gtk.threads_init()

import cairo

from objects.document import Document
from objects.page import Page
from objects.origin import Origin
from objects.grid import Grid
from objects.guides import Guides
from objects.selection import Selection
from objects.size import Size
from objects.point import Point
from interfaces.signalizable import Signalizable

from objects.barcode import BarCode
from objects.image import Image
from objects.text import Text
from objects.table import Table
from objects.line import Line
from objects.box import Box
from objects.rounded import Rounded
from objects.arc import Arc
from objects.curve import Curve
from objects.connector import Connector
from objects.chart import Chart

from objects import *
from ui import singleton

import xml.parsers.expat
import xml.dom.minidom


class BaseCanvas(gtk.Layout, Signalizable):
    """This class represents a low level canvas"""

    #    canvas = None
    #
    #    def __new__(self):
    #        if self.canvas:
    #            return self.canvas
    #        else:
    #            self.canvas = super(BaseCanvas, self).__new__(self)
    #            self.canvas.initialize()
    #            return self.canvas
    #
    #    def initialize(self):
    def __init__(self, application=None):
        gtk.Layout.__init__(self)
        Signalizable.__init__(self)

        self.is_testing = False

        self.configure()
        #from ui.application import Application
        #self.application = Application()
        if application:
            self.application = application

        self.install_statics()

    def install_statics(self):
        class Statics:
            pass

        self.statics = Statics()
        self.statics.motion = 0
        self.statics.expose = 0
        self.statics.consumed = Statics()
        self.statics.consumed.motion = 0

    def configure(self):
        self.configure_events()
        self.configure_handlers()

        self.install_signals()

        self.set_can_default(True)
        self.set_can_focus(True)

    def configure_events(self):
        self.set_events(0)

        self.add_events(gtk.gdk.EXPOSURE_MASK |
                        gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.BUTTON_MOTION_MASK)
        #self.add_events(gtk.gdk.KEY_PRESS_MASK)

    def configure_handlers(self):
        self.expose_id = self.connect("expose-event", self.expose)
        self.motion_id = self.connect("motion-notify-event", self.motion)
        self.connect("button-press-event", self.press)
        self.connect("button-release-event", self.release)
        #self.connect("key-press-event", self.key_press)

    def install_signals(self):
        self.install_signal("select")
        self.install_signal("finalize")
        self.install_signal("edit-child")

    def consume(self, type, state):
        next = gtk.gdk.event_get()
        while next and next.type == type and next.state == state:
            next.free()
            next = gtk.gdk.event_get()
            self.statics.consumed.motion += 1

    #def key_press(self, widget, event):
    #    raise NotImplementedError

    def release(self, widget, event):
        raise NotImplementedError

    def motion(self, widget, event):
        raise NotImplementedError

    def press(self, widget, event):
        raise NotImplementedError

    def expose(self, widget, event):
        raise NotImplementedError


class CanvasImplementation(BaseCanvas):
    """This class represents a high level canvas implementation"""

    #    def initialize(self):
    #        BaseCanvas.initialize(self)
    def __init__(self, application):
        BaseCanvas.__init__(self, application)
        self.origin = Origin()
        self.grid = Grid()
        self.guides = Guides()
        self.selection = Selection()

        #        self.gradients = []
        #        grad = Gradient(type=LINEAR, name="1", x=0, y=0, x1=0, y1=0)
        #        grad.clear()
        #        grad.add_new_color(GradientColor(1.0, 0.0, 0.0, 1.0, 0.142))
        #        grad.add_new_color(GradientColor(1.0, 1.0, 0.0, 1.0, 0.285))
        #        grad.add_new_color(GradientColor(0.0, 1.0, 0.0, 1.0, 0.428))
        #        grad.add_new_color(GradientColor(0.0, 1.0, 1.0, 1.0, 0.571))
        #        grad.add_new_color(GradientColor(0.0, 0.0, 1.0, 1.0, 0.714))
        #        grad.add_new_color(GradientColor(1.0, 0.0, 1.0, 1.0, 0.857))
        #        grad.update()
        #        self.gradients.append(grad)

        self.document = Document()
        #self.document.pages[0].children = list()
        #self.document.pages = list()

        page = Page()
        self.total = Size()

        self.document.pages.append(page)
        self.zoom = 1.0
        self.origin.x = 0 # XXX
        self.origin.y = 0 # XXX
        self.border = 25

        self.pick = False
        self.updated = False
        self.child = None
        self.stop_cursor_change = False

        self.horizontal_ruler = None
        self.vertical_ruler = None
        self.clipboard = None

        self.hints = False

        self.motions = 0

    def release(self, widget, event):
        """
        This code is executed when you release the mouse button
        """
        if self.selection.active:
            self.unselect_all()
            for child in self.document.pages[0].children:
                if child.in_selection(self.selection):
                    child.selected = True
                    self.emit("select", child)
                    #elif child.resizing:
                    #    child.resizing ^= 1
            self.selection.active = False
        else:
            for child in self.document.pages[0].children:
                if child.selected:
                    self.emit("finalize", child)
                if child.resizing:
                    child.resizing ^= 1
                    child.direction = NONE
                    child.handler.pivot.active = False
                    self.emit("finalize", child)

        self.pick = False
        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW))

        self.updated = False
        self.update()
        self.stop_cursor_change = False
        return True

    def motion(self, widget, event):
        """
        This code is executed when move the mouse pointer
        """
        self.statics.motion += 1
        #self.consume(gtk.gdk.MOTION_NOTIFY, event.state)
        self.disconnect(self.motion_id)
        if self.horizontal_ruler:
            self.horizontal_ruler.motion(self.horizontal_ruler, event, True)
        if self.vertical_ruler:
            self.vertical_ruler.motion(self.vertical_ruler, event, True)
        x = event.x / self.zoom
        y = event.y / self.zoom

        if not self.stop_cursor_change:
            def get_direction_for_child_at_position(x, y, children):
                for child in children:
                    if child.selected and child.handler.at_position(x, y):
                        direction = child.handler.get_direction(x, y)
                        widget.bin_window.set_cursor(child.get_cursor(direction))
                        return direction
                return NONE

            direction = get_direction_for_child_at_position(x, y, self.document.pages[0].children)

            if direction == NONE:
                if self.pick:
                    widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.PENCIL))
                else:
                    widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW))

        if self.selection.active:
            self.selection.width = x - self.selection.x
            self.selection.height = y - self.selection.y
            self.updated = False
            self.update() # XXX
        elif event.state & gtk.gdk.BUTTON1_MASK:
            for child in self.document.pages[0].children: # TODO
                if child.selected:
                    target = Point()
                    if child.resizing:
                        target.x = self.grid.nearest(x)
                        target.y = self.grid.nearest(y)
                        target = self.guides.nearest(target)
                        if child.direction < ANONIMOUS:
                            child.resize(target.x, target.y)
                        else:
                            child.transform(target.x, target.y)
                    else:
                        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
                        target.x = self.grid.nearest(x - child.offset.x)
                        target.y = self.grid.nearest(y - child.offset.y)
                        target = self.guides.nearest(target)
                        # XXX-TEST
                        if self.is_testing:
                            def magnetize(target, children):
                                for child in children:
                                    if not child.selected and child.magnetos.is_magnetized(target):
                                        return child.magnetos.get_magnetized(target)
                                return target

                            target = magnetize(target, self.document.pages[0].children)
                        # XXX-TEST
                        child.move(target.x, target.y)
                    self.emit("edit-child", child)
                    self.update()
        self.motion_id = self.connect("motion-notify-event", self.motion)
        return True

    def press(self, widget, event):
        """
        This code is executed when you press the mouse button
        """
        self.emit("focus", gtk.DIR_TAB_FORWARD)

        x = event.x / self.zoom
        y = event.y / self.zoom

        def start_resize(child):
            self.unselect_all()
            child.selected = True
            child.resizing = True
            if child.direction < ANONIMOUS:
                control = child.handler.control[opposite(child.direction)]
                child.pivot.x = self.grid.nearest(control.x)
                child.pivot.y = self.grid.nearest(control.y)
                child.pivot = self.guides.nearest(child.pivot)
                child.handler.pivot.x = control.x
                child.handler.pivot.y = control.y
                child.handler.pivot.active = True

        if self.pick:
            self.unselect_all()
            #x, y = self.get_pointer()
            target = Point()
            child = self.child
            self.add(child)
            child.selected = True
            target.x = self.grid.nearest(x)
            target.y = self.grid.nearest(y)
            target = self.guides.nearest(target)
            child.x = target.x
            child.y = target.y
            child.width = 0
            child.height = 0
            child.direction = SOUTHEAST
            child.handler.control[opposite(child.direction)].y = child.y
            child.handler.control[opposite(child.direction)].x = child.x
            start_resize(child)
            widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.BOTTOM_RIGHT_CORNER))
            self.emit("select", child)
            return True

        selection = True

        def start_move(child, x, y):
            child.offset.x = x - child.x
            child.offset.y = y - child.y
            child.press(x, y)

        def select(child):
            if not event.state & gtk.gdk.CONTROL_MASK:
                self.unselect_all()
            child.selected = True

        for child in sorted(self.document.pages[0].children, key=lambda child: child.z):
            if child.selected:
                if child.handler.at_position(x, y):
                    child.direction = child.handler.get_direction(x, y)
                    selection = False
                    start_resize(child)
                elif child.at_position(x, y):
                    #start_move(child, x, y)
                    start_move(child, x, y)
                    selection = False
                else:
                    continue
            elif child.at_position(x, y):
                selection = False
                select(child)
                start_move(child, x, y)
            else:
                continue

        if selection:
            self.selection.x = x
            self.selection.y = y
            self.selection.width = 0
            self.selection.height = 0
            self.selection.active = True
            widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))
        else:
            self.stop_cursor_change = True
            #self.updated = False
        self.update() # XXX

        return True

    def expose(self, widget, event):
        self.statics.expose += 1
        self.disconnect(self.expose_id)
        context = widget.bin_window.cairo_create()
        context.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        context.clip()
        context.scale(self.zoom, self.zoom)
        self.total.width = int(self.document.pages[0].width * self.zoom + 2 * self.border)
        self.total.height = int(
            len(self.document.pages) * self.document.pages[0].height * self.zoom +
            (len(self.document.pages) + 1) * self.border)
        self.set_size_request(self.total.width, self.total.height)
        context.set_source_rgb(0.55, 0.55, 0.55) #background
        context.paint()

        page = self.document.pages[0]

        self.document.draw(context, self.border, self.zoom, self.hints)

        self.origin.x = page.x + page.left # + self.border
        self.origin.y = page.y + page.top # + self.border

        if self.grid.active:
            self.grid.x = self.origin.x
            self.grid.y = self.origin.y
            self.grid.width = page.width - page.left - page.right
            self.grid.height = page.height - page.top - page.bottom
            self.grid.draw(context)

        if self.guides.active:
            self.guides.x = self.origin.x
            self.guides.y = self.origin.y
            self.guides.width = page.width - page.left - page.right
            self.guides.height = page.height - page.top - page.bottom
            self.guides.draw(context)

        if self.selection.active:
            self.selection.draw(context)
        self.updated = True
        self.expose_id = self.connect("expose-event", self.expose)
        return True

    add = lambda self, child: self.document.pages[0].children.append(child)

    #update = lambda self: self.queue_draw()
    def update(self):
        if not self.updated:
            pass
        self.queue_draw()


class ExtendedCanvas(CanvasImplementation):
    """This class represents a high level canvas implementation"""

    #    def initialize(self):
    #        Canvas.initialize(self)
    def __init__(self, application):
        CanvasImplementation.__init__(self, application)

    def add_page(self):
        page = self.document.pages[0] #Page()
        self.document.pages.append(page)
        self.queue_draw()

    def set_scale_absolute(self, scale):
        self.zoom = scale
        self.queue_draw()

    def set_scale_factor(self, factor):
        self.zoom += factor
        if self.zoom < 0.05:
            self.zoom = 0.05
        self.queue_draw()

    zoom_out = lambda self, factor=-0.05: self.set_scale_factor(factor)

    zoom_in = lambda self, factor=0.05: self.set_scale_factor(factor)

    zoom_normal = lambda self: self.set_scale_absolute(1.0)

    def create(self, child):
        self.stop_cursor_change = False
        self.pick = True
        self.child = child
        child.z = len(self.document.pages[0].children)
        #child.connect("changed", self.update, child)

    def cut(self, *args):
        self.copy()
        self.delete()

    def copy(self, *args):
        self.clipboard = '<clipboard>'
        for child in self.document.pages[0].children:
            if child.selected:
                self.clipboard += child.serialize()
        self.clipboard += '</clipboard>'

    def paste(self, *args):
        self.unselect_all(False)
        self.unserialize(self.clipboard, True)
        #self.select_last()
        # Select last

    def delete(self, *args):
        restart = True # i don't remember why use this
        while restart:
            restart = False
            for child in self.document.pages[0].children:
                if child.selected:
                    child.delete()
                    restart = True
                    break
        self.update()

    def select_all(self, *args):
        for child in self.document.pages[0].children:
            child.selected = True
        self.queue_draw()

    def unselect_all(self, update=True, *args):
        for child in self.document.pages[0].children:
            child.selected = False
        if update:
            self.update()

    #def select_last(self, *args):
    #    self.document.pages[0].children[len(self.document.pages[0].children) - 1].selected = True
    #    self.update()

    def bring_to_back(self, *args):
        for child in self.document.pages[0].children:
            if child.selected:
                child.z -= 1
            else:
                child.z += 1
        self.update()

    def bring_to_front(self, *args):
        for child in self.document.pages[0].children:
            if child.selected:
                child.z += 1
            else:
                child.z -= 1
        self.update()

    def remove_split(self, *args):
        for child in self.document.pages[0].children:
            if child.selected and child.__name__ == 'Box':
                child.remove_separator()
        self.update()

    def split_vertically(self, *args):
        for child in self.document.pages[0].children:
            if child.selected and child.__name__ == 'Box':
                child.add_separator_vertical(child.width / 2)
        self.update()

    def split_horizontally(self, *args):
        for child in self.document.pages[0].children:
            if child.selected and child.__name__ == 'Box':
                child.add_separator_horizontal(child.height / 2)
        self.update()

    def paper_center_horizontal(self, *args):
        for child in self.document.pages[0].children:
            if child.selected:
                child.x = int((self.document.pages[0].width - child.width) / 2 - self.border)
        self.update()

    def get_first_page(self):
        return self.document.pages[0]

    def draw_children(self, page, context): # XXX
        for child in page.children:
            selected = child.selected
            child.selected = False
            child.x += page.left
            child.y += page.top
            child.draw(context)
            child.x -= page.left
            child.y -= page.top
            child.selected = selected

    def toggle_snap(self, *args):
        self.grid.snap ^= 1

    def toggle_grid(self, *args):
        self.grid.active ^= 1
        self.update()

    def toggle_guides(self, *args):
        self.guides.active ^= 1
        self.update()

    def toggle_margins(self, *args):
        for page in self.document.pages:
            page.active ^= 1
        self.update()

    def toggle_hints(self, *args):
        self.hints ^= 1
        self.update()

    def get_filename(self, filename, extension):
        if not filename.endswith("." + extension):
            return filename + "." + extension
        else:
            return filename

    def save_to_pdf(self, filename):
        filename = self.get_filename(filename, "pdf")
        for i, page in enumerate(self.document.pages):
            surface = cairo.PDFSurface(filename, page.width, page.height)
            context = cairo.Context(surface)
            self.draw_children(page, context)
            #context.show_page()
            surface.flush()

    def save_to_png(self, filename):
        filename = self.get_filename(filename, "png")
        # TODO: Multiple pages
        page = self.get_first_page()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, page.width, page.height)
        context = cairo.Context(surface)
        self.draw_children(page, context)
        context.show_page()
        #surface.flush()

    def save_to_postscript(self, filename):
        pass # TODO

    def save_to_xml(self, filename):
        filename = self.get_filename(filename, "xml")
        document = self.serialize()
        handle = open(filename, 'w')
        handle.write(document)
        handle.close()

    def load_from_xml(self, filename):
        handle = open(filename)
        document = handle.read()
        handle.close()
        self.unserialize(document)

    def unserialize(self, document, from_clipboard=False):
        globals()["object"] = None
        globals()["depth"] = 0

        def element_start(name, attributes):
            global object, depth

            if name == "object":
                depth += 1
                type = attributes["type"]
                code = "%s()" % type
                object = eval(code)
            elif name == "property":
                attribute = attributes["name"]
                type = attributes["type"]
                value = attributes["value"]
                object.set_property(attribute, value, type)

        def element_end(name):
            global depth

            if name == "object":
                if from_clipboard:
                    self.add(object)
                    object.x += 10
                    object.y += 10
                    object.selected = True
                else:
                    depth -= 1
                    if  depth == 0:
                        self.add(object)

        #def element_body(data):
        #  print "data:", repr(data)

        parser = xml.parsers.expat.ParserCreate()

        parser.StartElementHandler = element_start
        parser.EndElementHandler = element_end
        #parser.CharacterDataHandler = element_body

        parser.Parse(document, 1)

        self.update()

    def serialize(self):
        string = self.document.serialize()
        node = xml.dom.minidom.parseString(string)
        return node.toprettyxml(indent='    ', newl="\n", encoding="utf-8")

@singleton
class ProductionCanvas(ExtendedCanvas):
    """This class represents a production canvas"""

    def __init__(self, application):
        ExtendedCanvas.__init__(self, application)

@singleton
class TestingCanvas(ExtendedCanvas):
    """This class represents a testing canvas"""

    #    def initialize(self):
    #        ExtendedCanvas.initialize(self)
    def __init__(self, application):
        ExtendedCanvas.__init__(self, application)
        self.is_testing = True
        print _("WARNING: You are using a testing canvas.")

Canvas = TestingCanvas if "--testing" in sys.argv else ProductionCanvas
