#!/bin/bash
find `pwd`/`dirname $0`/.. \( -name \*.pyc -o -name \*.pyo -o -name \*.o \) -exec rm -f {} \;
