#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk

from ui import *

class Notification(gtk.HBox):
    """This class represents a notification bar"""

    def __init__(self):
        gtk.HBox.__init__(self)
        self.set_spacing(3)
        #self.set_border_width(6)

        self.image = gtk.Image()
        self.image.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_MENU)
        self.image.set_alignment(1.0, 0.5)
        self.image.set_padding(6, 0)
        self.pack_start(self.image, False, False)

        self.label = gtk.Label("")
        self.label.set_markup(_("Press <i><b>F1</b></i> to get help."))
        self.label.set_alignment(0.0, 0.5)
        self.pack_start(self.label, False, False)

    def set_text(self, text):
        self.label.set_markup(text)

    def notificate(self, message, type):

        if type == INFORMATION:
            self.image.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_MENU)
            color = "black"
            weight = "normal"
        if type == ERROR:
            self.image.set_from_stock(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_MENU)
            color = "red"
            weight = "heavy"
        if type == WARNING:
            self.image.set_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_MENU)
            color = "yellow"
            weight = "heavy"
        self.set_text('<span weight="%s" color="%s">%s</span>' % (weight, color, message))
        self.show()

if __name__ == '__main__':
    window = gtk.Window()
    window.connect("delete-event", gtk.main_quit)
    notification = Notification()
    window.add(notification)
    window.show_all()
    gtk.main()
