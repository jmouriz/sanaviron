#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk

from ui.button import Button
from ui.entry import LinearEntry, AngularEntry
from ui.options import Options
from objects import *
from objects.observer import Observer
from objects.barcode import barcodes
from objects.charts import *
from objects.color import Color

from ui.textpad import TextPad
from ui.columnseditor import ColumnsEditor
from ui.gradienteditor import LinearGradientEditor
import sys

class Form(gtk.VBox):
    """This class represents a properties form"""

    def __init__(self, name, properties):
        gtk.VBox.__init__(self)
        self.group = properties.group
        self.observer = properties.observer
        self.__name = name
        self.table = None
        self.entries = 0

    def add_section(self, caption):
        expander = gtk.Expander('<b>' + caption + '</b>')
        expander.set_expanded(True)
        label = expander.get_label_widget()
        label.set_use_markup(True)
        self.add(expander)

        table = gtk.Table()
        table.set_row_spacings(6)
        table.set_col_spacings(12)
        alignment = gtk.Alignment(0.0, 0.0, 1.0, 0.0)
        alignment.add(table)
        alignment.set_padding(6, 0, 12, 0)
        expander.add(alignment)

        self.table = table
        self.entries = 0

    def add_entry(self, caption, entry, property, expanded=False):
        if caption:
            label = gtk.Label(caption + ':')
            self.group.add_widget(label)
            label.set_alignment(0.0, 0.5)
            self.table.attach(label, 0, 1, self.entries, self.entries + 1, gtk.FILL, 0)
            alignment = gtk.Alignment(0.0, 0.5, float(expanded))
            alignment.add(entry)
            self.table.attach(alignment, 1, 2, self.entries, self.entries + 1, gtk.EXPAND | gtk.FILL, 0)
        else:
            self.table.attach(entry, 0, 2, self.entries, self.entries + 1, gtk.EXPAND | gtk.FILL, 0)
        observable = "%s-%s" % (self.__name, property)
        self.observer.install_observable(observable, entry)
        self.entries += 1

class PositionedObjectForm(Form):
    """TODO"""

    def __init__(self, name, properties):
        Form.__init__(self, name, properties)

        self.add_section(_("Position"))

        entry = LinearEntry()
        self.add_entry(_("Horizontal"), entry, "x")

        entry = LinearEntry()
        self.add_entry(_("Vertical"), entry, "y")


class AngledObjectForm(Form):
    """TODO"""

    def __init__(self, name, properties):
        Form.__init__(self, name, properties)

        self.add_section(_("Angle"))

        entry = AngularEntry()
        self.add_entry(_("Start Angle"), entry, "start")

        entry = AngularEntry()
        self.add_entry(_("Stop Angle"), entry, "end")


class SizedObjectForm(PositionedObjectForm):
    """TODO"""

    def __init__(self, name, properties):
        PositionedObjectForm.__init__(self, name, properties)

        self.add_section(_("Size"))

        entry = LinearEntry()
        self.add_entry(_("Width"), entry, "width")

        entry = LinearEntry()
        self.add_entry(_("Height"), entry, "height")


class ColorizedObjectForm(SizedObjectForm):
    """TODO"""

    def __init__(self, name, properties):
        SizedObjectForm.__init__(self, name, properties)

        self.canvas = properties.canvas
        self.add_section(_("Color"))

        entry = Options()
        entry.add_option(_("Color"))
        entry.add_option(_("Gradient"))
        entry.add_option(_("Pattern"))
        #entry = gtk.HButtonBox()
        #entry.set_layout(gtk.BUTTONBOX_SPREAD)
        #entry.set_spacing(10)
        #entry.add(gtk.ToggleButton(_("Color")))
        #entry.add(gtk.ToggleButton(_("Gradient")))
        #entry.add(gtk.ToggleButton(_("Pattern")))
        self.add_entry(_("Fill style"), entry, "fill_style")

        entry = gtk.ColorButton()
        entry.set_use_alpha(True)
        entry.connect("color-set", self.set_stroke_color)
        self.add_entry(_("Stroke"), entry, "foreground")

        entry = gtk.ColorButton()
        entry.set_use_alpha(True)
        entry.connect("color-set", self.set_fill_color)
        self.add_entry(_("Fill"), entry, "background")


        entry = LinearGradientEditor()
        entry.connect("update", self.set_gradient)
        self.add_entry(_("Gradient"), entry, "gradient")

    def set_gradient(self, widget, data):
        for child in self.canvas.document.pages[0].children:
            if child.selected:
                gradient = widget.gl.gradient
                child.set_gradient(gradient)
                self.canvas.queue_draw()

    def set_stroke_color(self, widget):
        for child in self.canvas.document.pages[0].children:
            if child.selected:
                color = Color(red=widget.get_color().red_float,
                              green=widget.get_color().green_float,
                              blue=widget.get_color().blue_float,
                              alpha=widget.get_alpha() / 65535.0)
                child.set_stroke_color(color)
                self.canvas.queue_draw()

    def set_fill_color(self, widget):
        for child in self.canvas.document.pages[0].children:
            if child.selected:
                color = Color(red=widget.get_color().red_float,
                              green=widget.get_color().green_float,
                              blue=widget.get_color().blue_float,
                              alpha=widget.get_alpha() / 65535.0)
                child.set_fill_color(color)
                self.canvas.queue_draw()


