#!/usr/bin/python
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from gi.repository import GObject

from interfaces.signalizable import Signalizable

class MenuBar(Gtk.MenuBar, Signalizable):
    """This class represents a pull-down menu bar"""

    def __init__(self, application):
        GObject.GObject.__init__(self)
        Signalizable.__init__(self)

        #from ui.application import Application
        #self.application = Application()
        self.application = application
        self.stack = None
        self.submenu = None

    def append_menu(self, stock, descend=False, right=False):
        menuitem = Gtk.ImageMenuItem(stock)
        if right:
            menuitem.set_right_justified(True)
        if descend:
            self.stack = self.submenu
            self.submenu.append(menuitem)
        else:
            self.append(menuitem)
        self.submenu = Gtk.Menu()
        menuitem.set_submenu(self.submenu)

    def append_item(self, stock, signal, accelerator = None):
        menuitem = Gtk.ImageMenuItem(stock)
        self.submenu.append(menuitem)
        menuitem.connect("activate", self.activate, signal)
        self.install_signal(signal)
        if accelerator:
            key, mask = Gtk.accelerator_parse(accelerator)
            menuitem.add_accelerator("activate", self.application.bindings, key, mask, Gtk.AccelFlags.VISIBLE)

    def append_toggle(self, stock, signal, accelerator = None, toggled = True):
        info = Gtk.stock_lookup(stock)
        label = info.label if info else stock
        menuitem = Gtk.CheckMenuItem(label)
        menuitem.set_active(toggled)
        self.submenu.append(menuitem)
        menuitem.connect("toggled", self.activate, signal)
        self.install_signal(signal)
        if accelerator:
            key, mask = Gtk.accelerator_parse(accelerator)
            menuitem.add_accelerator("toggled", self.application.bindings, key, mask, Gtk.AccelFlags.VISIBLE)

    def append_separator(self):
        separator = Gtk.SeparatorMenuItem()
        self.submenu.append(separator)

    def ascend(self):
        self.submenu = self.stack

    def activate(self, widget, data):
        self.emit(data, None)
