#!/usr/bin/python
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from gi.repository import GObject

from .__init__ import *

class Notification(Gtk.HBox):
    """This class represents a notification bar"""

    def __init__(self):
        GObject.GObject.__init__(self)
        self.set_spacing(3)
        #self.set_border_width(6)

        self.image = Gtk.Image()
        self.image.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.MENU)
        self.image.set_alignment(1.0, 0.5)
        self.image.set_padding(6, 0)
        self.pack_start(self.image, False, False, 0)

        self.label = Gtk.Label(label="")
        self.label.set_markup(_("Press <i><b>F1</b></i> to get help."))
        self.label.set_alignment(0.0, 0.5)
        self.pack_start(self.label, False, False, 0)

    def set_text(self, text):
        self.label.set_markup(text)

    def notificate(self, message, type):

        if type == INFORMATION:
            self.image.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.MENU)
            color = "black"
            weight = "normal"
        if type == ERROR:
            self.image.set_from_stock(Gtk.STOCK_DIALOG_ERROR, Gtk.IconSize.MENU)
            color = "red"
            weight = "heavy"
        if type == WARNING:
            self.image.set_from_stock(Gtk.STOCK_DIALOG_WARNING, Gtk.IconSize.MENU)
            color = "yellow"
            weight = "heavy"
        self.set_text('<span weight="%s" color="%s">%s</span>' % (weight, color, message))
        self.show()

if __name__ == '__main__':
    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    notification = Notification()
    window.add(notification)
    window.show_all()
    Gtk.main()