class Properties(gtk.ScrolledWindow):
    """This class represents the properties bar"""

    def __init__(self, application):
        gtk.ScrolledWindow.__init__(self)

        self.observer = Observer()

        self.objects = dict()

        from canvas import Canvas
        self.canvas = Canvas(application)

        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        properties = gtk.VBox()
        self.add_with_viewport(properties)

        self.group = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)

        #---START-------------------------------------------------------
        button = Button(_("General properties"))
        properties.pack_start(button, False, False)

        form = Form("general", self)
        button.add(form)

        form.add_section(_("Units"))

        entry = gtk.combo_box_new_text()
        entry.append_text(CENTIMETERS)
        entry.append_text(MILLIMETERS)
        entry.append_text(DOTS)
        entry.append_text(INCHES)
        entry.set_active(1)

        form.add_entry(_("Preferred linear unit"), entry, "linear-unit")

        entry = gtk.combo_box_new_text()
        entry.append_text(DEGREES)
        entry.append_text(RADIANS)
        entry.set_active(1)

        form.add_entry(_("Preferred angular unit"), entry, "angular-unit")
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Document properties"))
        properties.pack_start(button, False, False)

        form = Form("document", self)
        button.add(form)

        form.add_section(_("Size"))

        entry = LinearEntry()
        form.add_entry(_("Width"), entry, "width")

        entry = LinearEntry()
        form.add_entry(_("Height"), entry, "height")

        form.add_section(_("Margins"))

        entry = LinearEntry()
        form.add_entry(_("Top"), entry, "top-margin")

        entry = LinearEntry()
        form.add_entry(_("Bottom"), entry, "bottom-margin")

        entry = LinearEntry()
        form.add_entry(_("Left"), entry, "left-margin")

        entry = LinearEntry()
        form.add_entry(_("Right"), entry, "right-margin")

        form.add_section(_("Config"))

        entry = LinearEntry()
        form.add_entry(_("Grid size"), entry, "grid-size")

        entry = LinearEntry()
        form.add_entry(_("Guides size"), entry, "guides-size")

        entry = gtk.CheckButton(_("Show margins"))
        form.add_entry(None, entry, "margins-active")

        entry = gtk.CheckButton(_("Show guides"))
        form.add_entry(None, entry, "guides-active")

        entry = gtk.CheckButton(_("Show grid"))
        form.add_entry(None, entry, "grid-active")

        entry = gtk.CheckButton(_("Enable snap"))
        form.add_entry(None, entry, "snap")
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Line properties"))
        self.objects["Line"] = button
        properties.pack_start(button, False, False)

        form = SizedObjectForm("line", self)
        button.add(form)
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Box properties"))
        self.objects["Box"] = button
        properties.pack_start(button, False, False)

        form = ColorizedObjectForm("box", self)
        button.add(form)
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Rounded box properties"))
        self.objects["Rounded"] = button
        properties.pack_start(button, False, False)

        form = ColorizedObjectForm("rounded", self)
        button.add(form)

        form.add_section(_("Shape"))

        entry = LinearEntry()
        entry.set_value(0)
        form.add_entry(_("Radius"), entry, "radius")
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Text properties"))
        self.objects["Text"] = button
        properties.pack_start(button, False, False)

        form = ColorizedObjectForm("text", self)
        button.add(form)

        form.add_section(_("Format"))

        entry = gtk.FontButton()
        entry.connect("font-set", self.change_font)
        form.add_entry(_("Font"), entry, "font")

        entry = gtk.CheckButton(_("Preserve aspect"))
        entry.connect("toggled", self.preserve)
        form.add_entry(None, entry, "preserve")

        form.add_section(_("Text"))

        entry = TextPad(application)
        self.disconnect_handler = entry.buffer.connect("changed", self.changed)
        entry.connect("cursor-moved", self.cursor_moved)
        form.add_entry(None, entry, "text")
        #---END---------------------------------------------------------

        #---START--------ARC properties-----------------------------------------------
        button = Button(_("Arc properties"))
        self.objects["Arc"] = button
        properties.pack_start(button, False, False)

        form = ColorizedObjectForm("arc", self)
        button.add(form)

        form.add_section(_("Angle"))
        self.angle_start = AngularEntry()
        form.add_entry(_("Start Angle"), self.angle_start, "start")
        self.angle_start.spin.connect("value-changed", self.change_angle_start)

        self.angle_stop = AngularEntry()
        form.add_entry(_("Stop Angle"), self.angle_stop, "stop")
        self.angle_stop.spin.connect("value-changed", self.change_angle_stop)

        form.add_section(_("Other"))
        self.closed_btn = gtk.CheckButton()
        form.add_entry(_("Closed Arc"), self.closed_btn, "closed")
        self.closed_btn.connect("toggled", self.close_arc)

        self.closed_at_centre_btn = gtk.CheckButton()
        self.closed_at_centre_btn.set_active(1)
        form.add_entry(_("Closed Arc at Centre"), self.closed_at_centre_btn,
                       "closed-at-centre")
        self.closed_at_centre_btn.connect("toggled", self.close_at_centre_arc)
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Table properties"))
        self.objects["Table"] = button
        properties.pack_start(button, False, False)

        form = PositionedObjectForm("table", self)
        button.add(form)

        form.add_section(_("Spacing"))

        entry = LinearEntry()
        entry.set_value(0)
        form.add_entry(_("Vertical"), entry, "vertical-spacing")

        entry = LinearEntry()
        entry.set_value(0)
        form.add_entry(_("Horizontal"), entry, "horizontal-spacing")

        form.add_section(_("Size"))

        entry = LinearEntry()
        entry.set_value(1)
        entry.connect("value-changed", self.set_table_columns)
        form.add_entry(_("Columns"), entry, "columns")

        entry = LinearEntry()
        entry.set_value(5)
        entry.connect("value-changed", self.set_table_rows)
        form.add_entry(_("Rows"), entry, "rows")

        form.add_section(_("Color"))

        entry = gtk.ColorButton()
        form.add_entry(_("Stroke"), entry, "stroke")

        entry = gtk.ColorButton()
        form.add_entry(_("Fill"), entry, "fill")

        form.add_section(_("Format"))

        entry = gtk.FontButton()
        entry.connect("font-set", self.set_table_font)
        form.add_entry(_("Font"), entry, "font")

        form.add_section(_("Columns"))

        entry = ColumnsEditor()
        entry.add_column()
        entry.connect("width-edited", self.set_table_column_width)
        entry.connect("title-edited", self.set_table_column_title)
        form.add_entry(None, entry, "columns-editor")
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Barcode properties"))
        self.objects["BarCode"] = button
        properties.pack_start(button, False, False)

        form = ColorizedObjectForm("barcode", self)
        button.add(form)

        form.add_section(_("Barcode"))

        entry = gtk.combo_box_new_text()
        entry.connect("changed", self.changed_barcode_type)
        for type in sorted(barcodes, key=lambda type: barcodes[type]):
            entry.append_text(type)
        form.add_entry(_("Type"), entry, "type")

        entry = gtk.Entry()
        entry.connect("changed", self.changed_barcode_code)
        form.add_entry(_("Code"), entry, "code")
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Image properties"))
        self.objects["Image"] = button
        properties.pack_start(button, False, False)

        form = SizedObjectForm("image", self)
        button.add(form)

        form.add_section(_("Image"))

        def update_preview(dialog, preview):
            filename = dialog.get_preview_filename()
            try:
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 128,
                                                              128)
                preview.set_from_pixbuf(pixbuf)
                have_preview = True
            except:
                have_preview = False
            dialog.set_preview_widget_active(have_preview)

        dialog = gtk.FileChooserDialog(title="Source image file",
                                       #parent = self,
                                       action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                       buttons=(
                                       gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                       gtk.STOCK_OPEN, gtk.RESPONSE_ACCEPT),
                                       backend=None)

        preview = gtk.Image()

        dialog.set_preview_widget(preview)
        dialog.connect("update-preview", update_preview, preview)

        #dialog.set_transient_for(self)
        dialog.set_default_response(gtk.RESPONSE_OK)

        def add_filter(dialog, name, pattern, type=None):
            filter = gtk.FileFilter()
            filter.set_name(name)
            if type:
                filter.add_mime_type(type)
            filter.add_pattern(pattern)
            dialog.add_filter(filter)

        add_filter(dialog, "PNG files", "*.png", "image/png")
        add_filter(dialog, "JPG files", "*.jpg", "image/jpg")
        add_filter(dialog, "All files", "*")

        dialog.connect("file-activated", self.changed_image_file)

        entry = gtk.FileChooserButton(dialog)
        form.add_entry(_("Image file"), entry, "file", True)
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Chart properties"))
        self.objects["Chart"] = button
        properties.pack_start(button, False, False)

        form = SizedObjectForm("chart", self)
        button.add(form)

        form.add_section(_("Chart"))

        entry = gtk.combo_box_new_text()
        entry.connect("changed", self.changed_chart_type)
        for type in sorted(chart_types, key=lambda type: chart_types[type]):
            entry.append_text(type)
        form.add_entry(_("Type"), entry, "type")
        #---END---------------------------------------------------------

        fill = gtk.Label("\n")
        properties.add(fill)

    def select(self, name, child):
        for key, object in self.objects.items():
            if key == name:
                object.show()

                def set_property_from_child(name, property, value):
                    observable = "%s-%s" % (name.lower(), property)
                    entry = self.observer.get_observable(observable)
                    entry.set_value(value)

                set_property_from_child(name, "x", child.x)
                set_property_from_child(name, "y", child.y)

                try:
                    set_property_from_child(name, "width", child.width)
                    set_property_from_child(name, "height", child.height)
                except:
                    pass

                # TODO: Colors
                set_property_from_child(name, "gradient", child.gradient)

                if name == "Arc":
                    value = child.get_property("angle_start")
                    entry = self.observer.get_observable("arc-start")
                    entry.set_value(value)
                    value = child.get_property("angle_stop")
                    entry = self.observer.get_observable("arc-stop")
                    entry.set_value(value)
                    value = child.get_property("closed")
                    entry = self.observer.get_observable("arc-closed")
                    entry.set_active(value)
                    value = child.get_property("closed_at_centre")
                    entry = self.observer.get_observable("arc-closed-at-centre")
                    entry.set_active(value)
                if name == "Rounded":
                    radius = child.get_property("radius")
                    entry = self.observer.get_observable("rounded-radius")
                    entry.set_value(float(radius))
                if name == "Text":
                    text = child.get_property("text")
                    entry = self.observer.get_observable("text-text")
                    entry.set_text(text)
                    preserve = child.get_property("preserve")
                    entry = self.observer.get_observable("text-preserve")
                    entry.set_active(preserve)
                if name == "Image":
                    image = child.get_property("image")
                    entry = self.observer.get_observable("image-file")
                    entry.set_filename(image)
                if name == "BarCode":
                    code = child.get_property("code")
                    type = int(child.get_property("type"))
                    entry = self.observer.get_observable("barcode-code")
                    entry.set_text(code)
                    entry = self.observer.get_observable("barcode-type")
                    entry.set_active(type)
                if name == "Table":
                    columns = child.get_property("columns").split(':')
                    titles = child.get_property("titles").split(':')
                    rows = child.get_property("rows")
                    entry = self.observer.get_observable("table-rows")
                    entry.set_value(int(rows))
                    entry = self.observer.get_observable("table-columns")
                    entry.set_value(len(columns))
                    entry = self.observer.get_observable("table-columns-editor")
                    entry.clear()
                    for i, title in enumerate(titles):
                        entry.add_column(title, int(columns[i]))
            else:
                object.hide()

    def set_table_column_title(self, widget, column, title):
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Table" and child.selected:
                titles = child.get_property('titles').split(':')
                titles[column] = title
                titles = ':'.join(titles)
                child.set_property('titles', titles)
                self.canvas.queue_draw()
                break

    def set_table_column_width(self, widget, column, width):
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Table" and child.selected:
                columns = child.get_property('columns').split(':')
                columns[column] = str(width)
                columns = ':'.join(columns)
                child.set_property('columns', columns)
                self.canvas.queue_draw()
                break

    def set_table_columns(self, widget, data):
        n_columns = widget.spin.get_value_as_int()
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Table" and child.selected:
                entry = self.observer.get_observable("table-columns-editor")
                columns = child.get_property('columns').split(':')
                titles = child.get_property('titles').split(':')
                if n_columns < len(columns):  # Remove column
                    del columns[n_columns]
                    del titles[n_columns]
                    entry.remove_column()
                elif n_columns > len(columns):  # Append column
                    columns.append('0')
                    title = _("Column %d") % n_columns
                    titles.append(title)
                    entry.add_column()
                else:
                    entry.add_column()
                columns = ':'.join(columns)
                #print titles
                titles = ':'.join(titles)
                child.set_property('columns', columns)
                child.set_property('titles', titles)
                self.canvas.queue_draw()
                break

    def set_table_rows(self, widget, data):
        rows = widget.spin.get_value_as_int()
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Table" and child.selected:
                child.set_property('rows', rows)
                self.canvas.queue_draw()
                break

    def set_text_foreground(self, widget):
        color = widget.get_color()
        print color.red
        print color.green
        print color.blue

    def cursor_moved(self, entry, position):
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Text" and child.selected:
                child.set_cursor_position(position)
                self.canvas.queue_draw()
                break

    def changed(self, buffer):
        start, end = buffer.get_bounds()
        text = buffer.get_text(start, end)
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Text" and child.selected:
                child.set_property('text', text)
                self.canvas.queue_draw()
                break

    def set_table_font(self, widget):
        font = widget.get_font_name()
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Table" and child.selected:
                child.set_property('font', font)
                self.canvas.queue_draw()
                break

    def close_arc(self, widget):
        state = widget.get_active()
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Arc" and child.selected:
                child.set_property('closed', int(state))
                self.canvas.queue_draw()
                # The user check closed arc, not closed at centre.
                # This property must be set only if the user check
                # closed at centre.
                #self.closed_at_centre_btn.set_sensitive(state)

    def close_at_centre_arc(self, widget):
        state = widget.get_active()
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Arc" and child.selected:
                child.set_property('closed_at_centre', int(state))
                self.canvas.queue_draw()

    def change_angle_start(self, widget):
        val = widget.get_value()
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Arc" and child.selected:
                child.set_property('angle_start', val)
                self.canvas.queue_draw()

    def change_angle_stop(self, widget):
        val = widget.get_value()
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Arc" and child.selected:
                child.set_property('angle_stop', val)
                self.canvas.queue_draw()

    def change_font(self, widget):
        font = widget.get_font_name()
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Text" and child.selected:
                child.set_property('font', font)
                self.canvas.queue_draw()
                break

    def preserve(self, widget):
        preserve = widget.get_active()
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Text" and child.selected:
                child.set_property('preserve', preserve)
                self.canvas.queue_draw()
                break

    def changed_barcode_type(self, widget):
        #selected = widget.get_active_text()
        #type = get_barcode_type_from_string(selected)
        type = widget.get_active()
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "BarCode" and child.selected:
                child.set_property('type', type)
                self.canvas.queue_draw()
                break

    def changed_barcode_code(self, editable):
        code = editable.get_chars(0, -1)
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "BarCode" and child.selected:
                child.set_property('code', code)
                self.canvas.queue_draw()
                break

    def changed_image_file(self, widget):
        filename = widget.get_filename()
        print filename
        if filename is not None:
            for child in self.canvas.document.pages[0].children:
                if child.__name__ == "Image" and child.selected:
                    child.set_property('image', filename)
                    self.canvas.queue_draw()
                    break

    def changed_chart_type(self, widget):
        #selected = widget.get_active_text()
        #type = get_barcode_type_from_string(selected)
        type = widget.get_active()
        for child in self.canvas.document.pages[0].children:
            if child.__name__ == "Chart" and child.selected:
                child.set_property('type', type)
                self.canvas.queue_draw()
                break


if __name__ == '__main__':
    def quit(widget, event):
        gtk.main_quit()
        return True

    window = gtk.Window()
    window.set_title(_("Properties panel"))
    window.connect("delete-event", quit)
    properties = Properties(None)
    window.add(properties)
    window.show_all()
    gtk.main()
