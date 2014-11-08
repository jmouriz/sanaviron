#!/bin/bash

test -z $BASH_SOURCE && {
   echo You must run this script invoking . $0 $1
   exit 1
}

LOCATION=`pwd`/`dirname $BASH_SOURCE`/..

alias run="cd $LOCATION; python sanaviron $1; cd -"
