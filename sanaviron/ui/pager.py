#!/usr/bin/python
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from gi.repository import GObject

class Pager(Gtk.HBox):
    """This class represents a pager"""

    def __init__(self, canvas):
        GObject.GObject.__init__(self)

        self.canvas = canvas

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        self.add(button)

        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_GOTO_FIRST, Gtk.IconSize.MENU)
        #button.connect("clicked", self.callback)
        button.add(image)

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        self.add(button)

        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_GO_BACK, Gtk.IconSize.MENU)
        #button.connect("clicked", self.callback)
        button.add(image)

        self.button = Gtk.Button()
        self.button.set_relief(Gtk.ReliefStyle.NONE)
        self.add(self.button)

        self.update()

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        self.add(button)

        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_GO_FORWARD, Gtk.IconSize.MENU)
        #button.connect("clicked", self.callback)
        button.add(image)

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        self.add(button)

        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_GOTO_LAST, Gtk.IconSize.MENU)
        #button.connect("clicked", self.callback)
        button.add(image)

        separator = Gtk.VSeparator()
        self.add(separator)

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        self.add(button)

        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_NEW, Gtk.IconSize.MENU)
        button.connect("clicked", self.add_page)
        button.add(image)

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        self.add(button)

        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_DELETE, Gtk.IconSize.MENU)
        #button.connect("clicked", self.callback)
        button.add(image)

    def update(self):
        pages = len(self.canvas.document.pages)
        caption = _("Page %(page)s of %(pages)s") % {"page": 1, "pages": pages}
        self.button.set_label(caption)

    def add_page(self, widget):
        self.canvas.add_page()
        self.update()

if __name__ == '__main__':
    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    pager = Pager()
    window.add(pager)
    window.show_all()
    Gtk.main()
