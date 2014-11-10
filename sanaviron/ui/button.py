#!/usr/bin/python
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from gi.repository import GObject

class Button(Gtk.VBox):
    """This class represents a expandable/collapsible button"""

    def __init__(self, title):
        GObject.GObject.__init__(self)

        self.expanded = True

        box = Gtk.HBox()
        box.set_spacing(6)
        self.image = Gtk.Image()
        box.pack_start(self.image, False, False, 0)
        self.image.set_from_stock(Gtk.STOCK_GO_DOWN, Gtk.IconSize.MENU)
        label = Gtk.Label(label="")
        label.set_markup("<b>%s</b>" % title)
        label.set_alignment(0.0, 0.5)
        box.add(label)
        button = Gtk.Button()
        button.add(box)
        #button.set_relief(Gtk.ReliefStyle.NONE)
        button.connect("clicked", self.clicked)
        self.pack_start(button, False, False, 0)

    def clicked(self, widget):
        self.expanded ^= 1
        if self.expanded:
            self.image.set_from_stock(Gtk.STOCK_GO_DOWN, Gtk.IconSize.MENU)
            self.get_children()[1].show()
        else:
            self.image.set_from_stock(Gtk.STOCK_GO_FORWARD, Gtk.IconSize.MENU)
            self.get_children()[1].hide()

if __name__ == '__main__':
    def quit(widget, event):
        Gtk.main_quit()
        return True

    window = Gtk.Window()
    window.set_title(_("Expander button"))
    window.connect("delete-event", quit)

    box = Gtk.VBox()
    window.add(box)

    button = Button(_("Document properties"))
    box.pack_start(button, False, False, 0)

    table = Gtk.Table()
    table.set_border_width(12)
    table.set_row_spacings(4)
    table.set_col_spacings(4)
    button.add(table)

    label = Gtk.Label(label=_("Top margin:"))
    label.set_alignment(0.0, 0.5)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 0, 1, Gtk.AttachOptions.FILL, 0)
    table.attach(alignment, 1, 2, 0, 1, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    label = Gtk.Label(label=_("Bottom margin:"))
    label.set_alignment(0.0, 0.5)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 1, 2, Gtk.AttachOptions.FILL, 0)
    table.attach(alignment, 1, 2, 1, 2, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    label = Gtk.Label(label=_("Left margin:"))
    label.set_alignment(0.0, 0.5)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 2, 3, Gtk.AttachOptions.FILL, 0)
    table.attach(alignment, 1, 2, 2, 3, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    label = Gtk.Label(label=_("Right margin:"))
    label.set_alignment(0.0, 0.5)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 3, 4, Gtk.AttachOptions.FILL, 0)
    table.attach(alignment, 1, 2, 3, 4, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    label = Gtk.Label(label=_("Grid size:"))
    label.set_alignment(0.0, 0.5)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 4, 5, Gtk.AttachOptions.FILL, 0)
    table.attach(alignment, 1, 2, 4, 5, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    label = Gtk.Label(label=_("Guides size:"))
    table.attach(label, 0, 1, 5, 6, Gtk.AttachOptions.FILL, 0)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.SpinButton()
    alignment.add(entry)
    table.attach(alignment, 1, 2, 5, 6, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    button = Gtk.CheckButton(_("Show margins"))
    label.set_alignment(0.0, 0.5)
    table.attach(button, 0, 2, 6, 7, Gtk.AttachOptions.FILL, 0)

    button = Gtk.CheckButton(_("Show guides"))
    table.attach(button, 0, 2, 7, 8, Gtk.AttachOptions.FILL, 0)

    button = Gtk.CheckButton(_("Show grid"))
    table.attach(button, 0, 2, 8, 9, Gtk.AttachOptions.FILL, 0)

    button = Gtk.CheckButton(_("Enable snap")) # Magnetic grid
    table.attach(button, 0, 2, 9, 10, Gtk.AttachOptions.FILL, 0)

    #--------------------------------
    button = Button(_("Object properties"))
    box.pack_start(button, False, False, 0)

    table = Gtk.Table()
    table.set_border_width(12)
    table.set_row_spacings(4)
    table.set_col_spacings(4)
    button.add(table)

    label = Gtk.Label(label="X:")
    label.set_alignment(0.0, 0.5)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 0, 1, Gtk.AttachOptions.FILL, 0)
    table.attach(alignment, 1, 2, 0, 1, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    label = Gtk.Label(label="Y:")
    label.set_alignment(0.0, 0.5)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 1, 2, Gtk.AttachOptions.FILL, 0)
    table.attach(alignment, 1, 2, 1, 2, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    label = Gtk.Label(label=_("Width:"))
    label.set_alignment(0.0, 0.5)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 2, 3, Gtk.AttachOptions.FILL, 0)
    table.attach(alignment, 1, 2, 2, 3, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    label = Gtk.Label(label=_("Height:"))
    label.set_alignment(0.0, 0.5)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 3, 4, Gtk.AttachOptions.FILL, 0)
    table.attach(alignment, 1, 2, 3, 4, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    label = Gtk.Label(label=_("Border color:"))
    label.set_alignment(0.0, 0.5)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.ColorButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 4, 5, Gtk.AttachOptions.FILL, 0)
    table.attach(alignment, 1, 2, 4, 5, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    label = Gtk.Label(label=_("Fill color:"))
    label.set_alignment(0.0, 0.5)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.ColorButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 5, 6, Gtk.AttachOptions.FILL, 0)
    table.attach(alignment, 1, 2, 5, 6, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    label = Gtk.Label(label=_("Text:"))
    label.set_alignment(0.0, 0.5)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.Entry()
    alignment.add(entry)
    table.attach(label, 0, 1, 6, 7, Gtk.AttachOptions.FILL, 0)
    table.attach(alignment, 1, 2, 6, 7, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    label = Gtk.Label(label=_("Font:"))
    label.set_alignment(0.0, 0.5)
    alignment = Gtk.Alignment.new(0.0, 0.5)
    entry = Gtk.FontButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 7, 8, Gtk.AttachOptions.FILL, 0)
    table.attach(alignment, 1, 2, 7, 8, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0)

    window.show_all()
    Gtk.main()
