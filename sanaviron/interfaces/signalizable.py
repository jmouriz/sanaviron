#!/usr/bin/python
# -*- coding: utf-8 -*-
import gobject

class Signalizable(gobject.GObject):
    """This class represents a GObject-like signalized object"""

    def __init__(self):
        gobject.GObject.__init__(self)

    def install_signal(self, signal):
        if not gobject.signal_lookup(signal, self.__class__):
            gobject.signal_new(signal, self.__class__, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                (gobject.TYPE_PYOBJECT,))
