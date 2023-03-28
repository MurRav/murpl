#!/bin/ksh

# This program takes two filename arguments

USAGE="Usage:  $0 filename1 filename2"

if (( $# != 2 )); then
    echo "$USAGE"
    exit 1
fi

if [[ ! -f "$1" || ! -f "$2" ]]; then
    echo "$USAGE"
    exit 1
fi
# ...
