"""
___init___.py
"""

__all__ = ["VERSION", "set_locale", "get_locale_language", "get_parsed_language", "install_gettext", "get_summary"]

import platform
import locale
import gettext
import os
import cairo
import gtk
import sys

VERSION = open(os.path.join(os.path.dirname(__file__), "..", "VERSION")).read()
DEFAULT_LANGUAGE = "en"

def get_locale_language():
    language = None
    if not os.getenv('LANG') or os.getenv('LANG') == 'C':
        LANGUAGE, ENCODING = locale.getdefaultlocale()
        if not LANGUAGE:
            language = DEFAULT_LANGUAGE
        else:
            language = LANGUAGE
    else:
        language = os.getenv('LANG')

    return language

def get_parsed_language():
    return get_locale_language().split('_')[0]

def set_locale():
    os.environ['LANG'] = get_locale_language()
#    if os.getenv('LANG') is None:
#        LANGUAGE, ENCODING = locale.getdefaultlocale()
#        os.environ['LANG'] = LANGUAGE

def install_gettext(domain):
    TRANSLATION_DOMAIN = domain
    LOCALE_DIR = os.path.join(os.path.dirname(__file__), "localization")
    gettext.install(TRANSLATION_DOMAIN, LOCALE_DIR)

def get_summary():
    summary = "Sanaviron version: %s (%s)\n" % (VERSION, 'Testing' if "--testing" in sys.argv else 'Production')
    summary += "System: %s %s %s\n" % (platform.system(), platform.release(), platform.version())
    summary += "Python version: %s\n" % platform.python_version()
    summary += "GTK version: %s\n" % '.'.join(map(str, gtk.ver))
    summary += "Cairo version: %s" % cairo.cairo_version_string()

    return summary
