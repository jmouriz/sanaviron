#!/usr/bin/python
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from gi.repository import GObject

class Climber(Gtk.HBox):
    """This class represents a zoom toolset"""

    def __init__(self, canvas):
        GObject.GObject.__init__(self)

        self.canvas = canvas

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        self.add(button)

        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_ZOOM_OUT, Gtk.IconSize.MENU)
        button.connect("clicked", self.zoom_out)
        button.add(image)

        self.button = Gtk.Button('1.00 (100%)')
        self.button.set_relief(Gtk.ReliefStyle.NONE)
        #self.button.connect("clicked", self.custom_zoom)
        self.add(self.button)

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        self.add(button)

        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_ZOOM_IN, Gtk.IconSize.MENU)
        button.connect("clicked", self.zoom_in)
        button.add(image)

        separator = Gtk.VSeparator()
        self.add(separator)

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        self.add(button)

        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_ZOOM_FIT, Gtk.IconSize.MENU)
        #button.connect("clicked", self.zoom_fit)
        button.add(image)

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        self.add(button)

        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_ZOOM_100, Gtk.IconSize.MENU)
        button.connect("clicked", self.zoom_normal)
        button.add(image)

    def update(self):
        label = "%0.02f (%d%%)" % (self.canvas.zoom, self.canvas.zoom * 100)
        self.button.set_label(label)

    def zoom_out(self, widget):
        self.canvas.zoom_out()
        self.update()

    def zoom_in(self, widget):
        self.canvas.zoom_in()
        self.update()

    def zoom_normal(self, widget):
        self.canvas.zoom_normal()
        self.update()

if __name__ == '__main__':
    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    climber = Climber()
    window.add(climber)
    window.show_all()
    Gtk.main()
