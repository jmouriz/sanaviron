#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from gi.repository import Gtk
from gi.repository import Pango
import traceback
from StringIO import StringIO
import gtksourceview2 as gtksourceview

class SourcePad(Gtk.ScrolledWindow):
    """This class represents a source code editor""" # No used yet!

    def __init__(self, application):
        GObject.GObject.__init__(self)

        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        adjustment = self.get_vadjustment()
        adjustment.need_scroll = True
        adjustment.connect("changed", self.update_adjustment)
        adjustment.connect("value-changed", self.update_value)
        self.buffer = gtksourceview.Buffer()
        entry = gtksourceview.View(self.buffer)
        entry.set_size_request(-1, 100)
        #self.disconnect_handler = buffer.connect("changed", self.changed)
        self.buffer.connect("insert-text", self.update_scroll, entry)
        #self.add_with_viewport(entry)
        self.add(entry)
        entry.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        entry.set_wrap_mode(Gtk.WrapMode.CHAR)

        font = Pango.FontDescription('monospace')
        entry.modify_font(font)
        entry.set_show_line_numbers(True)
        entry.set_show_line_marks(True)
        entry.set_tab_width(8)
        entry.set_auto_indent(True)
        entry.set_insert_spaces_instead_of_tabs(False)
        entry.set_show_right_margin(True)
        entry.set_right_margin(30)
        #entry.set_marker_pixbuf(marker_type, pixbuf)
        entry.set_smart_home_end(True)
        entry.connect("focus-in-event", self.focus_in)
        entry.connect("focus-out-event", self.focus_out)

        self.buffer.set_highlight_syntax(True)
        self.buffer.set_max_undo_levels(10)
        self.buffer.set_highlight_matching_brackets(True)
        self.set_language("python") # default

        #from application import Application
        #self.application = Application()
        self.application = application

    def focus_in(self, event, data):
        self.application.disable_bindings()

    def focus_out(self, event, data):
        self.application.enable_bindings()

    def set_language(self, language):
        manager = gtksourceview.LanguageManager()
        srclang = manager.get_language(language)
        self.buffer.set_language(srclang)

    def update_scroll(self, buffer, iter, text, length, view):
        mark = buffer.create_mark("end", iter, False)
        view.scroll_mark_onscreen(mark)

    # Methods for update the scrollbars of text area.
    def update_adjustment(self, adjustment):
        if adjustment.need_scroll:
            adjustment.set_value(adjustment.get_upper() - adjustment.get_page_size())
            adjustment.need_scroll = True

    def update_value(self, adjustment):
        adjustment.need_scroll = abs(
            adjustment.get_value() + adjustment.get_page_size() - adjustment.get_upper()) < adjustment.get_step_increment()

class CodeEditor(Gtk.VBox):
    """This class represents a source code editor""" # No used yet!

    def __init__(self, application):
        GObject.GObject.__init__(self)

        handle = Gtk.HandleBox()
        handle.set_handle_position(Gtk.PositionType.LEFT)
        self.pack_start(handle, False, False)

        toolbar = Gtk.Toolbar()
        toolbar.set_orientation(Gtk.Orientation.HORIZONTAL)
        #toolbar.set_style(Gtk.ToolbarStyle.ICONS)
        toolbar.set_style(Gtk.ToolbarStyle.BOTH_HORIZ)
        toolbar.set_icon_size(Gtk.IconSize.MENU)
        handle.add(toolbar)

        position = 0
        button = Gtk.ToolButton(Gtk.STOCK_MEDIA_PLAY)
        button.connect("clicked", self.run)
        toolbar.insert(button, position)

        position += 1
        button = Gtk.ToolButton(Gtk.STOCK_MEDIA_STOP)
        toolbar.insert(button, position)

        panel = Gtk.HPaned()
        panel.set_position(75) # TODO calculate
        self.add(panel)

        self.editor = SourcePad(application)
        panel.pack1(self.editor, True, False)

        view = Gtk.ScrolledWindow()
        view.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        panel.pack2(view, False, True)

        output = Gtk.TextView()
        font = Pango.FontDescription('monospace')
        output.modify_font(font)
        self.buffer = Gtk.TextBuffer()
        self.buffer.connect_after('insert-text', self.text_inserted, view)
        output.set_buffer(self.buffer)
        view.add(output)

        self.tags = []
        self.buffer.create_tag("normal", editable=False, wrap_mode=Gtk.WrapMode.WORD_CHAR)
        self.buffer.create_tag("error", foreground="#f00", weight=Pango.Weight.BOLD, style=Pango.Style.ITALIC)
        self.tags.append('normal')

    def set_error(self):
        self.tags.append('error')

    def unset_error(self):
        if 'error' in self.tags:
            del self.tags[self.tags.index('error')]

    def text_inserted(self, buffer, iter, text, length, view):
        position = buffer.get_iter_at_mark(buffer.get_insert())
        iter.backward_chars(length)

        for tag in self.tags:
            buffer.apply_tag_by_name(tag, position, iter)

    def run(self, widget):
        buffer = self.editor.buffer
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        code = buffer.get_text(start, end)
        stdio = (sys.stdin, sys.stdout, sys.stderr)
        io = StringIO()
        sys.stdout = sys.stderr = io
        self.unset_error()
        try:
            exec(code, locals(), globals())
            output = io.getvalue()
        except Exception, exception:
            self.set_error()
            output = str(exception) + "\n" + traceback.format_exc()
        sys.stdin, sys.stdout, sys.stderr = stdio
        self.buffer.set_text(output)

if __name__ == '__main__':
    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    editor = CodeEditor()
    window.add(editor)
    window.show_all()
    Gtk.main()
