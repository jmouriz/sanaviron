#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk

from interfaces.signalizable import Signalizable
from objects import HORIZONTAL, VERTICAL

class Toolbar(gtk.Toolbar, Signalizable):
    """This class represents a toolbar"""

    def __init__(self, orientation=VERTICAL):
        gtk.Toolbar.__init__(self)
        Signalizable.__init__(self)
        #self.connect("realize", self.realize)

        if orientation == HORIZONTAL:
            self.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        elif orientation == VERTICAL:
            self.set_orientation(gtk.ORIENTATION_VERTICAL)

        self.set_style(gtk.TOOLBAR_BOTH_HORIZ)
        self.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)

        self.position = 0
        self.submenu = None
        self.signals = list()

    def append(self, stock, signal):
        button = gtk.ToolButton(stock)
        self.insert(button, self.position)
        button.connect("clicked", self.clicked, signal)
        self.install_signal(signal)
        self.position += 1

    def append_toggle(self, stock, signal):
        button = gtk.ToggleToolButton(stock)
        button.set_active(True)
        self.insert(button, self.position)
        button.connect("clicked", self.clicked, signal)
        self.install_signal(signal)
        self.position += 1

    def append_separator(self):
        separator = gtk.SeparatorToolItem()
        self.insert(separator, self.position)
        self.position += 1

    def append_with_submenu(self, stock, signal=None):
        button = gtk.MenuToolButton(stock)
        self.insert(button, self.position)
        if signal:
            self.install_signal(signal)
            button.connect("clicked", self.clicked, signal)
        self.submenu = gtk.Menu()
        button.set_menu(self.submenu)
        self.position += 1

    def append_to_submenu(self, stock, signal):
        menuitem = gtk.ImageMenuItem(stock)
        self.submenu.append(menuitem)
        menuitem.connect("activate", self.clicked, signal)
        self.install_signal(signal)
        self.submenu.show_all()

    def clicked(self, widget, data):
        self.emit(data, None)
