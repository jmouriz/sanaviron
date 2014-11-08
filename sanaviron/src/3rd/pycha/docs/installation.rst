.. index:: pycha installation
.. _installation:

************
Installation
************

PyCha can be used on any system that supports `Python <http://www.python.org>`_
and `Cairo <http://www.cairographics.org/>`_.

.. index:: windows installation
.. _install-windows:

Windows
=======

Pycha needs PyCairo to works since it uses the Cairo graphics library. 
These are the recommended steps for installing PyCairo:

   1. Grab the latest `PyCairo Windows installer
   <http://ftp.gnome.org/pub/GNOME/binaries/win32/pycairo/>`_. You need to use
   the one that matches your Python version so take the one ending in -py2.4.exe
   for Python 2.4 or the one ending in -py2.5.exe for Python 2.5
   
   2. Install it in your Python environment (just follow the installation
   program instructions)
   
   3. Put the Cairo dlls inside the pycairo directory inside your site-packages
   directory or anywhere in your path. You can find the dlls `here
   <http://www.gimp.org/~tml/gimp/win32/downloads.html>`_. 
   Download the following packages:
   
   1. cairo.zip  (you just need libcairo-2.dll)
   2. libpng.zip (you just need libpng13.dll)
   3. zlib.zip   (you just need zlib1.dll)

Pycha is distributed as a Python Egg so it is easy to install. You just need to
type the following command:

    ``easy_install pycha``

.. index:: linux installation
.. _install-linux:

Linux
=====

There are three ways to install PyCha in Linux:


**Option A** (*good for new users*):

Use your distribution package system. 

Ubuntu example:

    ``sudo apt-get install python-pycha``
    
Benefits:

- better integration with your distribution

- it can be uninstalled easily

**Option B** (*good for python veterans*):

Use easy_install to get the latest official version. You need to
install the setuptools package to use easy_install.

Ubuntu example:

    ``apt-get install python-setuptools``
    
    ``easy_install pycha``
    
Fedora example:

    ``yum install python-setuptools``
    
    ``easy_install pycha``
    
Benefits: 

- you always get the latest stable version of PyCha

**Option C** (*good for PyCha developers*):

Get a checkout of the subversion trunk branch:

    ``svn co http://www.lorenzogil.com/svn/pycha/trunk pycha``

Benefits:

- this is the bleeding edge version of PyCha

