#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk

from interfaces.signalizable import Signalizable

class MenuBar(gtk.MenuBar, Signalizable):
    """This class represents a pull-down menu bar"""

    def __init__(self, application):
        gtk.MenuBar.__init__(self)
        Signalizable.__init__(self)

        #from ui.application import Application
        #self.application = Application()
        self.application = application
        self.stack = None
        self.submenu = None

    def append_menu(self, stock, descend=False, right=False):
        menuitem = gtk.ImageMenuItem(stock)
        if right:
            menuitem.set_right_justified(True)
        if descend:
            self.stack = self.submenu
            self.submenu.append(menuitem)
        else:
            self.append(menuitem)
        self.submenu = gtk.Menu()
        menuitem.set_submenu(self.submenu)

    def append_item(self, stock, signal, accelerator = None):
        menuitem = gtk.ImageMenuItem(stock)
        self.submenu.append(menuitem)
        menuitem.connect("activate", self.activate, signal)
        self.install_signal(signal)
        if accelerator:
            key, mask = gtk.accelerator_parse(accelerator)
            menuitem.add_accelerator("activate", self.application.bindings, key, mask, gtk.ACCEL_VISIBLE)

    def append_toggle(self, stock, signal, accelerator = None, toggled = True):
        info = gtk.stock_lookup(stock)
        label = info[1] if info else stock
        menuitem = gtk.CheckMenuItem(label)
        menuitem.set_active(toggled)
        self.submenu.append(menuitem)
        menuitem.connect("toggled", self.activate, signal)
        self.install_signal(signal)
        if accelerator:
            key, mask = gtk.accelerator_parse(accelerator)
            menuitem.add_accelerator("toggled", self.application.bindings, key, mask, gtk.ACCEL_VISIBLE)

    def append_separator(self):
        separator = gtk.SeparatorMenuItem()
        self.submenu.append(separator)

    def ascend(self):
        self.submenu = self.stack

    def activate(self, widget, data):
        self.emit(data, None)
