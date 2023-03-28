#!/bin/ksh

# This program takes two filename arguments

prog=${0##*/}
USAGE="Usage:  $prog filename1 filename2"

if (( $# != 2 )); then
    print -u2 "$USAGE"
    exit 1
fi

if [[ ! -f "$1" || ! -f "$2" ]]; then
    print -u2 "$USAGE"
    exit 1
fi
# ...
