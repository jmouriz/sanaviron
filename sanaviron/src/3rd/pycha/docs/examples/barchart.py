# Copyright (c) 2007-2008 by Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
#
# This file is part of PyCha.
#
# PyCha is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyCha is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PyCha.  If not, see <http://www.gnu.org/licenses/>.

import sys

import cairo

import pycha.bar

import precip

def barChart(output, chartFactory):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 300)

    dataSet = (
        ('Tainan', [(i, l[1]) for i, l in enumerate(precip.Tainan)]),
        ('Paris', [(i, l[1]) for i, l in enumerate(precip.Paris)]),
        )

    options = {
        'axis': {
            'x': {
                'ticks': [dict(v=i, label=l[0]) for i, l in enumerate(precip.Tainan)],
                'label': 'Month',
                'rotate': 25,
                },
            'y': {
                'tickCount': 4,
                'rotate': 25,
                'label': 'Precipitation (mm)'
            }
        },
        'background': {
            'chartColor': '#d8e7ec',
            'baseColor': '#efebe7',
            'lineColor': '#444444'
        },
        'colorScheme': '#6eafc1',
        'legend': {
            'hide': False,
            'position': {'top': 5, 'left': 5},
            },
        'padding': {
            'left': 135,
            'bottom': 55,
            },
        'title': 'Monthly Precipitation'
    }
    chart = chartFactory(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(output)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        output = sys.argv[1]
    else:
        output = 'barchart.png'
    barChart('v' + output, pycha.bar.VerticalBarChart)
    barChart('h' + output, pycha.bar.HorizontalBarChart)
