#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo
from charts import PIE_CHART_TYPE, get_chart_from_type
from object import Object
from objects import *

class Chart(Object):
    """This class represents a chart"""
    __name__ = "Chart"

    def __init__(self, type=PIE_CHART_TYPE):
        Object.__init__(self)

    def get_properties(self):
        return Object.get_properties(self) + ["type"]

    def post(self):
        self.handler.control[NORTHWEST].x = self.x
        self.handler.control[NORTHWEST].y = self.y
        self.handler.control[NORTHEAST].x = self.x + self.width
        self.handler.control[NORTHEAST].y = self.y
        self.handler.control[SOUTHWEST].x = self.x
        self.handler.control[SOUTHWEST].y = self.y + self.height
        self.handler.control[SOUTHEAST].x = self.x + self.width
        self.handler.control[SOUTHEAST].y = self.y + self.height
        self.handler.control[NORTH].x = self.x + self.width / 2
        self.handler.control[NORTH].y = self.y
        self.handler.control[SOUTH].x = self.x + self.width / 2
        self.handler.control[SOUTH].y = self.y + self.height
        self.handler.control[WEST].x = self.x
        self.handler.control[WEST].y = self.y + self.height / 2
        self.handler.control[EAST].x = self.x + self.width
        self.handler.control[EAST].y = self.y + self.height / 2

    def draw(self, context):
        type = self.get_property('type')

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(self.width), int(self.height))

        lines = (
            ('AMD Athlon II X3 425', 34.5),
            ('Intel Celeron E3300 @ 2.50GHz', 31),
            ('AMD Athlon II X2 240', 30.7),
            ('AMD Phenom 9750 Quad-Core', 29.9),
            ('AMD Athlon 64 X2 Dual Core 6000+', 29.2),
            ('Dual-Core AMD Opteron 1216', 27.1),
            ('AMD Sempron 140', 26.3),
            ('Pentium Dual-Core E5400 @ 2.70GHz', 24.7),
            ('Intel Core i7 920 @ 2.67GHz', 19.3),
            ('Intel Core2 Quad Q8200 @ 2.33GHz', 17.7),
            ('Intel Core2 Duo E7500 @ 2.93GHz', 17.2),
            )

        options = {
            'axis': {
                'x': {
                    'ticks': [dict(v=i, label=l[0]) for i, l in enumerate(lines)],
                    'label': 'Microprocesador',
                    'rotate': 25,
                    },
                'y': {
                    'tickCount': 4,
                    'rotate': 25,
                    'label': 'Relación precio rendimiento'
                }
            },

            'legend': {
                'hide': True,
                },
            }

        chart = get_chart_from_type(surface, type, options)

        dataSet = (
            ('AMD Athlon II X3 425', ((0, 34.5), )),
            ('Intel Celeron E3300 @ 2.50GHz', ((0, 31), )),
            ('AMD Athlon II X2 240', ((0, 30.7), )),
            ('AMD Phenom 9750 Quad-Core', ((0, 29.9), )),
            ('AMD Athlon 64 X2 Dual Core 6000+', ((0, 29.2), )),
            ('Dual-Core AMD Opteron 1216', ((0, 27.1), )),
            ('AMD Sempron 140', ((0, 26.3), )),
            ('Pentium Dual-Core E5400 @ 2.70GHz', ((0, 24.7), )),
            ('Intel Core i7 920 @ 2.67GHz', ((0, 19.3), )),
            ('Intel Core2 Quad Q8200 @ 2.33GHz', ((0, 17.7), )),
            ('Intel Core2 Duo E7500 @ 2.93GHz', ((0, 17.2), )),
            )

        chart.addDataset(dataSet)
        chart.render()
        context.set_source_surface(surface, self.x, self.y)
        context.paint()
        Object.draw(self, context)
