.. index:: options
.. _options:

*******
Options
*******

Many properties of graphs in PyCha can be easily customized. Options include
colors, font sizes, widths, placements, and opacity. You can get a feel for what
the options do with :ref:`chavier` (frontend gui for PyCha).

.. index:: default options
.. _default-options:

Default Options
===============

The default options are:

::

    DEFAULT_OPTIONS = Option(
        axis=Option(
            lineWidth=1.0,
            lineColor='#0f0000',
            tickSize=3.0,
            labelColor='#666666',
            labelFont='Tahoma',
            labelFontSize=9,
            labelWidth=50.0,
            x=Option(
                hide=False,
                ticks=None,
                tickCount=10,
                tickPrecision=1,
                range=None,
                rotate=None,
                label=None,
            ),
            y=Option(
                hide=False,
                ticks=None,
                tickCount=10,
                tickPrecision=1,
                range=None,
                rotate=None,
                label=None,
            ),
        ),
        background=Option(
            hide=False,
            baseColor=None,
            chartColor='#f5f5f5',
            lineColor='#ffffff',
            lineWidth=1.5,
        ),
        legend=Option(
            opacity=0.8,
            borderColor='#000000',
            hide=False,
            position=Option(top=20, left=40, bottom=None, right=None),
        ),
        padding=Option(
            left=30,
            right=30,
            top=30,
            bottom=30,
        ),
        stroke=Option(
            color='#ffffff',
            hide=False,
            shadow=True,
            width=2
        ),
        fillOpacity=1.0,
        shouldFill=True,
        barWidthFillFraction=0.75,
        pieRadius=0.4,
        colorScheme=DEFAULT_COLOR,
        title=None,
        titleFont='Tahoma',
        titleFontSize=12,
    )
    
.. index:: changing defaults
.. _changing-defaults:
    
Changing Defaults
=================

