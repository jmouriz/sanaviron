#!/usr/bin/python
#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk

class LayerSelector(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self)

        self.set_spacing(6)

        label = gtk.Label(_("Layer:"))
        self.add(label)

        alignment = gtk.Alignment(0.0, 0.5)
        self.add(alignment)
        entry = gtk.combo_box_new_text()
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
        gtk.main_quit()
        return True

    window = gtk.Window()
    window.set_title(_("Layer selector"))
    window.connect("delete-event", quit)
    entry = LayerSelector()
    window.add(entry)
    window.show_all()
    gtk.main()
