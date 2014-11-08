#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk

class Pager(gtk.HBox):
    """This class represents a pager"""

    def __init__(self, canvas):
        gtk.HBox.__init__(self)

        self.canvas = canvas

        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)
        self.add(button)

        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_GOTO_FIRST, gtk.ICON_SIZE_MENU)
        #button.connect("clicked", self.callback)
        button.add(image)

        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)
        self.add(button)

        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_GO_BACK, gtk.ICON_SIZE_MENU)
        #button.connect("clicked", self.callback)
        button.add(image)

        self.button = gtk.Button()
        self.button.set_relief(gtk.RELIEF_NONE)
        self.add(self.button)

        self.update()

        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)
        self.add(button)

        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_GO_FORWARD, gtk.ICON_SIZE_MENU)
        #button.connect("clicked", self.callback)
        button.add(image)

        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)
        self.add(button)

        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_GOTO_LAST, gtk.ICON_SIZE_MENU)
        #button.connect("clicked", self.callback)
        button.add(image)

        separator = gtk.VSeparator()
        self.add(separator)

        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)
        self.add(button)

        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_NEW, gtk.ICON_SIZE_MENU)
        button.connect("clicked", self.add_page)
        button.add(image)

        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)
        self.add(button)

        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU)
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
    window = gtk.Window()
    window.connect("delete-event", gtk.main_quit)
    pager = Pager()
    window.add(pager)
    window.show_all()
    gtk.main()