The default options can be changed using a Python dictionary (``options = {}``).
A typical user option dictionary looks like::

    options = {
            'axis': {
                'x': {
                    'ticks': [dict(v=i, label=l[0]) for i, l in enumerate(Tainan)],
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
            'stroke': {'hide': True},
            'title': 'Monthly Precipitation'
        }

.. index:: axis options
.. _axis-options:
        
Axis Options
------------

.. These terms should be bold by default, not sure why they are not

**lineWidth**
    Sets the width of both axes. 
    
    ``float, default = 1.0``
    
**lineColor**
    Sets the color of both axes. 
    
    ``hexadecimal color code, default = '#0f0000'``
            
**tickSize**
    Sets the tick size of both axes. 
    
    ``float, default = 3.0``
    
**labelColor**
    Sets the color of the labels of both axes. 
    
    ``hexadecimal color code, default = '#666666'``
    
**labelFont**
    Sets the font of the labels of both axes. 
    
    ``font name, default = 'Tahoma'``
            
**labelFontSize**
    Sets the font size of the labels of both axes. 
    
    ``integer, default = 9``
    
**labelWidth**
    Sets the width of the labels of both axes.
     
    ``float, default = 50.0``

.. _x-axis-options:

X-Axis Options
^^^^^^^^^^^^^^

**hide**
    Toggles x-axis visibility.
    
    ``boolean, default = False``

.. _xticks:

**ticks**
    Sets the tick labels for the x-axis. The format is:
    
    ``[{'v': x, 'label': m}, {'v': x+1, 'label': n}]``
    
    where x is the index (starting from 0) and m and n are the tick labels.
    
    If your data is in the form:
    
    Rain = (
    ('Jan', 32.7),
    ('Feb', 9.5),
    ('Mar', 25.5),
    ('Apr', 13.7),
    ('May', 41.5),
    ('Jun', 782.2),
    )
    
    and it is imported as Rain, then you can generate the ticks using:
    
    'ticks': [dict(v=i, label=l[0]) for i, l in enumerate(Rain)],
    
    ``list of dictionaries, default = None``

**tickCount**
    Sets the number of ticks on the x-axis.
    
    ``integer, default = 10``
    
**tickPrecision**
    Sets the precision (number of decimal places) of ticks on the x-axis.
    
    ``integer, default = 1``
    
**range**
    Sets the range for the x-axis. For example, if you want to show 3 bars on a
    chart big enough for 6 bars:
    
    ``range = (0.0, 5.0)``
    
    ``float, default = None``
    
**rotate**
    Sets the rotation angle of the x-axis ticks.
    
    ``degrees, default = None``
    
**label**
    Sets the x-axis label.
    
    ``string, default = None``
    
.. _y-axis-options:

Y-Axis Options
^^^^^^^^^^^^^^

**hide**
    Toggles y-axis visibility.
    
    ``boolean, default = False``

**ticks**
    
    ``list of dictionaries, default = None``

**tickCount**
    Sets the number of ticks on the y-axis.
    
    ``integer, default = 10``
    
**tickPrecision**
    Sets the precision (number of decimal places) of ticks on the y-axis.
    
    ``integer, default = 1``
    
**range**
    Sets the range for the y-axis. For example, if you want to leave some room at
    the top of your chart:
    
    ``range = (0.0, ymax+(ymax/3.0))``
    
    where ``ymax`` is the maximum y value. The above will leave 1/3 of the chart
    empty at the top.
    
    ``float, default = None``
    
**rotate**
    Sets the rotation angle of the y-axis ticks.
    
    ``degrees, default = None``
    
**label**
    Sets the y-axis label.
    
    ``string, default = None``

Background Options
------------------

**hide**
    Toggles the visibility of the background.
    
    ``boolean, default = False``
    
**baseColor**
    Sets the color of the area around the chart. It's the background color for
    the ticks and labels.
    
    ``hexadecimal color code, default = None``
    
**chartColor**
    Sets the color of the chart.
    
    ``hexadecimal color code, default = '#f5f5f5'``
    
**lineColor**
    Sets the color of the chart line.
    
    ``hexadecimal color code, default = '#ffffff'``
    
**lineWidth**
    Sets the width of the chart line.
    
    ``float, default = 1.5``

.. index:: legend options
.. _legend-options:

Legend Options
--------------

**opacity**
    Sets the opacity of the legend. The value ranges from 0 to 1.0.
    
    ``float, default = 0.8``
    
**borderColor**
    Sets the border color of the legend.
    
    ``hexadecimal color code, default = '#000000'``
    
**hide**
    Toggles the visibility of the legend.
    
    ``boolean, default = False``
    
**position**
    This option can be used to place the legend at a particular location on the
    chart. The top, bottom, left, and right offsets can be adjusted.
    
    ``int, default = top: 20, left: 40, bottom: None, right: None``
    
.. index:: padding options
.. _padding-options:

Padding Options
---------------

**left**
    Sets the left padding for the chart.
    
    ``int, default = 30``
    
**right**
    Sets the right padding for the chart.
    
    ``int, default = 30``
    
**top**
    Sets the top padding for the chart.
    
    ``int, default = 30``
    
**bottom**
    Sets the bottom padding for the chart.
    
    ``int, default = 30``    

.. index:: stroke options
.. _stroke-options:

Stroke Options
--------------

**color**
    Sets the color of the bar outline stroke.
    
    ``hexadecimal color code, default = '#ffffff'``
    
**hide**
    Toggles the visibility of the bar outline stroke.
    
    ``boolean, default = False``
    
**shadow**
    Toggles the visibility of a shadow around each bar.
    
    ``boolean, default = True``
    
**width**
    Sets the width of the bar outline stroke.
    
    ``int, default = 2``
    
.. index:: yval options
.. _yval-options:

Yval Options
------------

.. versionadded:: 0.4.2

**show**
    Toggles the visibility of y values above the bars.
    
    ``boolean, default = False``
    
**inside**
    Toggles the placement of the y values. They are above the bars by default. If
    a bar is too small to show its y value inside the bar, the value is drawn above
    the bar.
    
    ``boolean, default = False``
    
**fontSize**
    Sets the font size of the y values.
    
    ``int, default = 11``
    
**fontColor**
    Sets the color of the font of the y values.
    
    ``hexadecimal color code, default = '#000000'``
    
.. index:: miscellaneous options
.. _misc-options:

Miscellaneous Options
---------------------

**fillOpacity**
    Sets the opacity of the bars.
    
    ``float, default = 1.0``
    
**shouldFill**
    Toggles whether the bars should be filled.
    
    ``boolean, default = True``
    
**barWidthFillFraction**
    Sets the fraction of the width that will be used to draw the bar. For example,
    a fraction of 1.0 will use the whole width to draw the bars (the bars will touch).
    
    ``float, default = 0.75``
    
**pieRadius**
    Sets the radius of the pie chart. This option is ignored for other charts.
    
    ``float, default = 0.4``
    
**colorScheme**
    Sets the color scheme of the chart. Available schemes include    
    red, green, blue, grey, black, and darkcyan. DEFAULT_COLOR is
    '#3c581a' (green).
    
    ``hexadecimal color code, default = DEFAULT_COLOR``    
        
**title**
    Sets the title of the chart.
    
    ``string, default = None``
    
**titleFont**
    Sets the font of the chart title.
    
    ``font name, default = 'Tahoma'``
    
**titleFontSize**
    Sets the size of the chart title font.
    
    ``int, default = 12``

