#!/usr/bin/python
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from gi.repository import GObject

class Statusbar(Gtk.Statusbar):
    """This class represents a status bar"""

    def __init__(self):
        GObject.GObject.__init__(self)

if __name__ == '__main__':
    def quit(widget, event):
        Gtk.main_quit()
        return True

    window = Gtk.Window()
    window.set_title("status bar")
    window.connect("delete-event", quit)
    status = Statusbar()
    window.add(status)
    window.show_all()
    Gtk.main()

