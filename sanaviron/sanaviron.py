#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main Sanaviron
"""

import platform
import sys
import gtk # because Linux run threads_init
import os

from __init__ import *
#sys.path.append('..')
#from sanaviron import set_locale

#if platform.system() == 'Windows':
#    set_locale()
#else:
#    gtk.threads_init()
#
#install_gettext("sanaviron")

def startapp():
    if platform.system() == 'Windows':
        set_locale()
    else:
        gtk.threads_init()

    install_gettext("sanaviron")

    if '--debug' in sys.argv:
        import gc
        gc.enable()
        gc.set_debug(gc.DEBUG_LEAK)

    print(get_summary())
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    from ui.application import Application
    application = Application()

    if '--sample' in sys.argv:
        application.editor.canvas.load_from_xml(os.path.join("..", "examples", "invoice.xml"))

    application.run()

if __name__ == '__main__':
    startapp()
