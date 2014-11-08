#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk

from interfaces.signalizable import Signalizable
from objects import *

class Entry(gtk.HBox, Signalizable):
    """This class represents a entry with unit combobox"""

    def __init__(self):
        gtk.HBox.__init__(self)
        Signalizable.__init__(self)

        self.set_spacing(1)
        alignment = gtk.Alignment(0.0, 0.5)
        self.add(alignment)
        self.spin = gtk.SpinButton()
        alignment.add(self.spin)

        self.spin.set_digits(2)
        self.spin.set_increments(1.0, 10.0)
        self.spin.set_numeric(True)
        self.spin.set_wrap(False)

        alignment = gtk.Alignment(0.0, 0.5)
        self.add(alignment)
        self.entry = gtk.combo_box_new_text()
        alignment.add(self.entry)

        self.install_signal("value-changed")

    def append_unit(self, unit):
        self.entry.append_text(unit)

    def set_active(self, active):
        self.entry.set_active(active)

    def set_value(self, value):
        self.spin.set_value(value)

    def value_changed(self, widget):
        self.emit("value-changed", None)

class LinearEntry(Entry):
    """This class represents a entry for linear units"""

    def __init__(self, unit=CENTIMETERS):
        Entry.__init__(self)

        self.spin.set_range(0.0, 10000.0)
        self.append_unit(CENTIMETERS)
        self.append_unit(MILLIMETERS)
        self.append_unit(DOTS)
        self.append_unit(INCHES)

        self.set_active(0)


class AngularEntry(Entry):
    """This class represents a entry for angular units"""

    def __init__(self, unit=DEGREES):
        Entry.__init__(self)

        self.spin.set_range(0.0, 360.0)
        self.append_unit(DEGREES)
        self.append_unit(RADIANS)

        self.set_active(0)

if __name__ == '__main__':
    def quit(widget, event):
        gtk.main_quit()
        return True

    window = gtk.Window()
    window.set_title("Units entry")
    window.connect("delete-event", quit)
    entry = Entry()
    window.add(entry)
    window.show_all()
    gtk.main()
