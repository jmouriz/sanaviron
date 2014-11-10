#!/usr/bin/python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
from gi.repository import GObject

from objects import HORIZONTAL, VERTICAL

from interfaces.signalizable import Signalizable

class Toolbar(Gtk.Toolbar, Signalizable):
    """This class represents a toolbar"""

    def __init__(self, orientation=VERTICAL):
        GObject.GObject.__init__(self)
        Signalizable.__init__(self)
        #self.connect("realize", self.realize)

        if orientation == HORIZONTAL:
            self.set_orientation(Gtk.Orientation.HORIZONTAL)
        elif orientation == VERTICAL:
            self.set_orientation(Gtk.Orientation.VERTICAL)

        self.set_style(Gtk.ToolbarStyle.BOTH_HORIZ)
        self.set_icon_size(Gtk.IconSize.SMALL_TOOLBAR)

        self.position = 0
        self.submenu = None
        self.signals = list()

    def append(self, stock, signal):
        button = Gtk.ToolButton(stock)
        self.insert(button, self.position)
        button.connect("clicked", self.clicked, signal)
        self.install_signal(signal)
        self.position += 1

    def append_toggle(self, stock, signal):
        button = Gtk.ToggleToolButton(stock)
        button.set_active(True)
        self.insert(button, self.position)
        button.connect("clicked", self.clicked, signal)
        self.install_signal(signal)
        self.position += 1

    def append_separator(self):
        separator = Gtk.SeparatorToolItem()
        self.insert(separator, self.position)
        self.position += 1

    def append_with_submenu(self, stock, signal=None):
        button = Gtk.MenuToolButton(stock)
        self.insert(button, self.position)
        if signal:
            self.install_signal(signal)
            button.connect("clicked", self.clicked, signal)
        self.submenu = Gtk.Menu()
        button.set_menu(self.submenu)
        self.position += 1

    def append_to_submenu(self, stock, signal):
        menuitem = Gtk.ImageMenuItem(stock)
        self.submenu.append(menuitem)
        menuitem.connect("activate", self.clicked, signal)
        self.install_signal(signal)
        self.submenu.show_all()

    def clicked(self, widget, data):
        self.emit(data, None)
