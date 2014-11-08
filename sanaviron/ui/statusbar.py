#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk

class Statusbar(gtk.Statusbar):
    """This class represents a status bar"""

    def __init__(self):
        gtk.Statusbar.__init__(self)

if __name__ == '__main__':
    def quit(widget, event):
        gtk.main_quit()
        return True

    window = gtk.Window()
    window.set_title("status bar")
    window.connect("delete-event", quit)
    status = Statusbar()
    window.add(status)
    window.show_all()
    gtk.main()

