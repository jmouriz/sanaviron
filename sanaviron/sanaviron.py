#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main Sanaviron
"""

import platform
import sys
from gi.repository import Gtk
import os

from __init__ import *
#sys.path.append('..')

#if platform.system() == 'Windows':
#    set_locale()
#else:
#    Gtk.threads_init()
#
#install_gettext("sanaviron")

def startapp():
    if platform.system() == 'Windows':
        #from .__init__ import set_locale
        set_locale()
    else:
        pass #Gtk.threads_init()

    install_gettext("sanaviron")

    if '--debug' in sys.argv:
        import gc
        gc.enable()
        gc.set_debug(gc.DEBUG_LEAK)

    print(get_summary())
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from ui.application import Application
    application = Application()

    if '--sample' in sys.argv:
        application.editor.canvas.load_from_xml(os.path.join("..", "examples", "invoice.xml"))

    application.run()

if __name__ == '__main__':
    startapp()
