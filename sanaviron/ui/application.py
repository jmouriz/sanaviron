#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf
import sys
import os

from .__init__ import singleton

from sanaviron import VERSION, get_parsed_language, get_summary

from objects.arc import Arc
from objects.barcode import BarCode
from objects.box import Box
from objects.chart import Chart
from objects.curve import Curve
from objects.connector import Connector
from objects.image import Image
from objects.line import Line
from objects.rounded import Rounded
from objects.table import Table
from objects.text import Text
from objects.shape import Shape
from objects import HORIZONTAL, VERTICAL

from .menubar import MenuBar
from .stock import *
from .menubar import MenuBar
from .toolbar import Toolbar
from .editor import Editor
from .statusbar import Statusbar

@singleton
class Application(Gtk.Window):
    """This class represents an application"""
#    application = None
#
#    def __new__(cls, *args, **kwargs):
#        if cls.application:
#            return cls.application
#        else:
#            cls.application = super(Application, cls).__new__(cls)
#            cls.application.initialize()
#            return cls.application
#
#    def initialize(self):
    def __init__(self):
        GObject.GObject.__init__(self)
        self.set_size_request(640, 480)
        self.set_default_size(1366, 768)
        #self.set_default_size(800, 600)
        self.winstate = 0
        self.maximize()
        self.connect("delete-event", self.quit)

        self.bindings = Gtk.AccelGroup()
        self.add_accel_group(self.bindings)

        self.setup = Gtk.PageSetup()
        self.settings = Gtk.PrintSettings()

        self.filename = None
        self.update_title()

        icon = GdkPixbuf.Pixbuf.new_from_file(os.path.join(os.path.dirname(__file__), "..", "images", "canvas-logo.png"))
        self.set_icon(icon)

        vbox = Gtk.VBox()
        self.add(vbox)

        self.menu = MenuBar(self)
        vbox.pack_start(self.menu, False, False, 0)

        self.menu.append_menu(_("File"))
        self.menu.append_item(Gtk.STOCK_NEW, "new", "<Control>N")
        self.menu.append_item(Gtk.STOCK_OPEN, "open", "<Control>O")
        self.menu.append_item(Gtk.STOCK_SAVE, "save", "<Control>S")
        self.menu.append_item(Gtk.STOCK_SAVE_AS, "save-as", "<Control><Shift>S")
        self.menu.append_separator()
        self.menu.append_item(Gtk.STOCK_PAGE_SETUP, "page-setup")
        self.menu.append_item(Gtk.STOCK_PRINT_PREVIEW, "print-preview", "<Control><Shift>P")
        self.menu.append_item(Gtk.STOCK_PRINT, "print", "<Control>P")
        self.menu.append_separator()
        self.menu.append_menu(_("Document"), True)
        self.menu.append_item(SET_BACKGROUND, "set-background")
        self.menu.ascend()
        self.menu.append_separator()
        self.menu.append_menu(_("Export"), True)
        self.menu.append_item(EXPORT_TO_PDF, "export-to-pdf")
        self.menu.ascend()
        self.menu.append_separator()
        self.menu.append_item(Gtk.STOCK_QUIT, "quit", "<Control>Q")

        self.menu.append_menu(_("Edit"))
        self.menu.append_item(Gtk.STOCK_UNDO, "undo", "<Control>Z")
        self.menu.append_item(Gtk.STOCK_REDO, "redo", "<Control>Y")
        self.menu.append_separator()
        self.menu.append_item(Gtk.STOCK_COPY, "copy", "<Control>C")
        self.menu.append_item(Gtk.STOCK_CUT, "cut", "<Control>X")
        self.menu.append_item(Gtk.STOCK_PASTE, "paste", "<Control>V")
        self.menu.append_separator()
        self.menu.append_item(Gtk.STOCK_DELETE, "delete", "Delete")
        self.menu.append_separator()
        self.menu.append_item(Gtk.STOCK_SELECT_ALL, "select-all", "<Control>A")

        self.menu.append_menu(_("View"))
        self.menu.append_toggle(MARGINS_ENABLED, "margins")
        self.menu.append_toggle(GRID, "grid")
        self.menu.append_toggle(GUIDES, "guides")
        self.menu.append_toggle(SNAP_ENABLED, "snap")
        self.menu.append_toggle(_("Z-Order hint"), "hints", toggled = False)
        self.menu.append_separator()
        self.menu.append_toggle(Gtk.STOCK_PROPERTIES, "properties")
        self.menu.append_toggle(_("Menubar"), "menubar")
        self.menu.append_toggle(_("Statusbar"), "statusbar")

        self.menu.append_menu(_("Insert"))
        self.menu.append_item(LINE, "line")
        self.menu.append_item(ARC, "arc")
        self.menu.append_item(CURVE, "curve")
        self.menu.append_item(CONNECTOR, "connector")
        self.menu.append_menu(BOX, "box", True)
        self.menu.append_item(BOX, "box")
        self.menu.append_item(SPLIT_HORIZONTALLY, "split-horizontally")
        self.menu.append_item(SPLIT_VERTICALLY, "split-vertically")
        self.menu.append_item(REMOVE_SPLIT, "remove-split")
        self.menu.ascend()
        self.menu.append_item(ROUNDED_BOX, "rounded-box")
        self.menu.append_item(TEXT, "text")
        self.menu.append_item(TABLE, "table")
        self.menu.append_item(CHART, "chart")
        self.menu.append_item(BARCODE, "barcode")
        self.menu.append_item(IMAGE, "image")

        self.menu.append_menu(_("Format"))
        self.menu.append_item(Gtk.STOCK_SELECT_FONT, "select-font")
        self.menu.append_separator()
        self.menu.append_item(Gtk.STOCK_SELECT_COLOR, "select-color")

        self.menu.append_menu(_("Tools"))
        self.menu.append_item(GROUP, "group", "<Control>G")
        self.menu.append_item(UNGROUP, "ungroup", "<Control><Shift>G")
        self.menu.append_separator()
        self.menu.append_item(BRING_TO_FRONT, "bring-to-front", "<Control>plus")
        self.menu.append_item(BRING_TO_BACK, "bring-to-back", "<Control>minus")
        self.menu.append_separator()
        self.menu.append_menu(_("Zoom"), True)
        self.menu.append_item(Gtk.STOCK_ZOOM_FIT, "zoom-fit", "<Control>0")
        self.menu.append_item(Gtk.STOCK_ZOOM_100, "zoom-100", "<Control>1")
        self.menu.append_item(Gtk.STOCK_ZOOM_IN, "zoom-in", "<Control><Shift>plus")
        self.menu.append_item(Gtk.STOCK_ZOOM_OUT, "zoom-out", "<Control><Shift>minus")
        self.menu.ascend()
        self.menu.append_separator()
        self.menu.append_menu(_("Objects alignment"), True)
        self.menu.append_item(ALIGN_OBJECTS_NORTHWEST, "align-objects-northwest")
        self.menu.append_item(ALIGN_OBJECTS_NORTH, "align-objects-north")
        self.menu.append_item(ALIGN_OBJECTS_NORTHEAST, "align-objects-northeast")
        self.menu.append_item(ALIGN_OBJECTS_SOUTHWEST, "align-objects-southwest")
        self.menu.append_item(ALIGN_OBJECTS_SOUTH, "align-objects-south")
        self.menu.append_item(ALIGN_OBJECTS_SOUTHEAST, "align-objects-southeast")
        self.menu.append_item(ALIGN_OBJECTS_WEST, "align-objects-west")
        self.menu.append_item(ALIGN_OBJECTS_CENTER_BOTH, "align-objects-center-both")
        self.menu.append_item(ALIGN_OBJECTS_EAST, "align-objects-east")
        self.menu.append_item(ALIGN_OBJECTS_CENTER_HORIZONTAL, "align-objects-center-horizontal")
        self.menu.append_item(ALIGN_OBJECTS_CENTER_VERTICAL, "align-objects-center-vertical")
        self.menu.ascend()
        self.menu.append_menu(_("Paper alignment"), True)
        self.menu.append_item(ALIGN_PAPER_NORTHWEST, "align-paper-northwest")
        self.menu.append_item(ALIGN_PAPER_NORTH, "align-paper-north")
        self.menu.append_item(ALIGN_PAPER_NORTHEAST, "align-paper-northeast")
        self.menu.append_item(ALIGN_PAPER_SOUTHWEST, "align-paper-southwest")
        self.menu.append_item(ALIGN_PAPER_SOUTH, "align-paper-south")
        self.menu.append_item(ALIGN_PAPER_SOUTHEAST, "align-paper-southeast")
        self.menu.append_item(ALIGN_PAPER_WEST, "align-paper-west")
        self.menu.append_item(ALIGN_PAPER_CENTER_BOTH, "align-paper-center-both")
        self.menu.append_item(ALIGN_PAPER_EAST, "align-paper-east")
        self.menu.append_item(ALIGN_PAPER_CENTER_HORIZONTAL, "align-paper-center-horizontal")
        self.menu.append_item(ALIGN_PAPER_CENTER_VERTICAL, "align-paper-center-vertical")
        self.menu.ascend()

        self.menu.append_menu(_("Window"))
        self.menu.append_item(Gtk.STOCK_FULLSCREEN, "fullscreen", "<Control>F")

        self.menu.append_menu(_("Help"), right=True)
        self.menu.append_item(Gtk.STOCK_HELP, "help", "F1")
        self.menu.append_separator()
        self.menu.append_item(Gtk.STOCK_ABOUT, "about")

        self.menu.show_all()

        htoolbar = Toolbar(HORIZONTAL)
        vbox.pack_start(htoolbar, False, False, 0)

        htoolbar.append(Gtk.STOCK_NEW, "new")
        htoolbar.append(Gtk.STOCK_OPEN, "open")
        htoolbar.append(Gtk.STOCK_SAVE, "save")
        htoolbar.append_separator()
        htoolbar.append(Gtk.STOCK_PRINT, "print")
        htoolbar.append_separator()
        htoolbar.append(Gtk.STOCK_UNDO, "undo")
        htoolbar.append(Gtk.STOCK_REDO, "redo")
        htoolbar.append_separator()
        htoolbar.append(Gtk.STOCK_CUT, "cut")
        htoolbar.append(Gtk.STOCK_COPY, "copy")
        htoolbar.append(Gtk.STOCK_PASTE, "paste")
        htoolbar.append_separator()
        htoolbar.append(Gtk.STOCK_DELETE, "delete")
        htoolbar.append_separator()
        htoolbar.append_with_submenu(LINE_STYLE_CONTINUOUS, "line-style-continuous")
        htoolbar.append_to_submenu(LINE_STYLE_POINT_DASH, "line-style-point-dash")
        htoolbar.append_to_submenu(LINE_STYLE_POINT, "line-style-point")
        htoolbar.append_to_submenu(LINE_STYLE_DASH, "line-style-dash")
        htoolbar.append_separator()
        htoolbar.append_with_submenu(Gtk.STOCK_ZOOM_FIT, "zoom-fit")
        htoolbar.append_to_submenu(Gtk.STOCK_ZOOM_100, "zoom-100")
        htoolbar.append_to_submenu(Gtk.STOCK_ZOOM_IN, "zoom-in")
        htoolbar.append_to_submenu(Gtk.STOCK_ZOOM_OUT, "zoom-out")
        htoolbar.append_separator()
        htoolbar.append_toggle(MARGINS_ENABLED, "margins")
        htoolbar.append_toggle(GRID, "grid")
        htoolbar.append_toggle(GUIDES, "guides")
        htoolbar.append_toggle(SNAP_ENABLED, "snap")
        htoolbar.append_separator()
        htoolbar.append(EXPORT_TO_PDF, "export-to-pdf")
        htoolbar.append_separator()
        htoolbar.append_toggle(GROUP, "group")
        htoolbar.append_separator()
        htoolbar.append(BRING_TO_FRONT, "bring-to-front")
        htoolbar.append(BRING_TO_BACK, "bring-to-back")
        htoolbar.append_separator()
        htoolbar.append_with_submenu(ALIGN_OBJECTS_CENTER_BOTH, "align-object-center-both")
        htoolbar.append_to_submenu(ALIGN_OBJECTS_NORTHWEST, "align-object-northwest")
        htoolbar.append_to_submenu(ALIGN_OBJECTS_NORTH, "align-object-north")
        htoolbar.append_to_submenu(ALIGN_OBJECTS_SOUTHWEST, "align-object-southwest")
        htoolbar.append_to_submenu(ALIGN_OBJECTS_NORTHEAST, "align-object-northeast")
        htoolbar.append_to_submenu(ALIGN_OBJECTS_SOUTH, "align-object-south")
        htoolbar.append_to_submenu(ALIGN_OBJECTS_SOUTHEAST, "align-object-southeast")
        htoolbar.append_to_submenu(ALIGN_OBJECTS_WEST, "align-object-west")
        htoolbar.append_to_submenu(ALIGN_OBJECTS_EAST, "align-object-east")
        htoolbar.append_to_submenu(ALIGN_OBJECTS_CENTER_HORIZONTAL, "align-object-center-horizontal")
        htoolbar.append_to_submenu(ALIGN_OBJECTS_CENTER_VERTICAL, "align-object-center-vertical")
        htoolbar.append_with_submenu(ALIGN_PAPER_CENTER_BOTH, "align-paper-center-both")
        htoolbar.append_to_submenu(ALIGN_PAPER_NORTHWEST, "align-paper-northwest")
        htoolbar.append_to_submenu(ALIGN_PAPER_NORTH, "align-paper-north")
        htoolbar.append_to_submenu(ALIGN_PAPER_SOUTHWEST, "align-paper-southwest")
        htoolbar.append_to_submenu(ALIGN_PAPER_NORTHEAST, "align-paper-northeast")
        htoolbar.append_to_submenu(ALIGN_PAPER_SOUTH, "align-paper-south")
        htoolbar.append_to_submenu(ALIGN_PAPER_SOUTHEAST, "align-paper-southeast")
        htoolbar.append_to_submenu(ALIGN_PAPER_WEST, "align-paper-west")
        htoolbar.append_to_submenu(ALIGN_PAPER_EAST, "align-paper-east")
        htoolbar.append_to_submenu(ALIGN_PAPER_CENTER_HORIZONTAL, "align-paper-center-horizontal")
        htoolbar.append_to_submenu(ALIGN_PAPER_CENTER_VERTICAL, "align-paper-center-vertical")
        htoolbar.append_separator()
        htoolbar.append(Gtk.STOCK_HELP, "help")

        hbox = Gtk.HBox()
        vbox.add(hbox)

        vtoolbar = Toolbar()
        vtoolbar.set_style(Gtk.ToolbarStyle.ICONS)
        hbox.pack_start(vtoolbar, False, False, 0)

        vtoolbar.append(LINE, "line")
        vtoolbar.append(ARC, "arc")
        vtoolbar.append(CURVE, "curve")
        vtoolbar.append(CONNECTOR, "connector")
        vtoolbar.append_with_submenu(BOX, "box")
        vtoolbar.append_to_submenu(SPLIT_HORIZONTALLY, "split-horizontally")
        vtoolbar.append_to_submenu(SPLIT_VERTICALLY, "split-vertically")
        vtoolbar.append_to_submenu(REMOVE_SPLIT, "remove-split")
        vtoolbar.append(ROUNDED_BOX, "rounded-box")
        vtoolbar.append(TEXT, "text")
        vtoolbar.append(BARCODE, "barcode")
        vtoolbar.append(TABLE, "table")
        vtoolbar.append(CHART, "chart")
        vtoolbar.append(IMAGE, "image")

        notebook = Gtk.Notebook()
        notebook.set_show_tabs(True)
        notebook.set_show_border(False)
        #notebook.set_tab_pos(Gtk.PositionType.LEFT)
        notebook.set_tab_pos(Gtk.PositionType.RIGHT)
        hbox.add(notebook)

        self.status = Statusbar()
        self.id = self.status.get_context_id(_("Edit mode"))
        vbox.pack_start(self.status, False, False, 0)

        label = Gtk.Label(label=_("Design view"))
        label.set_angle(90)

        self.editor = Editor(self)
        self.editor.set_paper()
        notebook.append_page(self.editor, label)

        label = Gtk.Label(label=_("XML view"))
        label.set_angle(90)

        def get_source_view():
            source = Gtk.ScrolledWindow()
            source.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

            view = Gtk.TextView()
            self.code = Gtk.TextBuffer()
            view.set_buffer(self.code)
            source.add(view)

            return source

        if '--source-editor-test' in sys.argv:
            while True:
                try:
                    from ui.code_editor import SourcePad
                except:
                    source = get_source_view()
                    break

                source = SourcePad(self)
                self.code = source.buffer
                source.set_language("xml")
                break
        else:
            source = get_source_view()

        notebook.append_page(source, label)

        self.menu.connect("new", self.new)
        self.menu.connect("open", self.open)
        self.menu.connect("save", self.save)
        self.menu.connect("save-as", self.save_as)
        self.menu.connect("page-setup", self.page_setup)
        self.menu.connect("export-to-pdf", self.export_to_pdf)
        self.menu.connect("set-background", self.set_background)
        self.menu.connect("quit", self.quit)

        self.menu.connect("cut", self.editor.canvas.cut)
        self.menu.connect("copy", self.editor.canvas.copy)
        self.menu.connect("paste", self.editor.canvas.paste)
        self.menu.connect("delete", self.editor.canvas.delete)
        self.menu.connect("select-all", self.editor.canvas.select_all)

        self.menu.connect("margins", self.editor.canvas.toggle_margins)
        self.menu.connect("grid", self.editor.canvas.toggle_grid)
        self.menu.connect("guides", self.editor.canvas.toggle_guides)
        self.menu.connect("snap", self.editor.canvas.toggle_snap)
        self.menu.connect("hints", self.editor.canvas.toggle_hints)
        self.menu.connect("properties", self.editor.toggle_properties)
        self.menu.connect("menubar", self.toggle_menubar)
        self.menu.connect("statusbar", self.toggle_statusbar)

        self.menu.connect("bring-to-front", self.editor.canvas.bring_to_front)
        self.menu.connect("bring-to-back", self.editor.canvas.bring_to_back)

        self.menu.connect("align-paper-center-horizontal", self.editor.canvas.paper_center_horizontal)

        self.menu.connect("line", self.create, "Line")
        self.menu.connect("curve", self.create, "Curve")
        self.menu.connect("connector", self.create, "Connector")
        self.menu.connect("box", self.create, "Box")
        self.menu.connect("rounded-box", self.create, "Rounded")
        self.menu.connect("text", self.create, "Text")
        self.menu.connect("barcode", self.create, "BarCode")
        self.menu.connect("table", self.create, "Table")
        self.menu.connect("image", self.create, "Image")
        self.menu.connect("chart", self.create, "Chart")

        self.menu.connect("fullscreen", self.fullscreen)
        self.menu.connect("about", self.about)
        self.menu.connect("help", self.help)

        self.menu.connect("split-horizontally", self.editor.canvas.split_horizontally)
        self.menu.connect("split-vertically", self.editor.canvas.split_vertically)
        self.menu.connect("remove-split", self.editor.canvas.remove_split)

        htoolbar.connect("new", self.new)
        htoolbar.connect("open", self.open)
        htoolbar.connect("save", self.save)
        htoolbar.connect("snap", self.editor.canvas.toggle_snap)
        htoolbar.connect("grid", self.editor.canvas.toggle_grid)
        htoolbar.connect("guides", self.editor.canvas.toggle_guides)
        htoolbar.connect("margins", self.editor.canvas.toggle_margins)
        htoolbar.connect("cut", self.editor.canvas.cut)
        htoolbar.connect("copy", self.editor.canvas.copy)
        htoolbar.connect("paste", self.editor.canvas.paste)
        htoolbar.connect("delete", self.editor.canvas.delete)
        htoolbar.connect("bring-to-front", self.editor.canvas.bring_to_front)
        htoolbar.connect("bring-to-back", self.editor.canvas.bring_to_back)
        htoolbar.connect("export-to-pdf", self.export_to_pdf)
        htoolbar.connect("help", self.help)

        vtoolbar.connect("line", self.create, "Line")
        vtoolbar.connect("arc", self.create, "Arc")
        vtoolbar.connect("curve", self.create, "Curve")
        vtoolbar.connect("connector", self.create, "Connector")
        vtoolbar.connect("box", self.create, "Box")
        vtoolbar.connect("rounded-box", self.create, "Rounded")
        vtoolbar.connect("text", self.create, "Text")
        vtoolbar.connect("barcode", self.create, "BarCode")
        vtoolbar.connect("table", self.create, "Table")
        vtoolbar.connect("image", self.create, "Image")
        vtoolbar.connect("chart", self.create, "Chart")

        vtoolbar.connect("split-horizontally", self.editor.canvas.split_horizontally)
        vtoolbar.connect("split-vertically", self.editor.canvas.split_vertically)
        vtoolbar.connect("remove-split", self.editor.canvas.remove_split)

        notebook.connect("switch-page", self.switch)

        self.connect("key-press-event", self.key_press)

    def run(self):
       self.show_all()
       Gtk.main()

    def update_title(self):
        document = self.filename if self.filename else _("New document")
        title = _("%(document)s - Sanaviron %(version)s") % {"document": document, "version": VERSION}
        self.set_title(title)

    def disable_bindings(self):
        self.remove_accel_group(self.bindings)

    def enable_bindings(self):
        self.add_accel_group(self.bindings)

    def switch(self, widget, child, page):
        document = self.editor.canvas.serialize()
        self.code.set_text(str(document))

    def key_handler(self, keyname):
        if keyname == "<Control><Shift>V":
            self.editor.canvas.add_box_separator_vertical()
        if keyname == "<Control><Shift>H":
            self.editor.canvas.add_box_separator_horizontal()
        if keyname == "<Control><Shift>Escape":
            self.toggle_menubar()
        if keyname in ["<Control><Shift>Colon", "<Control><Shift>Period"]:
            self.editor.canvas.hints ^= 1
            self.editor.canvas.update()

    def key_press(self, widget, event):
        keyval = event.keyval
        keyname = Gdk.keyval_name(keyval)
        if keyname and (keyname.startswith('Control') or \
                        keyname.startswith('Shift') or \
                        keyname.startswith('Alt')):
            return False
        keyname = keyname.capitalize()
        if event.get_state() & Gdk.ModifierType.SHIFT_MASK:
            keyname = "<Shift>%s" % keyname
        if event.get_state() & Gdk.ModifierType.CONTROL_MASK:
            keyname = "<Control>%s" % keyname
        self.key_handler(keyname)
        return False

    def toggle_menubar(self, *args):
        if self.menu.get_visible():
            self.menu.hide()
            self.editor.notification.notificate(_("Press <i><b>Control+Shift+Escape</b></i> to show again."),
                                                INFORMATION)
        else:
            self.menu.show()

    def toggle_statusbar(self, *args):
        if self.status.get_visible():
            self.status.hide()
        else:
            self.status.show()

    def new(self, widget, data):
        self.editor.canvas.children = list()
        self.editor.canvas.queue_draw()

    def open(self, widget, data):
        # XXX funcional
        dialog = Gtk.FileChooserDialog(title=_("Open document"),
            parent=self,
            action=Gtk.FileChooserAction.OPEN,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                     Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))

        dialog.set_transient_for(self)
        dialog.set_default_response(Gtk.ResponseType.OK)

        filter = Gtk.FileFilter()
        filter.set_name(_("XML files"))
        filter.add_mime_type("document/xml")
        filter.add_pattern("*.xml")
        dialog.add_filter(filter)

        filter = Gtk.FileFilter()
        filter.set_name(_("All files"))
        filter.add_pattern("*")
        dialog.add_filter(filter)

        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            filename = dialog.get_filename()
            self.filename = filename
            if filename is not None:
                self.editor.canvas.load_from_xml(filename)
                self.update_title()

        dialog.destroy()

    def save(self, widget, data):
        if not self.filename:
            return
        current = self.editor.canvas.serialize()
        original = open(self.filename).read()
        print(original)
        print(current)
        print("saving")
        return
        print("saving")
        #self.editor.canvas.save_to_xml(self.filename)

    def save_as(self, widget, data):
        dialog = Gtk.FileChooserDialog(title=_("Save document as"),
            parent=self,
            action=Gtk.FileChooserAction.SAVE,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                     Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))

        dialog.set_transient_for(self)
        dialog.set_default_response(Gtk.ResponseType.ACCEPT)

        filter = Gtk.FileFilter()
        filter.set_name(_("XML files"))
        filter.add_mime_type("document/xml")
        filter.add_pattern("*.xml")
        dialog.add_filter(filter)

        filter = Gtk.FileFilter()
        filter.set_name(_("All files"))
        filter.add_pattern("*")
        dialog.add_filter(filter)

        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            filename = dialog.get_filename()
            self.filename = filename
            if filename is not None:
                self.editor.canvas.save_to_xml(filename)
                self.update_title()

        dialog.destroy()

    def page_setup(self, widget, data):
        self.setup.settings = self.settings
        self.setup = Gtk.print_run_page_setup_dialog(self, self.setup, self.settings)

        size = self.setup.get_paper_size()
        orientation = self.setup.get_orientation()

        # TODO canvas->margins
        for page in self.editor.canvas.pages:
            page.top = self.setup.get_top_margin(Gtk.UNIT_POINTS)
            page.left = self.setup.get_left_margin(Gtk.UNIT_POINTS)
            page.bottom = self.setup.get_bottom_margin(Gtk.UNIT_POINTS)
            page.right = self.setup.get_right_margin(Gtk.UNIT_POINTS)

        width = size.get_width(Gtk.UNIT_POINTS)
        height = size.get_height(Gtk.UNIT_POINTS)

        # no int
        if orientation in (Gtk.PAGE_ORIENTATION_PORTRAIT, Gtk.PAGE_ORIENTATION_REVERSE_PORTRAIT):
            orientation = _("Vertical")
            width = int(width)
            height = int(height)
        else:
            orientation = _("Landscape")
            saved_height = height
            height = int(width)
            width = int(saved_height)

        # TODO: canvas->page_size
        for page in self.editor.canvas.pages:
            page.width = width
            page.height = height

        name = size.get_display_name()
        text = "%s %s (%d dots x %d dots)" % (name, orientation, width, height)
        self.status.push(self.id, text)
        self.editor.canvas.queue_draw()

    def export_to_pdf(self, widget, format):
        dialog = Gtk.FileChooserDialog(title=_("Save PDF file as"),
            parent=self,
            action=Gtk.FileChooserAction.SAVE,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                     Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))

        dialog.set_transient_for(self)
        dialog.set_default_response(Gtk.ResponseType.ACCEPT)

        filter = Gtk.FileFilter()
        filter.set_name(_("PDF files"))
        filter.add_mime_type("document/pdf")
        filter.add_pattern("*.pdf")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            filename = dialog.get_filename()
            if filename is not None:
                self.editor.canvas.save_to_pdf(filename)

        dialog.destroy()

    def set_background(self, widget, data):
        dialog = Gtk.FileChooserDialog(title=_("Select background"),
            parent=self,
            action=Gtk.FileChooserAction.OPEN,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                     Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))

        def update_preview(dialog, preview):
            filename = dialog.get_preview_filename()
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filename, 128,
                                                              128)
                preview.set_from_pixbuf(pixbuf)
                have_preview = True
            except:
                have_preview = False
            dialog.set_preview_widget_active(have_preview)

        preview = Gtk.Image()

        dialog.set_preview_widget(preview)
        dialog.connect("update-preview", update_preview, preview)

        dialog.set_transient_for(self)

        def add_filter(dialog, name, pattern, type=None):
            filter = Gtk.FileFilter()
            filter.set_name(name)
            if type:
                filter.add_mime_type(type)
            filter.add_pattern(pattern)
            dialog.add_filter(filter)

        add_filter(dialog, "PNG files", "*.png", "image/png")
        add_filter(dialog, "JPG files", "*.jpg", "image/jpg")
        add_filter(dialog, "All files", "*")

        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            filename = dialog.get_filename()
            self.filename = filename
            if filename is not None:
                self.editor.canvas.document.pages[0].background = filename
                self.editor.canvas.update ()

        dialog.destroy()

    def fullscreen(self, widget, data):
        if not self.winstate:
            self.winstate = not self.winstate
            self.window.fullscreen()
        else:
            self.window.unfullscreen()

    def quit(self, widget, event):
        print("Motion events:", self.editor.canvas.statics.motion)
        print("Expose events:", self.editor.canvas.statics.expose)
        print("Consumed motion events:", self.editor.canvas.statics.consumed.motion)
        print("Bye ;-)")
        Gtk.main_quit()
        return True

    create = lambda self, widget, data, name: self.editor.canvas.create(Shape(name))

    def help(self, widget, data):
        cwd = os.getcwd()
        language = get_parsed_language()
        url = 'file://%s/../doc/help/%s/index.html' % (cwd, language)
        import webbrowser

        webbrowser.open_new(url)

    def about(self, widget, data):
        dialog = Gtk.AboutDialog()
        dialog.set_transient_for(self)
        dialog.set_program_name("sanaviron")
        dialog.set_name("sanaviron")
        dialog.set_version(VERSION)
        dialog.set_copyright("Copyright 2012 - Juan Manuel Mouriz, Ivlev Denis")
        dialog.set_comments(_("A program to design reports, invoices, documents, labels and more. Based on the 2D "
                              "drawing engine \"sanaviron\".\n\n" + get_summary()))
        dialog.set_website("http://www.sanaviron.org/")
        dialog.set_website_label(_("Official site"))
        dialog.set_license(open(os.path.join(os.path.dirname(__file__),  "..", "..", "COPYING")).read())
        dialog.set_wrap_license(False)
        dialog.set_authors(["Juan Manuel Mouriz <jmouriz@sanaviron.org>", "Ivlev Denis <ivlevdenis.ru@gmail.com>"])
        dialog.set_documenters([_("Undocumented yet :'(")])
        dialog.set_artists(["Juan Manuel Mouriz <jmouriz@sanaviron.org>", "Ivlev Denis <ivlevdenis.ru@gmail.com>"])
        dialog.set_translator_credits("Juan Manuel Mouriz <jmouriz@sanaviron.org> " + _(
            "(Spanish)") + "\n" + "Ivlev Denis <ivlevdenis.ru@gmail.com> " + _("(Russian)"))
        logo = GdkPixbuf.Pixbuf.new_from_file(os.path.join(os.path.dirname(__file__), "..", "images", "canvas-logo.png"))
        dialog.set_logo(logo)
        #dialog.set_logo_icon_name(self.icon_name)
        dialog.run()
        dialog.destroy()
