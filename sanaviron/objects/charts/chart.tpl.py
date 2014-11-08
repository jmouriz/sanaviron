from charts.bar import HorizontalBarChart, VerticalBarChart
from charts.line import LineChart
from charts.pie import PieChart
from charts.scatter import ScatterplotChart
from charts.stackedbar import StackedVerticalBarChart, StackedHorizontalBarChart

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
    #"Barras verticales": VERTICAL_BAR_CHART_TYPE,
    #"Barras horizontales": HORIZONTAL_BAR_CHART_TYPE,
    #"Líneas": LINE_CHART_TYPE,
    #"Torta circular": PIE_CHART_TYPE,
    #"Puntos dispersos": SCATTER_PLOT_CHART_TYPE,
    #"Barras apiladas verticalmente": STACKED_VERTICAL_BAR_CHART_TYPE,
    #"Barras apiladas horizontalmente": STACKED_HORIZONTAL_BAR_CHART_TYPE,
    "Barras": VERTICAL_BAR_CHART_TYPE,
    "Líneas": LINE_CHART_TYPE,
    "Torta circular": PIE_CHART_TYPE,
    "Puntos dispersos": SCATTER_PLOT_CHART_TYPE,
    "Barras apiladas": STACKED_VERTICAL_BAR_CHART_TYPE,
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
