#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['NONE', 'NORTHWEST', 'NORTH', 'NORTHEAST', 'WEST', 'EAST', 'SOUTHWEST', 'SOUTH', 'SOUTHEAST', 'ANONIMOUS',
           'MANUAL', 'AUTOMATIC', 'COLOR', 'GRADIENT', 'PATTERN', 'LINEAR', 'RADIAL', 'HORIZONTAL', 'VERTICAL', 'BOTH',
           'CENTIMETERS', 'MILLIMETERS', 'DOTS', 'INCHES', 'RADIANS', 'DEGREES', 'TOP_LEFT', 'TOP', 'TOP_RIGHT', 'RIGHT',
           'BOTTOM_RIGHT', 'BOTTOM', 'BOTTOM_LEFT', 'LEFT', 'CENTER','print_text', 'grad2rad', 'rad2grad',
           'angle_from_coordinates', 'get_side', 'opposite', 'set_as_point', 'get_default_font']

import pango, pangocairo,platform,gtk
from math import pi, atan2

NONE = -1

# direction
NORTHWEST = 0
NORTH = 1
NORTHEAST = 2
WEST = 3
EAST = 4
SOUTHWEST = 5
SOUTH = 6
SOUTHEAST = 7
ANONIMOUS = 8

MANUAL = 1
AUTOMATIC = 2

# fill type, type NONE present
COLOR = 0
GRADIENT = 1
PATTERN = 3

# gradient types
LINEAR = 0
RADIAL = 1

# orientation types
VERTICAL = 0
HORIZONTAL = 1
BOTH = 2

# units
CENTIMETERS = _("centimeters")
MILLIMETERS = _("millimeters")
DOTS = _("dots")
INCHES = _("inches")
RADIANS = _("radians")
DEGREES = _("degrees")

#text align types
LEFT = 0
RIGHT = 1
TOP = 2
BOTTOM = 3
CENTER = 4
TOP_LEFT = 5 
TOP_RIGHT = 6
BOTTOM_LEFT = 7
BOTTOM_RIGHT = 8

def get_default_font():
    if platform.system() == 'Windows':
        fontname = 'Sans'
    else:
        fontname = 'Ubuntu'
    return fontname


def grad2rad(grad):
    return float(grad) * pi / 180.0


def rad2grad(rad):
    return float(rad) * 180 / pi


def angle_from_coordinates(x, y, x0, y0, a, b):
    """
    calculation of the angle from coordinates
    """
    x = x - x0
    y = y - y0
    x /= a
    y /= b
    ang = atan2(y, x)
    ang = rad2grad(ang)
    if ang < 0:
        ang += 360
    return ang


def get_side(direction):
    if direction in [EAST, WEST]:
        return HORIZONTAL
    elif direction in [NORTH, SOUTH]:
        return VERTICAL
    else:
        return NONE


def opposite(direction):
    """
    opposite(direction)

    return opposite direction of input 'direction'

    direction is int see direction types
    """
    if direction == NORTHEAST:
        return SOUTHWEST
    elif direction == NORTH:
        return SOUTH
    elif direction == NORTHWEST:
        return SOUTHEAST
    elif direction == SOUTHEAST:
        return NORTHWEST
    elif direction == SOUTH:
        return NORTH
    elif direction == SOUTHWEST:
        return NORTHEAST
    elif direction == WEST:
        return EAST
    elif direction == EAST:
        return WEST
    return NONE


def set_as_point(instance):
    instance.x = 0.0
    instance.y = 0.0

def context_align(context,rect,align,lw,lh,border):
    """
    context_align(context,rect,align,lw,lh,border)


    context is cairo.Context
    rect is dict type {'x': int, 'y': int, 'w': int, 'h': int}
    align is int see align types
    lw is int width of object
    lh is int height of object
    border is int border size
    """
    if align is TOP_LEFT:
        context.translate(rect["x"] + border, rect["y"] + border)
    elif align is TOP:
        context.translate(rect['x'] + (rect["w"] - lw) * 0.5,
                        rect["y"] + border)
    elif align is TOP_RIGHT:
        context.translate(rect['x'] + rect['w'] - lw - border,
                        rect["y"] + border)
    elif align is RIGHT:
        context.translate(rect['x'] + rect['w'] - lw - border,
                        rect["y"] + (rect['h'] - lh) * 0.5)
    elif align is BOTTOM_RIGHT:
        context.translate(rect['x'] + rect['w'] - lw - border * 2,
                        rect['y'] + rect['h'] - lh - border)
    elif align is BOTTOM:
        context.translate(rect['x'] + (rect["w"] - lw) * 0.5,
                        rect['y'] + rect['h'] - lh - border)
        print(rect['x'] + (rect["w"] - lw) * 0.5,
              rect['y'] + rect['h'] - lh - border)
    elif align is BOTTOM_LEFT:
        context.translate(rect['x'] + border,
                        rect['y'] + rect['h'] - lh - border)
    elif align is LEFT:
        context.translate(rect['x'] + border,
                        rect["y"] + (rect['h'] - lh) * 0.5)
    elif align is CENTER:
        context.translate(rect['x'] + (rect["w"] - lw) * 0.5,
                        rect["y"] + (rect['h'] - lh) * 0.5)


def print_text(context, text="", rect={'x': 0, 'y': 0, 'w': 1, 'h': 1},
               font="",
               font_name="",
               font_style="", font_size=None,
               align=TOP_LEFT, border=4, letter_spacing=[(0,0)],scale=0):
    """
    print_text(context, text, rect,font,font_name,font_style, font_size,align, border, letter_spacing)

    context is cairo.Context
    text is any types
    rect is dict type {'x': int, 'y': int, 'w': int, 'h': int}
    font is string font description, example:'Ubuntu Normal 10' -- Ubuntu - font name,
                                                                   Normal - style,
                                                                   10-size
    if font != "" then font_name,font_style,font_size do not used!
    font_name is string
    font_style is string
    font_size is int
    align is int see align types
    border is int border size
    letter_spacing is list of tuple letter_spacing size,example: letter_spacing=[(2,3)(5,5)(10,0)]
                                                                 after the 2nd character letter spacing is 5
                                                                 after the 5th character letter spacing is 5
                                                                 after the 10th character letter spacing reset to 0
    """
    context.save()
    font = font or " ".join([font_name, font_style, str(font_size)]) or gtk.Style().font_desc.to_string()
    layout = pangocairo.CairoContext.create_layout(context)
    desc = pango.FontDescription(font)
    layout.set_font_description(desc)
    attr_list=pango.AttrList()
    if len(letter_spacing):
        for i in letter_spacing:
            attr = pango.AttrLetterSpacing(int(i[1]*pango.SCALE),i[0],len(text))
            attr_list.insert(attr)
    layout.set_attributes(attr_list)
    layout.set_markup(str(text))
    pangocairo.CairoContext.update_layout(context, layout)
    lw, lh = layout.get_size()
    lw /= pango.SCALE
    lh /= pango.SCALE
    context_align(context,rect,align,lw,lh,border)
    pangocairo.CairoContext.show_layout(context, layout)
    context.restore()
