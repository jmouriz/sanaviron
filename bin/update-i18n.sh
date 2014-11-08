#!/bin/bash
find `pwd`/`dirname $0`/.. -name \*.py -exec echo {} \; > `pwd`/`dirname $0`/../sanaviron/src/i18n/input/sanaviron.files
