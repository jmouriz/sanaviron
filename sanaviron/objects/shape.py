#!/usr/bin/python
# -*- coding: utf-8 -*-

from arc import Arc
from barcode import BarCode
from box import Box
from chart import Chart
from curve import Curve
from connector import Connector
from image import Image
from line import Line
from rounded import Rounded
from table import Table
from text import Text

class Shape(object):
    def __new__(self, shape):
        if shape == "Chart":
            return Chart()
        if shape == "Image":
            return Image()
        if shape == "Table":
            return Table()
        if shape == "BarCode":
            return BarCode()
        if shape == "Text":
            return Text()
        if shape == "Rounded":
            return Rounded()
        if shape == "Box":
            return Box()
        if shape == "Connector":
            return Connector()
        if shape == "Curve":
            return Curve()
        if shape == "Line":
            return Line()
        if shape == "Arc":
            return Arc()

        return None