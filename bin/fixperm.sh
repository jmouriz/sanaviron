#!/bin/bash
find `pwd`/`dirname $0`/.. \( -name \*.py -a ! -name __\*__.py \) -exec chmod 755 {} \;
find `pwd`/`dirname $0`/.. -name \*.png -a -exec chmod 644 {} \;
chmod 755 `pwd`/`dirname $0`/sanaviron
