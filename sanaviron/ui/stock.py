#!/usr/bin/python
# -*- coding: utf-8 -*-
__all__ = ['ALIGN_OBJECTS_CENTER_BOTH', 'ALIGN_OBJECTS_CENTER_HORIZONTAL', 'ALIGN_OBJECTS_CENTER_VERTICAL',
           'ALIGN_OBJECTS_EAST', 'ALIGN_OBJECTS_NORTH', 'ALIGN_OBJECTS_NORTHEAST', 'ALIGN_OBJECTS_NORTHWEST',
           'ALIGN_OBJECTS_SOUTH', 'ALIGN_OBJECTS_SOUTHEAST', 'ALIGN_OBJECTS_SOUTHWEST', 'ALIGN_OBJECTS_WEST',
           'ALIGN_PAPER_CENTER_BOTH', 'ALIGN_PAPER_CENTER_HORIZONTAL', 'ALIGN_PAPER_CENTER_VERTICAL', 'ALIGN_PAPER_EAST',
           'ALIGN_PAPER_NORTH', 'ALIGN_PAPER_NORTHEAST', 'ALIGN_PAPER_NORTHWEST', 'ALIGN_PAPER_SOUTH',
           'ALIGN_PAPER_SOUTHEAST', 'ALIGN_PAPER_SOUTHWEST', 'ALIGN_PAPER_WEST', 'ARC', 'GUIDES', 'BARCODE', 'BOX',
           'BRING_TO_BACK', 'BRING_TO_FRONT', 'CHART', 'CURVE', 'EXPORT_TO_PDF', 'CONNECTOR', 'GRID', 'GROUP', 'IMAGE',
           'LINE', 'LINE_STYLE_CONTINUOUS', 'LINE_STYLE_DASH', 'LINE_STYLE_POINT', 'LINE_STYLE_POINT_DASH',
           'MARGINS_DISABLED', 'MARGINS_ENABLED', 'ROUNDED_BOX', 'SNAP_DISABLED', 'SNAP_ENABLED', 'TABLE', 'TEXT',
           'UNGROUP', 'EXPAND_PROPERTIES', 'CONTRACT_PROPERTIES', 'SPLIT_HORIZONTALLY', 'SPLIT_VERTICALLY',
           'REMOVE_SPLIT', 'SET_BACKGROUND']
           
import gtk

def register(name, label, key):
    filename = "%s.png" % name
    import os

    filename = os.path.join(os.path.dirname(__file__), "stock", filename)
    domain = "sanaviron"
    id = "%s-stock-%s" % (domain, name)
    pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
    iconset = gtk.IconSet(pixbuf)
    factory = gtk.IconFactory()
    factory.add(id, iconset)
    factory.add_default()
    keyval = gtk.gdk.keyval_from_name(key)
    modifier = gtk.gdk.MOD1_MASK
    gtk.stock_add([(id, label, modifier, keyval, domain)])
    return id

ALIGN_OBJECTS_CENTER_BOTH = register("align-objects-center-both", _("Center"), "X")
ALIGN_OBJECTS_CENTER_HORIZONTAL = register("align-objects-center-horizontal", _("Center horizontally"), "X")
ALIGN_OBJECTS_CENTER_VERTICAL = register("align-objects-center-vertical", _("Center vertically"), "X")
ALIGN_OBJECTS_EAST = register("align-objects-east", _("Align to east"), "X")
ALIGN_OBJECTS_NORTHEAST = register("align-objects-northeast", _("Align to northeast"), "X")
ALIGN_OBJECTS_NORTH = register("align-objects-north", _("Align to north"), "X")
ALIGN_OBJECTS_SOUTH = register("align-objects-south", _("Align to south"), "X")
ALIGN_OBJECTS_NORTHWEST = register("align-objects-northwest", _("Align to northwest"), "X")
ALIGN_OBJECTS_SOUTHEAST = register("align-objects-southeast", _("Align to southeast"), "X")
ALIGN_OBJECTS_SOUTHWEST = register("align-objects-southwest", _("Align to southwest"), "X")
ALIGN_OBJECTS_WEST = register("align-objects-west", _("Align to west"), "X")
ALIGN_PAPER_CENTER_BOTH = register("align-paper-center-both", _("Center in paper"), "X")
ALIGN_PAPER_CENTER_HORIZONTAL = register("align-paper-center-horizontal", _("Center horizontally in paper"), "X")
ALIGN_PAPER_CENTER_VERTICAL = register("align-paper-center-vertical", _("Center vertically in paper"), "X")
ALIGN_PAPER_EAST = register("align-paper-east", _("Align to east of paper"), "X")
ALIGN_PAPER_NORTHEAST = register("align-paper-northeast", _("Align to northeast of paper"), "X")
ALIGN_PAPER_NORTH = register("align-paper-north", _("Align to north of paper"), "X")
ALIGN_PAPER_SOUTH = register("align-paper-south", _("Align to sourth of paper"), "X")
ALIGN_PAPER_NORTHWEST = register("align-paper-northwest", _("Align to northwest of paper"), "X")
ALIGN_PAPER_SOUTHEAST = register("align-paper-southeast", _("Align to southeast of paper"), "X")
ALIGN_PAPER_SOUTHWEST = register("align-paper-southwest", _("Align to southwest of paper"), "X")
ALIGN_PAPER_WEST = register("align-paper-west", _("Align to west of paper"), "X")
BRING_TO_FRONT = register("bring-to-front", _("Bring to front"), "X")
BRING_TO_BACK = register("bring-to-back", _("Bring to back"), "X")
BOX = register("box", _("Box"), "X")
IMAGE = register("image", _("Image"), "X")
LINE = register("line", _("Line"), "X")
ARC = register("arc", _("Arc"), "X")
CURVE = register("curve", _("Curve"), "X")
CONNECTOR = register("connector", _("Connector"), "X")
ROUNDED_BOX = register("rounded-box", _("Rounded box"), "X")
TEXT = register("text", _("Text"), "X")
BARCODE = register("barcode", _("Barcode"), "X")
TABLE = register("table", _("Table"), "X")
CHART = register("chart", _("Chart"), "X")
GROUP = register("group", _("Group"), "X")
UNGROUP = register("ungroup", _("Ungroup"), "X")
GUIDES = register("guides", _("Guides"), "X")
GRID = register("grid", _("Grid"), "X")
SNAP_ENABLED = register("snap-enabled", _("Enable snap"), "X")
SNAP_DISABLED = register("snap-disabled", _("Disable snap"), "X")
MARGINS_ENABLED = register("margins-enabled", _("Show margins"), "X")
MARGINS_DISABLED = register("margins-disabled", _("Hide margins"), "X")
LINE_STYLE_CONTINUOUS = register("line-style-continuous", _("Continuous line"), "X")
LINE_STYLE_POINT = register("line-style-point", _("Dotted line"), "X")
LINE_STYLE_DASH = register("line-style-dash", _("Dashed line"), "X")
LINE_STYLE_POINT_DASH = register("line-style-point-dash", _("Axis line"), "X")
EXPORT_TO_PDF = register("export-to-pdf", _("Export to PDF"), "X")
EXPAND_PROPERTIES = register("expand-properties", _("Expand properties"), "X")
CONTRACT_PROPERTIES = register("contract-properties", _("Contract properties"), "X")
SPLIT_HORIZONTALLY = register("split-horizontally", _("Split horizontally"), "X")
SPLIT_VERTICALLY = register("split-vertically", _("Split vertically"), "X")
REMOVE_SPLIT = register("remove-split", _("Remove split"), "X")
SET_BACKGROUND = register("set-background", _("Set background"), "X")
