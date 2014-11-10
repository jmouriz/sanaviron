#!/usr/bin/python
#!/usr/bin/python
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from gi.repository import GObject

class LayerSelector(Gtk.HBox):
    def __init__(self):
        GObject.GObject.__init__(self)

        self.set_spacing(6)

        label = Gtk.Label(label=_("Layer:"))
        self.add(label)

        alignment = Gtk.Alignment.new(0.0, 0.5, 0.0, 0.0)
        self.add(alignment)
        entry = Gtk.ComboBoxText()
        #entry.connect("changed", self.changed_barcode_type)
        alignment.add(entry)

        entry.append_text(_("All"))
        entry.append_text(_("layer-1"))
        entry.append_text(_("layer-2"))
        entry.append_text(_("layer-3"))
        entry.append_text(_("layer-4"))

        entry.set_active(0)

if __name__ == '__main__':
    def quit(widget, event):
        Gtk.main_quit()
        return True

    window = Gtk.Window()
    window.set_title(_("Layer selector"))
    window.connect("delete-event", quit)
    entry = LayerSelector()
    window.add(entry)
    window.show_all()
    Gtk.main()
