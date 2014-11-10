# Copyright(c) 2007-2009 by Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
#
# This file is part of Chavier.
#
# Chavier is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Chavier is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Chavier.  If not, see <http://www.gnu.org/licenses/>.

import random
import webbrowser

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class TextInputDialog(Gtk.Dialog):
    def __init__(self, toplevel_window, suggested_name):
        flags = Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT
        buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                   Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
        super(TextInputDialog, self).__init__(u'Enter a name for the dataset',
            toplevel_window, flags, buttons)
        self.set_default_size(300, -1)

        hbox = Gtk.HBox(spacing=6)
        hbox.set_border_width(12)

        label = Gtk.Label(label=u'Name')
        hbox.pack_start(label, False, False)

        self.entry = Gtk.Entry()
        self.entry.set_text(suggested_name)
        self.entry.set_activates_default(True)
        hbox.pack_start(self.entry, True, True)

        self.vbox.pack_start(hbox, False, False)

        self.vbox.show_all()

        self.set_default_response(Gtk.ResponseType.ACCEPT)

    def get_name(self):
        return self.entry.get_text()


class PointDialog(Gtk.Dialog):
    def __init__(self, toplevel_window, initial_x, initial_y):
        flags = Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT
        buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                   Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
        super(PointDialog, self).__init__(u'Enter the point values',
            toplevel_window, flags, buttons)

        initials = {u'x': str(initial_x), u'y': str(initial_y)}
        self.entries = {}
        for coordinate in (u'x', u'y'):
            hbox = Gtk.HBox(spacing=6)
            hbox.set_border_width(12)

            label = Gtk.Label(label=coordinate)
            hbox.pack_start(label, False, False)

            entry = Gtk.Entry()
            entry.set_activates_default(True)
            entry.set_text(initials[coordinate])
            hbox.pack_start(entry, True, True)

            self.entries[coordinate] = entry

            self.vbox.pack_start(hbox, False, False)

        self.vbox.show_all()

        self.set_default_response(Gtk.ResponseType.ACCEPT)

    def get_point(self):
        return (float(self.entries[u'x'].get_text()),
                float(self.entries[u'y'].get_text()))


class OptionDialog(Gtk.Dialog):
    def __init__(self, toplevel_window, label, value, value_type):
        flags = Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT
        buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                   Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
        super(OptionDialog, self).__init__(u'Enter the option value',
            toplevel_window, flags, buttons)

        hbox = Gtk.HBox(spacing=6)
        hbox.set_border_width(12)

        label = Gtk.Label(label=label)
        hbox.pack_start(label, False, False)

        self.entry = Gtk.Entry()
        self.entry.set_text(value or '')
        self.entry.set_activates_default(True)
        hbox.pack_start(self.entry, True, True)

        self.vbox.pack_start(hbox, False, False)

        self.vbox.show_all()

        self.set_default_response(Gtk.ResponseType.ACCEPT)

    def get_value(self):
        return self.entry.get_text()


class RandomGeneratorDialog(Gtk.Dialog):
    def __init__(self, toplevel_window):
        flags = Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT
        buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                   Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
        super(RandomGeneratorDialog, self).__init__(u'Points generation',
            toplevel_window,
            flags, buttons)

        self.size_group = Gtk.SizeGroup(Gtk.SizeGroupMode.HORIZONTAL)

        self.number = self._create_spin_button('Number of points to generate',
            0, 1, 5, 1, 1000, 10)
        self.min = self._create_spin_button('Minimum y value',
            2, 0.5, 1, -1000, 1000, 0)
        self.max = self._create_spin_button('Maximum y value',
            2, 0.5, 1, 0, 1000, 10)

        self.vbox.show_all()

        self.set_default_response(Gtk.ResponseType.ACCEPT)

    def _create_spin_button(self, label_text, digits, step, page,
                            min_value, max_value, value):
        hbox = Gtk.HBox(spacing=6)
        hbox.set_border_width(12)

        label = Gtk.Label(label=label_text)
        label.set_alignment(1.0, 0.5)
        self.size_group.add_widget(label)
        hbox.pack_start(label, False, False)

        spin_button = Gtk.SpinButton(digits=digits)
        spin_button.set_increments(step, page)
        spin_button.set_range(min_value, max_value)
        spin_button.set_value(value)
        spin_button.set_activates_default(True)
        hbox.pack_start(spin_button, True, True)

        self.vbox.pack_start(hbox, False, False)

        return spin_button

    def generate_points(self):
        n = self.number.get_value_as_int()
        min_value = self.min.get_value()
        max_value = self.max.get_value()
        return [(x, random.uniform(min_value, max_value))
        for x in range(n)]


class AboutDialog(Gtk.AboutDialog):
    def __init__(self, toplevel_window):
        super(AboutDialog, self).__init__()
        self.set_transient_for(toplevel_window)

        self.set_name('Chavier')
        self.set_version('0.1')
        self.set_comments('A Chart Viewer for the Pycha library')
        self.set_copyright('Copyleft 2008 Lorenzo Gil Sanchez')
        #self.set_license('LGPL')
        author = 'Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>'
        self.set_authors([author])
        self.set_program_name('Chavier')
        self.set_website('http://www.lorenzogil.com/projects/pycha')
        self.set_website_label('Project website')


def url_handler(dialog, link, data=None):
    webbrowser.open(link)

Gtk.about_dialog_set_url_hook(url_handler)


def warning(window, msg):
    dialog = Gtk.MessageDialog(window,
        Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
        Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, msg)
    dialog.run()
    dialog.destroy()
