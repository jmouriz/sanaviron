#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import sys

from objects import HORIZONTAL, VERTICAL
from ui.notification import Notification
from ui.stock import EXPAND_PROPERTIES, CONTRACT_PROPERTIES
from ui.properties import Properties
from ui.climber import Climber
from ui.pager import Pager
from ui.ruler import HorizontalRuler, VerticalRuler
from ui.layerselector import LayerSelector
from ui import *

class Editor(gtk.HPaned):
    """This class represents the main editor"""

    def __init__(self, application):
        gtk.HPaned.__init__(self)
        from ui.canvas import Canvas
        self.canvas = Canvas(application)
        self.properties = Properties(application)

        self.canvas.connect("select", self.select)
        self.canvas.connect("finalize", self.finalize)
        self.canvas.connect("edit-child", self.edit_child)
        self.canvas.connect("scroll-event", self.wheel)

        box = gtk.VBox()

        self.notification = Notification()

        code_editor = None

        if '--source-editor-test' in sys.argv:
            while True:
                try:
                    from ui.code_editor import CodeEditor
                except:
                    self.notification.notificate(_("No module GtkSourceView installed"), ERROR)
                    self.pack1(box, True, False)
                    break

                panel = gtk.VPaned()
                panel.pack1(box, True, False)
                code_editor = CodeEditor(application)
                code_editor.editor.set_language("sql")
                panel.pack2(code_editor, False, True)
                self.pack1(panel, True, False)
                break
        else:
            self.pack1(box, True, False)

        self.pack2(self.properties, False, True)

        top = gtk.HBox()
        box.pack_start(top, False, False)

        top.pack_start(self.notification, False, False)

        layer_selector = LayerSelector()
        alignment = gtk.Alignment(1.0, 0.5)
        alignment.add(layer_selector)
        top.pack_start(alignment, True, True)

        separator = gtk.VSeparator()
        top.pack_start(separator, False, False)

        self.image = gtk.Image()
        self.image.set_from_stock(CONTRACT_PROPERTIES, gtk.ICON_SIZE_MENU)
        button = gtk.Button()
        button.set_image(self.image)
        button.set_relief(gtk.RELIEF_NONE)
        button.connect("clicked", self.toggle_properties)
        top.pack_start(button, False, False)

        table = gtk.Table()
        box.add(table)

        bottom = gtk.HBox()
        box.pack_start(bottom, False, False)

        self.climber = Climber(self.canvas)
        bottom.pack_start(self.climber, False, False)

        pager = Pager(self.canvas)
        alignment = gtk.Alignment(1.0, 0.5)
        alignment.add(pager)
        bottom.pack_start(alignment, True, True)

        self.horizontal_ruler = HorizontalRuler()
        self.horizontal_ruler.connect("append-tag", self.append_tag)
        self.horizontal_ruler.connect("move-tag", self.move_tag)
        table.attach(self.horizontal_ruler, 1, 2, 0, 1, gtk.FILL | gtk.EXPAND, 0)

        self.vertical_ruler = VerticalRuler()
        self.vertical_ruler.connect("append-tag", self.append_tag)
        self.vertical_ruler.connect("move-tag", self.move_tag)
        table.attach(self.vertical_ruler, 0, 1, 1, 2, 0, gtk.FILL | gtk.EXPAND)

        area = gtk.ScrolledWindow()
        area.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        adjustment = area.get_vadjustment()
        adjustment.connect("value-changed", self.scroll, VERTICAL)
        adjustment = area.get_hadjustment()
        adjustment.connect("value-changed", self.scroll, HORIZONTAL)
        table.attach(area, 1, 2, 1, 2, gtk.FILL | gtk.EXPAND, gtk.FILL | gtk.EXPAND)

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
            self.image.set_from_stock(EXPAND_PROPERTIES, gtk.ICON_SIZE_MENU)
            properties.hide()
        else:
            self.image.set_from_stock(CONTRACT_PROPERTIES, gtk.ICON_SIZE_MENU)
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
        #print "edit", child

    def wheel(self, widget, event):
        if event.state & gtk.gdk.CONTROL_MASK:
            if event.direction == gtk.gdk.SCROLL_UP:
                self.canvas.zoom_in()
                self.climber.update()
            elif event.direction == gtk.gdk.SCROLL_DOWN:
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
        #print "Selected object \"%s\"" % child.__name__
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
            #print "putting text \"%s\"" % text
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
