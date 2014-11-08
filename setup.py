#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sanaviron setup script
"""

import os
from distutils.core import setup

ROOT_DIR = os.path.dirname(__file__)
if ROOT_DIR:
    os.chdir(ROOT_DIR)
PACKAGE = 'sanaviron'
APP_VERSION = open(os.path.join(PACKAGE,'VERSION')).read()

if __name__ == '__main__':
    # Compile the list of packages available, because distutils doesn't have
    # an easy way to do this.
    EXCLUDES = ['.', '..', '.svn', 'src', 'examples','images','.idea']
    PACKAGES, DATAFILES = [], []

    for dirpath, dirnames, filenames in os.walk(PACKAGE):
        for i, dirname in enumerate(dirnames):
            if dirname in EXCLUDES:
                del dirnames[i]
        if '__init__.py' in filenames:
            pkg = dirpath.replace(os.path.sep, '.')
            if os.path.altsep:
                pkg = pkg.replace(os.path.altsep, '.')
            PACKAGES.append(pkg)
        elif filenames:
            prefix = dirpath[len(PACKAGE) + 1:] # Strip package directory + path separator
            for f in filenames:
                DATAFILES.append(os.path.join(prefix, f))
    DATAFILES +=['AUTHORS','NEWS','TODO','ChangeLog','COPYING','INSTALL','README','VERSION','GUIDELINES','README.RU']

setup(
    name=PACKAGE,
    version=APP_VERSION,
    platforms=['Linux'],
    scripts=['bin/sanaviron'],
    packages=PACKAGES,
    package_data={PACKAGE: DATAFILES},
    data_files=[('/usr/share/applications', ['bin/sanaviron.desktop']),
                ('/usr/share/icons', ['bin/sanaviron.png']),
                (os.path.join('/usr/share/doc', PACKAGE), [os.path.join(PACKAGE, 'COPYING')]), # TODO: Include help files here
    ],
    url='http://sanaviron.org',
    download_url='http://sanaviron.org/git/sanaviron/archive/tip.zip',
    license='Apache License 2.0',
    author='Juan Manuel Mouriz, Ivlev Denis',
    author_email='jmouriz@sanaviron.org, ivlevdenis@sanaviron.org',
    description='The Sanaviron Project is an 2D drawing engine\
     fully written in Python for represent composite vector graphics.\
      This is essentially a GTK+ Cairo based canvas.',
    long_description=open(os.path.join(PACKAGE,'README')).read(),
    keywords='2d,vector,document,editor',
    requires=[],
)
