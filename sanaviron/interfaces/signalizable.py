#!/usr/bin/python
# -*- coding: utf-8 -*-
from gi.repository import GObject

class Signalizable(GObject.GObject):
    """This class represents a GObject-like signalized object"""

    def __init__(self):
        GObject.GObject.__init__(self)

    def install_signal(self, signal):
        if not GObject.signal_lookup(signal, self.__class__):
            GObject.signal_new(signal, self.__class__, GObject.SignalFlags.RUN_LAST, None,
                (GObject.TYPE_PYOBJECT,))
