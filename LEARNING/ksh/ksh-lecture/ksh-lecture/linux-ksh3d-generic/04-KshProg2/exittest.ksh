#!/bin/ksh

prog=${0##*/}
USAGE="Usage:  $prog fromfile todir"

if (( $# < 2 )); then
    echo "$USAGE" >&2
    exit 1
fi

if [[ ! -r "$1" ]]; then
    echo "No read permission on '$1'." >&2
    echo "$USAGE" >&2
    exit 2
fi

if [[ ! -d "$2" ]]; then
    echo "'$2' is not a directory." >&2
    echo "$USAGE" >&2
    exit 3
fi
cp "$1" "$2"
