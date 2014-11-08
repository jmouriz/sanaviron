#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk

from interfaces.signalizable import Signalizable

COLUMN_TITLE = 0
COLUMN_WIDTH = 1
COLUMN_UNIT = 2

class ColumnsEditor(gtk.ScrolledWindow, Signalizable):
    """This class represents a table columns editor"""

    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        Signalizable.__init__(self)

        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        units = gtk.ListStore(str)
        units.append([_("millimeters")])
        units.append([_("inches")])
        units.append([_("pixels")])

        self.liststore = gtk.ListStore(str, int, str)

        treeview = gtk.TreeView(self.liststore)
        treeview.set_size_request(-1, 100)
        treeview.set_rules_hint(True)
        treeview.set_grid_lines(True)
        self.add(treeview)

        cell = gtk.CellRendererText()
        cell.connect("edited", self.title_edited)
        cell.set_property("editable", True)
        column = gtk.TreeViewColumn(_("Title"))
        column.pack_start(cell, True)
        column.set_attributes(cell, text=COLUMN_TITLE)
        treeview.append_column(column)
        treeview.set_search_column(COLUMN_TITLE)

        adjustment = gtk.Adjustment(0, 0, 100, 1)
        cell = gtk.CellRendererSpin()
        cell.connect("edited", self.width_edited)
        cell.set_property("editable", True)
        cell.set_property("adjustment", adjustment)
        cell.set_property("xalign", 1.0)
        column = gtk.TreeViewColumn(_("Width"))
        column.pack_start(cell, True)
        column.set_attributes(cell, text=COLUMN_WIDTH)
        treeview.append_column(column)

        cell = gtk.CellRendererCombo()
        cell.set_property("editable", True)
        cell.set_property("has-entry", False)
        cell.set_property("model", units)
        cell.set_property("text-column", 0)
        column = gtk.TreeViewColumn(_("Unit"))
        column.pack_start(cell, True)
        column.set_attributes(cell, text=COLUMN_UNIT)
        treeview.append_column(column)

        self.install_signals()

    def install_signals(self):
        self.install_signal("width-edited")
        self.install_signal("title-edited")

    def width_edited(self, cell, path, text):
        width = int(text)
        column = int(path)
        self.liststore[path][COLUMN_WIDTH] = width
        self.emit("width-edited", column, width)

    def title_edited(self, cell, path, text):
        column = int(path)
        self.liststore[path][COLUMN_TITLE] = text
        self.emit("title-edited", column, text)

    def add_column(self, title=None, size=0):
        row = len(self.liststore) + 1
        if not title:
            title = "Columna %d" % row
        self.liststore.append([title, size, _("millimeters")])

    def remove_column(self):
        last = len(self.liststore) - 1
        del self.liststore[last]

    def clear(self):
        self.liststore.clear()

if __name__ == '__main__':
    def quit(widget, event):
        gtk.main_quit()
        return True

    window = gtk.Window()
    window.set_size_request(400, 200)
    window.set_title("Tabla de muestra")
    window.connect("delete-event", quit)
    columns_editor = ColumnsEditor()
    columns_editor.add_column()
    columns_editor.add_column()
    columns_editor.add_column()
    window.add(columns_editor)
    window.show_all()
    gtk.main()
