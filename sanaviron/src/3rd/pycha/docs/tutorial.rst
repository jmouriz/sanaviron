.. index:: tutorial
.. _tutorial:

********
Tutorial
********

Using PyCha is quite simple. You always follow the same 5 simple steps:

   1. Create a Cairo surface to draw the chart on.
   2. Build a list of data sets from which your chart will be created.
   3. Customize the chart options.
   4. Create the chart, add the datasets, and render it.
   5. Save the results into a file or do whatever you want with the Cairo surface.

.. index:: create cairo surface  
.. _creating-cairo-surface:
   
Creating a Cairo Surface
========================

Detailed information on the Cairo library can be found on their `website
<http://www.cairographics.org/>`_. 

To create the Cairo surface, you need to specify the type of surface and its
dimensions::

   import cairo
   width, height = (500, 400)
   surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

.. index:: build dataset
.. _building-datasets:

Building Datasets
=================

PyCha requires a dataset in the form::

    dataSet = (
         ('dataSet 1', ((0, 1), (1, 3), (2, 2.5))),
         ('dataSet 2', ((0, 2), (1, 4), (2, 3))),
         ('dataSet 3', ((0, 5), (1, 1), (2, 0.5))),     
    )
    
Each data set is a tuple, of which the first element is the name of the data set
and the second is a tuple of two points (x, y).

.. index:: customize options
.. _customizing-options:

Customizing Options
===================

Please refer to :ref:`changing-defaults`.

.. index:: render chart
.. _creating-rendering-chart:

Create and Render Chart
=======================

Now we are ready to instantiate the chart, add the dataset, and render it::

   import pycha.bar
   chart = pycha.bar.VerticalBarChart(surface, options)
   chart.addDataset(dataSet)
   chart.render()
   
Please see :ref:`PyCha chart types <pycha-chart-types>` for supported outputs.

.. _saving-results:

Saving Results
==============

Finally, you can write the surface to a file using the Cairo library::

   surface.write_to_png('output.png')

That's it! Please see :ref:`save-chart-to-file` and :ref:`embed-chart-in-gtk-app`
for examples.

