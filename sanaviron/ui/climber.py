#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk

class Climber(gtk.HBox):
    """This class represents a zoom toolset"""

    def __init__(self, canvas):
        gtk.HBox.__init__(self)

        self.canvas = canvas

        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)
        self.add(button)

        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_ZOOM_OUT, gtk.ICON_SIZE_MENU)
        button.connect("clicked", self.zoom_out)
        button.add(image)

        self.button = gtk.Button('1.00 (100%)')
        self.button.set_relief(gtk.RELIEF_NONE)
        #self.button.connect("clicked", self.custom_zoom)
        self.add(self.button)

        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)
        self.add(button)

        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_ZOOM_IN, gtk.ICON_SIZE_MENU)
        button.connect("clicked", self.zoom_in)
        button.add(image)

        separator = gtk.VSeparator()
        self.add(separator)

        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)
        self.add(button)

        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_ZOOM_FIT, gtk.ICON_SIZE_MENU)
        #button.connect("clicked", self.zoom_fit)
        button.add(image)

        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)
        self.add(button)

        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_ZOOM_100, gtk.ICON_SIZE_MENU)
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
    window = gtk.Window()
    window.connect("delete-event", gtk.main_quit)
    climber = Climber()
    window.add(climber)
    window.show_all()
    gtk.main()
