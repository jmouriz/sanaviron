#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk

class Button(gtk.VBox):
    """This class represents a expandable/collapsible button"""

    def __init__(self, title):
        gtk.VBox.__init__(self)

        self.expanded = True

        box = gtk.HBox()
        box.set_spacing(6)
        self.image = gtk.Image()
        box.pack_start(self.image, False, False)
        self.image.set_from_stock(gtk.STOCK_GO_DOWN, gtk.ICON_SIZE_MENU)
        label = gtk.Label("")
        label.set_markup("<b>%s</b>" % title)
        label.set_alignment(0.0, 0.5)
        box.add(label)
        button = gtk.Button()
        button.add(box)
        #button.set_relief(gtk.RELIEF_NONE)
        button.connect("clicked", self.clicked)
        self.pack_start(button, False, False)

    def clicked(self, widget):
        self.expanded ^= 1
        if self.expanded:
            self.image.set_from_stock(gtk.STOCK_GO_DOWN, gtk.ICON_SIZE_MENU)
            self.get_children()[1].show()
        else:
            self.image.set_from_stock(gtk.STOCK_GO_FORWARD, gtk.ICON_SIZE_MENU)
            self.get_children()[1].hide()

if __name__ == '__main__':
    def quit(widget, event):
        gtk.main_quit()
        return True

    window = gtk.Window()
    window.set_title(_("Expander button"))
    window.connect("delete-event", quit)

    box = gtk.VBox()
    window.add(box)

    button = Button(_("Document properties"))
    box.pack_start(button, False, False)

    table = gtk.Table()
    table.set_border_width(12)
    table.set_row_spacings(4)
    table.set_col_spacings(4)
    button.add(table)

    label = gtk.Label(_("Top margin:"))
    label.set_alignment(0.0, 0.5)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 0, 1, gtk.FILL, 0)
    table.attach(alignment, 1, 2, 0, 1, gtk.EXPAND | gtk.FILL, 0)

    label = gtk.Label(_("Bottom margin:"))
    label.set_alignment(0.0, 0.5)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 1, 2, gtk.FILL, 0)
    table.attach(alignment, 1, 2, 1, 2, gtk.EXPAND | gtk.FILL, 0)

    label = gtk.Label(_("Left margin:"))
    label.set_alignment(0.0, 0.5)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 2, 3, gtk.FILL, 0)
    table.attach(alignment, 1, 2, 2, 3, gtk.EXPAND | gtk.FILL, 0)

    label = gtk.Label(_("Right margin:"))
    label.set_alignment(0.0, 0.5)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 3, 4, gtk.FILL, 0)
    table.attach(alignment, 1, 2, 3, 4, gtk.EXPAND | gtk.FILL, 0)

    label = gtk.Label(_("Grid size:"))
    label.set_alignment(0.0, 0.5)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 4, 5, gtk.FILL, 0)
    table.attach(alignment, 1, 2, 4, 5, gtk.EXPAND | gtk.FILL, 0)

    label = gtk.Label(_("Guides size:"))
    table.attach(label, 0, 1, 5, 6, gtk.FILL, 0)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.SpinButton()
    alignment.add(entry)
    table.attach(alignment, 1, 2, 5, 6, gtk.EXPAND | gtk.FILL, 0)

    button = gtk.CheckButton(_("Show margins"))
    label.set_alignment(0.0, 0.5)
    table.attach(button, 0, 2, 6, 7, gtk.FILL, 0)

    button = gtk.CheckButton(_("Show guides"))
    table.attach(button, 0, 2, 7, 8, gtk.FILL, 0)

    button = gtk.CheckButton(_("Show grid"))
    table.attach(button, 0, 2, 8, 9, gtk.FILL, 0)

    button = gtk.CheckButton(_("Enable snap")) # Magnetic grid
    table.attach(button, 0, 2, 9, 10, gtk.FILL, 0)

    #--------------------------------
    button = Button(_("Object properties"))
    box.pack_start(button, False, False)

    table = gtk.Table()
    table.set_border_width(12)
    table.set_row_spacings(4)
    table.set_col_spacings(4)
    button.add(table)

    label = gtk.Label("X:")
    label.set_alignment(0.0, 0.5)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 0, 1, gtk.FILL, 0)
    table.attach(alignment, 1, 2, 0, 1, gtk.EXPAND | gtk.FILL, 0)

    label = gtk.Label("Y:")
    label.set_alignment(0.0, 0.5)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 1, 2, gtk.FILL, 0)
    table.attach(alignment, 1, 2, 1, 2, gtk.EXPAND | gtk.FILL, 0)

    label = gtk.Label(_("Width:"))
    label.set_alignment(0.0, 0.5)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 2, 3, gtk.FILL, 0)
    table.attach(alignment, 1, 2, 2, 3, gtk.EXPAND | gtk.FILL, 0)

    label = gtk.Label(_("Height:"))
    label.set_alignment(0.0, 0.5)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.SpinButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 3, 4, gtk.FILL, 0)
    table.attach(alignment, 1, 2, 3, 4, gtk.EXPAND | gtk.FILL, 0)

    label = gtk.Label(_("Border color:"))
    label.set_alignment(0.0, 0.5)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.ColorButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 4, 5, gtk.FILL, 0)
    table.attach(alignment, 1, 2, 4, 5, gtk.EXPAND | gtk.FILL, 0)

    label = gtk.Label(_("Fill color:"))
    label.set_alignment(0.0, 0.5)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.ColorButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 5, 6, gtk.FILL, 0)
    table.attach(alignment, 1, 2, 5, 6, gtk.EXPAND | gtk.FILL, 0)

    label = gtk.Label(_("Text:"))
    label.set_alignment(0.0, 0.5)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.Entry()
    alignment.add(entry)
    table.attach(label, 0, 1, 6, 7, gtk.FILL, 0)
    table.attach(alignment, 1, 2, 6, 7, gtk.EXPAND | gtk.FILL, 0)

    label = gtk.Label(_("Font:"))
    label.set_alignment(0.0, 0.5)
    alignment = gtk.Alignment(0.0, 0.5)
    entry = gtk.FontButton()
    alignment.add(entry)
    table.attach(label, 0, 1, 7, 8, gtk.FILL, 0)
    table.attach(alignment, 1, 2, 7, 8, gtk.EXPAND | gtk.FILL, 0)

    window.show_all()
    gtk.main()
