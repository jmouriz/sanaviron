#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk

from interfaces.signalizable import Signalizable

class Options(gtk.VBox, Signalizable):
    """This class represents a multiple radio options"""

    def __init__(self):
        gtk.VBox.__init__(self)
        Signalizable.__init__(self)

        self.options = list()

        self.install_signal("selected")

    def add_option(self, caption):
        count = len(self.options)
        if count:
            last = self.options[count - 1]
        else:
            last = None
        option = gtk.RadioButton(last, caption)
        option.connect("toggled", self.selected, count)
        self.options.append(option)
        self.add(option)

    def selected(self, widget, data):
        self.emit("selected", data)
