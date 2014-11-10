#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

from objects import HORIZONTAL, VERTICAL

from .__init__ import *

from .notification import Notification
from .stock import EXPAND_PROPERTIES, CONTRACT_PROPERTIES
from .properties import Properties
from .climber import Climber
from .pager import Pager
from .ruler import HorizontalRuler, VerticalRuler
from .layerselector import LayerSelector

class Editor(Gtk.HPaned):
    """This class represents the main editor"""

    def __init__(self, application):
        GObject.GObject.__init__(self)
        from .canvas import Canvas
        self.canvas = Canvas(application)
        self.properties = Properties(application)

        self.canvas.connect("select", self.select)
        self.canvas.connect("finalize", self.finalize)
        self.canvas.connect("edit-child", self.edit_child)
        self.canvas.connect("scroll-event", self.wheel)

        box = Gtk.VBox()

        self.notification = Notification()

        code_editor = None

        if '--source-editor-test' in sys.argv:
            while True:
                try:
                    from .code_editor import CodeEditor
                except:
                    self.notification.notificate(_("No module GtkSourceView installed"), ERROR)
                    self.pack1(box, True, False)
                    break

                panel = Gtk.VPaned()
                panel.pack1(box, True, False)
                code_editor = CodeEditor(application)
                code_editor.editor.set_language("sql")
                panel.pack2(code_editor, False, True)
                self.pack1(panel, True, False)
                break
        else:
            self.pack1(box, True, False)

        self.pack2(self.properties, False, True)

        top = Gtk.HBox()
        box.pack_start(top, False, False, 0)

        top.pack_start(self.notification, False, False, 0)

        layer_selector = LayerSelector()
        alignment = Gtk.Alignment.new(1.0, 0.5, 0.0, 0.0)
        alignment.add(layer_selector)
        top.pack_start(alignment, True, True, 0)

        separator = Gtk.VSeparator()
        top.pack_start(separator, False, False, 0)

        self.image = Gtk.Image()
        self.image.set_from_stock(CONTRACT_PROPERTIES, Gtk.IconSize.MENU)
        button = Gtk.Button()
        button.set_image(self.image)
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.connect("clicked", self.toggle_properties)
        top.pack_start(button, False, False, 0)

        table = Gtk.Table()
        box.add(table)

        bottom = Gtk.HBox()
        box.pack_start(bottom, False, False, 0)

        self.climber = Climber(self.canvas)
        bottom.pack_start(self.climber, False, False, 0)

        pager = Pager(self.canvas)
        alignment = Gtk.Alignment.new(1.0, 0.5, 0.0, 0.0)
        alignment.add(pager)
        bottom.pack_start(alignment, True, True, 0)

        self.horizontal_ruler = HorizontalRuler()
        self.horizontal_ruler.connect("append-tag", self.append_tag)
        self.horizontal_ruler.connect("move-tag", self.move_tag)
        table.attach(self.horizontal_ruler, 1, 2, 0, 1, Gtk.AttachOptions.FILL | Gtk.AttachOptions.EXPAND, 0)

        self.vertical_ruler = VerticalRuler()
        self.vertical_ruler.connect("append-tag", self.append_tag)
        self.vertical_ruler.connect("move-tag", self.move_tag)
        table.attach(self.vertical_ruler, 0, 1, 1, 2, 0, Gtk.AttachOptions.FILL | Gtk.AttachOptions.EXPAND)

        area = Gtk.ScrolledWindow()
        area.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        adjustment = area.get_vadjustment()
        adjustment.connect("value-changed", self.scroll, VERTICAL)
        adjustment = area.get_hadjustment()
        adjustment.connect("value-changed", self.scroll, HORIZONTAL)
        table.attach(area, 1, 2, 1, 2, Gtk.AttachOptions.FILL | Gtk.AttachOptions.EXPAND, Gtk.AttachOptions.FILL | Gtk.AttachOptions.EXPAND)

        self.canvas.code_editor = code_editor
        self.canvas.horizontal_ruler = self.horizontal_ruler
        self.canvas.vertical_ruler = self.vertical_ruler
        self.connect("realize", self.realize, area)

    def realize(self, widget, area):
        area.add_with_viewport(self.canvas)
        self.canvas.show()

    def toggle_properties(self, *args):
        properties = self.get_children()[1]
        if self.properties.get_visible():
            self.image.set_from_stock(EXPAND_PROPERTIES, Gtk.IconSize.MENU)
            properties.hide()
        else:
            self.image.set_from_stock(CONTRACT_PROPERTIES, Gtk.IconSize.MENU)
            properties.show()

    def append_tag(self, widget, tag):
        self.canvas.guides.add_tag(tag)
        self.canvas.update()

    def move_tag(self, widget, tag):
        self.canvas.queue_draw()

    def select(self, widget, child):
        self.update(child)

    def finalize(self, widget, child):
        self.update(child)

    def update(self, child):
        self.properties.select(child.__name__, child)

    def edit_child(self, widget, child):
        pass
        #print("edit", child)

    def wheel(self, widget, event):
        if event.get_state() & Gdk.ModifierType.CONTROL_MASK:
            if event.direction == Gdk.ScrollDirection.UP:
                self.canvas.zoom_in()
                self.climber.update()
            elif event.direction == Gdk.ScrollDirection.DOWN:
                self.canvas.zoom_out()
                self.climber.update()
            self.horizontal_ruler.zoom = self.canvas.zoom
            return True

    def scroll(self, adjustment, direction):
        offset = adjustment.get_value()
        if direction == VERTICAL:
            self.canvas.vertical_ruler.offset = offset
        elif direction == HORIZONTAL:
            self.canvas.horizontal_ruler.offset = offset

    def key_press(self, widget, event):
        pass

    def _select(self, widget, child, buffer):
        #print("Selected object \"%s\"" % child.__name__)
        #if child.__name__ == "Table":
        #if child.__name__ == "Text":
        #   if not child.x and not child.y:
        #     return

        #  textpad = TextPad()
        #  textpad.set_size_request(150, -1)
        #  textpad.show_all()
        #  self.canvas.put(textpad, child.x + self.canvas.origin.x, child.y + self.canvas.origin.y)
        if child.__name__ == "Text":
            text = child.get_property("text")
            #print("putting text \"%s\"" % text)
            buffer.handler_disconnect(self.disconnect_handler)
            buffer.set_text(text)
            self.disconnect_handler = buffer.connect("changed", self.changed)

    def set_paper(self):
        for page in self.canvas.document.pages:
            page.x = 25
            page.y = 25

            page.width = 800
            page.height = 1500

            page.top = 25
            page.left = 25
            page.bottom = 25
            page.right = 25

            page.active = True

            self.canvas.grid.active = True
            self.canvas.grid.size = 16 # 31 # 32

            self.canvas.guides.active = True
            self.canvas.guides.size = 16 * 8 # 128

            self.canvas.grid.snap = True
