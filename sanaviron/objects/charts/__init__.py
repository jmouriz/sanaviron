# -*- coding: utf-8 -*-
# Copyright(c) 2007-2009 by Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
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

version = "0.5.1dev"

from objects.charts.bar import HorizontalBarChart, VerticalBarChart
from objects.charts.line import LineChart
from objects.charts.pie import PieChart
from objects.charts.scatter import ScatterplotChart
from objects.charts.stackedbar import StackedVerticalBarChart, StackedHorizontalBarChart

CHART_TYPES = (
    VerticalBarChart,
    HorizontalBarChart,
    LineChart,
    PieChart,
    ScatterplotChart,
    StackedVerticalBarChart,
    StackedHorizontalBarChart,
    )

VERTICAL_BAR_CHART_TYPE = 0
HORIZONTAL_BAR_CHART_TYPE = 1
LINE_CHART_TYPE = 2
PIE_CHART_TYPE = 3
SCATTER_PLOT_CHART_TYPE = 4
STACKED_VERTICAL_BAR_CHART_TYPE = 5
STACKED_HORIZONTAL_BAR_CHART_TYPE = 6

chart_types = {
    _("Verticals bars"): VERTICAL_BAR_CHART_TYPE, # Barras verticales
    _("Horizontals bars"): HORIZONTAL_BAR_CHART_TYPE, # Barras horizontales
    _("Lines"): LINE_CHART_TYPE, # Líneas
    _("Pie"): PIE_CHART_TYPE, # Torta circular
    _("Scatter plot"): SCATTER_PLOT_CHART_TYPE, # Puntos dispersos
    _("Stacked verticals bars"): STACKED_VERTICAL_BAR_CHART_TYPE, # Barras apiladas verticalmente
    _("Stacked horizontals bars"): STACKED_HORIZONTAL_BAR_CHART_TYPE, # Barras apiladas horizontalmente
    #"Líneas": LINE_CHART_TYPE,
    #"Torta circular": PIE_CHART_TYPE,
    #"Puntos dispersos": SCATTER_PLOT_CHART_TYPE,
    #"Barras apiladas": STACKED_VERTICAL_BAR_CHART_TYPE,
    }

#(VERTICAL_BAR_CHART_TYPE,
# HORIZONTAL_BAR_CHART_TYPE,
# LINE_CHART_TYPE,
# PIE_CHART_TYPE,
# SCATTER_PLOT_CHART_TYPE,
# STACKED_VERTICAL_BAR_CHART_TYPE,
# STACKED_HORIZONTAL_BAR_CHART_TYPE) = range(len(CHART_TYPES))

def get_chart_from_type(surface, type=PIE_CHART_TYPE, options=None):
    factory = CHART_TYPES[type]
    return factory(surface, options)
